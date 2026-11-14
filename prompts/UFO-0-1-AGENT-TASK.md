# AGENT TASK — pureport-17ultra: HyperOS 4 Port + Kernel UFO-0.1 (joyeuse / miatoll)

Kamu adalah senior Android ROM port engineer + kernel builder. **Kerjakan HANYA pekerjaan ini.** Jika ada error, PERBAIKI DULU sebelum lanjut. JANGAN lompat tugas lain. **Build kernel boleh dilakukan di sesi ini (ini sesi kerja)** — tapi tetap laporkan tiap fase ke user sebelum flash; keputusan-keputusan besar tanyakan ke user, jangan kerjakan tanpa konfirmasi. Laporkan jujur — jangan mengarang hasil.

> 🎯 **Keputusan terbaru user (14 Nov 2026):**
> UFO-0.1 = **BUILD BARU DARI AWAL (from scratch)** — BUKAN sekadar rename Synthetica-3.2.
> Material di bawah ini sudah diverifikasi; jangan kerja dari dugaan.

## Lingkungan kerja (PC ini — Linux Mint 22.3 Zena)
- CPU Haswell 4C, RAM 7,7 GB (hati-hati OOM), disk ~317 GB free
- Repo publik: https://github.com/dwp29/pureport-17ultra (dokumentasi & script — **BUKAN** tempat firmware/source privat)
  - Clone lokal: `~/ROM-Tools/pureport-17ultra` (START-HERE.md, docs/, skills/, prompts/)
- Arsip bahan: `~/ROM-Tools/pureport-17ultra-WORK-2026-11-14.tar` (16 GB — ROMs: nezha, stock, dizasports)
- Source-kit kernel (LOKAL, JANGAN di-push kemana pun):
  `/home/puresaturday/ROM-Tools/synthetica-arsip/SYNTHETICA-KERNEL-ARSIP-LENGKAP-2026-11-13/03-SOURCE-KIT-DAN-BUILD/2026-11-13_SOURCE-KIT-Synthetica-Rollercoaster-UFO-46-berkas.zip`
  - 46 berkas / ~14 MB; isinya: `build-rollercoaster.sh`, `recipes/build_synthetica31.py`, `build_synthetica32_final.py`, `package_synthetica32_final.py`, `package_release.py`, `build-rollercoaster.sh`
  - Patches (`patches/`): `kernelsu-1.0.0.patch`, `apk-sign-accept-v3.patch`, `rc_compat.c/h`, `aw8624-drop-timed_output.patch`, `port-allow-foreign-vermagic.patch`
  - Profiles (`profiles/`): `00-common.config`, `chronicle.config`, `critical.config`, `lite.config`, `port.config`, `portn.config`, `synthetica.config`
  - Prebuilts: `ksud` (5,5 MB), `manager/base.apk` (8,5 MB)
  - AnyKernel (`anykernel/anykernel.sh`) & docs (`docs/SYNTHETICA-3.0..4.0-PENGEMBANGAN.md`)
- Arsip Synthetica penuh: `~/ROM-Tools/synthetica-arsip/SYNTHETICA-KERNEL-ARSIP-LENGKAP-2026-11-13/`
  - `01-KERNEL-SEMUA-VERSI/05-SOURCE-KIT-Synthetica-3.0-Pengembangan-PRIVAT/GABUNGKAN.py` — reassemble 4 part (`.zip.001..004`, total 368 MB) → `Synthetica-3.0-Pengembangan-PRIVAT.zip` (**file part tidak ada di arsip** — TANYA user)
- Recipe yang WAJIB DIBACA sebelum build: `docs/SYNTHETICA-3.2-RELEASE-AND-DEV-GUIDE.md`,
  `docs/SYNTHETICA-3.0.md`, `docs/SYNTHETICA-4.0-PENGEMBANGAN.md` (di dalam source-kit UFO)
