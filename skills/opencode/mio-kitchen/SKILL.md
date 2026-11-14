---
name: mio-kitchen
description: Use MIO-KITCHEN to unpack and repack Android ROM images (boot.img, payload.bin, super.img, erofs/ext4/f2fs, dtbo, logo) on Linux
---

# MIO-KITCHEN (`mio-kitchen` — GUI ROM kitchen)

Location: `~/ROM-Tools/mio-kitchen` · Launch: `mio-kitchen` (or app menu "MIO-KITCHEN", icon: splash.png)
Python venv: `~/ROM-Tools/mio-kitchen/.venv` (all requirements incl. PySide6, androguard, avro, python-lzo — complete)
Bundled binaries (no separate install): `bin/Linux/x86_64/` — magiskboot, mkbootimg, mke2fs, make_ext4fs, mkfs.erofs, extract.erofs, extract.f2fs, afptool, dtc, img2simg, imgkit, e2fsdroid, delta_generator, cpio, busybox, zstd, brotli, cpio, apg…
First run creates `bin/settings.json` — keep `Language` as `app_en_US.qm` (change before first launch if user wants Chinese/id).

## Typical workflows

### Unpack boot.img
GUI: drop `boot.img` into MIO-KITCHEN → select **Unpack Boot** → it extracts kernel + ramdisk to `work/` with `split_img/` and `ramdisk/`.
CLI fallback: `magiskboot unpack boot.img out/` (in MIO bin dir or `~/ROM-Tools/mio-kitchen/bin/Linux/x86_64/magiskboot`)

### Unpack payload.bin
GUI: **Utils → Payload Dumper** (or `payload-dumper-go` directly from terminal: `payload-dumper-go payload.bin -o out/`)

### Unpack super.img
GUI: **Unpack Super Image** → outputs per-partition `system.img`, `vendor.img`, etc.
CLI fallback: `lpunpack super.img out/` (binary at `~/.local/bin/lpunpack`)

### Unpack erofs/ext4/f2fs
GUI: **Unpack Image** → pick file → auto detects fs type → decompresses to output dir
CLI fallback (erofs): `extract.erofs -x image.img --output out/`

### Repack
Same screens reversed: select **Pack** mode, set output name/size → done. For boot.img keep ramdisk intact; for partition images use the same padding/alignment as original (check `.config`/partition table from `lpdump`).

## Tips
- GUI runs under X11 (`DISPLAY=:0`); the PC runs Mint XFCE
- Logs go to `~/ROM-Tools/mio-kitchen/log.txt` if a button click silently fails
- `SELINUX` note: repacked boot.img keeps `selinux=1` — don't change kernel cmdline unless you know
- `vbmeta.img` usually does **not** need repacking; flash stock `vbmeta` with `--disable-verity --disable-verification` if boot fails signature checks
- To deodex: use `smali`/`baksmali` (apt, v2.5.2) or MTK/UniversalDeodexer
