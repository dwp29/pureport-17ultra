---
name: smali-apktool
description: Decompile, edit and recompile Android APKs with apktool/smali/baksmali — patches inside framework, hosts, permissions, and troubleshooting build errors
---

# APK Decompile → Edit → Recompile

## Tools (this PC)
- `apktool` 2.7 (apt) — also ships `smali`/`baksmali` 2.5.2 (apt, bundled as dep)
- `jadx` 1.5.6 at `~/ROM-Tools/jadx` (symlinked into `~/.local/bin/jadx`) — read-only Java decompile
- `dex2jar` v2.4 at `~/ROM-Tools/dex2jar` (CLI `d2j-dex2jar`, needs Java — use `/usr/bin/java`)
- `Android.mk`/`Apktool.yml` inspection: `apktool.yml` contains sdk/target levels — edit `minSdkVersion`/`targetSdkVersion` there, not in manifest XML only

## Workflow
```bash
# 1. Decompile
apktool d target.apk -o out -f
# 2. Edit smali (or resources: res/layout/*.xml, values/strings.xml)
# 3. Recompile
apktool b out -o out.apk -f
# 4. Sign (debug keystore auto for debug; release → see skill: apk-build-release)
java -jar ~/Android/Sdk/build-tools/37.0.0/lib/apksigner.jar sign -ks release.keystore out.apk
# or: apksigner sign --ks release.keystore out.apk
# 5. Install
adb install -r out.apk
```

## Common patches on porting
- **framework-res** (`/system/framework/framework-res.apk`): often needs overlay/skin tweaks only via MIO-KITCHEN, not smali
- **Hosts block**: add lines to `/system/etc/hosts` instead of patching APKs
- **Permissions**: `AndroidManifest.xml` — apktool handles
- **arm64 libs**: don't touch unless missing → copy from donor ROM build to `lib/arm64-v8a/`

## Troubleshooting `apktool b` failures
`could not find any resources on letter ...` → corrupt resources → check `res/values/public.xml` matches `res/` entries; re-decode:
`apktool d -s target.apk -o out` (skip dex disassembly) when only resources need edits
`Multiple resources on File ...` → duplicate key in `values/public.xml` → remove duplicate
`Access denied finding 9-patch image` → run as non-root (never build as root/sudo)
`invalid opcode` in smali → edit broke syntax → revert that .smali file
`UNEXPECTED TOP-LEVEL EXCEPTION: java.lang.OutOfMemoryError` → `export _JAVA_OPTIONS=-Xmx2g`

## Verify
`aapt dump badging out.apk` (keep same package name/version) + `adb install` on device
If app launches but crashes instantly → re-check `lib/` matches device ABI (armeabi-v7a vs arm64-v8a)
