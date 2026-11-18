---
name: logcat-error-diagnosis
description: Diagnosis error app/ROM port dari logcat, ANR, dan crash dump. Dipakai ketika app FC/borok/timeout/layanan system crash.
---

# Logcat Error Diagnosis

## Alat
- `~/Android/Sdk/platform-tools/adb logcat`
- `dumpsys`, `dropbox`

## Alur kerja

### 1. Ambil crash/ANR yang relevan
```bash
# Semua buffer, bersih dulu
adb logcat -b all -c; adb logcat -b all -v threadtime > /tmp/logcat-full.txt
# Hanya crash
adb shell "logcat -b crash -d -v threadtime" > /tmp/crash.txt
# ANR traces
adb shell "cat /data/anr/traces.txt" > /tmp/anr.txt
# Dropbox (mengapa system mati)
adb shell "dumpsys dropbox --print" > /tmp/dropbox.txt
```

### 2. Ekstrak error sebenarnya
```bash
grep -iE "fatal|E .*: |RuntimeException|FATAL|AndroidRuntime|System.out: |zygote|PackageManager" /tmp/logcat-full.txt | head -40
```

Pola-pola umum:
- **`java.lang.SecurityException: ...`** → permission/Selinux/signature mismatch — bukan bug kode, tapi konfigurasi.
- **`ClassNotFoundException / NoClassDefFoundError`** → framework/ABI mismatch (contoh: framework A16 di vendor A14 atau sebaliknya).
- **`java.lang.NoSuchMethodError`** → framework Android 17 memanggil method HAL yang tidak ada di vendor target (contoh: audio/VNDK). Solusi: null-safety patch di smali atau vendor downgrade.
- **`libselinux` denial + `avc` di dmesg** → policy missing. Tambahkan rule di `*_file_contexts` atau permissive (sementara).
- **`OutOfMemoryError`** → app butuh RAM lebih dari yang tersedia (ZRAM). Naikkan ZRAM atau tutup app lain.
- **`deadlock / frozen main thread`** → ANR; `traces.txt` menunjukkan thread manapun yang blocked.

### 3. Laporan
```
App/service: <nama>
Error class: <SecurityException | CNFE | NoSuchMethodError | ANR | OOM | permission | AVC>
Root cause: <bukan hanya "error" — jelaskan mengapa>
Fix: <langkah konkret>
Fallback: <siapan kegagalan>
```

## Jangan lakukan
- Jangan tangkap `-b all` tanpa filter kalau log sangat besar — pakai `-b main -b system -b crash`.
- Jangan patch smali tanpa paham alur pemanggilan (misal: npk menulis signature bypass tanpa mengetahui dipanggilnya).
- Jangan asumsikan "system crash = bug app" — bisa juga vendor/kernel/SELinux.
