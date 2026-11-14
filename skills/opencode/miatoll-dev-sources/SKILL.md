---
name: miatoll-dev-sources
description: Complete verified index of ALL miatoll / SM6250 / SM7125 repositories — LineageOS, crDroid, Pixel, Elixir, ArrowOS, SailfishOS, eOS, PostmarketOS, mainline, ports/miui/hyperos, recoveries, vendor blobs, firmware — for Redmi Note 9 Pro joyeuse
---

# Miatoll Family — COMPREHENSIVE Source Index (Nov 2026)

Devices: **joyeuse** (Note 9 Pro Global), curtana (Note 9S), excalibur (Note 9 Pro Max), gram (Poco M2 Pro), lancelot (Note 10 Lite). SoC: SM7125 (Snapdragon 720G, "Atoll" platform), kernel 4.14, Treble, A/B.

## A. LineageOS (official, actively maintained)
- `LineageOS/android_device_xiaomi_miatoll` — branches 18.1…23.2 (Android 11…16; 22.2 = Android 15)
- `LineageOS/android_device_xiaomi_sm6250-common` — shared SM7125/SM6125/SM6250
- `LineageOS/android_kernel_xiaomi_sm6250` — branches 18.1…22.2
- `LineageOS-miatoll/kernel_xiaomi_sm6250` — org mirror, lineage-22.2 (`build.py`, `regen-defconfig.py`)
- Wiki variant3: https://lineageos.github.io/lineage_wiki/devices/miatoll/variant3/ (joyeuse Global; maintainers: dereference23, ItsVixano)
- Build deps: `device/xiaomi/sm6250-common`

## B. crDroid (16.0 = Android 16; maintained by swiitchOFF)
- `crdroidandroid/android_device_xiaomi_miatoll` — default branch 16.0
- `crdroidandroid/android_device_xiaomi_sm6250-common` — shared
- `crdroidandroid/android_kernel_xiaomi_sm6250` — branch 16.0 (cloned to `~/ROM-Tools/kernel_joyeuse`)
- OTA manifest: `crdroidandroid/android_vendor_crDroidOTA/miatoll.json` → https://sourceforge.net/projects/crdroid/files/miatoll/12.x/
- XDA: https://xdaforums.com/t/rom-oss-15-0-16-0-official-crdroid-v11-x-v12-x-for-curtana-excalibur-gram-joyuese-miatoll.4782339/

## C. xiaomi-sm6250-devs org (original maintainer org, LineageOS-derived)
- `xiaomi-sm6250-devs/android_device_xiaomi_miatoll` — unified
- `xiaomi-sm6250-devs/android_device_xiaomi_sm6250-common`
- `xiaomi-sm6250-devs/android_kernel_xiaomi_sm6250` — lineage-22.2
- `xiaomi-sm6250-devs/android_vendor_xiaomi_miatoll` + `android_vendor_xiaomi_sm6250-common`
- `xiaomi-sm6250-devs/android_hardware_lineage_compat` + `android_hardware_libhardware` + `android_hardware_interfaces`

## D. ArrowOS / Xtended / P404 / Nusantara / Kry9toN / SonalSingh
- `ArrowOS-Devices/android_device_xiaomi_miatoll` + `ArrowOS-Devices/android_vendor_xiaomi_miatoll` — ArrowOS
- `Xtended-Devices/device_xiaomi_miatoll` — XTended (Pixel experience-ish)
- `P404-Devices/device_xiaomi_sm6250-common` — shared
- `NusantaraROM-Devices/device_xiaomi_sm6250-common` — shared
- `Kry9toN/device_xiaomi_miatoll` — community build
- `SonalSingh18/android_device_xiaomi_miatoll` + `SonalSingh18/android_vendor_xiaomi_miatoll`

