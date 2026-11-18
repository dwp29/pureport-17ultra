# ATTRIBUTION — `extern/`

Folder `extern/` berisi salinan bersih (tanpa `.git`) dari repo pihak ketiga yang di-review dan di-clone
untuk studi & referensi porting. Semua hak milik repo aslinya dan lisensinya tetap berlaku.
**Tidak ada firmware/ROM yang disertakan.**

| Path | Sumber (upstream) | Lisensi | Catatan |
|---|---|---|---|
| `extern/android-adb-control/` | https://github.com/robbin/android-adb-control | MIT | Agent skill ADB control |
| `extern/Android_boot_image_editor/` | https://github.com/cfig/Android_boot_image_editor | Apache-2.0 | Unpack/repack boot/vbmeta/payload |
| `extern/android-kernel-lkm/` | https://github.com/Yunnijian/android-kernel-lkm | GPL | SKILL.md LKM/kprobe |
| `extern/compose-skill/` | https://github.com/aldefy/compose-skill | MIT | Jetpack Compose 2026 agent skill |
| `extern/mobile-mcp/` | https://github.com/mobile-next/mobile-mcp | Apache-2.0 | MCP server kontrol device |
| `extern/reproduce-android-kernel-builds/` | https://github.com/aFunnyStrange/reproduce-android-kernel-builds | — (tidak ada LICENSE di repo) | Reproducible kernel build workflow; dipakai sebagai referensi saja |
| `extern/xiaomi17-kernel-skills/` | https://github.com/Ma6302/xiaomi17-kernel-skills | MIT | 10 skill kernel Xiaomi SM8850 (GKI 6.12) — **referensi saja, bukan untuk miatoll 4.14** |

## Aturan pemakaian

- Baca `LICENSE` di masing-masing folder sebelum memakai apa pun.
- Repo dengan klaim/zawodu tinggi (`xiaomi17-kernel-skills`, `reproduce-android-kernel-builds`) belum diuji pada miatoll — verifikasi lokal, jangan percaya mentah-mentah.
- Script yang memanggil `fastboot flash` / `make` / `erase` **tidak dijalankan otomatis**; review dulu sebelum eksekusi.
