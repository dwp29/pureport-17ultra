---
name: reproduce-android-kernel-builds
description: Reproduce or qualify Android device kernel, root-provider, GKI LKM, and boot-image workflows for user-owned or explicitly authorized devices. Use for locking source revisions, diagnosing incomplete vendor drops, building reproducible baselines, selecting KernelSU Next, SukiSU Ultra, or other provider profiles, qualifying official provider releases or device-specific prebuilts, selecting KMI, repacking exact OTA or live stock boot/init_boot images, migrating providers, temporary or flash-based validation, reversible installation, and rollback gates.
---

# Reproduce Android Kernel Builds

Treat an Android kernel image as the output of a locked multi-repository supply chain. Prove the unmodified
baseline before integrating a patch, and separate build work from device-changing actions.

## Resolve instruction precedence

Treat this Skill as a set of defaults. Follow the user's current explicit task and project instructions when
they differ from these defaults. Do not treat a vague request as activation of a draft or as permission to
expand scope. Never use a user instruction to override higher-priority instructions, required authorization or
safety boundaries, or verified facts. If applicable instructions remain materially incompatible, report the
conflict and request direction instead of silently blending them.

## Enforce authorization and mutation gates

Proceed only for a device, source tree, boot image, and modification the user owns or is explicitly authorized
to use.

The following are separate authorizations or cleanup scopes:

1. inspect device facts and files
2. download sources
3. build and repack images
4. push staging files to the device
5. install or uninstall a manager application
6. unlock the bootloader or wipe data
7. temporarily boot an image
8. flash a named partition/slot, including an inactive slot after OTA
9. reboot the device for validation
10. install or remove root modules
11. remove downloads/staging files, application data, shared root-provider state, or module data
12. relock the bootloader

Never infer a later authorization from an earlier one. Do not push, install, uninstall, unlock, wipe, boot,
flash, reboot, switch slots, clean shared state, remove modules, or relock unless the user explicitly requests
that scope and the corresponding stop gate passes.

## Capture immutable device facts

Record before selecting sources:

- manufacturer, model, codename, board, SoC, ABI
- framework Android/SDK, vendor generation, factory build ID/fingerprint, and security patch
- `uname -a` and full kernel release
- device/provider-reported KMI and how it was derived
- bootloader lock state
- active slot and partition layout
- presence of `boot`, `init_boot`, `vendor_boot`, `dtbo`, and other relevant partitions
- boot header/AVB metadata
- provenance tier and hashes of the exact stock images used for rollback
- device-reported module versions, vermagic, and ABI evidence when applicable

Do not select a kernel or generic module by framework Android version alone. Treat framework Android, vendor
generation, full kernel release, KMI, and boot layout as separate dimensions. Select a generic GKI LKM by KMI;
a patch-level vermagic difference is a compatibility signal, not an automatic failure.

Read [gki-lkm-ota-repack.md](references/gki-lkm-ota-repack.md) before selecting a generic GKI LKM, repacking an
OTA/live stock image, choosing `boot` versus `init_boot`, or migrating provider state.

## Resolve and lock the source graph

1. Use the device kernel release and factory build as the primary anchors.
2. Locate the official device kernel branch, main kernel commit, and matching historical manifest when
   available.
3. Enumerate every manifest-managed and external input repository, toolchain, packaging tool, and third-party
   integration source.
4. Resolve each input to an exact commit and trusted remote.
5. Write a candidate source lock.
6. Audit the candidate against official source history and device evidence.
7. Accept it as the reproducible lock only after review.

A Repo manifest may still contain branch revisions. `repo sync` proves what was downloaded today, not that the
result exactly matches a historical factory build.

Read [source-locks-and-profiles.md](references/source-locks-and-profiles.md) before resolving commits or adapting
the workflow to another device.

Use `scripts/verify_source_lock.py` to compare a checked-out workspace with a TSV lock:

```bash
python3 scripts/verify_source_lock.py source-lock.tsv --workspace /path/to/workspace
```

## Select a route and evidence coordinates

Choose one formal route before building or repacking:

