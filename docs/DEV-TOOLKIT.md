# Dev Toolkit PC — ROM Porting • Build APK • AI
Installed on: Linux Mint 22.3 (Zena) — Nov 12 2026 · Status: **DONE & verified**

## H. Browser / Media / Desktop / Xiaomi flash
- **Google Chrome 157** (.deb resmi Google, apt) — jadi default `x-www-browser`; ketik `google-chrome` atau menu app
- **Spotify Client 1.2.95** (flathub, user) — menu app "Spotify"
- **spotipy 2.26.0** (library Python API Spotify) — venv `~/.venvs/spotipy/bin/python` (akan import `spotipy`; butuh client-id/secret dari Spotify for Developers)
- **Tauon Music Box 13.1.1** (flathub) — pemutar musik offline, UI modern + fitur lengkap (lirik, radio, Last.fm, transcode, gapless). `flatpak run com.github.taiko2k.tauonmb` atau menu app
- **VLC 3.0.20** — video/audio player serba bisa
- **Nemo** — file manager (Mint default, tadi hilang — sekarang terinstall); desktop icons aktif (`org.nemo.desktop show-desktop-icons=true`)
- **Shortcut desktop** (`~/Desktop/`, 12 shortcut, macOS-style lean): Google Chrome, Files (Nemo), Terminal, VS Code, Android Studio, MIO-KITCHEN, OpenCode, AnythingLLM, Tauon Music Box, Celluloid, Spotify, Telegram
- **Wallpaper macOS** (26-Tahoe Light/Dark, 15-Sequoia Light/Dark, Sonoma Horizon) di `~/Pictures/Wallpapers/` — sumber: github.com/LAYTAT/macOS-Wallpapers (asset Apple, kredit Apple; hak cipta tetap pada Apple). Aktif: **26-Tahoe-Light-6K** (semua workspace + monitor)
- **Ikon Desktop**: size 36 (macOS-like) via `xfconf-query -c xfce4-desktop -p /desktop-icons/icon-size -s 36`
- **FreeTube**: di-UNINSTALL (user request). **Hypnotix** (TV) & **VLC** & **Rhythmbox**: menunggu uninstall manual via terminal kamu (lihat catatan) — shortcut desktop sudah dihapus
- **Tema desktop — yang aktif: Colloid-Dark** (GTK Dark) + **ikon Papirus-Dark** (cakra cakupan tray/system paling lengkap: wifi, bluetooth, volume, battery, notifikasi) + cursor WhiteSur-cursors; xfwm4 window borders Colloid-Dark via `xfconf-query` + `xfwm4 --replace`. **PC ini pakai Mint XFCE edition** — pengaturan lewat `xfconf-query` (bukan `org.cinnamon.*` gsettings!), live langsung terlihat
- Alternatif terpasang: **WhiteSur** (macOS-style), **Mint-Y** / **Mint-Y-Dark** / **Mint-Y-Aqua** (bawaan). Balik ke Mint-Y-Aqua: `/Net/ThemeName=Mint-Y-Aqua` dsb. Source di `~/.local/share/whitesur/`
- **Cairo-Dock** — dock ala macOS/Windows, paling populer & customizable di Linux (`cairo-dock`). Autostart on login; right-click dock → Configure untuk tema, ukuran, zoom, posisi (bawaan sudah mirip macOS). Plank dihapus karena kurang cocok
- **Xiaomi flashtool (EDL)** — `edl` (bkerler/edl, Qualcomm Firehose client) di `~/.local/bin/edl`, source `~/ROM-Tools/edl`, deps di venv `~/.venvs/edl`
  - butuh **firehose programmer** (`.mbn/xbl`) sesuai device (joyeuse / miatoll dari official Xiaomi firmware), misal: `edl printgpt` / `edl r boot boot.img`
  - EDL mode: device masuk Qualcomm 9008 (power+vol-down/edl testpoint)
  - **Mi Flash = Windows-only**; di Linux pakai fastboot (unlocked) atau EDL (locked/brick)
- **udev rules** baru: `/etc/udev/rules.d/99-android-flash.rules` — akses USB penuh (MODE 0666 + uaccess) untuk Qualcomm (05c6), MediaTek (0e8d), Samsung (04e8), Xiaomi (2717), Google (18d1), UNISOC (1782); `51-android.rules` bawaan sudah mencakup adb/fastboot semua vendor

