# GKI LKM and Exact-Stock Repack

## Contents

- Route and evidence coordinates
- Compatibility dimensions and KMI
- Official provider release qualification
- Exact stock source tiers
- Patch-target selection
- Repack and AVB invariants
- Temporary versus flash validation
- Provider migration and shared-state cleanup
- Runtime evidence levels
- Required record

## Route and evidence coordinates

Treat an official generic GKI LKM repacked into an exact stock image as a first-class route. It does not require
proof that a device kernel source build is impossible, and it is not a device-specific community prebuilt.

Record three orthogonal coordinates:

| Axis | Values |
| --- | --- |
| origin | `reproduced-source`, `official-provider-release`, `community-prebuilt` |
| integration | `built-in`, `kernel-replacement`, `lkm-stock-repack` |
| qualification | `candidate`, `runtime-qualified`, `retained` |

Use `qualified-provider-repack` as a compact final label only for
`official-provider-release + lkm-stock-repack + runtime-qualified/retained`. Keep `qualified-prebuilt` for a
qualified `community-prebuilt`. Never use either label to imply reproduced device kernel source.

The three formal routes are therefore:

1. reproduce source, prove an unmodified baseline, and integrate an isolated change;
2. qualify an official provider release and locally repack it into an exact stock image;
3. after source reproduction stops, qualify a device-specific community prebuilt.

## Compatibility dimensions and KMI

Keep these facts separate:

- framework Android version and SDK;
- vendor/device generation and factory build;
- full running kernel release and patch level;
- GKI Kernel Module Interface (KMI) generation;
- architecture, module-signing policy, and boot layout.

Select a generic GKI LKM by KMI, not by framework Android version. Prefer a current official provider command
that derives KMI from the running device, such as `ksud boot-info current-kmi`, and retain its output. When no
provider command exists, derive the candidate KMI from the full kernel release and corroborate it with official
provider compatibility data.

Do not reject an LKM solely because its patch-level vermagic is not byte-identical to the running kernel.
Qualify all of the following instead:

- KMI generation and architecture;
- `CONFIG_MODVERSIONS` and symbol-version/CRC behavior;
- required exported symbols or KALLSYMS availability;
- module-signing enforcement and provider signing/loading behavior;
- the provider's early loader or symbol-resolution contract;
- runtime module-load diagnostics.

A successful module load is runtime qualification for the retained module, provider release, and device state.
It does not prove arbitrary modules with the same KMI will load.

## Official provider release qualification

For an `official-provider-release` input, retain:

- official release URL, version, timestamp, filenames, and immutable hashes;
- manager package identity/version and hash;
- the exact embedded or companion daemon/patcher hash;
- LKM filename, module identity, hash, KMI, architecture, and vermagic;
- official compatibility/install guidance or source snapshot used to interpret loader behavior;
- the exact provider command and arguments used to produce the candidate.

Keep manager, daemon, loader, driver/LKM, and provider-specific modules from the same compatible provider
release unless current official evidence explicitly permits another combination.

## Exact stock source tiers

Classify every stock boot-chain input:

1. `live-partition-exact`: read from the current slot after rechecking build, slot, and partition identity;
2. `package-exact`: extracted from a complete OTA/factory/fastboot package whose internal metadata exactly
   matches the current target build/fingerprint;
3. `candidate-package`: filename or advertised version appears to match, but internal metadata has not proved
   target identity.

Only the first two may provide an exact rollback image. For a package source, record package filename, size,
SHA-256 and published checksum when available; `pre-device`, `post-build`, SDK, SPL; payload size and relevant
metadata hash; extraction-tool version, source, and hash; and hashes of every extracted boot-chain image.

Do not call every source a factory image. A matching full Recovery OTA `payload.bin` can be the strongest exact
source for a device/build.

## Patch-target selection

Parse the actual boot and vendor-boot headers before choosing a partition. Record, at minimum, header version,
kernel size, ramdisk size, total image/partition size, and AVB footer/descriptor facts.

