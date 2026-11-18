---
name: kernelsu-module-dev
description: Development module KernelSU Next — struktur, lifecycle, verifikasi di device (rooted, tanpa flash ROM).
---

# KernelSU Next Module Dev

## Kapan pakai
Ketika kamu ingin membuat module untuk KernelSU Next (bukan meng-install module orang lain).

## Struktur module (standar MAGISK/KSU)
```
mymodule/
├── module.prop          # id, name, version, autorun
├── customize.sh         # dijalankan (choose) oleh installer KSU
├── service.sh           # background service (nohup-ish, di-late_start)
├── post-fs-data.sh      # di-post-fs-data (sebelum boot selesai)
├── system.prop          # props untuk setprop
├── sepolicy.rule        # opsional: SELinux rule
├── META-INF/            # updater-script / update-binary (opsional tapi direkomendasikan)
└── common/              # file yang akan di-merge ke /data/adb/modules/<id>/
```

## Isi minimal `module.prop`
```properties
id=<module-id>
name=<Module Name>
version=v1.0.0
versionCode=1
author=Your Name
description=<deskripsi>
```

## `service.sh` contoh
```bash
#!/system/bin/sh
MODDIR=${0%/*}
# menjalankan binary atau instruksi yang diinginkan
nohup "$MODDIR/common/mybin" > /dev/null 2>&1 &
```

## Install ke device (dengan KSU Manager rooted)
1. Zip module: `mymodule/` → `mymodule.zip` (format zip, bukan XZ).
2. Di KSU Next Manager → **Modules** → **Install module from storage** → pilih zip.
3. Reboot.

## Verifikasi
```bash
# di rooted adb shell (adb root atau su)
su -c "ls /data/adb/modules/"
su -c "cat /data/adb/modules/<id>/module.prop"
su -c "mybin --version 2>&1" || echo "binary tidak ada/eksek gagal"
```

## Jangan lakukan
- Jangan hardcode path `/system` — module tinggal di `/data/adb/modules`, overlay dibaca dari sana.
- Jangan tulis file ke root filesystem (itu bukan cara KSU bekerja untuk module; gunakan `system.prop` dan `system/` overlay).
- Jangan lupakan signature module: `service.sh`/`post-fs-data.sh` harus **executable** (chmod 755).

## Kalau perlu debugging
- `logcat -s <module-name>`
- `cat /data/adb/modules/<id>/service.log` (kalau kamu redirect log)
