# Source Locks and Device Profiles

## Contents

- Trust model
- Candidate and accepted locks
- Profile responsibilities
- Adapter responsibilities
- Artifact identity
- Verifier scope

## Trust model

Separate human judgment from mechanical verification:

```text
human:
  identify device/factory build
  choose the correct official manifest history
  match kernel release to the main kernel commit

mechanical:
  enumerate all repositories
  checkout accepted commits
  verify remotes and clean worktrees
  record toolchain and artifact hashes
  run baseline and ABI gates
```

Automation can record the current checkout; it cannot prove that a branch HEAD is the historically correct
input without external evidence.

## Candidate and accepted locks

Use a TSV lock. Optional booleans activate expensive checks only where required:

```text
path	commit	remote	require_signed_commit	verify_submodules	verify_lfs
kernel/msm	40-character-commit	https://trusted.example/kernel/msm	true	true	false
prebuilts/clang	40-character-commit	https://trusted.example/clang	false	false	true
```

Lifecycle:

```text
resolve sources
  -> source-lock.candidate.tsv
  -> review remote and historical evidence
  -> baseline/ABI validation
  -> source-lock.tsv
```

Never overwrite an accepted lock with a fresh `repo sync` result. Generate a new candidate and review the
difference.

## Profile responsibilities

A device profile owns data:

- codename, build ID, kernel release
- manifest URL/revision/name
- expected repositories and source lock path
- defconfig and fragment inputs
- toolchain identifiers
- expected image, DTB/DTBO, modules, and output layout
- boot partition/header/AVB facts
- validation commands and thresholds
- source availability classification and known missing inputs
- selected root provider, provider commit/release, manager compatibility, and integration mode
- evidence origin, integration, and qualification coordinates
- KMI, provider loader/signing behavior, and exact stock-source tier where applicable
- optional third-party artifact provenance and expected hash

Keep profiles declarative. Do not hide destructive commands inside a sourced configuration file.

## Adapter responsibilities

Adapters implement device-family operations:

- probe device facts
- resolve source candidates
- build baseline
- integrate the authorized change
- collect DTB/module ABI evidence
- unpack/repack boot artifacts
- validate an output

The workflow owns state progression and stop gates; the adapter owns device-specific mechanics.

## Artifact identity

Record SHA-256 for:

- exact stock package archive or live-partition capture record
- extracted stock boot/init_boot/vendor_boot inputs
- baseline kernel artifact
- modified kernel artifact
- repacked test image
- final authorized image
- optional manager/APK/module artifacts

Record Git commits for source trees. A locally created integration commit may differ because of author/time
metadata, so also retain the actual diff, base commit, third-party commit, configuration, and final artifact
hashes.

For a third-party prebuilt, record the source and build evidence that actually exists, but never synthesize
missing commits. Distinguish:

```text
reproduced:
  complete accepted source lock + verified baseline + isolated modification

qualified-provider-repack:
  official provider release + exact stock repack + authorized runtime evidence

qualified-prebuilt:
  community artifact hash + publisher/release provenance + compatibility inspection + authorized runtime evidence
```

The device profile may select `kernelsu-next`, `sukisu-ultra`, `kernelsu`, or another provider. The profile
must also select the integration mode; the provider name alone is insufficient.

## Verifier scope

`verify_source_lock.py` compares commits, equivalent common Git remote URL forms, worktree state, and optional
commit-signature, recursive submodule, and Git LFS checks. Bound large manifests with `--max-concurrency`.

The script does not prove historical source correctness or toolchain identity. Lock compiler archives,
container images, Repo manifests, packaging/extraction tools, and other non-repository inputs separately with
version, origin, and immutable hash. Signature verification also depends on an available trusted keyring; an
unavailable key is a failed gate, not proof that a commit is unsigned.
