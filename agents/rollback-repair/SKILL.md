---
name: rollback-repair
description: Pulihkan device dari bad flash ke state yang diketahui baik (mis. Lunaris A16 dari PREFLASH-BACKUP).
---

# Rollback & Repair

## Kapan pakai
Setelah flash gagal membuat device bootloop/soft-brick. Juga sebagai checklist sebelum flash yang berisiko.

## 1. Sebelum flash — lakukan BACKUP
```bash
# dari oFox/TWRP atau adb shell (root)
mkdir -p /sdcard/ROLLBACK-<DATE>
dd if=/dev/block/bootdevice/by-name/boot of=/sdcard/ROLLBACK-<DATE>/boot.img bs=4096
dd if=/dev/block/bootdevice/by-name/dtbo of=/sdcard/ROLLBACK-<DATE>/dtbo.img bs=4096
dd if=/dev/block/by-name/super of=/sdcard/ROLLBACK-<DATE>/super.img bs=4096
# vendor biasanya ikut di super; ekstrak terpisah kalau perlu
# checksum masing-masing
sha256sum /sdcard/ROLLBACK-<DATE>/*
```
Copy ke PC/komputer.

## 2. Kalau boot gagal — langkah pemulihan
1. Boot ke recovery (oFox): tombol power+vol up, atau `adb reboot recovery`.
2. **Format Data** kalau enkripsi rusak (lihat FLASH-MANUAL 2.6).
3. Flash kembali rollback:
```bash
# dari recovery TWRP/oFox via adb (root)
adb shell "dd if=/sdcard/ROLLBACK-<DATE>/super.img of=/dev/block/by-name/super bs=4096"
adb shell "dd if=/sdcard/ROLLBACK-<DATE>/boot.img of=/dev/block/by-name/boot bs=4096"
adb shell "dd if=/sdcard/ROLLBACK-<DATE>/dtbo.img of=/dev/block/by-name/dtbo bs=4096"
```
Atau dari PC via fastboot (jika slot mendukung — karena joyeuse A-only, ini mungkin tidak applicable).
4. Reboot system, tunggu 5–15 menit.

## 3. Verifikasi pemulihan
- `adb devices` → `device` (bukan `recovery`/`offline`)
- `getprop sys.boot_completed` = 1
- dumpsys disk/MEM ok

## 4. Kalau rollback juga tidak boot
- Ini berarti partisi lain rusak (vendor/init) atau bootloader issue.
- Ambil persediaan: stock MIUI 12 recovery ROM (`miui_JOYEUSEGlobal_...zip`), oFox, dan jalankan flash **stock** — mengembalikan device ke kondisi awal.
- Kalau tetap tidak boot → EDL/firehose (hanya untuk yang berpengalaman).

## 5. Checklist pasca-rollback
- Verifikasi hash `super.img`/`boot.img`/`dtbo.img` cocok dengan file yang kamu simpan.
- Boot ke system dan cek fungsi dasar: WiFi, RIL, storage, kamera.
- Simpan log ke PC.
