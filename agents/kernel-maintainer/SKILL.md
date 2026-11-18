---
name: kernel-maintainer
description: Workflow memelihara kernel Android upstream — patch, defconfig, build, verify, sign.
---

# Kernel Maintainer

## Kapan pakai
Ketika kamu "custom kernel" (Stormbreaker, UFO-0.1, Synthetica) — dan kamu ingin di-repeat dengan disiplin.

## Filosofi
1. **Satu sumber kebenaran** — pilih branch upstream (AOSP, Lineage, atau custom). Jangan dicampur tanpa alasan.
2. **Patch minimal** — hanya yang diperlukan dan berdokumentasi.
3. **Config yang ditrace** — simpan `.config` bersama commit.
4. **Build deter** — selalu `make mrproper` sebelum `make nconfig` manual.

## Langkah build
```bash
cd /path/to/kernel-source
mkdir -p out
# merge config (Android-style)
build/kernel/merge-config.sh out/.config arch/arm64/configs/<base_defconfig> <ksu.fragment.config> <user.fragments.config> 2>&1 | tee merge-config.log
# verifikasi hasil
make O=out defconfig
# atau langsung dari .config
cp .config out/.config
make O=out -j$(nproc)Image.gz
```

## Verifikasi ekstensif
- `readelf -a out/Image.gz | head -30` — cek ELF header
- AVB repack boot.img (lihat skill `avb-fix-repack`)
- Hash binary `Image.gz` → simpan `sha256sum` di `HASHES.txt`
- Boot test di device nyata (lihat `boot-failure-inspection`)

## Kebersihan & disiplin commit
- Jangan commit artifact: `out/`, `.config`, `Image*.gz`, `*.ko` non-sumber.
- Gunakan **branch terpisah** per patch/experiement.
- Gunakan **`.clang-format`** kalau ada; jangan ubah gaya acak.

## Ketika gagal build
- `make O=out Image.gz V=1` → lihat error baris demi baris.
- Cari symbol yang hilang: itu berarti `.config` tidak konsisten dengan fragmen yang kamu tambah. Basis config harus cocok dengan kernel branch target (mis. 4.14 milik AOSP vs Lineage).

## Rollback
Kalau kernel baru bootloop:
1. Flash kernel lama yang sudah terbukti (`boot.img`).
2. Diagnosis dari `last_kmsg` / `dmesg` (lihat `boot-failure-inspection`).
3. Jangan coba combine dua kernel yang gagal langsung ke device — bisect timpa yang berkedip dulu.
