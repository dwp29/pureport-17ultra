---
name: rom-regression-suite
description: Satu perintah tolok-ukur integritas paket ROM secara offline sebelum flash ke device.
---

# ROM Regression Suite

## Kapan pakai
Setiap selesai membangun/mengedit paket ROM — sebelum flash.

## Langkah verifikasi (format checklist)

```bash
ZIP="<path ke UFO-0.1-*.zip>"
echo "=== 1. ZIP utuh (unzip -t)"
unzip -t "$ZIP"

echo "=== 2. List entri (harus 5: update-binary, updater-script, boot, dtbo, super)"
unzip -l "$ZIP"

echo "=== 3. Hashs — bandingkan dengan file .sha256 yang kamu miliki"
sha256sum "$ZIP"
cat "${ZIP}.sha256" 2>/dev/null

echo "=== 4. Extract image ke /tmp (berhati-hati, ruang disk)"
mkdir -p /tmp/rom-verify && cd /tmp/rom-verify && unzip -o -j "$ZIP"

echo "=== 5. AVB boot.img"
python3 "<path to avbtool>" info_image --image boot.img 2>&1 || echo "avbtool tidak ada"

echo "=== 6. dump EROFS / fsck image"
dump.erofs -S super.img 2>&1 || fsck.erofs super.img 2>&1 || echo "erofs tools tidak ada"

echo "=== 7. Verifikasi rollback files ada sebelum flash"
ls /path/to/PREFLASH-BACKUP-* 2>&1 || echo "BACKUP TIDAK ADA — JANGAN FLASH"
```

## Lulus kalau
- unzip -t OK
- 5 entri, SHA-256 cocok, AVB digest VALID, fsck clean
- Rollback tersedia

## Gagal combat
Boleh dilanjutkan hanya jika kamu tahu persis kenapa gagal (mis. image yang di-repack sengaja berubah — itu memang tidak akan cocok hash-nya; tapi AVB harus tetap valid atau AVB harus aktif).
