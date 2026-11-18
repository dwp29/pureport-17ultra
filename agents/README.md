# Portable Agent Skills — pureport-17ultra
Paket skill mandiri yang bisa dipakai di agent mana pun (OpenCode, Claude Code, Codex, Pi, Hermes, dll).
Tiap folder berisi satu `SKILL.md` — tidak bergantung pada OpenCode global config.

## Cara pakai per agent
- **OpenCode:** salin folder skill ke `~/.config/opencode/skills/<nama>/` (artinya agent akan melihatnya sebagai skill). Proyek ini sudah punya skill lokal di `skills/opencode/` — pilih salah satu.
- **Claude Code:** salin sebagai `.claude/skills/<nama>/SKILL.md`.
- **Codex / Pi / Hermes / lainnya:** baca `SKILL.md`, tempel isinya sebagai system/user prompt, atau copy ke folder skill agent tsb.
- **Manual:** baca sebagai checklist; semua isinya bisa dijalankan manusia.

## Daftar skill di paket ini
| Skill | Fungsi |
|---|---|
| boot-failure-inspection | Diagnosis bootloop/soft-brick setelah flash |
| logcat-error-diagnosis | Baca logcat/ANR/crash, ekstrak error nyata |
| apk-signing-verify | Audit chain signing APK sebelum flash |
| secret-scan | Cegah key/password bocor ke repo |
| rollback-repair | Dari bad flash kembali ke state aman (Lunaris A16) |
| payload-extract | `lpunpack` payload.bin → images |
| rom-regression-suite | Satu perintah: zip+hash+AVB → PASS/FAIL |
| kernelsu-module-dev | Dev module KernelSU Next |
| kernel-maintainer | Workflow patch/build/sign/rollback kernel |
| rom-spoofing | Batas spoofing, Play Integrity — jujur |
| avb-fix-repack | unpack→verify→patch→recompute→repack AVB |
| ui-ux-animation-apk | Compose animations & design polish |
