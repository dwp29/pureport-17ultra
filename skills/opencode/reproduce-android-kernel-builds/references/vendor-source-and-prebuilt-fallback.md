# Vendor Source and Prebuilt Fallback

## Contents

- Evidence classes
- Vendor source gap analysis
- Recovered `chopin` pattern
- Third-party artifact record
- Root provider expansion
- Relationship to official provider repacks

## Evidence classes

Keep source-gap conclusions separate from artifact qualification:

| Class | Meaning |
| --- | --- |
| `reproduced` | Exact critical inputs are locked; an unmodified baseline and intended modification are verified |
| `candidate-only` | Plausible source exists, but historical/device correspondence remains unproven |
| `incomplete-source` | Critical source, generated input, module, toolchain, or revision is unavailable |
| `qualified-provider-repack` | An immutable official provider release was locally integrated into exact stock and passed runtime gates |
| `qualified-prebuilt` | An immutable community prebuilt passed provenance, compatibility, recovery, and runtime gates |

A booting image can qualify a prebuilt, but cannot upgrade it to `reproduced`.

For every candidate also record origin (`reproduced-source`, `official-provider-release`, or
`community-prebuilt`), integration (`built-in`, `kernel-replacement`, or `lkm-stock-repack`), and qualification
(`candidate`, `runtime-qualified`, or `retained`).

## Vendor source gap analysis

For every official vendor drop, answer:

1. Does an exact target build or kernel release map to a tag/commit, or only to a broad Android branch?
2. Are all manifest repositories and historical revisions present?
3. Are vendor modules, DTB/DTBO inputs, generated headers, firmware interfaces, and build scripts present?
4. Is the original toolchain obtainable and pinned?
5. Can an unmodified image be built without reconstructing unknown vendor changes?
6. Does its release string, config, ABI, modules, and boot packaging match the stock artifact?

If the answer to a critical item is no, stop at `candidate-only` or `incomplete-source`. Fixing individual
compiler errors does not fill a historical source gap.

## Recovered `chopin` pattern

Use this as a generalized case study, not a device-ready recipe:

- The recovered device was Redmi Note 10 Pro 5G / POCO X3 GT, codename `chopin`. Do not substitute the
  similarly marketed `sweet` or `sweetin` families.
- A named official vendor branch existed, but the recovered unmodified baseline stopped because a required
  Mali GPU source component was absent. Branch presence therefore did not establish a complete source graph.
- A community source candidate was also insufficient for the requested result because the intended root
  provider implementation was not present. A plausible kernel tree is not proof of the requested integration.
- The authorized fallback used a device-specific KernelSU Next prebuilt repacked into the exact stock boot
  template. Its runtime success is `qualified-prebuilt` evidence, not reproduced-source evidence.
- A temporary boot attempt failed in the loader path before normal kernel validation, and the alternate slot
  was not independently bootable. Only a later, separately authorized flash to the resolved stock slot
  produced the successful boot and hardware/root smoke evidence.

This pattern preserves both facts: the source-build attempt failed for evidence/supply-chain reasons, while a
separate prebuilt route may still succeed safely enough for the authorized device.

## Third-party artifact record

Record:

```text
device:
  manufacturer
  model
  codename and regional variant
  build/ROM and security patch
  kernel release
  architecture
  active slot and target partition
  boot header/AVB facts

provider:
  name
  manager package/version
  integration mode
  claimed source/release commit

artifact:
  publisher
  release URL and timestamp
  retained filename
  SHA-256
  signature/attestation
  available source, config, toolchain, build log, and CI run
  unpacked metadata

recovery:
  exact stock image SHA-256
  temporary-boot support and observed loader behavior
  independently proven slot viability
  rollback command and host/device prerequisites

result:
  proposed/temporarily booted/flashed
  runtime checks
  provider activation evidence
  remaining unknowns
```

Do not trust screenshots, filenames, or success comments as artifact identity.

## Root provider expansion

Keep provider selection inside the device profile:

```text
provider
provider source/release commit
manager compatibility
integration mode
kernel/architecture support
required hooks/config/patches
artifact source and hash
validation commands
```

KernelSU Next and SukiSU Ultra are independent providers even when they share ancestry or concepts. Re-run
official compatibility checks at use time and keep their managers, drivers, modules, setup scripts, and
provider-specific patches isolated.

For SukiSU Ultra or any other provider:

1. add a provider profile pinned to official source/release evidence
2. select the compatible GKI/LKM/non-GKI/provider-specific mode for the exact device
3. rerun the unchanged source, baseline or prebuilt, packaging, recovery, and runtime gates
4. retain provider-specific KPM or companion patch provenance where used

Do not make SukiSU Ultra support contingent on rewriting the common workflow.

## Relationship to official provider repacks

Do not route an official generic GKI LKM through this fallback merely because it is a precompiled `.ko`.
`official-provider-release + lkm-stock-repack` is a first-class path and does not require a failed device-source
build. Follow [gki-lkm-ota-repack.md](gki-lkm-ota-repack.md) for KMI, exact-stock, partition-target, AVB,
temporary-validation, and provider-migration rules.