- Bahan ROM (di dalam arsip tar — ekstrak dulu):
  - nezha → `nezha_global-ota_full-OS4.0.0.8.XPAMIXM-user-17.0-55863f99f3.zip` (9,7 GB; SHA-256 `9e8c7795e9089787f33b8199208a0fa2defd90aceb96ddd002f1f5dd549d6cbe`)
  - stock → `miui_JOYEUSEGlobal_V14.0.3.0.SJZMIXM_df17e3fabf_12.0.zip` (2,9 GB; MD5 `df17e3fabf2284cc28efe8d10d012007`)
  - HOS-4 port (bukti boot) → `HyperOS-4_MIATOLL-STABLE-dizasports.zip` (4,5 GB; belum ada hash resmi — hitung sendiri)
  - Ekstrak: `tar -xf ~/ROM-Tools/pureport-17ultra-WORK-2026-11-14.tar -C ~/ROM-Tools "pureport-17ultra-WORK/ROMs/<nama>.zip"`
- Root tools (toolbox, `~/ROM-Tools/toolbox/`): `OrangeFox-R11.3_FBEv2-Unofficial-joyeuse.zip` (72 MB, CRC ok; unofficial joyeuse; install via `fastboot flash recovery recovery.img`), KernelSU Next Manager v3.2.0 (spoofed + normal official), `ksud` (aarch64)
- Repo private user lainnya (biar tidak salah tulis di sini): `rollercoasterhyp` (pipeline ROM "Rollercoaster Hypos 4.0.1.7" joyeuse, kernel `Rollercoaster-Roll.3.3.zip`) — BUKAN bagian tugas UFO-0.1, tapi menunjukkan pola kerja yang dipakai user. **Jangan modifikasi tanpa perintah user.**

## Kernel Synthetica-3.2 (fakta dari `SYNTHETICA-3.2-RELEASE-AND-DEV-GUIDE.md` + arsip)
- **Tree**: `Saamitk/kernel_xiaomi_sm6250-switchoff` @ `c1e6f795b557b7bf92220c91f05a42b456de7a74` (`4.14.357-openela`)
- **KSU Next**: `KernelSU-Next/KernelSU-Next` @ `d86ff76cd7f8efab5fb7ebfd6ab7ef6b3b3b9f50` (Rollercoaster `34000`) — `CONFIG_KSU=y`, `CONFIG_KSU_MANUAL_HOOK=y`, `CONFIG_MODULES=y`, `CONFIG_MODVERSIONS=y`
- **Toolchain**: Neutron Clang 18.0.0 (`06092026`, SHA-256 `531083928c8e37f6b31e324dbfd0b5a8323f989b1c57ff2c1368b889b5b1bd30`) — JANGAN clang sistem 18; JANGAN clang 11 (itu khusus tree crDroid experimental)
- **Patch inti**: `0001-mglru-4.14`, `0002-uclamp-walt-stune`, `0003-uclamp-correctness`, `0004/0005-mglru*`, `0006-neutron-enum-cast`, `0001-ksu-manager-preserve-seccomp`, `0001-manager-fd-after-exec` — wajib hadir, tanpa pengecualian
- **Config**: 3.0→3.1→3.2 `.config` berbeda HANYA `CONFIG_LOCALVERSION` (ABI dipertahankan ¡). Untuk UFO-0.1 **configurasinya baru**; `Module.symvers` TIDAK akan identik — catat ini
- **Profiles** (untuk config tree kamu): `synthetica.config` (fitur Synthetica: MGLRU, UCLAMP, WALT, ZRAM, LZ4/ZSTD, BBR, KSU, MODULE_SIG_FORCE) + `00-common.config`; gunakan salah satu sebagai starting point, gabung ke defconfig (ikuti pola recipe, JANGAN asal ubah)
- **AVB**: `tools/fix-avb --if-unsigned` untuk A17 stock dengan footer `AVBf` + `AVB0` unsigned (fix-descriptor unsigned cuma kalau `algorithm_type == 0`) — diperlukan untuk boot di Project Infinity X 4.1 & mungkin HOS-4 port
- **Manager identity Synthetica**: `net.ember.labs` (manager sendiri user) — untuk UFO-0.1 TANYA user: pakai identity yang sama, atau identity baru? (ini SEBUAH keputusan, bukan dugaan agen)

