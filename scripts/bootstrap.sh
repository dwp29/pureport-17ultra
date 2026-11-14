#!/usr/bin/env bash
# Bootstrap Stormbreaker kernel (miatoll) build di mesin baru / sesi baru.
# Menyiapkan: host deps (apt), kernel source, clang 11 pinned, gcc 4.9 prebuilt, AnyKernel3.
# Usage: bash scripts/bootstrap.sh [WORK_DIR]   (default: $HOME/ROM-Tools)
set -euo pipefail
WORK="${1:-$HOME/ROM-Tools}"
mkdir -p "$WORK"; cd "$WORK"

echo "==> Host dependencies"
if command -v apt-get >/dev/null 2>&1; then
  SUDO=""; [ "$(id -u)" -ne 0 ] && SUDO="sudo"
  $SUDO apt-get update
  $SUDO apt-get install -y git zip make bison flex bc rsync cpio \
    libelf-dev libncurses-dev python3 ccache dwarves \
    openjdk-17-jdk-headless aarch64-linux-gnu-gcc || \
  echo "WARN: apt install failed; pastikan dependensi sudah ada (lihat docs/DEV-TOOLKIT.md)"
fi

echo "==> Kernel source (crDroid branch 16.0)"
if [ ! -d kernel_joyeuse ]; then
  git clone --depth=1 -b 16.0 \
    https://github.com/crdroidandroid/android_kernel_xiaomi_sm6250.git kernel_joyeuse
fi
cd kernel_joyeuse

echo "==> Pinned clang 11 (r6443078) + gcc 4.9 prebuilts"
[ -a clang ] || git clone --depth=1 https://github.com/crdroidandroid/android_prebuilts_clang_host_linux-x86_clang-6443078 clang
[ -a gcc64 ] || git clone --depth=1 https://github.com/LineageOS/android_prebuilts_gcc_linux-x86_aarch64_aarch64-linux-android-4.9 gcc64
[ -a gcc32 ] || git clone --depth=1 https://github.com/LineageOS/android_prebuilts_gcc_linux-x86_arm_arm-linux-androideabi-4.9 gcc32

echo "==> AnyKernel3"
[ -a AnyKernel ] || git clone --depth=1 -b r5x https://github.com/Amritorock/AnyKernel3 AnyKernel

echo "==> Build (Image.gz -> flashable AnyKernel zip)"
./build.sh

echo "DONE: hasil ada di kernel_joyeuse/out/arch/arm64/boot/Image* dan kernel_joyeuse/AnyKernel/*.zip"
