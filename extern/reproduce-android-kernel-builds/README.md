# Reproduce Android Kernel Builds

> Status: **active**. Approved on 2026-07-30; continue validation only on user-owned or authorized devices.

This Skill builds an evidence-backed workflow for Android kernels, root providers, and boot images on
user-owned or explicitly authorized devices. It covers exactly pinned source builds, official generic GKI LKM
repacking into exact live/OTA stock images, and third-party artifact audits when vendor source is incomplete.

## Quick start

```text
Use $reproduce-android-kernel-builds to establish source locks, a baseline, and validation gates for this
authorized device.
```

## Main capabilities

- Select the correct source route from device codename, factory build, and kernel release.
- Pin manifests, managed repositories, external tools, and third-party integrations to exact commits.
- Record source discovery as complete, `candidate-source`, or `incomplete-source`; only a complete locked route
  receives the `reproduced-source` origin.
- Treat official Provider GKI/LKM releases as a first-class route that does not require source reproduction to
  fail first.
- Record origin, integration, and qualification as independent evidence coordinates.
- Build an unmodified baseline before validating DTB, module ABI, vermagic, and artifact format.
- Audit a device-specific third-party artifact when source cannot be reproduced, while labeling the result only
  as `qualified-prebuilt`.
- Support KernelSU Next, SukiSU Ultra, KernelSU, and other implementations/integration modes through provider
  profiles.
- Express device differences through device profiles/adapters instead of hard-coding Pixel or one partition
  layout.
- Repack from the exact stock image while preserving hashes, metadata, and rollback images.
- Distinguish framework Android, vendor generation, kernel release, and KMI; select generic LKMs by KMI and
  qualify modversions, signing, symbols, and Provider loader behavior.
- Resolve `boot`/`init_boot`/`vendor_boot` from parsed headers and Provider behavior, including the rule that an
  `init_boot`-only candidate is not automatically valid input to `fastboot boot`.
- Protect shared `/data/adb` Provider/module state during migration and authorize app, staging, shared-state,
  and module cleanup separately.
- Treat temporary boot, permanent flashing, data wiping, and bootloader relocking as separate authorization and
  stop gates.
- Distinguish a loader-path temporary-boot failure from kernel incompatibility, and prove inactive-slot
  bootability before treating it as rollback.
- Separate authorization to flash for a first runtime test from the later decision to retain the validated
  artifact as a permanent installation.

## Safety

Permission to inspect information, download source, or complete a build does not authorize bootloader
unlocking, data wiping, temporary booting, flashing, or relocking. Obtain explicit confirmation again before
changing a physical device.

## Install for Codex

Link the complete `reproduce-android-kernel-builds/` source directory into the user Skill directory. The link
must resolve to a directory whose top level directly contains `SKILL.md`; do not install by copying the source.

Windows PowerShell:

```powershell
$skillsRoot = Join-Path $HOME ".agents\skills"
$source = (Resolve-Path "<repository-root>\reproduce-android-kernel-builds").Path
$link = Join-Path $skillsRoot "reproduce-android-kernel-builds"
New-Item -ItemType Directory -Force -Path $skillsRoot | Out-Null
if (Test-Path -LiteralPath $link) { throw "Destination already exists: $link" }
New-Item -ItemType Junction -Path $link -Target $source | Out-Null
```

macOS:

```bash
skills_root="$HOME/.agents/skills"
source_dir="$(cd "<repository-root>/reproduce-android-kernel-builds" && pwd)"
link_path="$skills_root/reproduce-android-kernel-builds"
mkdir -p "$skills_root"
if [ -e "$link_path" ] || [ -L "$link_path" ]; then echo "Destination already exists: $link_path" >&2; exit 1; fi
ln -s "$source_dir" "$link_path"
```

Codex normally detects Skill changes automatically; restart it if the Skill does not appear. Invoke it as
`$reproduce-android-kernel-builds`. For cross-agent reuse, CC Switch v3.13 or newer can use
`~/.agents/skills` as shared source storage: open **Skills**, scan/import the local Skill if needed, enable the
target agents, and sync. Recheck device authorization, tools, and safety gates after import.

## Files

- `SKILL.md`: complete workflow, safety boundary, and phase gates.
- `references/source-locks-and-profiles.md`: source locks, device profiles, and adapter design.
- `references/validation-gates.md`: stop gates from device identification through flashing and rollback.
- `references/vendor-source-and-prebuilt-fallback.md`: vendor source gaps and third-party artifact fallback.
- `references/gki-lkm-ota-repack.md`: official Provider GKI/LKM, exact OTA/live stock, KMI, partition, AVB,
  validation, migration, and cleanup rules.
- `scripts/verify_source_lock.py`: bounded read-only verification of Git HEAD, equivalent remote URLs, worktree,
  and optional commit-signature, submodule, and LFS gates.
