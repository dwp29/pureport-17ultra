#!/usr/bin/env python3
"""Verify Git repositories against an Android kernel source-lock TSV."""

import argparse
import asyncio
import csv
import io
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import List, Optional, Sequence
from urllib.parse import urlsplit


COMMIT_PATTERN = re.compile(r"^[0-9a-fA-F]{40}$")


@dataclass(frozen=True)
class LockEntry:
    """Describe one locked Git repository."""

    path: str
    commit: str
    remote: str
    require_signed_commit: bool = False
    verify_submodules: bool = False
    verify_lfs: bool = False


@dataclass(frozen=True)
class VerificationResult:
    """Describe verification results for one repository."""

    path: str
    expected_commit: str
    actual_commit: Optional[str]
    expected_remote: str
    actual_remote: Optional[str]
    dirty: Optional[bool]
    signed_commit: Optional[bool]
    submodules_clean: Optional[bool]
    lfs_ok: Optional[bool]
    errors: List[str]

    @property
    def ok(self) -> bool:
        """Return whether every requested check passed."""
        return not self.errors


def parse_bool_field(value: Optional[str], field: str, line_number: int) -> bool:
    """Parse an optional TSV boolean field."""
    normalized = (value or "").strip().lower()
    if normalized in {"", "0", "false", "no"}:
        return False
    if normalized in {"1", "true", "yes"}:
        return True
    raise ValueError(f"Line {line_number}: {field} must be true or false")


def normalize_remote_url(remote: str) -> str:
    """Normalize common Git remote URL forms for identity comparison."""
    value = remote.strip().rstrip("/")
    scp_match = re.fullmatch(r"(?:[^@/]+@)?([^:/]+):(.+)", value)
    if scp_match and "://" not in value:
        host = scp_match.group(1).lower()
        path = scp_match.group(2).strip("/")
    else:
        parsed = urlsplit(value)
        if not parsed.hostname:
            return value.removesuffix(".git")
        host = parsed.hostname.lower()
        port = parsed.port
        if port is not None:
            host = f"{host}:{port}"
        path = parsed.path.strip("/")
    return f"{host}/{path.removesuffix('.git')}"


def remote_urls_equivalent(expected: str, actual: str) -> bool:
    """Return whether two common Git remote URL forms identify one repository."""
    return normalize_remote_url(expected) == normalize_remote_url(actual)


def parse_lock(text: str) -> List[LockEntry]:
    """Parse a source-lock TSV document.

    Args:
        text: TSV content with path, commit, and optional remote columns.

    Returns:
        Validated lock entries.

    Raises:
        ValueError: If the header, path, or commit is invalid.
    """
    reader = csv.DictReader(io.StringIO(text), delimiter="\t")
    if reader.fieldnames is None or not {"path", "commit"}.issubset(
        set(reader.fieldnames)
    ):
        raise ValueError("Lock TSV requires path and commit columns")
    entries: List[LockEntry] = []
    seen_paths = set()
    for line_number, row in enumerate(reader, start=2):
        path = (row.get("path") or "").strip()
        commit = (row.get("commit") or "").strip().lower()
        remote = (row.get("remote") or "").strip()
        if not path or Path(path).is_absolute():
            raise ValueError(
                f"Line {line_number}: path must be a non-empty relative path"
            )
        if not COMMIT_PATTERN.fullmatch(commit):
            raise ValueError(
                f"Line {line_number}: commit must contain 40 hexadecimal characters"
            )
        normalized_path = Path(path).as_posix().rstrip("/")
        if normalized_path in seen_paths:
            raise ValueError(f"Line {line_number}: duplicate repository path: {path}")
        seen_paths.add(normalized_path)
        entries.append(
            LockEntry(
                path=path,
                commit=commit,
                remote=remote,
                require_signed_commit=parse_bool_field(
                    row.get("require_signed_commit"),
                    "require_signed_commit",
                    line_number,
                ),
                verify_submodules=parse_bool_field(
                    row.get("verify_submodules"),
                    "verify_submodules",
                    line_number,
                ),
                verify_lfs=parse_bool_field(
                    row.get("verify_lfs"), "verify_lfs", line_number
                ),
            )
        )
    if not entries:
        raise ValueError("Lock TSV contains no repository entries")
    return entries


def resolve_repo(workspace: Path, relative_path: str) -> Path:
    """Resolve a locked repository without allowing workspace escape."""
    root = workspace.resolve()
    candidate = (root / relative_path).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as error:
        raise ValueError(f"Repository path escapes workspace: {relative_path}") from error
    return candidate