## CATATAN BUG & RISET PORT DIZA (HyperOS 4 miatoll) — WAJIB DIBACA SEBELUM BUILD
Source: post resmi Telegram @Miatoll (author @dizasports, Nov 2026):
- **HyperOS 4.0.0.6 Beta**: bug Face Unlock + Vibration; KSU Next v3.2.0 spoofed; launcher diganti modded; lock-screen personalization crash → workaround Settings > Personalization; search bar aneh → Home Search > Compact
- **HyperOS 4.0.0.32 Beta**: ported from Xiaomi 17; build "90% stable"; perlu ±1 hari settle; Play Store included; bug: Face Unlock
- **HyperOS 4.0.0.32 Beta HOTFIX**: Smart Home app dibuang; soft reboot FIXED; RIL + glass effect OK; camera "incompatible" → GCam; bug: Face Unlock
- **HyperOS 4.0.17.0 Semi-Stable** — kemungkinan besar file user (`HyperOS-4_MIATOLL-STABLE-dizasports.zip`, 4,5 GB): ported from Xiaomi 18 Pro Max; KSU Next v3.2.0 spoofed; Play Store included; parallel animations; **NO camera app — wajib GCam / Leica Camera Module**; bug: **Face Unlock**
- **HyperOS 4 | Joyeuse Beta** (@itsxiima, 19.08.2026, ported from **nezha**): bug **vibration** — referensi, bukan rilis Diza

**Bug yang tercatat (kemungkinan besar untuk file STABLE kamu):**
1. **Face Unlock** — TIDAK berfungsi. Jangan "diperbaiki"
2. **Camera app bawaan** — TIDAK ADA → GCam / Leica Camera Module
3. **Vibration** — uji motor haptics (`/sys/class/leds/`, vendor haptics HAL)
4. **Soft reboot** — fixed di HOTFIX 0.0.32+
5. **Settle period** — ±1 hari pertama
6. **Root** — KernelSU Next v3.2.0 spoofed (BUKAN Magisk)
7. **Wipe** — selalu Wipe Cache & Dalvik + Format Data

**Verifikasi wajib (Fase 0):**
A. Extract `ro.build.display.id`, `ro.product.device`, `ro.product.model`, dari `*/build.prop` di dalam zip
B. Bandingkan `ro.product.device`/`ro.build.ota...` donor nezha vs dizasports — JANGAN anggap sama
C. Catat init/service yang ada (QTI haptics, camera provider, face HAL)
D. Cek Telegram @Miatoll + @dizasportschat laporan terbaru

## URUTAN KERJA

### FASE 0 — REKON (tanpa build)
1. Verifikasi hash (`sha256sum`, `md5sum`) di dalam arsip tar — jika tidak cocok, STOP
2. `unzip -l` ketiga zip (payload.bin? boot.img? vbmeta? dtbo?)
3. Ekstrak payload stock & donor (payload-dumper-go, lpunpack): fstab, DTB, AVB, build.prop
4. **Analisis dizasports (bukti boot) MENDALAM** — ini acuan utama, BUKAN nezha
5. Laporkan temuan `FINDINGS.md`

### FASE 1 — KERNEL UFO-0.1 (build baru dari awal)
**SUMBER DATA (semua sudah di PC kamu):**
1. Clone tree: `git clone https://github.com/Saamitk/kernel_xiaomi_sm6250-switchoff` @ `c1e6f795b557b7bf92220c91f05a42b456de7a74`
2. Extract source-kit `2026-11-13_SOURCE-KIT-Synthetica-Rollercoaster-UFO-46-berkas.zip`
3. Baca README-SOURCE-KIT.txt + docs/ — ikuti pola recipe (`build_synthetica32_final.py` sebagai blueprint, BUKAN salin persis — UFO-0.1 = build kamu sendiri)
4. **Steps**:
   a. Checkout tree `c1e6f795`
   b. Clone KSU Next @ `d86ff76` (panggil `ksu.sh` / ikuti recipe — jangan improvisasi)
   c. Apply patches DARI SOURCE-KIT (manual order per recipe)
   d. **Config**: salin `profiles/synthetica.config` + `profiles/00-common.config` sebagai starting point; gabung dengan defconfig `vendor/xiaomi/miatoll_defconfig`? TANYA user dahulu (pilihan metode: `scripts/kconfig/merge_config.sh` vs `merge_defconfig.py` vs menuconfig) — JANGAN asal
   e. Set `CONFIG_LOCALVERSION="-UFO-0.1"` (wajib)
   f. Build (adaptasi path recipe; toolchain Neutron Clang 18 `06092026`; JANGAN `-j` melebihi RAM)