## I. Flash tools (Android)
| Vendor | Tool | Keterangan |
|---|---|---|
| Qualcomm (joyeuse SD 720G) | `fastboot` 37 + **`edl`** (bkerler) `~/.local/bin/edl` | fastboot = unlocked flash; EDL 9008 = bricked/locked. Butuh firehose programmer `.mbn/xbl` per-device dari Xiaomi firmware |
| MediaTek | **`mtkclient`** (CLI `mtk` + GUI `mtkclient`) `~/ROM-Tools/mtkclient`, venv `~/.venvs/mtkclient` | SP Flash Tool equivalent: BROM/VCOM flash, read/write partisi, factory reset, FRP |
| Samsung | **heimdall-flash** + **heimdall-frontend** (GUI) | ODIN alternative resmi open-source; flash via Download mode |
| Xiaomi | fastboot / edl (QC) / mtkclient (MTK varian, mis. Redmi Note 9 = Helio G85) | **Mi Flash = Windows-only** — tidak tersedia di Linux |
- **Driver di Linux = udev rules + kernel modules (cdc_acm, usb_storage) — tidak ada "driver pack installer" seperti Windows**
- Di Linux, USB access langsung setelah udev rules; user group `adbusers` menangani adb


## E. Kernel build (Android kernel)
- clang 18.1.3 + lld + llvm (Android kernels build with clang, e.g. `make ARCH=arm64 LLVM=1 vendor/<device>_defconfig`)
- ccache 4.9.1 (rebuild speed), bison, flex, libncurses-dev (menuconfig), libelf-dev, libdw-dev, bc, dwarves/pahole 1.25 (BTF), cpio, rsync, gcc-multilib/g++-multilib
- `repo` launcher 2.71 at `~/.local/bin/repo` (fetch AOSP/LineageOS/kernel sources)
- Kernel build **SUCCESS (12 Nov 2026)** via `./build.sh` (Clang 11.0.1 prebuilt + gcc 4.9 prebuilt): `out/arch/arm64/boot/Image.gz` (13 MB) + `Image` (33 MB) + `dtb.img`/`dtbo.img`. Flashable zip: `~/ROM-Tools/kernel_joyeuse/AnyKernel/Stormbreaker-miatoll-20261112-22.zip` (AnyKernel3, 15 MB) — flash via custom recovery (TWRP). Build dengan clang 18 bawaan sistem GAGAL (sp/constraint error) — wajib pakai toolchain pinned
- Defconfig: `vendor/xiaomi/miatoll_defconfig` (kernel 4.14.357-openela)
- Full AOSP/LineageOS ROM **source build** is possible on paper (disk 419 GB free) but very heavy on 7.7 GB RAM — expect heavy swap use and long builds; kernel + `fastboot boot` test cycle is the practical route on this PC

## Key paths
- Android SDK: `~/Android/Sdk`  (platform-tools 37.0.1, cmdline-tools, platforms 35 & 36, build-tools 36.1.0 & 37.0.0, sources API 36)
- Android Studio: `~/Android/android-studio`  → launch from app menu "Android Studio" or type `studio`
- ROM tools: `~/ROM-Tools/mio-kitchen`, `~/ROM-Tools/jadx`, `~/ROM-Tools/dex2jar`, `~/ROM-Tools/kernel_joyeuse` (kernel source, branch 16.0)
- User-space binaries: `~/.local/bin` (payload-dumper-go, lpunpack, lpdump, lpmake, lpadd, lpflash, jadx, d2j-*, code, studio, mio-kitchen)
- PATH & env are appended in `~/.bashrc` AND `~/.profile` (ANDROID_HOME, ANDROID_SDK_ROOT, JAVA_HOME=java-17, PATH). New terminals pick it up automatically.

