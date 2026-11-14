# pureport-17ultra

**Project: HyperOS port untuk Redmi Note 9 Pro (joyeuse) — donor dari Xiaomi 17 Ultra (nezha)**

Project riset & porting: mempelajari cara port HyperOS 4 ke device **miatoll family** (joyeuse = Redmi Note 9 Pro Global) menggunakan donor firmware **nezha** (Xiaomi 17 Ultra) sebagai referensi.

> ⚠️ **Disclaimer**
> - Repo ini **tidak** mendistribusikan ROM/firmware. Semua firmware adalah hak Xiaomi / pemegang hak masing-masing. Kami hanya menyimpan dokumentasi, catatan, dan tooling.
> - Porting ROM kustom = risiko brick. Test hanya di device yang kamu siap tanggung (bukan device harian tanpa backup penuh).
> - Trademarks: Xiaomi, HyperOS, MIUI — milik Xiaomi Inc. LineageOS, crDroid — community projects masing-masing.

## Target & donor

| Item | Detail |
|---|---|
| **Device** | joyeuse — Redmi Note 9 Pro (Global), keluarga *miatoll* (+ curtana / excalibur / gram / lancelot) |
| **SoC** | Qualcomm SM7125 (Snapdragon 720G) — kernel 4.14 |
| **Donor ROM** | `nezha_global-ota_full-OS4.0.0.8.XPAMIXM-user-17.0-55863f99f3.zip` (9,72 GB, Android 17, CDN resmi Xiaomi) — **hanya developer reference; tidak di-upload ke sini** |
| **Stock reference** | `V14.0.3.0.SJZMIXM` (Android 12) — dari mifirm.net / xiaomi.com |
| **Recovery** | OrangeFox R11.3 FbeV2 (recommended untuk HyperOS ports) / TWRP |
| **Recovery flash** | `fastboot flash recovery` (unlocked) → boot recovery |

## Status

| Tahap | Status |
|---|---|
| Riset & device tree index | ✅ `skills/opencode/miatoll-dev-sources` |
| Donor ROM nezha download (CDN resmi Xiaomi) | ✅ selesai (SHA-256 diverifikasi lokal) |
| Stock firmware joyeuse V14.0.3.0.SJZMIXM | ⏳ mifirm (multi-mirror, lambat) |
| Payload extraction nezha → super/boot/dtbo | ⏳ `payload-dumper-go` + `lpunpack` + MIO-KITCHEN |
| Build kernel (4.14, clang 11 pinned) | ✅ lokal — Stormbreaker `AnyKernel` zip built (`skills/opencode/joyeuse-kernel`) |
| Port dry-run + vbmeta/flash test | ⏳ |
| Flash ke device | ⏳ (backup penuh wajib) |

## ⚠️ Reality check (jujur)

Port ROM **full** dari donor *different device* (nezha → joyeuse) **tidak bisa langsung jalan** dengan "zip → flash". Yang realistis:
1. **Kernel & sepotong kecil komponen** — bisa dipelajari & diekstrak dari payload donor.
2. **Full ROM bootable** — komunitas biasanya port lewat device tree (LineageOS miatoll) atau lewat proven port (Xiaomi.EU / @dizasports HyperOS-4 miatoll). Repo ini mendokumentasikan eksperimen dan pembelajaran, **bukan** rilis ROM "stabil".
3. **Camera & Face Unlock** pada donor miatoll ports sering **tidak berfungsi** — perlu GCam / workaround.

## Struktur repo

```
docs/               # DEV-TOOLKIT.md, porting notes (sanitized)
skills/opencode/    # OpenCode skills project-specific (rom-porting, miatoll-dev-sources, kernel, flash tools)
.github/workflows/  # CI contoh: build Stormbreaker kernel di GitHub Actions
```

## Quick start untuk contributor

```bash
git clone https://github.com/<user>/pureport-17ultra.git
cd pureport-17ultra
less docs/DEV-TOOLKIT.md   # environment & tools di mesin pengembang
```

Local toolchain (Linux Mint 22.3): platform-tools (fastboot 37), MIO-KITCHEN, payload-dumper-go, lpunpack, jadx, apktool, clang 11 pinned + gcc 4.9 prebuilts, Ollama (lokal), OpenCode (agent CLI with free models).

## Legal

Konten yang dibuat oleh project ini (docs, scripts, workflow) dirilis di bawah MIT (lihat `LICENSE`). Semua firmware/ROM files hak milik pemegang haknya masing-masing dan tidak didistribusikan di repo ini.