## E. Xiaomi-SD720G-Devices / Klozz / Saamitk / Velvet / Nitro / Forza / Sailfish
- `Xiaomi-SD720G-Devices/android_device_xiaomi_miatoll` — `thirteen` (stable)
- `Xiaomi-SD720G-Devices/android_device_xiaomi_sm6250-common` — `thirteen`
- `Xiaomi-SD720G-Devices/android_kernel_xiaomi_sm6250` — `thirteen` (build.sh → "RedCherry", cust_defconfig)
- `Klozz/android_kernel_xiaomi_sm7125` — `Yuki-inline-rebase`, inline encryption, CAF rebase LA.UM.9.1
- `Saamitk/kernel_xiaomi_SM6250_SKYNET` — SkyNet kernel
- `Saamitk/kernel_xiaomi_sm6250-switchoff` @ `c1e6f795` — **BASE Synthetica-3.2 & UFO-0.1** (4.14.357-openela, Neutron Clang 18, KSU Next d86ff76 manual hook, Module.symvers 12.236 simbol)
- `Abhishek001konni/kernel_xiaomi_sm6250` — Forza kernel (`4.14-inline`)
- `AntonIXO/SailfishOS-Miatoll-Kernel` — SailfishOS kernel (`sailfish`)
- `ProjectVelvet/kernel_xiaomi_sm6250` — Velvet Kernel v4.14.349-OpenELA
- `Miatoll-Lab/kernel_xiaomi_miatoll` — `twelve`
- `LeddaZ/android_kernel_xiaomi_sm7125` — Nitro kernel
- `negrroo/LawRun_xiaomi_sm6250` — LawRun kernel

## F. PixelExperience / PixelOS / Elixir
- `PixelExperience-Devices/kernel_xiaomi_sm6250` + `PixelExperience-Devices/kernel_xiaomi_miatoll`
- `PixelOS-Devices-old/device_xiaomi_miatoll` — branch fourteen (archived)
- `PixelOS-Devices-old/kernel_xiaomi_miatoll`
- `ProjectElixir-Devices/vendor_xiaomi_miatoll` — vendor blobs (LP-maintained)
- `ProjectElixir-Devices/kernel_xiaomi_sm6250`

## G. AOSPA / CAF
- `AOSPA/android_kernel_xiaomi_miatoll` — CAF 4.14
- `reaPeR1010/android_kernel_xiaomi_miatoll` — `kernel.lnx.4.14.r15-rel` (stock CAF r15)
- `pa-xe/android_kernel_xiaomi_miatoll` — AOSP + KSU
- `Foxy2nd/kernel_xiaomi_miatoll`

## H. /e/OS & PostmarketOS & mainline & Sailfish
- **/e/OS** build: https://doc.e.foundation/devices/miatoll/build (variant3, Android 14/15)
- `sm7125-mainline/linux` — mainline kernel source (`LineageOS-6.16`)
- `sm7125-mainline/u-boot`, `sm7125-mainline/pmaports`, `sm7125-mainline/nightly-builds`, `sm7125-mainline/firmware-xiaomi-miatoll`, `sm7125-mainline/alsa-ucm-conf`
- `android-sm7125/android_device_xiaomi_mi7125-mainline` — lineage-22.2; kernel `kernel/xiaomi/mi7125-mainline`
- `asidko/qcom-camss-mainline` — camera fix (mainline)
- `asidko/pm6150-charger-mainline` — PM6150 charge fix
- `99degree/postmarketos-nightly-builds` — PostmarketOS nightly images for miatoll
- `99degree/linux` — WIP miatoll kernel

## I. Recovery (flash targets)
- `OrangeFoxRecovery/device_xiaomi_miatoll` — **official** OrangeFox, branch fox_11.0
- `AyusmanNanda/orangefox_device_xiaomi_miatoll` — community build
- `clarencelol/twrp_device_xiaomi_miatoll` — community TWRP
- `Positron-B/twrp_device_xiaomi_miatoll` — older TWRP
- TWRP prebuilts: `skkk/twrp_device_xiaomi_miatoll` (verify build availability)

## J. Performance / custom kernels
- `psndna88/AGNi_pureMIUI` — 110★
- `kardebayan/android_kernel_xiaomi_sm6250` — Stormbreaker
- `jandaX/kernel_xiaomi_joyeuse`
- `sudonite/android_kernel_xiaomi_miatoll`
- `heySaish/Void-Kernel`, `heySaish/VoidSU`