## A. ROM Porting
| Tool | Usage |
|---|---|
| adb / fastboot (platform-tools 37.0.1) | `adb`, `fastboot` on PATH (apt version 34 also present) |
| payload-dumper-go 2.1.0 | `payload-dumper-go payload.bin` (extract OTA payload.bin) |
| lpunpack / lpdump / lpmake / lpadd / lpflash | `~/.local/bin/*` — static x86_64 binaries (Android 35-based), for super.img & logical partitions |
| MIO-KITCHEN (GUI, Python) | type `mio-kitchen` or app menu "MIO-KITCHEN" — unpack/repack payload, super.img, erofs, ext4, boot.img, etc. All requirements installed (PySide6 6.12, python-lzo OK) |
| simg2img / img2simg | apt `android-sdk-libsparse-utils` + `img2simg` bundled in MIO-KITCHEN |
| brotli / zstd / lz4 / xz / lzip | apt + binaries bundled in MIO-KITCHEN |
| erofs (mkfs.erofs, extract.erofs) | apt `erofs-utils` 1.7.1 + bundled in MIO-KITCHEN |
| magiskboot, make_ext4fs, mke2fs, dtc, afptool, imgkit, e2fsdroid | bundled in MIO-KITCHEN `~/ROM-Tools/mio-kitchen/bin/Linux/x86_64/` |
| apktool 2.7 (+ smali/baksmali 2.5.2) | `apktool d app.apk` / `apktool b app` |
| jadx 1.5.6 | `jadx -d out app.apk` or `jadx-gui` (GUI, verified working) |
| dex2jar v2.4 | `d2j-dex2jar classes.dex` — needs java (java-17 installed) |
| binwalk 2.3.3, unrar, 7zip/p7zip | apt (firmware analysis/extraction) |
| git 2.43 + git-lfs | apt (clone kernel/ROM sources) |
| aapt (Android Asset Packaging) | apt |

General porting flow:
1. `payload-dumper-go payload.bin` → per-partition images
2. super.img: `lpunpack super.img out/` (or the MIO-KITCHEN GUI)
3. unpack erofs/ext4 via MIO-KITCHEN
4. decompile APK: `jadx` / `apktool` / `smali` → edit → repack
5. repack via MIO-KITCHEN → flash: `fastboot flash ...`

## B. Build APK
- Android Studio 2026.2.2 Patch 1 ("Rabbit 2") — ships with JBR 25, verified working
- JDK 17 (apt) for Gradle CLI; `java`/`javac` → /usr/lib/jvm/java-17-openjdk-amd64 (update-alternatives)
- Build via CLI: `./gradlew assembleDebug`; IDE: open project → Run ▶
- SDK licenses accepted (sdkmanager); adb USB udev rules: `android-sdk-platform-tools-common`
- NDK not installed (skipped, ~2.5GB); if needed: `sdkmanager "ndk;27.0.12077973" "cmake;3.22.1"`

## C. AI (offline, local — CPU-only, 7.7GB RAM)
- Ollama installed & `ollama.service` **active** (systemd, port 11434)
- Models present:
  - `qwen2.5-coder:3b` (1.9GB) — coding/autocomplete cepat
  - `deepseek-r1:7b` (4.7GB) — RECOMMENDED untuk analisis berat build/ROM/APK (lambat tapi paling pintar)
  - `qwen3:8b` (5.2GB) — all-rounder generasi baru
  - `llama3.2:3b` (2.0GB) — general chat
  - `nomic-embed-text` (274MB) — embeddings
- CLI: `ollama run qwen2.5-coder:3b` / `ollama run deepseek-r1:7b`
- VS Code 1.139.1 (Flatpak, user install) + extensions:
  - **Continue** v2.0.0 — local config `~/.continue/config.yaml` → Ollama + free-API presets
  - **Python** + Pylance
  - **Gemini Code Assist** v2.107.0 (Google, free tier — sign in with Google account in VS Code)
- Free API presets in Continue (all $0, need a free key pasted into config.yaml):
  - Gemini 2.5 Flash — https://aistudio.google.com/apikey
  - Groq Llama 3.3 70B — https://console.groq.com
  - GitHub Models gpt-4o-mini (free w/ GitHub account) — https://github.com/settings/tokens
  - OpenRouter `:free` models — https://openrouter.ai/keys
- Launch: app menu "Visual Studio Code" or type `code`
- Installed locally: `qwen2.5-coder:3b`, `llama3.2:3b`, `deepseek-r1:7b`, `qwen3:8b`, `nomic-embed-text`

