---
name: secret-scan
description: Cegah keystore, password, API key, token bocor ke repo publik. Dipakai sebelum commit/push apa pun.
---

# Secret Scan (repo hygiene)

## Kapan pakai
Sebelum **git add/commit/push** — khususnya repo publik (mis. `dwp29/*`).

## Checklist wajib
1. **`git diff --cached --stat`** → lihat file yang akan di-commit.
2. Cari pola rahasia:
```bash
git diff --cached | grep -iE -n "password|passwd|secret|api[_-]?key|token|private[_-]?key|keystore|\.p12|\.jks|bearer |authorization:" || echo CLEAN
```
3. Cek file binari/keystores yang tidak sengaja ikut:
```bash
git diff --cached --name-only | grep -iE "\.(p12|jks|keystore|pfx|pem|key|der|asc)$"
```
4. `git rev-parse` tidak boleh mengandung file besar > beberapa MB:
```bash
git diff --cached --name-only | xargs -I{} sh -c 'echo "$(stat -c%s {}) {}"' | sort -rn | head
```
5. Cek berkas `secrets/` / `.env` / `credentials*` ikut ter-track atau tidak.

## Kebijakan repo yang aman
- `.gitignore` minimal:
```
*.p12
*.jks
*.keystore
*.pfx
*.pem
*.key
*.der
secrets/
.env
credentials*
*.keystore.b64
```
- Selalu simpan keystores di luar repo (mis. `~/ROM-Tools/synthetica-arsip/`).
- Key/password TIDAK BOLEH di-embed di source code, bahkan sebagai fallback. Selalu `/connect` atau env.

## Kalau terlanjur ter-commit
1. **JANGAN push** sampai dibersihkan.
2. `git reset --soft HEAD~1` → `git restore --staged <file>` → tambah `.gitignore` → commit ulang.
3. Kalau sudah terlanjur push: **CAIRKAN PASSWORD/KEY SEGERA** (revoke di provider), rewrite history (`git filter-repo`), atau laporkan ke tim security/reviewer.
