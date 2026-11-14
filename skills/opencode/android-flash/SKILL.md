---
name: android-flash
description: Flash Android devices — fastboot, EDL (Qualcomm), Download mode (Samsung), BROM/VCOM (MediaTek) — with correct udev modes and safety steps
---

# Flashing Android — fastboot / EDL / BROM / Download

## Device cable modes (check `lsusb` to know which)
| Mode | VID:PID | Tool |
|---|---|---|
| fastboot | `2717:ff40` / `05c6:*` / `18d1:4ee0` | `fastboot` (Android platform-tools 37, also apt's 34) |
| Qualcomm EDL | `05c6:9008` | `edl` (bkerler) — **needs firehose programmer** (`.mbn/xbl`, per device) |
| MediaTek BROM/VCOM | `0e8d:0003` / `0e8d:2000` | `mtkclient` (CLI `mtk` at `~/.local/bin/mtk`, GUI `mtkclient`) |
| Samsung Download/ODIN | `04e8:*` | `heimdall-frontend` (GUI at `/usr/bin/heimdall-frontend`) or `heimdall flash` |

This PC's udev rules (`/etc/udev/rules.d/99-android-flash.rules` + `51-android.rules` + `99-xiaomi-edl.rules`): all above VID/PID pairs get `MODE=0666` + `uaccess` → **no root needed**. Reload: `sudo udevadm control --reload-rules && sudo udevadm trigger`.

## fastboot (unlocked only)
```bash
adb reboot bootloader          # or: hold Power+Vol Down at boot
fastboot devices               # must list the device
fastboot --set-active=_a       # keep A/B active slot consistent
fastboot flashing get_unlock_ability   # <1> = allowed (Xiaomi still requires Mi Unlock Tool)
fastboot flash boot boot.img
fastboot flash vbmeta --disable-verity --disable-verification vbmeta.img
fastboot reboot
```
**Xiaomi caution**: even after unlocking, MiUI verifies partition signatures (`vbmeta` Bakery/AVB) — flashing stock vbmeta without `--disable-verity` on a custom boot usually renders device unbootable.

## EDL (bricked / locked devices — Qualcomm, incl. joyeuse)
1. Enter EDL (power+vol keys at boot, or testpoint on PCB to BROM/EDL)
2. Get **firehose programmer** for the exact device from official Xiaomi firmware (`.mbn` or `xbl.mbn`) — cannot be distributed in this doc
3. `edl --loader=prog_firehose.mbn printgpt`
4. `edl --loader=... r boot boot.img` — read; `edl w boot boot.img` — write
5. Restore GPT only from dumped backups — partition table mismatch = hard brick

## MediaTek BROM (Helio G-series Xiaomi ≤ Note 9 era)
```bash
mtk printgpt
mtk w boot boot.img --filename boot.img
```
A "DA" (Download Agent) from the ROM's firmware is needed — mtkclient ships generic loaders; official ones work more reliably.

## Samsung (Download mode)
```bash
heimdall detect
heimdall download-pit --output out.pit
heimdall flash --BOOT boot.img --SYSTEM system.img.pit   # example
```
or `heimdall-frontend` GUI — PIT mapping shown graphically.

## Safety order of operations
1. **Back up** first: `edl r` / `mtk r` boot, system, persist, modemst1, modemst2 (IMEI!), devinfo (unlock state)
2. Don't touch partitions you don't understand (`devinfo`, `frp`, `persist`)
3. `fastboot flash` is atomic per partition; EDL/VCOM write directly — wrong image = unbootable
4. Keep stock ROM zip handy for EDL recovery