async def run_git(repo: Path, *arguments: str) -> str:
    """Run a read-only Git query and return stripped stdout."""
    process = await asyncio.create_subprocess_exec(
        "git",
        "-C",
        str(repo),
        *arguments,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    if process.returncode != 0:
        message = stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(message or f"git exited with {process.returncode}")
    return stdout.decode("utf-8", errors="replace").strip()


async def verify_entry(workspace: Path, entry: LockEntry) -> VerificationResult:
    """Verify one repository against its lock entry."""
    repo = resolve_repo(workspace, entry.path)
    errors: List[str] = []
    actual_commit: Optional[str] = None
    actual_remote: Optional[str] = None
    dirty: Optional[bool] = None
    signed_commit: Optional[bool] = None
    submodules_clean: Optional[bool] = None
    lfs_ok: Optional[bool] = None
    if not repo.is_dir():
        errors.append("repository directory is missing")
    else:
        try:
            actual_commit = (await run_git(repo, "rev-parse", "HEAD")).lower()
            if actual_commit != entry.commit:
                errors.append("HEAD does not match locked commit")
        except RuntimeError as error:
            errors.append(f"cannot read HEAD: {error}")
        try:
            dirty = bool(await run_git(repo, "status", "--porcelain"))
            if dirty:
                errors.append("worktree is dirty")
        except RuntimeError as error:
            errors.append(f"cannot read worktree status: {error}")
        if entry.remote:
            try:
                actual_remote = await run_git(repo, "remote", "get-url", "origin")
                if not remote_urls_equivalent(entry.remote, actual_remote):
                    errors.append("origin remote does not match locked remote")
            except RuntimeError as error:
                errors.append(f"cannot read origin remote: {error}")
        if entry.require_signed_commit:
            try:
                await run_git(repo, "verify-commit", "HEAD")
                signed_commit = True
            except RuntimeError as error:
                signed_commit = False
                errors.append(f"commit signature verification failed: {error}")
        if entry.verify_submodules:
            try:
                submodule_status = await run_git(repo, "submodule", "status", "--recursive")
                bad_submodules = [
                    line
                    for line in submodule_status.splitlines()
                    if line and line[0] in {"-", "+", "U"}
                ]
                submodules_clean = not bad_submodules
                if bad_submodules:
                    errors.append("submodule state does not match the recorded checkout")
            except RuntimeError as error:
                submodules_clean = False
                errors.append(f"cannot verify submodules: {error}")
        if entry.verify_lfs:
            try:
                await run_git(repo, "lfs", "fsck")
                lfs_ok = True
            except RuntimeError as error:
                lfs_ok = False
                errors.append(f"Git LFS verification failed: {error}")
    return VerificationResult(
        path=entry.path,
        expected_commit=entry.commit,
        actual_commit=actual_commit,
        expected_remote=entry.remote,
        actual_remote=actual_remote,
        dirty=dirty,
        signed_commit=signed_commit,
        submodules_clean=submodules_clean,
        lfs_ok=lfs_ok,
        errors=errors,
    )


async def async_main(arguments: Optional[Sequence[str]] = None) -> int:
    """Run source-lock verification asynchronously."""
    parser = argparse.ArgumentParser(
        description="Verify repository HEAD, origin, and cleanliness against a TSV lock."
    )
    parser.add_argument("lock_file", type=Path)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--max-concurrency", type=int, default=8)
    args = parser.parse_args(arguments)
    if args.max_concurrency < 1:
        parser.error("--max-concurrency must be at least 1")
    lock_text = await asyncio.to_thread(args.lock_file.read_text, encoding="utf-8")
    entries = parse_lock(lock_text)
    semaphore = asyncio.Semaphore(args.max_concurrency)

    async def verify_limited(entry: LockEntry) -> VerificationResult:
        """Verify one entry without exceeding the manifest concurrency bound."""
        async with semaphore:
            return await verify_entry(args.workspace, entry)

    results = await asyncio.gather(
        *(verify_limited(entry) for entry in entries)
    )
    report = {
        "ok": all(result.ok for result in results),
        "repository_count": len(results),
        "results": [
            {
                **asdict(result),
                "ok": result.ok,
            }
            for result in results
        ],
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["ok"] else 1


def main(arguments: Optional[Sequence[str]] = None) -> int:
    """Run the asynchronous verifier from a synchronous process entrypoint."""
    return asyncio.run(async_main(arguments))


if __name__ == "__main__":
    raise SystemExit(main())
