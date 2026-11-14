# AGENT TASK — pureport-17ultra: HyperOS 4 Port + Kernel UFO-0.1 (joyeuse / miatoll)

Kamu adalah senior Android ROM port engineer + kernel builder. **Kerjakan HANYA pekerjaan ini.** Jika ada error, PERBAIKI DULU sebelum lanjut. JANGAN lompat tugas lain. Laporkan jujur — jangan mengarang hasil.

## Lingkungan kerja (PC ini — Linux Mint 22.3 Zena)
- CPU Haswell 4C, RAM 7,7 GB (hati-hati OOM; gunakan `make -j$(( $(nproc)/2 + 1 ))` jika perlu), disk ~300 GB free
- Repo publik: https://github.com/dwp29/pureport-17ultra (dokumentasi & script; TIDAK berisi firmware)
  - Clone lokal: `~/ROM-Tools/pureport-17ultra` (START-HERE.md, docs/DEV-TOOLKIT.md, docs/PORTING-NOTES.md, docs/HASHES.txt)
- Arsip bahan: `~/ROM-Tools/pureport-17ultra-WORK-2026-11-14.tar` (16 GB; berisi repo + 3 ROM)
- Tool utama terpasang: fastboot 37, platform-tools adb, MIO-KITCHEN (unpack/repack payload/super/erofs/ext4),
  payload-dumper-go, lpunpack/lpdump/lpmake, jadx, apktool, brotli/zstd/lz4/xz, simg2img, erofs-utils, binwalk,
  Ollama, OpenCode, git, aarch64-linux-gnu-gcc
- **Toolchain tergantung tree sumber**:
  - crDroid 16.0 tree → `build.sh` mengunduh clang 11 pinned (r6443078) + gcc 4.9 — clang ≥12 GAGAL di tree ini.
  - Tree buatan user (Synthetica/Rollercoaster-UFO) → **clang 18 / Neutron Clang** (sudah terbukti di arsip; `.kernel work`).
  - `bash ~/ROM-Tools/pureport-17ultra/scripts/bootstrap.sh` hanya untuk jalur crDroid
- Kernel build Stormbreaker pernah sukses (out/arch/arm64/boot/Image.gz + AnyKernel zip) di `~/ROM-Tools/kernel_joyeuse`

## Bahan (integritas WAJIB dicek dulu)
| File | Ukuran | Verifikasi |
|---|---|---|
| nezha_global-ota_full-OS4.0.0.8.XPAMIXM-user-17.0-55863f99f3.zip (donor, HyperOS 4 / Android 17, Xiaomi 17 Ultra) | 9,7 GB | SHA-256 `9e8c7795e9089787f33b8199208a0fa2defd90aceb96ddd002f1f5dd549d6cbe` |
| miui_JOYEUSEGlobal_V14.0.3.0.SJZMIXM_df17e3fabf_12.0.zip (stock, Android 12 Recovery) | 2,9 GB | MD5 `df17e3fabf2284cc28efe8d10d012007` |
| HyperOS-4_MIATOLL-STABLE-dizasports.zip (port komunitas @dizasports — BUKTI boot di joyeuse) | 4,5 GB | belum ada hash resmi; hitung sendiri: `sha256sum` |
- Lokasi file: `~/ROM-Tools/pureport-17ultra-WORK-2026-11-14.tar` → ekstrak dulu: `tar -xf ~/ROM-Tools/pureport-17ultra-WORK-2026-11-14.tar -C /home/puresaturday/ROM-Tools "pureport-17ultra-WORK/ROMs/<nama>.zip"` (~/Downloads dibersihkan 14 Nov 2026)
- Arsip synthetic kernel: `~/ROM-Tools/synthetica-arsip/SYNTHETICA-KERNEL-ARSIP-LENGKAP-2026-11-13-20261113T155641Z-1-001.zip`

## CATATAN BUG & RISET PORT DIZA (HyperOS 4 miatoll) — WAJIB DIBACA SEBELUM BUILD

Source: post resmi Telegram **@Miatoll** (update channel), port author **@dizasports** (dibaca Nov 2026):

