# Android Kernel Validation Gates

## Contents

- Gate 0: authorization and recovery
- Gate 1: device identity
- Gate 2: source lock
- Gate 2B: incomplete-source/prebuilt branch
- Gate 2C: official provider release repack
- Gate 3: baseline
- Gate 4: modified build
- Gate 5: repack
- Gate 6: temporary boot
- Gate 6B: flash-based first runtime validation
- Gate 7: permanent install
- Gate 7B: provider migration and cleanup
- Gate 8: relock

## Gate 0: authorization and recovery

- Confirm the device is owned/authorized.
- Confirm inspection, download, build/repack, device staging, manager app changes, unlock/wipe, temporary boot,
  named partition/slot flash, reboot, module changes, cleanup scopes, and relock separately as applicable.
- Preserve exact stock recovery images and hashes.
- Confirm bootloader/fastboot connectivity and a host-side recovery path.
- Stop if a required rollback artifact is missing.

## Gate 1: device identity

- Match codename, model, framework/SDK, vendor/factory build, fingerprint, SPL, full kernel release, KMI, ABI,
  slot, and partition layout.
- Inspect actual boot header and AVB metadata.
- Stop on any ambiguity between similar device variants or builds.

## Gate 2: source lock

- Verify every repository HEAD, remote, and worktree.
- Verify toolchain and packaging tool versions.
- Explain branch-based manifest revisions and lock them to commits.
- Stop if a critical source comes from an unverified mirror or moving branch.

If an official vendor branch exists but cannot be mapped to the target build or lacks required inputs, classify
it as `candidate-source` or `incomplete-source`. Do not approve the baseline gate by assumption.

## Gate 2B: incomplete-source/prebuilt branch

Use only when source reproduction has stopped and the user chooses to evaluate a third-party artifact.

- Record the exact missing source inputs and failed baseline evidence.
- Match device codename and regional variant exactly.
- Match target ROM/build, kernel release, architecture, partition, boot header, and provider integration mode.
- Capture immutable artifact hash and available publisher/release/source/build evidence.
- Unpack and inspect the image before device use.
- Verify the exact stock rollback image and host recovery path.
- Stop on ambiguous provenance, generic device claims, mismatched metadata, or a moving artifact without a
  retained hash.

Passing this gate records `community-prebuilt + <integration> + candidate`; it does not yield a reproduced
build or a runtime-qualified prebuilt.

## Gate 2C: official provider release repack

Use for an official generic GKI LKM or another immutable provider release repacked locally into exact stock.
This branch does not require source reproduction to fail.

- Lock the official release URL/version and hashes of the manager, daemon/patcher, LKM/driver, and source
  snapshot or guidance used to interpret the loader.
- Record framework Android, vendor generation, full kernel release, KMI, architecture, `CONFIG_MODVERSIONS`,
  vermagic, symbol/KALLSYMS requirements, signing policy, and provider loader behavior.
- Prefer the provider's current official KMI command and retain its output.
- Parse boot headers and cross-check the provider target decision before selecting `boot`, `init_boot`, or
  `vendor_boot`.
- Qualify exact stock provenance and rollback before running the patcher.
- Stop on an unverified release, unexplained provider component mix, unresolved KMI/loader contract, ambiguous
  target partition, or non-exact stock input.

Passing this gate records `official-provider-release + lkm-stock-repack + candidate`.

## Gate 3: baseline

- Build without the intended modification.
- Compare release, config, DTB/DTBO, module ABI/vermagic/CRC, and artifact format.
- Stop if the unmodified baseline does not match the target closely enough for the device-specific plan.

## Gate 4: modified build

- Pin and review the modification.
- Build from clean baseline inputs.
- Compare baseline and modified outputs.
- Run compile/static tests and device-specific artifact validation.
- Stop on unexplained changes.

For a prebuilt branch, replace the source-diff check with the Gate 2B provenance and compatibility record. Do
not invent a baseline comparison that cannot be performed.

## Gate 5: repack

- Classify stock input as `live-partition-exact`, `package-exact`, or `candidate-package`; only the first two may
  become a device candidate or exact rollback artifact.
- For packages, verify internal build/device metadata and record archive/payload/extractor identity and hashes.
- Parse headers before choosing the target: a generic-ramdisk LKM commonly belongs in `init_boot` when `boot`
  has a kernel but no ramdisk, but observed layout and provider logic must decide.