5. Output: `UFO-0.1-miatoll-<tanggal>.zip` (AnyKernel, dari `anykernel.sh` source-kit) + SHA-256
6. **Catatan penting**: docs/`SYNTHETICA-4.0-PENGEMBANGAN.md` sebagai referensi perkembangan; JANGAN di-merge (masih "perkembangan")
7. **CI fallback** (opsional, keputusan user): `.github/workflows/` di source-kit — bisa dipicu di Actions repo PRIVATE user (rollercoasterhyp) atau repo `Syntenthica` — TANYA user

> ⚠️ **Dynamic decisions to ASK USER FIRST (do not decide):**
> - Manager identity (`net.ember.labs` dipertahankan, atau identity UFO baru?)
> - `Synthetica-3.0-Pengembangan-PRIVAT` parts location (untuk referensi `.config` 3.2 yang persis?) — bertanya saja, JANGAN reassemble tanpa perintah
> - Dipilih: defconfig+fragment merge vs menuconfig manual
> - CI atau local-only?

### FASE 2 — PORT ROM (zip flashable OrangeFox, debloated, kompresi maks)
Base utama = port dizasports (mis. karena bukti boot ada). Strategi:
1. Repack zip flashable OrangeFox (struktur zip dikenali oFox: `META-INF/com/google/android/updater-script`, dual-boot-img/anykernel style)
2. GANTI kernel dengan **UFO-0.1** — perhatikan dtb/dtb.img compatibility; jika tidak → pertahankan dtb Diza
3. **Debloat** logis (`DEBLOAT-LIST.md`: sehat→hapus, tentukan alasan)
4. **Kompresi maksimal** (uji `unzip -t` round trip; tetap oFox-compatible)
5. Update build.prop konsisten (`ro.build.version.incremental`, `ro.kernel.version` sesuai UFO-0.1)
6. vbmeta: sediakan catatan flash `fastboot flash --disable-verity --disable-verification vbmeta vbmeta.img` (unlocked only)
7. **JANGAN flash tanpa perintah eksplisit user** — siapkan skrip terpisah `FLASH-MANUAL.txt`

### FASE 3 — DOKUMENTASI
`~/ROM-Tools/UFO-0.1-LOG/`: `SESSION-LOG.md`, `FINDINGS.md`, `DEBLOAT-LIST.md`, `BUILD-LOG-KERNEL.txt`, `BUILD-LOG-ROM.txt`, `DECISIONS.md`, `VERIFY-LOG.md`, `PORT-SUMMARY.md`

### FASE 4 — GITHUB
Commit hanya docs/log/scripts (TIDAK ADA source/firmware/biner >100 MB di repo publik). Source-kit TIDAK PERNAH di-push.

## ATURAN KERAS
0. SEBELUM FASE 1, **WAJIB BACA** `SYNTHETICA-3.2-RELEASE-AND-DEV-GUIDE.md` + `SYNTHETICA-3.0.md` (di source-kit)
1. Error → langsung pahami & perbaiki sebelum lanjut
2. Jangan ganti task; fase selesai → lapor → fase berikut
3. vbmeta/AVB hanya unlocked; JANGAN RELOCK bootloader
4. HOS ports butuh KernelSU Next spoofed, BUKAN Magisk
5. Flashing = tunggu perintah user sebagai langkah terpisah
6. Setiap fase = catat di `SESSION-LOG.md`
7. Blocked > 2 percobaan → ringkas + tanya user
8. **JANGAN push firmware/source privat ke repo publik** (repo `pureport-17ultra` tetap docs only)

## KRITERIA SELESAI
- [ ] `UFO-0.1-miatoll-<tanggal>.zip` — flashable OrangeFox, hash tercatat
- [ ] `HyperOS-4-pureport-joyeuse-<tanggal>.zip` — flashable oFox, debloated, kompresi maks
- [ ] Keduanya tercantum di VERIFY-LOG.md
- [ ] PORT-SUMMARY.md final (flash order, vbmeta cmd, known bugs)
- [ ] Semua Fase 0–4 tercatat rapi di UFO-0.1-LOG/
- [ ] Firmware/source privat tidak pernah di-push ke repo publik mana pun

Mulai dari FASE 0. Sebelum build apa pun, laporkan tabel hash & list isi payload ke user.