1. `reproduced-source`: lock exact critical inputs, prove an unmodified baseline, and isolate the modification.
2. `official-provider-release`: qualify a provider's immutable generic GKI/LKM release and locally repack it
   into an exact stock image. This route does not require source reproduction to fail first.
3. `community-prebuilt`: after source reproduction stops, qualify an immutable device-specific artifact.

Record the result on three independent axes:

- origin: `reproduced-source`, `official-provider-release`, or `community-prebuilt`
- integration: `built-in`, `kernel-replacement`, or `lkm-stock-repack`
- qualification: `candidate`, `runtime-qualified`, or `retained`

Source discovery may separately stop at `candidate-source` or `incomplete-source`. Only a complete source route
may be described as reproduced. Do not keep patching compile errors when the source graph is incomplete.

Read [vendor-source-and-prebuilt-fallback.md](references/vendor-source-and-prebuilt-fallback.md) for the vendor
source gap analysis, recovered `chopin` case, and third-party artifact qualification.

## Build the unmodified baseline first

Stop before integrating any kernel patch until the original source combination builds successfully.

Verify the baseline against the stock device/image:

- kernel release string
- architecture and compiler/toolchain identity
- expected primary image format
- DTB/DTBO identity or device-specific equivalent
- module count, names, vermagic, symbol versions, and CRCs where available
- configuration and required vendor options
- bootability evidence appropriate to the project

If the baseline does not match, fix source selection, configuration, toolchain, or packaging. Do not compensate
by patching the modified build.

## Isolate the modification

- Pin the third-party or local change to an exact commit.
- Record the baseline commit, integration commit/diff, configuration changes, and generated files.
- Keep device-specific integration in a profile/adapter rather than hard-coding it in a global workflow.
- Rebuild from a clean, verified state.
- Compare baseline and modified artifacts so every difference has an intended cause.
- Preserve the complete build log, configuration, source lock, toolchain version, and artifact hashes.

Treat the root implementation as a profile-selected provider, not a hard-coded global dependency. Record:

- provider and exact source/release commit
- manager identity and compatible version
- integration mode such as GKI image, LKM, legacy/non-GKI built-in, or provider-specific kernel patch
- supported kernel range and architecture
- required hooks, configuration, modules, and companion patches
- partition and packaging expectations

For KernelSU Next, SukiSU Ultra, KernelSU, or another provider, verify current official compatibility against
the actual kernel generation and partition layout. Never mix one provider's manager, module, kernel driver, or
installation instructions with another provider unless their official compatibility contract explicitly
permits it. Do not treat GKI/LKM/provider mode and temporary/permanent installation as the same dimension.

Provider selection is a profile change, not a rewrite of common source, artifact, recovery, or flash gates.

## Qualify an official provider repack separately

For an official generic GKI LKM or provider release:

- retain the official release, manager, daemon/patcher, LKM, source snapshot when used, and immutable hashes
- derive KMI from the device with the current provider's official command when available
- qualify architecture, modversions/symbol behavior, module-signing policy, and provider loader behavior
- select the target partition only after parsing actual boot headers and cross-checking provider logic
- repack only an exact `live-partition-exact` or `package-exact` stock image
- label a passing result `qualified-provider-repack`, not `qualified-prebuilt` or `reproduced`

Follow [gki-lkm-ota-repack.md](references/gki-lkm-ota-repack.md) for the complete record and migration gate.

## Qualify a third-party artifact separately

When a reproducible source build is impossible and the user chooses a prebuilt:

- require exact device codename/variant, ROM/factory build, kernel release, Android/vendor generation, boot
  header, partition, slot, and architecture compatibility
- capture the release URL, publisher, timestamp, filename, SHA-256, signature/attestation when available, and
  any source commit, build log, config, toolchain, or CI evidence
- unpack and inspect the artifact before device use
- reject a generic filename, chat attachment, moving link, mismatched codename, unexplained repack, or missing
  rollback image
- label the result `qualified-prebuilt`, never `reproduced`
- prefer temporary boot when the exact device supports it and the user separately authorizes it

Successful boot is runtime evidence for that artifact/device state; it does not reconstruct missing source
provenance.