- **HyperOS 4.0.0.6 Beta** — bug: **Face Unlock** + **Vibration**; notes: KernelSU Next v3.2.0 spoofed; launcher diganti modded (stock buggy); lock-screen personalization crash → workaround: Settings > Personalization; search bar aneh → Home Screen Settings > More > Home Search > Compact; "device is 6 years old".
- **HyperOS 4.0.0.32 Beta** — ported from Xiaomi 17; build "90% stable"; perlu ±1 hari settle; Play Store included; bug: **Face Unlock**.
- **HyperOS 4.0.0.32 Beta HOTFIX** — Smart Home app dibuang; soft reboot **FIXED**; RIL + glass effect OK; camera "incompatible" → pakai GCam; bug: **Face Unlock**.
- **HyperOS 4.0.17.0 Semi-Stable** — paling cocok dengan file user (`HyperOS-4_MIATOLL-STABLE-dizasports.zip`, 4,5 GB, "ported from Xiaomi 18 Pro Max"): KSU Next v3.2.0 spoofed; **Play Store included**; parallel animations a la flagship; **NO camera app — wajib GCam atau Leica Camera Module**; bug: **Face Unlock** ("Other than that? Share with us" = tidak ada laporan bug lain). Credits: Nezuko (vendor+kernel), Ram1n, Xiima (patches), Venusidk (vulkan), OBITO XD (overlays).
- **PitchBlack Recovery Project** (@dizasports, untuk MIUI/HyperOS ports): bring-up FBEv2; touch di layar aftermarket butuh charger saat recovery.
- **HyperOS 4 | Joyeuse Beta** (@itsxiima, 19.08.2026, ported from **nezha**): bug: **vibration** — bukan rilis Diza; hanya referensi terkait donor nezha.

**Bug yang tercatat untuk base file STABLE (kemungkinan besar ±4.0.17.0):**
1. **Face Unlock** — tidak berfungsi. JANGAN "diperbaiki" (face HAL vendor tidak portable lintas SoC tanpa source asli).
2. **Camera app bawaan** — tidak ada. Workaround resmi: **GCam / Leica Camera Module** (agen Fase 0 pilih yang cocok SM7125).
3. **Vibration** — bug di Beta 0.0.6 (vendor haptics HAL); belum terkonfirmasi di STABLE → **uji motor haptics di first boot**.
4. **Soft reboot** — fixed di HOTFIX 0.0.32+; tetap uji stabilitas stress.
5. **Settle period** — ±1 hari pertama pemakaian sebelum performa normal (bukan bug).
6. **Root** — **KernelSU Next v3.2.0 spoofed**, BUKAN Magisk (Play Integrity).
7. **Vulkan** — patch Venusidk khusus port (jangan dihapus).
8. **Vendor+kernel** — port memakai kombinasi "Nezuko" (bukan Stormbreaker/crDroid repo) — analisis ini di Fase 0.
9. **Launcher** — beberapa build mengganti launcher stock (buggy) dengan modded; versi STABLE diduga stock + parallel animations.
10. **Wipe** — selalu Wipe Cache & Dalvik + Format Data saat flash.

**Verifikasi wajib di zip kamu (Fase 0):**
A. Extract `ro.build.display.id`, `ro.product.device`, `ro.product.model`, `ro.vendor...` dari `*/build.prop` dalam zip.
B. Bandingkan `ro.build.ota...` donor nezha vs dizasports (duga: donor = OS4.0.0.8 XPAMIXM nezha murni; STABLE kamu mungkin base 18 Pro Max — **JANGAN dianggap sama**).
C. Catat init/service list (QTI haptics, camera provider, face HAL) — penyebab bug 1 & 3.
D. Cek Telegram @Miatoll + @dizasportschat untuk laporan bug TERBARU sebelum flash (channel aktif tiap minggu).
E. Semua temuan → `FINDINGS.md` (folder `~/ROM-Tools/UFO-0.1-LOG/`).

## Urutan kerja — TAK BOLEH DILOMPAT

### FASE 0 — REKON (tanpa build apa pun)
1. Verifikasi hash ketiga ROM (`sha256sum`/`md5sum`); jika tidak cocok → STOP, jangan lanjut
2. `unzip -l` ketiga zip: daftar payload.bin/boot.img/dtbo/dtb/super.img/...
3. Ekstrak payload stock & donor (payload-dumper-go + lpunpack): fstab, DTB, build.prop, vbmeta flags, AVB
4. **Pelajari dizasports (bukti boot) MENDALAM**: susun laporan arsitektur (partition layout, avr-verity dtb, sepolicy, init.rc, vendor blob list, kernel version string, DTB, camera absence) — ini acuan utama, BUKAN nezha (SM8850 vs SM7125 = beda generasi total)
5. Output: `FINDINGS.md` (dalam folder log — lihat Fase 3)

