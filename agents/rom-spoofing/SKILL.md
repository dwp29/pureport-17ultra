---
name: rom-spoofing
description: Spoofing untuk Play Integrity BASIC di ROM kustom — apa yang boleh, apa yang harus dihindari, jujur.
---

# ROM Spoofing — Batas & Cara yang Aman

## Kapan pakai
Ketika kamu ingin device yang di-flash kustom tetap bisa mengakses Google Play Store, dan kamu **sadar risiko dan batasannya**.

## Prinsip
1. **BASIC bisa dispoof** — ini kenyataan, bukan janji.
2. **STRONG TIDAK BISA** — yang diperiksa Google (TEE/StrongBox attestation signature) tidak bisa dipalsukan dari userspace ROM.
3. **Jangan jual/distribsikan ROM yang mengaku "Play Store certified"** — itu menyesatkan.
4. **Jangan gunakan untuk fraud/duplikasi akun** — itu违法.

## Cara minimal (yang dipakai di UFO-0.1)
```properties
# di /vendor/build.prop
ro.oem_unlock_supported=0
ro.boot.flash_locked=1
ro.boot.verifiedbootstate=green
ro.boot.vbmeta.device_state=locked
```
+ **cmdline boot.img** (`androidboot.locked=1` dll.) — ini yang benar-benar dibaca oleh Play Integrity API pada first boot.

## Cara tepat "spoof" — apa yang diklaim dan tidak
| Klaim | Status |
|---|---|
| "Device terlihat locked" | ✅ Spoofable — via ini saja Play Integrity BASIC biasanya lolos |
| "Device ter-certifikasi penuh oleh Google" | ❌ Tidak — butuh attestation hardware. Jangan klaim ini. |
| "Play Store jalan normal" | ⚠️ Sering jalan, tapi bisa berubah kapan saja. |
| "Tidak bisa dideteksi" | ❌ Google & bank app bisa mendeteksi (root, custom ROM, KSUNEXT). |

## Keberatan teknis
- **Play Integrity API (Strong)** mengecek `KEY_MASTER`/`KeyMint`/`StrongBox` attestation — signature kunci Google yang **hanya bisa digenerate di hardware TEE/SE**. Userspace **tidak bisa** memalsukannya.
- **Device state locked** di cmdline hanya menghindari *soft ban*, bukan strong attestation.

## Checklist sebelum flash spoofed ROM
- [ ] Device sudah backup (`PREFLASH-BACKUP-*`)
- [ ] Kamu tahu cara membatalkan (rollback-repair)
- [ ] Kamu tidak mengandalkan bank/Play Protect untuk keamanan sensitif
- [ ] Kamu tidak menyebarkan ke orang lain tanpa konteks

## Jangan lakukan
- Jangan mengubah `ro.build.fingerprint` sembarangan — itu membuat Play Store menolak device sebagai tidak sah.
- Jangan percaya "PATCH Play Integrity" yang beredar di forum — biasanya hanya BASIC, dan sering usang persis.
