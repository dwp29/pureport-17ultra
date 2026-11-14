---
name: rom-porting
description: End-to-end ROM porting workflow — from OTA payload.bin to a flashable build, including vbmeta/AVB, boot patching (Magisk), and flashing via TWRP
---

# ROM Porting Workflow (joyeuse / miatoll family — Redmi Note 9 Pro)

## ⭐ DEFAULT base ROM (pilih ini dulu)
- **Xiaomi.EU HyperOS** (miatoll) — `MiatollCave/Xiaomi.EU-Miatoll` (Unlicense) — stable HyperOS port, branch `main`. Recommended for first port; best stability/Play Store/camera fixes in miatoll community.
- Alternatives: CaveOfMiatoll (`iput-object/CaveOfMiatoll`, branches `hyperos-15` & `hyperos-15-cn`) — generic ports, less tested.
- Support & downloads: Telegram `@Miatoll`, `@MiatollOfficial`, `@MiatollClouds`, `@miatollcave`, `@miatollcavesupport`.



## Pipeline
1. **Extract OTA**
   - Payload: `payload-dumper-go payload.bin -o out/` (binary: `~/.local/bin/payload-dumper-go`)
   - super.img: `lpunpack out/super.img out/super -d` (binary: `~/.local/bin/lpunpack`)
   - Check image types: `binwalk out/*.img` (erofs/ext4/android_sparse)
2. **Unpack filesystems**
   - Prefer **MIO-KITCHEN** GUI: `mio-kitchen` (unpack boot/vendor/system/product/etc.) — handles erofs/ext4/f2fs, payload, super.img, .br files, boot.img
   - CLI fallback: `extract.erofs -x -L /path/image.img` (bundled in MIO-KITCHEN bin dir), `simg2img` (apt), `debugfs`
3. **Port (common recipes)**
   - overlay: `Overlayfs: replace /vendor/overlay/* with donor device's`
   - fstab: ensure donor line in `vendor/etc/fstab.*` matches target's partitions/labels (`vendor_b`, etc.)
   - `build.prop`: replace `ro.product.*`, `ro.build.fingerprint`, `ro.board.platform`, `ro.hardware`, `ro.vendor.product.*` with target values
   - Remove `vendor/lib*/hw/*.so` not needed/duplicate; add missing HALs from donor if vendor libs reference them
   - `init.target.rc` → target device policies; donor `init.rc` entries here
   - For MIUI ports: keep xiaomi framework jars + `xiaomi` libs; don't blindly replace `/system/framework*`
4. **Patch boot.img for Magisk (optional)**
   - `magiskboot unpack boot.img` → keep `kernel` + `ramdisk.cpio` → patch with Magisk → `magiskboot repack`
   - Or repatch on-device via Magisk app (recommended)
5. **Repack & flash**
   - `mkfs.erofs` / `mkfs.ext4` via MIO-KITCHEN GUI (recommended) or `img2simg` for sparse
   - AnyKernel3 zip: copy patched Image + dtb to AnyKernel folder → zip → flash via TWRP
   - Or `fastboot flash boot boot.img && fastboot flash vbmeta vbmeta.img`
6. **vbmeta/AVB** — if port fails to boot after boot.img: `fastboot flash --disable-verity --disable-verification vbmeta vbmeta.img` (unlocked only)

## Common failure modes
- Bootloop right after flash → wrong `fstab` offsets, or vendor HALs mismatched → check `vendor/etc/init/hw/*.rc`
- `dm-verity` errors → flash vbmeta with verification disabled (step above)
- "partition table doesn't match" → don't repack super.img blindly; use `lpmake` sized as original (`lpdump super.img` shows geometry)
- Signature verification → sign any flashable zips with testkey or disable via recovery

## Project conventions for this PC
- ROM workdir: `~/ROM-Tools/`
- MIO-KITCHEN: `~/ROM-Tools/mio-kitchen`
- Device: **joyeuse** (Redmi Note 9 Pro, miatoll family) — SD 720G "atoll", kernel 4.14, Treble (launcher3_21, vendor.img)
- Android targets: 11–16 (any GSI-portable ROM with Treble compatibility); MIUI-based ports work best
