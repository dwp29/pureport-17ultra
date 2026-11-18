---
name: payload-extract
description: Ekstrak Android OTA payload.bin → image (boot/vendor/super) menggunakan lpunpack.
---

# Payload Extract (`lpunpack`)

## Kapan pakai
Ketika kamu punya OTA ZIP hibrid (mis. `nezha_global-ota...payload.bin`) dan ingin mengekstrak image-nya.

## Alat
`lpunpack` (dari AOSP `build/make` atau `vendor/ota`). Cek:
```bash
which lpunpack && lpunpack --version 2>&1 | head -1 || echo "lpunpack belum terpasang"
```
Kalau belum ada: build dari AOSP atau ambil binary dari `aosp-tools`.

## Langkah
1. **Verify**: SHA-256 file `payload.bin` cocok dengan checksum yang diberikan (mis. nezha 9e8c7795…).
2. **List**: `lpunpack --list payload.bin` (atau `--info`) → lihat partisi yang tersedia.
3. **Extract**:
```bash
mkdir -p payload-out
lpunpack payload.bin payload-out/
```
Hasil: `boot.img`, `vendor.img`, `product.img`, `system.img`, dll.
4. **Verifikasi**: sha256sum setiap output vs catatan develop.
5. **Shim**: kalau image dinamis (super.img), ekstrak dengan `lpunpack` lalu proses ulang:
```bash
lpunpack --system system_a super.img super-patched/
```

## Caveat
- Beberapa OTA hibrid menyimpan image di dalam `payload.bin` yang di-gzip/zstd, bukan image mentah. `lpunpack` menangani itu otomatis.
- Extract image yang besar (super.img 8 GB) butuh ruang disk cukup — `df -h` dulu.
- **Jangan ubah payload.bin asli** — ekstrak ke folder kerja baru saja.
- Untuk OTA yang punya `payload_properties.txt`, verifikasi properti `block_device` dan `partition`.