- **AnythingLLM v1.19.0** (AppImage `~/.local/bin/AnythingLLM.AppImage`, 905MB) — AI chat desktop (Ollama/RAG). **Wajib `--disable-gpu`** (Haswell iGPU Vulkan tidak lengkap → GPU process crash code 1002) — shortcut sudah memakai flag. First-run: masuk sebagai "local/agentless", lalu Settings → LLM Provider → Ollama (http://127.0.0.1:11434) → pilih `qwen2.5-coder:3b`. Warning `xdg-settings` di XFCE tidak berbahaya

## AI agents — sejenis OpenCode (terminal)
- **OpenCode** — already installed (what you're using now)
- **Gemini CLI 0.68.0** (Google official, free tier: login Google, ~1000 req/day) — `gemini` di terminal; butuh Node ≥ 20 → **Node 22.23.5 via nvm** (`nvm use 22`; nvm blocks ~/.bashrc — buka terminal baru). Login pertama: `gemini` (browser auth)
- **Aider** (open-source, Apache-2.0 — multi-provider) — via pipx; bisa pakai Ollama lokal / Gemini free / Groq free / OpenRouter :free. Set key sekali: `export GEMINI_API_KEY=...` atau langsung `aider --model gemini-2.5-flash`
- VS Code **Continue** (v2.0.0) + **GitHub Pull Requests** (v0.166.1, official GitHub) + **Gemini Code Assist** (free, Google sign-in)
- **Node 18 dari apt terlalu tua** untuk Gemini CLI → pakai nvm Node 22.23.5 (default alias `22`, masuk `~/.bashrc` otomatis)

## J. OpenCode — optimasi model & agent gratis (smart free)
| Agent | Model | Catatan |
|---|---|---|
| `smart-free` | `openrouter/nvidia/nemotron-3-ultra-550b-a55b:free` | Paling pintar gratis (AA Index 22.9), 1M ctx, reasoning & orkestrasi berat — lambat (~29 tok/s) |
| `fast-free` | `openrouter/nvidia/nemotron-3.5-super-vl:free` | Terandal & tercepat (20/20 passed, 106 tok/s), 1M ctx, text+image+video |
| `code-free` | `openrouter/cohere/north-mini-code:free` | Agent coding terbaik gratis (30B MoE, dilatih utk OpenCode/SWE-Agent), 256K ctx |
| `gemini-flash-free` | `google/gemini-2.5-flash` | Google free tier — cepat; perlu key aistudio.google.com/apikey (gratis) |
| `rom-free` | `openrouter/nvidia/nemotron-3-ultra-550b-a55b:free` | ROM porting specialist (Treble/fstab/overlay/Magisk/vbmeta/AVB/erofs) |
- Cadangan gratis lain: `openrouter/thinkingmachines/inkling-2-small:free` (model yang dipakai sesi ini; hanya via agentic harness seperti OpenCode), `openrouter/google/gemma-4-31b-it:free` (multimodal, sering 429), `openrouter/nvidia/nemotron-3.5-lightning:free` (volume tinggi)
- Limit gratis: **50 req/hari** (20/menit); **1.000/hari** setelah sekali top-up $10

### Filter & disable model berbayar (diterapkan 13 Nov 2026)
- **OpenRouter**: 365 model berbayar/berisiko **disabled** (semua yang cost>0 + `openrouter/auto|fusion|pareto-code|bodybuilder` yang bisa route ke model berbayar). Tersisa 18 model gratis (gemma-4:free, nemotron:free, north-mini-code:free, inkling-2-small:free, dst. + `openrouter/free`)
- **Google**: 33 model **disabled**. Tersisa hanya yang cost==0: `gemma-4-31b-it`, `gemma-4-26b-a4b-it`, `lyria-3-clip-preview`, `lyria-3-pro-preview`
- **Konsekuensi**: `google/gemini-2.5-flash` & `gemini-2.5-pro` dimatikan (katalog berbayar; gratis hanya kuota terbatas di AI Studio). Mau diaktifkan manual? Set `"disabled": false` untuk keduanya di `~/.config/opencode/opencode.json` (bagian `providers.google.models`)
- Agent `gemini-flash-free` → `google/gemma-4-26b-a4b-it`, `gemini-pro-free` → `google/gemma-4-31b-it` (selalu gratis)

### Skills (di `~/.config/opencode/skills/` — global, semua agent & session)
| Skill | Untuk |
|---|---|
| `joyeuse-kernel` | Build kernel Redmi Note 9 Pro (miatoll) — toolchain wajib pinned clang 11, defconfig `vendor/xiaomi/miatoll_defconfig`, perintah build & flash |
| `rom-porting` | Porting ROM dari OTA payload → flashable zip (boot patch Magisk, vbmeta, repack erofs/ext4, overlay, fstab, build.prop) |
| `mio-kitchen` | Pakai MIO-KITCHEN (unpack/repack: boot, super.img, erofs/ext4/f2fs, payload, .br, dtbo) — CLI fallback included |
| `apk-build-release` | Build/sign APK: `./gradlew assembleDebug/Release`, keystore, apksigner, common Gradle errors, decompile |
| `smali-apktool` | Decompile → edit → recompile (arm64 libs, permissions, hosts, res values) |
| `android-flash` | Flashing USB: fastboot, EDL, BROM/VCOM, Download mode — udev, SOS sequence, firehose, vbmeta/AVB cautions |
| `synthetica-kernel` | Synthetica Kernel + HOS 4 ROM di joyeuse: backup → flash ROM → kernel HOS4 zip → KSU Manager root check; path lengkap + perintah verifikasi; keamanan keystore |
| `miatoll-dev-sources` | COMPLETE index 117+ repos verified Nov 2026: LineageOS/crDroid/Pixel/Elixir/ArrowOS/SailfishOS/eOS/PostmarketOS/Mainline, recoveries, vendor, ports, local build paths |
- `~/.config/opencode/skills/` di-watch otomatis — agent bisa memanggil skill dengan `skill("joyeuse-kernel")` atau agen lintas sesi otomatis memakainya saat relevan
- Config: `~/.config/opencode/opencode.json` (`$schema` included) — OpenCode watch & reload otomatis, tidak perlu restart
- **Provider built-in tanpa config** (tinggal `/connect` atau env var):
  - **OpenCode built-in free** — `opencode/inkling-2-small-free` (sudah dipakai session ini, $0)
  - **Ollama** — `ollama/qwen2.5-coder:3b` (default) / `ollama/deepseek-r1:7b` (paling pintar) / `ollama/qwen3:8b` — lokal offline, $0
  - **OpenRouter** (free models, perlu key dari https://openrouter.ai/keys — gratis, no kartu): `openrouter/nvidia/nemotron-3-ultra-550b-a55b:free` (paling pintar yang free), `openrouter/cohere/north-mini-code:free` (coding), `openrouter/thinkingmachines/inkling-2-small:free`, `openrouter/google/gemma-4-31b-it:free`
  - **Google Gemini** (free tier, key dari https://aistudio.google.com/apikey): `google/gemini-2.5-flash` (smart, $0)
  - **Groq** (free tier, console.groq.com): `groq/openai/gpt-oss-120b` (ultra fast, $0)
- **Custom agents** (`~/.config/opencode/agents/*.md`) — tanpa restart:
  - `smart-free` — nemotron-3-ultra-550b-a55b:free — reasoning berat
  - `fast-free` — nemotron-3.5-super-vl:free — cepat & andal (106 tok/s, tercepat)
  - `code-free` — north-mini-code:free — coding specialist (dilatih untuk OpenCode)
- Aktivasi keys (pilih salah satu):
  1. Di OpenCode: ketik `/connect` → pilih OpenRouter/Google/Groq → paste key → `/models`
  2. Atau env var (berlaku untuk CLI & app yang di-launch dari terminal): `export OPENROUTER_API_KEY=sk-or-...` di `~/.bashrc`, lalu restart app
- Free models dibatasi rate-limit — untuk kerja offline/berat: `ollama/deepseek-r1:7b`

### External skill packs (terinstall 13 Nov 2026, source di `~/.local/share/android-skills/`)
- **android/skills** (Google, Apache-2.0) — 36 skill: jetpack-compose (performance, adaptive, XML→Compose), build-system/agp-9-upgrade, devtools/android-cli (CLI resmi Android), performance (r8-analyzer, anr-audit-and-fix), profilers, security, testing, play, camera/camerax, navigation-3
- **chrisbanes/skills** (Apache-2.0) — 21 skill Kotlin/Compose: performance, concurrency, animations, API design, subagent-delegation, gradle-run
- **suchobits/android-skills** (MIT) — 10 skill production workflow: architect, modularizer, build-logic, architecture-guard, lint-enforcement, testing, dev-workflow
- Total ~74 skill global tersedia untuk semua agent & session di `~/.config/opencode/skills/`

### Port ROM default (per 13 Nov 2026)
- **`MiatollCave/Xiaomi.EU-Miatoll`** (Unlicense) — **DEFAULT** — stable Xiaomi.EU HyperOS miatoll port; branch `main`. Recommended recovery: **OrangeFox R11.3 FbeV2**. Alternative: `iput-object/CaveOfMiatoll` (branches `hyperos-15`/`hyperos-15-cn`/`main`).
- HOS 4 port porting info: `~/Downloads/HyperOS-4_MIATOLL-STABLE-dizasports.zip` (@dizasports, base Xiaomi 18 Pro Max)
- Telegram: `@Miatoll`, `@MiatollOfficial`, `@MiatollClouds`, `@miatollcave`, `@miatollcavesupport`

## F. GitHub / CI
- `gh` CLI 2.45.0 — **logged in as dwp29** (HTTPS, device-code flow, 14 Nov 2026). git identity set: `xClaudeGptx` / `275995953+dwp29@users.noreply.github.com`
- SSH key (ed25519) generated: `~/.ssh/id_ed25519.pub`
  → 
  Public key: `[redacted — simpan di private local copy]`
- git identity **set** (global): `xClaudeGptx` / `275995953+dwp29@users.noreply.github.com`
- **Repo project: https://github.com/dwp29/pureport-17ultra (public)** — clone di `~/ROM-Tools/pureport-17ultra`. Berisi docs, OpenCode skills, donor-ROM notes, workflow `build-kernel.yml` (trigger manual / tag `kernel-v*`; runner build dari upstream crDroid branch 16.0, artifact .zip di tab Actions → Artifacts)

## G. Joyeuse kernel (Redmi Note 9 Pro — miatoll family, SD 720G = "atoll" platform)
- Cloned: `~/ROM-Tools/kernel_joyeuse` — crdroidandroid/android_kernel_xiaomi_sm6250 @ branch **16.0** (shallow, 1.5GB)
- Correct defconfig discovered & verified: `vendor/xiaomi/miatoll_defconfig` (kernel 4.14.357-openela)
- `make O=out ARCH=arm64 LLVM=1 vendor/xiaomi/miatoll_defconfig` → **works** (system clang 18)
- Build options:
  - Quick local build: `make O=out ARCH=arm64 LLVM=1 -j$(nproc)`
  - Full flashable zip (upstream script, downloads pinned prebuilts ~1.5-2GB): `./build.sh`
    (builds Image.gz → AnyKernel3 → Stormbreaker-miatoll-<date>.zip)
- Note: defconfig itself builds with system LLVM; full image build is untested — do a local build first before trusting CI
- Starter CI: `.github/workflows/kernel.yml` included in the clone (builds on GitHub runners, uploads Image.gz artifact). Needs push to YOUR fork to run; adjust `clang` package as needed.


## D. General
- nodejs 18.19 + npm 9.2 · golang 1.22 · python3 3.12 + pip · cmake 3.28 / ninja · build-essential · qemu-user-static (run ARM/x86 binaries)
- MIO-KITCHEN venv: `~/ROM-Tools/mio-kitchen/.venv` (all requirements installed: PySide6 6.12, androguard, python-lzo, etc.)
- Qt xcb plugin fix: `libxcb-cursor0` etc. installed (Nov 12 2026) — MIO-KITCHEN previously failed to load the xcb plugin

## Downloaded ROMs (verified)
- nezha_global-ota_full-OS4.0.0.8.XPAMIXM-user-17.0-55863f99f3.zip (9,7 GB, donor Xiaomi 17 Ultra, HyperOS 4 / Android 17) — SHA-256 `9e8c7795e9089787f33b8199208a0fa2defd90aceb96ddd002f1f5dd549d6cbe` — `~/Downloads/`
- miui_JOYEUSEGlobal_V14.0.3.0.SJZMIXM_df17e3fabf_12.0.zip (2,9 GB, stock Recovery Global Stable, Android 12) — MD5 `df17e3fabf2284cc28efe8d10d012007` (official, verified) — `~/Downloads/`

## Notes
1. The sudo password was typed in chat at your request. Consider changing it and/or clearing chat history.
2. git identity not set: `git config --global user.name "Name" && git config --global user.email "you@example.com"`
3. The installers (~1.9GB) in `~/downloads_tmp` were deleted after extraction.
4. The "Default Project" folder (where this chat ran) was left untouched.
