# START HERE — pureport-17ultra (sesi chat baru)

Kamu sekarang berada di project **HyperOS port untuk Redmi Note 9 Pro (joyeuse)**, donor: Xiaomi 17 Ultra (nezha).

## 1. Baca dulu (urutan)
1. `README.md` — overview, disclaimer, status
2. `docs/PORTING-NOTES.md` — analisis port nezha → joyeuse (kenapa tidak bisa langsung "zip → flash")
3. `docs/DEV-TOOLKIT.md` — environment PC pengembang (tools, paths, model OpenCode)
4. `docs/HASHES.txt` — hash semua file firmware terverifikasi

## 2. Verifikasi integritas file
```bash
md5sum  miui_JOYEUSEGlobal_V14.0.3.0.SJZMIXM_df17e3fabf_12.0.zip  # df17e3fabf2284cc28efe8d10d012007
sha256sum nezha_global-ota_full-OS4.0.0.8.XPAMIXM-user-17.0-55863f99f3.zip  # 9e8c7795e9089787f33b8199208a0fa2defd90aceb96ddd002f1f5dd549d6cbe
```
Kalau tidak cocok → jangan lanjut flash, download ulang.

## 3. Toolchain & kernel build
```bash
bash scripts/bootstrap.sh          # clone kernel crDroid 16.0 + clang 11 pinned + gcc 4.9 + AnyKernel3 + build.sh
```
Build lokal adalah jalur utama (PC Haswell 4C/7.7 GB RAM). CI opsional di `.github/workflows/build-kernel.yml`.

## 4. Port ROM — jalur realistis (pelajari sebelum flash!)
1. **Xiaomi.EU HyperOS** (MiatollCave/Xiaomi.EU-Miatoll) — stabil, direkomendasikan sebagai base
2. **HOS-4 @dizasports** (`HyperOS-4_MIATOLL-STABLE-dizasports.zip`) — community port, bugs: no camera (pakai GCam), Face Unlock rusak
3. Flash langgas OrangeFox R11.3 FbeV2: wipe cache/dalvik → flash zip → format data → reboot
4. **Jangan relock bootloader**; vbmeta dengan `--disable-verity --disable-verification` (unlocked); HOS ports pakai **KernelSU Next spoofed**, bukan Magisk

## 5. Aturan main
- ⚠️ JANGAN upload file firmware/ROM ke cloud publik/repo (hak cipta + ukuran)
- ⚠️ Semua eksperimen di device: backup penuh dulu (persist/nvram/modem/devinfo)
- ⚠️ vbmeta & AVB hanya di-flash di kondisi unlocked & dengan tanggung sendiri
- Repo ini = dokumentasi & tooling; **bukan** sumber ROM

## 6. GitHub
- Repo: https://github.com/dwp29/pureport-17ultra (publik)
- GitHub MCP di OpenCode sudah aktif (bisa baca/tulis repo dari sesi)
- `gh auth` global di PC; sesi baru langsung bisa `git push/pull`
