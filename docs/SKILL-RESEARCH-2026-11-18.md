# SKILL-RESEARCH — Repo riset skill AI untuk pureport-17ultra
Tanggal: 2026-11-18 (WIB) · Penulis: sesi OpenCode · Status: DIRENCANAKAN (belum dipasang)

Dokumen ini menyimpan hasil riset GitHub/komunitas agar tidak hilang. **Belum ada satu pun skill/repo di bawah ini yang di-clone atau di-install secara permanen.** Semua hanya dicatat.

## 1. Yang SUDAH terpasang di mesin (JANGAN duplikasi)
`~/.config/opencode/skills` (global) + `pureport-17ultra/skills/opencode/` (projek):
adaptive · agp-9-upgrade · android-architect · android-architecture-guard · android-benchmark-comparison · android-build-logic · android-cli · android-compose-designsystem · android-dev-workflow · android-flash · android-for-cars-parked-apps · android-intent-security · android-lint-enforcement · android-modularizer · android-offline-sync · android-permissions-security · android-profiler · android-setup · android-testing · anr-audit-and-fix · apk-build-release · appfunctions · camerax · changelog · compose-animations · compose-component-design · compose-focus-navigation · compose-performance · compose-state-and-effects · compose-ui-testing-patterns · deliver-spec · edge-to-edge · engage-sdk-integration · gradle-run · grounded-writing · ink-app-builder · ink-custom-brush-builder · jetpack-compose-performance · joyeuse-kernel · kotlin-* · leanback-to-compose-tv-migration · litert-lm · litert-runtime · media3-cast-integration · miatoll-dev-sources · migrate-xml-views-to-jetpack-compose · mio-kitchen · mlkit-* · navigation-3 · navigation-event · play-billing-library-version-upgrade · play-policy-insights · projected-hardware · r8-analyzer · release-kotlin-library · restore-credentials · rom-porting · shepherd · smali-apktool · subagent-delegation · synthetica-kernel · testing-setup · to-plan · using-chrisbanes-skills · verified-email · wear-*

## 2. Hasil riset GitHub (2026-11-18)

### A. Prioritas tinggi — device automation & kernel
| Repo | Stars | Isi | Relevansi |
|---|---|---|---|
| `mobile-next/mobile-mcp` | 10.6k | MCP server — agent AI drive Android device/emulator (install, tap, screenshot, verify UI) | Test build otomatis di HP joyeuse |
| `Yunnijian/android-kernel-lkm` | 15 | SKILL.md — LKM/kprobe Android kernel module dev (OpenCode/Claude/Codex) | KernelSU/Nezuko module work |
| `aFunnyStrange/reproduce-android-kernel-builds` | 0 (baru) | Reproducible kernel + boot image: source lock, ABI check, validation gate, rollback | Build kernel synthetica/stormbreaker dengan metadata |
| `Ma6302/xiaomi17-kernel-skills` | 1 | 10 agent skills build/tune kernel Xiaomi/SM8850 (donor nezha kamu) | Referensi pola kernel vendor SM8850 |
| `robbin/android-adb-control` | 97 | Agent skill ADB "observe, act, verify" untuk OpenCode | Otomasi device via agent |

### B. AVB/vbmeta tooling (bukan skill, tapi penting)
| Repo | Stars | Isi |
|---|---|---|
| `cfig/Android_boot_image_editor` | 1335 | Unpack/repack boot.img, vbmeta.img, payload.bin (Android 16) |
| `WessellUrdata/vbmeta-disable-verification` | 64 | Python port — disable AVB di vbmeta |
| `soe1hom-arch/vbmeta-toolkit` | 0 | Parse/patch vbmeta |
| `ShlomoHeller/AVB-Disabler` | 4 | Disable AVB python |
| `cpeoples/avbgraft` | 2 | Repack factory Pixel + re-sign AVB |

### C. UI/Compose agents (opsional)
| Repo | Stars | Isi |
|---|---|---|
| `aldefy/compose-skill` | 604 | Compose skill dengan bukti source androidx asli |
| `haidrrrry/compose-kotlin-agent-skills` | 66 | Compose + Kotlin K2 + MVI, CI-validated |
| `ayush016/android-lead-agent-skills` | 54 | Compose, transitions, arch, code review, MCP |
| `lennonpetrick/android-engineering-skills` | 41 | Architecture, testing, production patterns |

### D. Koleksi skill (hati-hati, baca dulu)
`HunterisLive-1/mobile-maya-skills` (5★) · `nyusternie/droid-skills` (0★) · `inyogeshwar/vaani-skills` (0★) · `oywjun/opencode-skills` (3★) · `Yunnijian/android-kernel-lkm` (15★) · `azkernel` (0★, Claude Code skill utk port kernel/ROM — perlu dibaca)

### E. ROM porting references (bukan skill siap pakai)
`rajdeep-3305/android-porting-guide` (archived, 24★) · `MiCode/legacy-patchrom` (217★, MIUI2.3 2012) · `toraidl/hyperos_port` (219★, HyperOS Android 13/14)

## 3a. Paket skill portable (SUDAH DIBUAT — 12 skill, siap disalin ke agent mana pun)
Lokasi: `pureport-17ultra/agents/<nama>/SKILL.md`

| # | Nama skill | Fungsi |
|---|---|---|
| 1 | boot-failure-inspection | Diagnosis bootloop/soft-brick setelah flash |
| 2 | logcat-error-diagnosis | Baca logcat/ANR/crash, ekstrak error nyata |
| 3 | apk-signing-verify | Audit chain signing APK sebelum flash |
| 4 | secret-scan | Cegah key/password bocor ke repo |
| 5 | rollback-repair | Dari bad flash kembali ke state aman (Lunaris A16) |
| 6 | payload-extract | `lpunpack` payload.bin → images |
| 7 | rom-regression-suite | Satu perintah: zip+hash+AVB → PASS/FAIL |
| 8 | kernelsu-module-dev | Dev module KernelSU Next |
| 9 | kernel-maintainer | Workflow patch/build/sign/rollback kernel |
| 10 | rom-spoofing | Batas spoofing, Play Integrity — jujur |
| 11 | avb-fix-repack | unpack→verify→patch→recompute→repack AVB |
| 12 | ui-ux-animation-apk | Compose animations & design polish |

Cara pakai: lihat `agents/README.md`.

## 3b. Yang AKAN dibuat nanti (belum ada SKILL.md)

| # | Nama skill (rencana) | Fungsi |
|---|---|---|
| 1 | `payload-extract` | SUDAH DIBUAT — lihat paket portable |
| 2 | `spkg-module-dev` | Langkah-langkah modul KernelSU Next untuk Synthetica Manager WebUI |
| 3 | `apk-regression-suite` | Perluas rom-regression-suite untuk kasus APK (signing + AVB + verify APK tools) |
| 4 | `rollback-full-fastboot` | Rollback via fastboot (EDL-lite) untuk device yang tidak masuk recovery |


## 4. Aturan pembuatan skill
- Baca setiap file yang akan dipakai; skill = instruksi yang diinjeksikan ke agent — sumber asing = prompt injection risiko
- Jangan meng-install apa pun sebelum kamu approve; hanya catatan & review
- Selalu buat skrip nyata, bukan placeholder
- Uji di environment aman sebelum dipakai device nyata
- Simpan `SKILL.md` + `scripts/` + `references/` (opsional) — format mengikuti standar agent skill
