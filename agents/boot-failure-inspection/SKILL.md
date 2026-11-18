---
name: boot-failure-inspection
description: Diagnosis bootloop, soft-brick, atau stuck-at-logo setelah flash atau kernel change di Android (khusus joyeuse/miatoll & ROM port). Dipakai ketika device tidak boot, masuk recovery terus, boot-loop.
---

# Boot Failure Inspection

Dipakai untuk mendiagnosis kenapa device tidak boot setelah flash ROM/kernel.
Hasilnya = laporan root cause + langkah yang aman untuk pemulihan.

## Kapan pakai
- Device boot-loop / stuck di logo / langsung ke recovery / mati total setelah flash.

## Alat yang dibutuhkan
- ADB (`~/Android/Sdk/platform-tools/adb`) atau fastboot
- OrangeFox / TWRP recovery di device
- Gambar hasil flash (zip, boot.img, super.img, dtbo.img) + hash-nya

## Langkah diagnosis (urutan aman)

### 1. Pastikan device merespons
```bash
adb devices
fastboot devices
```
- Kalau muncul di `adb devices` → masuk recovery, baca logcat.
- Kalau hanya di `fastboot devices` → device masih bootable ke fastboot, kernel/ramdisk masalah.
- Kalau tidak di keduanya → hard brick; hanya gunanya adalah EDL (firehose + programmer) — JANGAN coba flash apa pun, kumpulkan bahan dulu (Mi Toll tool, programmer).

### 2. Dari recovery (OrangeFox/TWRP) — read-only
```bash
# logcat dari boot terakhir
adb shell "cat /tmp/recovery.log" | tail -200
adb shell "logcat -b main -b system -b crash -d | grep -iE 'fatal|androidruntime|crash'" | head -50
# last_kmsg/pstore
adb shell "cat /proc/last_kmsg" > /tmp/last_kmsg.txt
adb shell "cat /sys/fs/pstore/console-ramoops-0" > /tmp/ramoops.txt
```
> Note: di OrangeFox `adb shell` biasanya root. Kalau tidak, baca dari `/sys/fs/pstore` saja.

### 3. Cek hal paling sering jadi penyebab (Urutan prioritas)
1. **fstab / dm-verity** — `/vendor/etc/fstab.qcom` tidak match image (terutama port lintas generasi). Tanda: `fs_mgr: failed to mount /` di last_kmsg.
2. **SELinux** — `avc: denied` di dmesg → device bootloop kalau `enforcing`. Sementara: `setenforce 0` dari recovery untuk uji (hanya sementara!).
3. **Vermagic / module** — modul vendor (4.14.190) di kernel baru (4.14.357) gagal insmod → `disagrees about version of symbol` di dmesg. Solusi: rebuild kernel dengan `port-allow-foreign-vermagic.patch`.
4. **AVB / vbmeta** — `dm-verity` error → image unsigned/diubah → bootloop. Solusi: relock verity cuma kalau vbmeta di-flash juga; selain itu patch vbmeta (`vbmeta --disable-verity --disable-verification`).
5. **Init ramdisk** — `init.rc` merujuk binary/file yang tidak ada (mis. spoofed fstab yang belum di-patch di ramdisk boot.img).
6. **EROFS mount fail** — kernel tidak punya `CONFIG_EROFS_FS` → `type "erofs" not supported` di dmesg. Cek kernel config kamu.
7. **Ukuran partisi** — super.img ditulis ke device yang tidak cukup besar (joyeuse butuh ≥ 8 GB super).

### 4. Troubleshoot cepat (kalau memungkinkan)
- **Boot ke system + logcat berjalan**: gunakan `adb logcat -b all | grep -iE "fatal|crash|error"`.
- **DTB/DTBO salah**: flash dtbo berbeda / disable dtbo di entri DTB boot.img.
- **Vendor mismatch**: flash vendor dari base yang sama (mis. Diza/Nezuko) kecuali yakin 100%.

### 5. Recovery (kalau akar diketahui)
- Bootloop ringan → re-flash **ZIP** dengan stock/base yang terverifikasi (SYNTHETICA/UF0-0.1 known-good).
- Kalau problem di kernel → flash **boot.img** yang sebelumnya jalan (fallback).
- Kalau problem di super → re-flash **super.img** dari rollback (`PREFLASH-BACKUP-*` tanpa suffix `.bak`).
- Kalau problem di dtbo → flash dtbo yang sesuai.

## Jangan lakukan
- Jangan relock bootloader setelah flash kustom — bisa permanently lock device.
- Jangan flash "vbmeta" random dari forum — bisa butuh key yang kamu tidak punya.
- Jangan coba "EDL boot" tanpa pengalaman — bisa mengubah device menjadi batu.

## Output laporan (format)
```
Device: <serial/model/fingerprint>
Kernel: <uname -r>
Gejala: <apa yang terjadi>
Root cause (duslep): <fstab/AVB/vermagic/init-SELinux/erofs/...>
Evidence: <baris logcat/last_kmsg>
Fix yang diusulkan: <langkah konkret>
Verifikasi: <cara memastikan perbaikan>
```
