---
name: synthetica-kernel
description: Flash & verify Synthetica kernel workflow for joyeuse/miatoll + HyperOS 4 (HOS 4) — ROM first, then kernel, then KSU Manager root check
---

# Synthetica Kernel Workflow (joyeuse / miatoll family — Redmi Note 9 Pro)

## Paths on this PC
- Extracted archive: `~/ROM-Tools/synthetica-arsip/SYNTHETICA-KERNEL-ARSIP-LENGKAP-2026-11-13/`
- ROM HOS 4: `~/Downloads/HyperOS-4_MIATOLL-STABLE-dizasports.zip` (4.5 GB; TWRP/OrangeFox flashable; porter @dizasports, base Xiaomi 18 Pro Max; bugs: **no camera app** — install GCam/Leica Camera Module; Face Unlock broken; needs 1 day to settle)
- Kernel for HOS4: `01-KERNEL-SEMUA-VERSI/04-KERNEL-Project-HOS-4.0-Synthetica-2.0/synthetica-2.0-kernel-hos4.zip` — README: same folder (`README-KERNEL-SYNTHETICA-2.md`), authoritative
- Daily Manager APK: `02-APK-MANAGER-SEMUA-VERSI/03-APK-Manager-6.0.0-Universal-SIGNED-R2/Synthetica-Manager-6.0.0-Universal-SIGNED-R2.apk`
  - SHA-256: `29fe923f091cc96306b7b32f9b617bd069ba807e02aa8026a0febca3d0f64697` (**verified matches panduan**)
- Diagnostics (log collector & boot audit): `06-ALAT-DIAGNOSTIK/`
- Security key notes: `05-KEY-SIGNING/` (NEVER distribute)
- One UI 8 bootloop log (12 Nov 2026): `07-LOG-DAN-BUKTI-KOMPILASI/2026-11-12_BOOTLOG-joyeuse-OneUI8-bootloop-Recovery-Log.zip`

## Flash order (SAFE — never skip steps)
1. **Backup first** (TWRP/OrangeFox): Data, persist, IMEI (EFS), vbmeta, boot — BEFORE touching anything
2. Flash ROM HOS 4 zip → wait first boot (3–10 min) → confirm it boots stable (+1 day)
3. Flash `synthetica-2.0-kernel-hos4.zip` — **data must be DECRYPTED in recovery** (ksud needs /data/adb)
4. Reboot → install KSU Manager (from `/system/priv-app/KSUManager/` or push APK) → verify root ("Root access granted")
5. Test in Termux: `su` → `id` → expect `uid=0(root)`
6. Optional: install Synthetica-Manager 6.0.0 R2 + diagnostics for bug reporting

## Warnings / Security
- **NO camera app** in HOS 4 build → install GCam or Leica Camera Module from Play Store
- **Face Unlock broken** — use fingerprint/PIN
- Never relock bootloader on a custom ROM/kernel
- **NEVER share archive or `05-KEY-SIGNING/`** — contains signing keys + your release certificate
- Pure Manager release key `A2:F9:42:45:2E:EC:...` is ALSO in PUBLIC GitHub repo `dwp29/Synthentica` (ci-stage/, used once for 0.10.0) → treat as burned for public releases; replace before distributing to anyone
- Do NOT re-sign Manager APKs — kernel checks signature (net.ember.labs)
- Kernel ZIPs marked DO-NOT-FLASH / TEST are build proofs, not releases
- On-device testing not independently verified (13 Nov 2026) — proceed at your own risk; keep original boot.img backup

## Diagnostics
- Use `06-ALAT-DIAGNOSTIK` tools to collect logs for bug reports (log collector + boot audit)
- On bootloop: capture logcat/last_kmsg → compare with One UI 8 bootloop log in `07-LOG-DAN-BUKTI-KOMPILASI`
