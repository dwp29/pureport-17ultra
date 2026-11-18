---
name: apk-signing-verify
description: Audit chain signing APK sebelum flash / distribute. Aman, read-only.
---

# APK Signing Verify

## Kapan pakai
Sebelum meng-install/meng-flash APK (terutama ROM build yang kamu tanda tangani sendiri).

## Alat
apksigner (`~/Android/Sdk/build-tools/*/apksigner.jar` atau binary), aapt, keytool, openssl.

## Protokol verifikasi (urutan)

### 1. Inspeksi signature APK
```bash
APK=path/ke/app.apk
BT=$(ls -d ~/Android/Sdk/build-tools/*/ | head -1)
java -jar "$BT"apksigner.jar verify --verbose --print-certs "$APK"
```
Cari:
- `Verified using v1 scheme: true/false`
- `Verified using v2 scheme: true/false`
- `Verified using v3 scheme: true/false`
- **Number of signers: 1** (selain itu, waspada)
- **Signer certificate SHA-256 digest** — cocokkan dengan **kernel-pin** yang diharapkan (mis. `fe833710…` untuk Synthetica Manager 6.0.0, `5CC7E1A7…` untuk 6.1 Themes). Kalau tidak cocok → **root tidak berfungsi** di device tersebut.
- `key algorithm: RSA` + `key size: 4096` (kuat)

### 2. Inspeksi package & min/max SDK
```bash
aapt dump badging "$APK" | grep -E "package|sdkVersion|targetSdkVersion|compileSdkVersion"
```
Pastikan `targetSdkVersion` cocok dengan ROM target (mis. A12 untuk joyeuse stock, A16 untuk UFO-0.1 port).

### 3. Verifikasi kesesuaian dengan kernel pin (kalau relevant)
```bash
# Bandingkan digest (tanpa whitespace)
java -jar "$BT"apksigner.jar verify --print-certs "$APK" | grep -oE '[0-9a-f]{64}'
# Cocokkan dengan expected (contoh Synthetica 6.0.0):
# fe833710a733f63061691c87ff222e84ca2fa462582aceaf5f577fe799ab4140
```
Beda = **jangan flash** ke device yang mengharapkan pin tersebut.

### 4. Cek eksposur rahasia (pre-flight)
- APK tidak boleh berisi keystores / passwords / private keys: `unzip -l "$APK" | grep -iE 'keystore|\.jks|\.p12|keysecret|private'`
- `resources.arsc` tidak boleh berisi kredensial mentah.

## Laporan
```
APK: <path>
Package: <name> · versionCode <n> · targetSdk <n>
Signer DN: <CN>
Signer SHA-256: <digest>
Signer count: <n>
Scheme: v1=<b> v2=<b> v3=<b>
Kernel pin match (jika diharapkan): YES/NO
Verdict: LAYAK FLASH / TIDAK LAYAK
```