Resolve the target from the provider's integration contract and observed image contents:

| Observed image and integration | Candidate target |
| --- | --- |
| kernel replacement in `boot` | exact `boot` image |
| generic LKM injected into the generic ramdisk | image that actually owns that ramdisk, commonly `init_boot` |
| vendor ramdisk fragment change | exact `vendor_boot` image/fragment |
| ambiguous or provider result disagrees with header inspection | stop and resolve before repacking |

The presence of `init_boot`, the framework Android version, or a generic online guide is not sufficient. Cross-
check the parsed result with the current official provider's automatic target decision when available.

## Repack and AVB invariants

Round-trip qualification does not require a provider-patched or restored image to be byte-identical to stock.
Classify differences:

- expected: authorized ramdisk contents/size, hash descriptor digest, `original_image_size`, `vbmeta_offset`,
  padding, or other tool-controlled values explained by the patch;
- invariant unless the plan explicitly changes it: header version, partition image size, kernel/ramdisk layout,
  page size, command line, OS/SPL fields, AVB algorithm and flags, and unrelated descriptors/components.

Run the provider's restore/unpatch operation only as structural evidence that its markers are recognized. Its
output is not the exact rollback artifact unless independently proven byte-identical to the retained
`live-partition-exact` or `package-exact` stock image.

## Temporary versus flash validation

Do not equate `fastboot boot` with validation of every boot-chain partition:

| Candidate | Temporary-validation rule |
| --- | --- |
| complete boot image accepted by the device loader | `fastboot boot` may be proposed after explicit authorization |
| `init_boot`-only patch | do not pass it to `fastboot boot` as if it were a complete boot image |
| `vendor_boot`-only patch | require a documented device/provider composite route or use the flash gate |
| loader rejects/crashes before kernel execution | preserve loader evidence; do not classify kernel/LKM incompatible |

When no exact non-flashing route exists, use the separately authorized flash-based first-runtime gate. Name the
partition, slot, candidate hash, exact stock rollback hash, expected interruption, and recovery command.

## Provider migration and shared-state cleanup

Treat provider migration as a separate cleanup gate after the new provider has passed runtime validation,
retention approval, and a second reboot.

- Prove the new manager/daemon/provider and intended LKM or driver are active.
- Inventory the old manager package and app sandbox separately from shared root state and installed modules.
- Do not infer ownership from compatibility names such as `ksu`, `ksud`, or `/data/adb/ksu`.
- Audit provider records, allowlists/profiles, logs, `/data/adb` module records, Zygisk/LSPosed state, and the
  provider's actual module store.
- Treat sparse `modules.img` or another provider-managed filesystem as an opaque managed artifact unless a
  separately reviewed tool and recovery plan authorizes inspection or repair. Do not ordinary-copy, mount,
  truncate, or repair it speculatively.
- Authorize removal of the old manager application, stale downloads/staging files, shared provider state, and
  root modules as separate cleanup scopes.

The safe default is to remove only the proven obsolete manager package/app data and explicitly identified
staging/download artifacts while preserving shared provider/module state.

## Runtime evidence levels

Separate automated proxy evidence from human functional evidence:

| Level | Examples |
| --- | --- |
| automated proxy | service present, device enumerated, sensor events observed, radio state, charging state, logs |
| human functional | actual photo capture, cellular call/data, fingerprint unlock, suspend/wake behavior |

Do not claim a human function passed from service presence alone. Record unperformed human checks as remaining
validation, even when automated proxies are healthy.

## Required record

Record the three evidence coordinates, device/build/kernel/KMI facts, provider inputs and hashes, stock-source
tier and provenance, parsed target decision, repack command and invariant diff, candidate and rollback hashes,
authorization events, temporary/flash path, first and second reboot evidence, automated proxies, human tests,
cleanup scopes, and retained unknowns.
