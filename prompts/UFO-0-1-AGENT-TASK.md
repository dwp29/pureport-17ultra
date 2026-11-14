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
- **Kernel 4.14 TIDAK BISA di-build dengan clang ≥ 12**; wajib clang 11 pinned (r6443078) + gcc 4.9 prebuilt.
  Jalankan: `bash ~/ROM-Tools/pureport-17ultra/scripts/bootstrap.sh`
- Kernel build Stormbreaker pernah sukses (out/arch/arm64/boot/Image.gz + AnyKernel zip) di `~/ROM-Tools/kernel_joyeuse`

## Bahan (integritas WAJIB dicek dulu)
| File | Ukuran | Verifikasi |
|---|---|---|
| nezha_global-ota_full-OS4.0.0.8.XPAMIXM-user-17.0-55863f99f3.zip (donor, HyperOS 4 / Android 17, Xiaomi 17 Ultra) | 9,7 GB | SHA-256 `9e8c7795e9089787f33b8199208a0fa2defd90aceb96ddd002f1f5dd549d6cbe` |
| miui_JOYEUSEGlobal_V14.0.3.0.SJZMIXM_df17e3fabf_12.0.zip (stock, Android 12 Recovery) | 2,9 GB | MD5 `df17e3fabf2284cc28efe8d10d012007` |
| HyperOS-4_MIATOLL-STABLE-dizasports.zip (port komunitas @dizasports — BUKTI boot di joyeuse) | 4,5 GB | belum ada hash resmi; hitung sendiri: `sha256sum` |
- Lokasi file: `~/Downloads/`
- Arsip synthetic kernel: `~/ROM-Tools/synthetica-arsip/SYNTHETICA-KERNEL-ARSIP-LENGKAP-2026-11-13-20261113T155641Z-1-001.zip`

## Urutan kerja — TAK BOLEH DILOMPAT

### FASE 0 — REKON (tanpa build apa pun)
1. Verifikasi hash ketiga ROM (`sha256sum`/`md5sum`); jika tidak cocok → STOP, jangan lanjut
2. `unzip -l` ketiga zip: daftar payload.bin/boot.img/dtbo/dtb/super.img/...
3. Ekstrak payload stock & donor (payload-dumper-go + lpunpack): fstab, DTB, build.prop, vbmeta flags, AVB
4. **Pelajari dizasports (bukti boot) MENDALAM**: susun laporan arsitektur (partition layout, avr-verity dtb, sepolicy, init.rc, vendor blob list, kernel version string, DTB, camera absence) — ini acuan utama, BUKAN nezha (SM8850 vs SM7125 = beda generasi total)
5. Output: `FINDINGS.md` (dalam folder log — lihat Fase 3)

### FASE 1 — KERNEL "UFO-0.1"
1. Inspeksi `~/ROM-Tools/synthetica-arsip/`: apakah ada SOURCE Synthetica-3.2?
   - Jika hanya prebuilt zip tanpa source → **TIDAK BISA** build dari situ; gunakan tree `~/ROM-Tools/kernel_joyeuse` (crDroid 16.0, 4.14.357-openela, defconfig `vendor/xiaomi/miatoll_defconfig`) dan NAMAi kernel `UFO-0.1`
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