## Repack from an exact stock source

- Classify the source as `live-partition-exact`, `package-exact`, or `candidate-package`.
- Use only an exact live partition or an internally verified complete OTA/factory/fastboot package for a
  candidate that may reach a device.
- Replace only the components required by the proven integration.
- Preserve header version, command line, ramdisk, compression, page size, OS/security fields, AVB properties,
  and device-specific metadata unless the design explicitly changes them.
- Repack with a version-compatible toolchain.
- Produce hashes for input stock image, baseline kernel, modified kernel, and repacked boot artifact.
- Keep the untouched stock image and a tested recovery route.

Do not assume `init_boot` exists or is the target because a newer device guide uses it. Parse boot headers and
identify which image owns the kernel, generic ramdisk, or vendor ramdisk required by the provider.

## Apply stop gates

Read [validation-gates.md](references/validation-gates.md) before any device-changing action.

Required progression:

```text
device facts
  -> route and evidence-coordinate selection
  -> [accepted source lock -> clean baseline -> isolated modification]
     OR [official provider release -> KMI/loader qualification -> exact-stock LKM repack]
     OR [third-party artifact provenance -> compatibility inspection]
  -> candidate artifact checks
  -> recovery plan
  -> explicit temporary-boot authorization
  -> temporary runtime validation
     OR explicit flash-based validation authorization
  -> runtime validation
  -> explicit retain/permanent-install decision
```

Prefer a supported temporary boot for first runtime validation, but do not describe it as risk-free. A patched
`init_boot` or `vendor_boot` image is not automatically a complete image accepted by `fastboot boot`. If the
device/provider has no exact temporary route for the changed partition, stop and present Gate 6B rather than
silently flashing or passing the partial image to a generic boot command.

Treat temporary-boot capability and slot fallback as device facts that must be demonstrated, not inferred.
A loader crash during a non-flashing boot attempt does not by itself prove that the image is invalid, and an
A/B layout does not prove that the inactive slot can boot independently. If the temporary route is unavailable
or fails before kernel execution, preserve that evidence and require a new explicit authorization before
proposing any flash-based validation. Treat permission to flash for the first runtime test separately from the
later decision to retain that installed artifact.

## Validate runtime and rollback

After an explicitly authorized temporary boot or flash, verify:

- expected kernel release and modification status
- ADB connectivity and boot completion
- storage, display, touch, radios, cameras, sensors, charging, suspend, and other device-critical functions
- module loading and kernel logs
- root/manager behavior only if that is the authorized modification
- reboot persistence only after permanent installation is explicitly authorized

Label service presence, device enumeration, sensor events, logs, and state queries as automated proxy evidence.
Label actual photo capture, calls/data, fingerprint use, and suspend/wake as human functional evidence. Do not
claim the latter from the former.

After retention and a passing second reboot, apply the provider migration/cleanup gate before removing an old
manager or data. Do not infer ownership from `ksu`, `ksud`, or `/data/adb/ksu`; treat manager app data, staging
files, shared provider state, sparse module images, and installed modules as separate authorization scopes.

Rollback immediately on boot loop, missing critical hardware, ABI/module failures, repeated kernel panic, or
unexpected verified-boot behavior.

Never relock the bootloader until a complete stock image has been restored, booted, and verified for the exact
device/build. Relocking a modified or mismatched image can make recovery substantially harder.

## Deliver a reproducible record

Document:

- device profile and captured facts
- source selection reasoning
- accepted source lock and trusted remotes
- baseline commands, logs, and validation
- integration diff and configuration
- artifact hashes and boot metadata
- every stop gate and its evidence
- commands that were only proposed versus actually executed
- temporary-boot/flash outcome
- exact rollback artifact and procedure
- remaining unverified assumptions

State the three evidence coordinates. When a compact label is useful, use `reproduced`, `candidate-only`,
`incomplete-source`, `qualified-provider-repack`, or `qualified-prebuilt` according to the mappings in
[gki-lkm-ota-repack.md](references/gki-lkm-ota-repack.md). Never claim a workflow is reproduced merely because
compilation completed, an official LKM loaded, or a third-party image booted.
