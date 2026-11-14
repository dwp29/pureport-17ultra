---
name: joyeuse-kernel
description: Build the Redmi Note 9 Pro (joyeuse / miatoll family, SD 720G) Android kernel with the correct toolchain and defconfig
---

## Kernel: joyeuse (miatoll family, Snapdragon 720G = "atoll" platform)

- Source: `~/ROM-Tools/kernel_joyeuse` — crdroidandroid/android_kernel_xiaomi_sm6250, branch **16.0** (kernel 4.14.357-openela)
- Defconfig: `vendor/xiaomi/miatoll_defconfig` (verified working)
- **Toolchain: MUST use the pinned prebuilt** — `./build.sh` auto-downloads clang 11.0.1 (r6443078) + gcc 4.9 prebuilts. **System clang 18 FAILS** with `register 'sp' unsuitable for global register variables` and `value '65536' out of range for constraint 'I'`
- Quick rebuild: `cd ~/ROM-Tools/kernel_joyeuse && make O=out ARCH=arm64 LLVM=1 vendor/xiaomi/miatoll_defconfig && make O=out ARCH=arm64 LLVM=1 -j$(nproc)`
- Full build + AnyKernel3 zip: `cd ~/ROM-Tools/kernel_joyeuse && ./build.sh`
  → Output: `out/arch/arm64/boot/Image.gz` and `AnyKernel/Stormbreaker-miatoll-<date>.zip`
- Verify toolchain in: `out/include/generated/compile.h` (`LINUX_COMPILER`)
- Flash via TWRP / custom recovery (AnyKernel3 installer). Device: Redmi Note 9 Pro (joyeuse) / 9S (curtana) / Pro Max (excalibur) / Poco M2 Pro (gram) — all miatoll
- CI (untested): `.github/workflows/kernel.yml` in the repo