### FASE 1 — KERNEL "UFO-0.1"
**BASE (fakta terverifikasi dari `SYNTHETICA-3.2-RELEASE-AND-DEV-GUIDE.md` di arsip user):**
- Kernel tree: **`Saamitk/kernel_xiaomi_sm6250-switchoff` @ `c1e6f795b557b7bf92220c91f05a42b456de7a74`** (4.14.357-openela) — tree yang SAMA dengan sumber Synthetica-3.2
- KernelSU-Next: `KernelSU-Next/KernelSU-Next` @ `d86ff76cd7f8efab5fb7ebfd6ab7ef6b3b3b9f50` (Rollercoaster 34000, `CONFIG_KSU_MANUAL_HOOK=y`, `CONFIG_KSU=y`)
- Toolchain: **Neutron Clang 18.0.0** (`06092026`, SHA-256 `531083928c8e37f6b31e324dbfd0b5a8323f989b1c57ff2c1368b889b5b1bd30`)
- Manager identity: `net.ember.labs` (manager sendiri user)
- 8 patch inti (MGLRU, UCLAMP+WALT, ksu seccomp preserve, ksu exec-fd, dll.) — JANGAN hilangkan/diubah tanpa alasan
- `Module.symvers` 12.236 simbol, identik 3.0=3.1=3.2; untuk UFO-0.1 ubah HANYA `CONFIG_LOCALVERSION="-UFO-0.1"` → JANGAN ubah ABI
- AVB: port `tools/fix-avb --if-unsigned` untuk A17 stock (unsigned AVBf/AVB0)
- Build recipe user: `build-kit/scripts/build_synthetica32_final.py` (ada di source-kit privat) — pelajari & sesuaikan menjadi "UFO-0.1"; CI workflow `.github/workflows/synthetica32-final.yml`
- Source-kit di arsip: `01-KERNEL-SEMUA-VERSI/05-SOURCE-KIT-Synthetica-3.0-Pengembangan-PRIVAT` (split parts; `GABUNGKAN.py` untuk reassemble — butuh 4 file `.zip.001..004`; TANYA user apakah parts tersedia untuk di-assemble)
1. TANYA user (keputusan user, bukan agen):
   a. Apakah source Synthetica-3.2 (dari `GABUNGKAN.py` + parts, atau clone `Saamitk/kernel_xiaomi_sm6250-switchoff` @ c1e6f795) siap/terinstall di PC ini?
   b. ABI: pertahankan `Module.symvers` identik (direkomendasikan) → hanya `CONFIG_LOCALVERSION="-UFO-0.1"`
2. Jika source tersedia → build dari itu; NAMAi kernel `UFO-0.1` (ubah `CONFIG_LOCALVERSION`)
3. Jika source ABSENT → fallback keterangan: clone `aarch64- Saamitk/kernel_xiaomi_sm6250-switchoff` + apply 8 patch MGLRU/UCLAMP/KSU + KSU @ d86ff76 (kerjaan besar; minta konfirmasi user, JANGAN rework from scratch tanpa izin)
4. Output: flashable AnyKernel zip `UFO-0.1-miatoll-<tanggal>.zip`; hash SHA-256 dicatat
5. Catat di BUILD-LOG-KERNEL.txt: tree commit, KSU commit, toolchain, patch list, `.config` diff vs 3.2, Module.symvers identik?
2. Set nama kernel: `CONFIG_LOCALVERSION` / EXTRAVERSION / `--kernel-version` → **UFO-0.1**; verifikasi `uname -r` konsep (contoh string `4.14.357-openela-UFO-0.1`)
3. Build via `~/ROM-Tools/kernel_joyeuse/build.sh` (clang 11 pinned, prebuilts sudah terunduh)
4. Output: flashable AnyKernel zip `UFO-0.1-miatoll-<tanggal>.zip` (di `AnyKernel/`)
5. Catat: perintah build, compiler exact, warning/error, ukuran Image.gz, dtb/dtbo status

