---
name: apk-build-release
description: Build, sign and troubleshoot Android APKs (debug/release, Gradle) on this machine — including signing keys, ProGuard/R8 and common build errors
---

# APK Build, Sign & Release

## Environment (this PC)
- Android Studio **2026.2.2 Patch 1** at `~/Android/android-studio` (JBR 25 bundled)
- SDK: `~/Android/Sdk` — platform-tools 37.0.1, platforms android-35 & 36, build-tools 36.1.0 & 37.0.0, sources API 36; licenses accepted
- `JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64` (apt openjdk-17) — also used by Gradle CLI
- `ANDROID_HOME=~/Android/Sdk` — set in `~/.bashrc` (login shell picks up via `~/.profile` too — verified with `bash -lc`)

## Build
```bash
cd <project>
./gradlew clean
./gradlew assembleDebug          # APK: app/build/outputs/apk/debug/app-debug.apk
./gradlew assembleRelease        # unsigned unless signing configured
./gradlew bundleRelease          # AAB for Play Store
./gradlew installDebug           # build + install to connected device (adb devices)
```

## Signing (release)
1. Create keystore **once**, keep it forever:
   ```bash
   keytool -genkey -v -keystore release.keystore -alias upload -keyalg RSA -keysize 2048 -validity 10000
   ```
2. `app/build.gradle`:
   ```gradle
   android {
     signingConfigs { release { storeFile file('../release.keystore'); storePassword ...; keyAlias 'upload'; keyPassword ... } }
     buildTypes { release { signingConfig signingConfigs.release } }
   }
   ```
3. Or per-build CLI sign: `apksigner sign --ks release.keystore app-release-unsigned.apk` (build-tools 37)

## Debug keystore auto
Android Studio creates `~/.android/debug.keystore` automatically; used for `assembleDebug` (SHA1 via `keytool -list -v -keystore ~/.android/debug.keystore -alias androiddebugkey -storepass android`)

## Verification
- `apksigner verify --print-certs app.apk`
- `aapt dump badging app.apk | head -20` (apt package `aapt`)

## Common build failures
- `Unsupported class file major version 65` → Gradle/AGP vs JDK mismatch → use JDK 17 with AGP 8.x, or bump `org.gradle.java.home` to JBR 25 (`~/Android/android-studio/jbr`)
- `Android SDK not found` → export `ANDROID_HOME` or local.properties `sdk.dir=~/Android/Sdk`
- `Duplicate class kotlin/...` → force resolution: `configurations.all { resolutionStrategy.force 'org.jetbrains.kotlin:kotlin-stdlib:2.0.21' }`
- `Execution failed … DexArchiveMerger` → bump `androidx.multidex` or `minSdk 21+`
- Memory: `gradle.properties` → `org.gradle.jvmargs=-Xmx2g` (this PC has 7.7GB RAM; keep 2G)

## Decompile/recompile
- `apktool d target.apk -o out/` → edit → `apktool b out -o out.apk` (apt apktool 2.7)
- `jadx -d out/ target.apk` — read-only decompile to Java (GUI: `jadx-gui`)
- `dex2jar d2j-dex2jar classes.dex` → `jar` → `cfr`/`procyon`