- Preserve all unchanged metadata.
- Classify round-trip differences. Authorized ramdisk and related AVB offset/hash changes may be expected;
  header version, total partition size, kernel/ramdisk layout, AVB algorithm/flags, and unrelated components
  remain invariant unless the plan explicitly changes them.
- Treat provider restore/unpatch output as structural evidence only. It is not the rollback image unless it is
  independently byte-identical to retained exact stock.
- Record hashes and inspect the final image.
- Stop if header, partition, compression, size, or AVB assumptions are unresolved.

## Gate 6: temporary boot

Requires explicit authorization.

- Confirm the device/bootloader supports the intended temporary-boot command.
- Distinguish loader acceptance from kernel execution; record where a failed attempt stopped.
- Keep the stock image and recovery command immediately available.
- Boot the candidate without flashing when supported.
- Verify critical hardware, logs, modules, and the intended feature.
- Stop and roll back on instability.
- Record the provider/manager pair and prove the intended root implementation is actually active.

Use this target decision table:

| Candidate | Gate 6 decision |
| --- | --- |
| complete boot image accepted by the loader | temporary boot may be proposed |
| `init_boot`-only patch | do not pass it to `fastboot boot` as a complete boot image |
| `vendor_boot`-only patch | require a documented composite route or use Gate 6B |
| loader fails before kernel execution | preserve loader evidence; compatibility remains unresolved |

If the temporary command fails before kernel execution, do not classify the candidate as incompatible solely
from that result. Stop, preserve the loader/crash evidence, and present the remaining validation choices. Any
flash-based test requires a new explicit authorization.

Do not treat an A/B partition layout as a rollback plan. Before relying on the inactive slot, prove that the
exact stock image on that slot boots independently and that slot switching is recoverable on this device.

## Gate 6B: flash-based first runtime validation

Use only when temporary boot is unavailable or fails before kernel execution. This is a device-changing
validation method, not implicit acceptance of permanent installation.

- Obtain explicit flash authorization that names the exact partition, candidate hash, stock rollback hash,
  expected interruption, and recovery path.
- Keep the host, cable, bootloader access, and tested stock restore command available.
- Flash only the resolved partition and perform the same critical runtime checks required by Gate 6.
- Immediately before writing, recheck product, current slot, unlocked state, resolved partition, candidate hash,
  and stock rollback hash.
- Roll back immediately on a failed critical check or at the user's request.
- After successful validation, ask whether to retain the installed artifact. Do not infer permanent acceptance
  from permission to perform this test.

## Gate 7: permanent install

Requires explicit acceptance after runtime validation. When Gate 6B already wrote the exact candidate, this
gate may record the decision to retain it rather than performing another write.

- Confirm active slot and exact target partition.
- Confirm the validated artifact hash matches the artifact to be retained or flashed.
- Preserve pre-flash facts and stock rollback image.
- If a write is still required, obtain separate authorization, flash only the resolved partition, and validate
  reboot persistence.
- Require a second reboot before declaring a provider migration retained or authorizing old-provider cleanup.
- Record whether the user chose retention, rollback, or later decision.

Record automated proxy evidence separately from human functional checks. Service presence, enumeration, sensor
events, logs, and state queries do not prove actual photo capture, cellular calling/data, fingerprint unlock,
or suspend/wake behavior.

## Gate 7B: provider migration and cleanup

Use only after the new provider is active, retention is explicit, and the second reboot passes.

- Prove the active manager, daemon, LKM/driver, root context, and retained module records.
- Inventory the old manager package/app sandbox separately from shared `/data/adb` provider and module state.
- Do not infer ownership from compatibility names such as `ksu`, `ksud`, or `/data/adb/ksu`.
- Audit provider logs/records, Zygisk/LSPosed state, and the real module store; `/data/adb/modules` may be empty
  while a provider-managed sparse `modules.img` remains active.
- Do not ordinary-copy, mount, truncate, repair, or delete a sparse provider-managed module image without a
  separately reviewed tool, authorization, and recovery plan.
- Obtain separate cleanup authorization for the obsolete manager app, downloads/staging, shared provider data,
  and installed root modules.
- Default to removing only the proven obsolete app/app data and explicitly identified downloads/staging while
  preserving shared state and modules.

## Gate 8: relock

Treat relocking as a separate high-risk operation.

- Restore a complete stock image for the exact build.
- Boot and verify it.
- Confirm no modified boot/vendor_boot/init_boot/dtbo artifacts remain.
- Follow current official device guidance.
- Do not relock merely because the modified kernel appears stable.