### FASE 2 — PORT ROM (zip flashable OrangeFox, debloated, kompresi maks)
Tujuan: HyperOS 4 yang berjalan di joyeuse. **Strategi realistis** (bukti boot = dizasports):
1. Buat ulang/modifikasi dizasports sebagai base (BUKAN port-from-scratch nezha — dokumentasikan alasannya):
   - Repack zip flashable OrangeFox (struktur zip yang dikenali oFox; periksa format installer/updater ter-verified)
   - Ganti kernel lama dengan **UFO-0.1** (dtb/dtb.img harus compatible; jika tidak compatible → pertahankan dtb dizasports & dokumentasikan)
   - **Debloat** logis: hapus system-preloads/health/fitness/game/assistant/bloatware — tulis `DEBLOAT-LIST.md` (app, alasan)
   - **Kompresi maksimal**: repack dengan kompresi PAKET terbaik yang masih dipahami OrangeFox (test: `unzip` round-trip + ukuran); PRIME SIZE yang aman
   - Update build.prop: ro.build.version.incremental dll. Dijaga konsisten; set `ro.kernel.version` sesuai UFO-0.1 jika valid
   - vbmeta: sertakan catatan flash (`fastboot flash --disable-verity --disable-verification vbmeta vbmeta.img`, unlocked only)
2. **JANGAN flash ke device tanpa perintah eksplisit user**; siapkan skrip terpisah `FLASH-MANUAL.txt`

### FASE 3 — DOKUMENTASI (repo kerja)
Semua output kerja dirapikan di `~/ROM-Tools/UFO-0.1-LOG/`:
```
UFO-0.1-LOG/
  SESSION-LOG.md      # append kronologis: waktu, aksi, hasil
  FINDINGS.md         # hasil Fase 0 (arsitektur, fstab, props, kernel)
  DEBLOAT-LIST.md     # app yang dibuang + alasan
  BUILD-LOG-KERNEL.txt
  BUILD-LOG-ROM.txt
  DECISIONS.md        # keputusan teknis & trade-off
  VERIFY-LOG.md       # hash & verifikasi artifact
  PORT-SUMMARY.md     # dalam/akhir: apa yang boot, apa yang rusak (camera/FaceUnlock/UI), vbmeta cmd, flash order
```

### FASE 4 — GITHUB
- Clone `https://github.com/dwp29/pureport-17ultra`, buat branch `UFO-0.1-work`
- COMMIT hanya docs/skrip/log (TIDAK ADA firmware/ROM/biner besar di repo!)
- CI yang ada: `.github/workflows/build-kernel.yml` — boleh dipakai untuk "clean build check"

## ATURAN KERAS
0. SEBELUM FASE 1 (dan sebagai bagian FASE 0), WAJIB BACA:
   `~/ROM-Tools/synthetica-arsip/SYNTHETICA-KERNEL-ARSIP-LENGKAP-2026-11-13/04-DOKUMEN-MD-CATATAN/01-DOKUMEN-MD-Synthetica-dan-Kernel/SYNTHETICA-3.2-RELEASE-AND-DEV-GUIDE.md`
   (Fakta kernel Synthetica-3.2 = base UFO-0.1; jangan kerja dari dugaan)
1. Error → langsung betulkan; JANGAN tinggalkan job gara-gara satu error
2. Jangan ganti task — fase selesai → lapor → fase berikut
3. vbmeta/AVB hanya unlocked; JANGAN RELOCK bootloader (brick permanen di custom/port ROM)
4. HOS ports butuh **KernelSU Next spoofed** (Play Integrity), bukan stock Magisk
5. Semua aksi flashing (fastboot/edl/TWRP) = tunggu perintah user sebagai langkah terpisah
6. Setiap fase = catatan di SESSION-LOG.md (waktu, perintah, keluaran)
7. Jika blocked > 2 percobaan → ringkas upaya + tanya (JANGAN lanjut membabi buta)

## KRITERIA SELESAI
- [ ] `UFO-0.1-miatoll-<tanggal>.zip` — flashable OrangeFox, hash MD5/SHA-256 tercatat
- [ ] `HyperOS-4-pureport-joyeuse-<tanggal>.zip` — flashable oFox, debloated, kompresi maks, size tercatat
- [ ] Keduanya tercantum di VERIFY-LOG.md
- [ ] PORT-SUMMARY.md final (flash order, vbmeta cmd, known bugs)
- [ ] Semua Fase 0–4 tercatat rapi di UFO-0.1-LOG/
- [ ] Firmware/ROM tidak pernah di-push ke repo mana pun

Mulai dari FASE 0. Sebelum build apa pun, kembalikan tabel hash & list payload ke user.
