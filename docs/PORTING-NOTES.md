# Porting Notes — nezha (Xiaomi 17 Ultra, HyperOS 4) → joyeuse (Redmi Note 9 Pro)

## Konteks
- Donor: `nezha_global-ota_full-OS4.0.0.8.XPAMIXM-user-17.0-55863f99f3.zip` (~9,72 GB, Android 17, HyperOS 4, CDN resmi Xiaomi).
- Target: joyeuse / miatoll (SM7125, kernel 4.14, Treble; stock Global firmware Android 12 V14.0.3.0.SJZMIXM).

## Fase riset yang aman (dilakukan lokal, tidak di repo)
1. **Integritas file** — cocokkan SHA-256 dengan CDN (`content-length` 9718410997 bytes).
2. **Listing isi OTA** — `unzip -l` → cari `payload.bin`, `boot.img`, `vbmeta.img`, `super.img`.
3. **Extract payload** — `payload-dumper-go payload.bin` → partisi per-image (system, vendor, product, system_ext).
4. **Inspeksi** — `lpunpack super.img`, erofs/ext4 mount read-only; `binwalk` boot.img; cek fstab & DTB.
5. **Catat offset**: ukuran system/vendor, project name di `build.prop`, library SM7125 vs SM8850 mismatch (donor & target beda SoC generasi).

## Kenapa nezha → joyeuse TIDAK bisa langsung boot (ringkas)
- Beda generasi SoC (donor: Snapdragon 8 Elite Gen? vs target: SM7125 SD 720G) — **device tree & kernel beda total**.
- `fstab`, DTB, device-info, HALs (camera, sensors, charger PM6150, audio ACDB) donor tidak compatible.
- Xiaomi menjaga dynamic analysis sulit: erofs + verity + vbmeta; perlu `fastboot flash --disable-verity --disable-verification` (unlocked).
- Kesimpulan: donor dipakai sebagai **reference asset** (props, frameworks blob checklist, on-device paths) — bukan sebagai base flash langsung.

## Jalur yang realistis (urutan)
1. **Stable daily** — Xiaomi.EU HyperOS (MiatollCave/Xiaomi.EU-Miatoll, unlicense) — flash di OrangeFox R11.3 FbeV2: wipe cache/dalvik → flash zip → format data → reboot.
2. **HOS 4 port** (@dizasports `HyperOS-4_MIATOLL-STABLE-dizasports.zip`) — flash via OrangeFox; dikenal bugs: no camera app (pakai GCam), Face Unlock broken.
3. **Kernel custom** — Stormbreaker build lokal (`skills/opencode/joyeuse-kernel`): `./build.sh` @ branch 16.0 → AnyKernel zip → flash TWRP.
4. **Nezha donor** — hanya untuk ekstraksi & pembelajaran (device tree diff, props, verify vbmeta signing flow) — bukan untuk flash full.

## vbmeta / AVB
- Custom kernel → `fastboot flash vbmeta --disable-verity --disable-verification vbmeta.img` (unlocked).
- **Jangan relocked bootloader** setelah flash custom/port — brick permanen.
- HOS ports: **KernelSU Next spoofed** (bukan Magisk) untuk Play Integrity; Magisk langsung bisa dideteksi.

## Recovery options untuk joyeuse
- OrangeFox R11.3 FbeV2 (HyperOS ports recommended)
- TWRP (community miatoll builds; Positron-B / clarencelol)
- Stock fastboot mode: `fastboot flash recovery recovery.img`

## Backup checklist (sebelum eksperimen apa pun)
1. `adb shell` koneksi OK → `adb pull` file penting ke PC
2. Backup IMEI/persist/proinfo (EDL/TWRP backup: persist, nvram, modem, devinfo)
3. Backup stock boot + vbmeta + dtbo ke PC
4. Catat fingerprint stock: `ro.build.fingerprint`
5. Pastikan battery > 50% dan kabel data baik