## K. Ports / Xiaomi.EU / HyperOS (DEFAULT: Xiaomi.EU HyperOS)
- **`MiatollCave/Xiaomi.EU-Miatoll`** (Unlicense) — **DEFAULT** — stable Xiaomi.EU HyperOS miatoll port, branch `main`
- `iput-object/CaveOfMiatoll` — organized port repo; branches: `hyperos-15` (stable), `hyperos-15-cn`, `main`
- `HyperOS-4_MIATOLL-STABLE-dizasports.zip` (`~/Downloads/HyperOS-4_MIATOLL-STABLE-dizasports.zip`) — our downloaded ROM port (Porter @dizasports); bugs: no camera, Face Unlock; Play Store included; base Xiaomi 18 Pro Max
- Recommended recovery (HyperOS ports): **OrangeFox R11.3 FbeV2**
- Install: OrangeFox → Wipe Cache & Dalvik → Flash ROM zip → Format Data → Reboot
- Telegram: `@Miatoll` (updates), `@MiatollOfficial` / `@MiatollClouds` (chat), `@miatollcave` (updates), `@miatollcavesupport` (help)
- XDA thread: https://xdaforums.com/t/rom-oss-15-0-16-0-official-crdroid-v11-x-v12-x-for-curtana-excalibur-gram-joyuese-miatoll.4782339/
- 4PDA: viewtopic=36
- `HunterXProgrammer/Termux-Docker-Kernel-Redmi-Xiaomi` — Termux/Docker kernel
- `petros402/AnyKernel3` — NetHunter-flashable kernel for LOS 22.2
- `caturpamunqkas/kernel-miatoll-nethunter` — NetHunter

## L. Vendor / firmware (blob extraction)
- Stock firmware: `xiaomifirmwareupdater.com` (filter: joyeuse/curtana/excalibur/gram), `miui.com`, `miuirom.com`
- Vendor stubs: `xiaomi-sm6250-devs/android_vendor_xiaomi_miatoll`, `xiaomi-sm6250-devs/android_vendor_xiaomi_sm6250-common`
- `AndroidOne-Experience/vendor_xiaomi_miatoll`, `MistOS-Devices/vendor_xiaomi_miatoll`,
  `SonalSingh18/android_vendor_xiaomi_miatoll`, `ArrowOS-Devices/android_vendor_xiaomi_miatoll`
- Extraction: `mka vendor` (LineageOS extract-utils) in a synced tree

## M. Local paths on this PC
- Kernel source: `~/ROM-Tools/kernel_joyeuse` (branch 16.0, `vendor/xiaomi/miatoll_defconfig`)
- Kernel build script: `~/ROM-Tools/kernel_joyeuse/build.sh` (Clang 11.0.1 r6443078 + gcc 4.9 prebuilts, Stormbreaker)
- Built kernel: `~/ROM-Tools/kernel_joyeuse/out/arch/arm64/boot/Image.gz`
- Stormbreaker flashable: `~/ROM-Tools/kernel_joyeuse/AnyKernel/Stormbreaker-miatoll-20261112-22.zip`

## N. Build setup (reference — LineageOS)
```shell
mkdir -p ~/bin && curl -o ~/bin/repo https://storage.googleapis.com/git-repo-downloads/repo && chmod +x ~/bin/repo
repo init -u https://github.com/LineageOS/android.git -b lineage-22.2 --depth=1
repo sync -j$(nproc --all)
mka vendor                                # extract blobs from stock ROM
# lunch lineage_miatoll-userdebug && mka -j$(nproc --all) bacon
```

## Known pitfalls
- Never relock bootloader on custom ROM (breaks vbmeta/AVB)
- Camera in ports often missing → GCam / Leica module
- HOS ports need KernelSU Next spoofed (not Magisk) for Play Integrity
- `vbmeta --disable-verity --disable-verification` for custom kernel
- `lpunpack`/`lpmake`/`lpdump` for dynamic partitions
- `fastboot flash vbmeta --disable-verity ...` only when unlocked
