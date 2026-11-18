---
name: avb-fix-repack
description: Unpack boot.img/vbmeta, modifikasi, recompute AVB footer, repack.
---

# AVB Fix & Repack

## Kapan pakai
Ketika kamu mengedit `boot.img` / `dtbo.img` / `vbmeta.img` dan perlu boot tetap valid (atau kamu memang ingin disable verification).

## Alat
`avbtool` (AOSP), `magiskboot` (untuk unpack/repack boot), python3.

## Protokol

### 1. Info image
```bash
python3 avbtool.py info_image --image boot.img
```
Output: `Footer version`, `Image size`, `VBMeta offset`, `Hash descriptor: digest`.

### 2. Unpack (kalau perlu edit)
```bash
magiskboot unpack boot.img
# edit kernel_dtb / ramdisk / fstab / cmdline sesuai kebutuhan
# JANGAN lupa simpan file asli sebelum diubah!
```

### 3. Repack + recompute AVB footer
```bash
magiskboot repack boot.img
# lalu perbaiki footer
python3 avbtool.py add_hash_footer --partition_name boot --partition_size <size-in-bytes> --image boot.img
# atau hanya re-extract digest:
python3 avbtool.py verify_image --image boot.img
```
Verifikasi ulang:
```bash
python3 avbtool.py verify_image --image boot.img
```
`Successfully verified sha256 hash of boot.img` = OK.

### 4. Kalau kamu sengaja disable verification
```bash
python3 avbtool.py info_image --image vbmeta.img
python3 avbtool.py disable_vbmeta_verification --image vbmeta.img
```
Hanya lakukan kalau kamu paham implikasi (Play Integrity BASIC saja yang terpengaruh; STRONG tidak — lihat `rom-spoofing`).

## Fakta
- AVB footer biasanya di **akhir** `boot.img` (offset = `Original image size`), bukan byte 0x800.
- `Hash descriptor` memiliki `salt` dan `digest`; keduanya harus cocok.
- Untuk `payload.bin`/OTA hibrid, AVB ditangani oleh `update_engine`, bukan langsung dari image — jangan disentuh.

## Laporan
```
boot.img: <path>
cmdline: <asli> → <baru>
footer: version=<v> digest=<VALID/INVALID>
action: <recompute | disable_verification | noop>
```
