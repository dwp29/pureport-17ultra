# Reproduce Android Kernel Builds

> 状态：**已激活**。于 2026-07-30 获得批准，后续只在用户自有或明确授权的设备上继续验证。

这个 Skill 用于在自有或明确授权设备上，建立 Android 内核、Root Provider 和 boot 镜像的证据化
流程。它既处理可精确锁定的源码构建，也把“官方通用 GKI LKM + 精确实时/OTA stock 镜像本地
重打包”作为正式路线，并处理厂商源码不完整时的停止条件与第三方产物审计。

## 快速使用

```text
使用 $reproduce-android-kernel-builds 为这个授权设备整理内核源码锁、baseline 和验证流程。
```

## 主要能力

- 从设备 codename、Factory Build 和 kernel release 定位正确源码路线。
- 将 Manifest 管理仓库、外部工具和第三方集成全部锁定到精确 commit。
- 将源码发现区分为完整、`candidate-source` 和 `incomplete-source`；只有完整锁定路线才使用
  `reproduced-source` 来源。
- 将官方 Provider GKI/LKM Release 作为不依赖“源码路线先失败”的一等路径。
- 把来源、集成方式和验证状态记录为三个正交证据维度。
- 强制先构建未修改 baseline，再验证 DTB、模块 ABI、vermagic 和产物格式。
- 源码确实不可复现时，可独立审计设备专用第三方产物，但只标记为 `qualified-prebuilt`。
- 通过 Provider Profile 支持 KernelSU Next、SukiSU Ultra、KernelSU 等不同实现和集成模式。
- 使用设备 Profile/Adapter 表达机型差异，避免在总流程写死 Pixel 或某个分区。
- 从准确的 stock 镜像重打包，并保留 hash、元数据和回滚镜像。
- 区分 Framework Android、Vendor Generation、Kernel Release 和 KMI；按 KMI 选择通用 LKM，并联合
  判断 modversions、签名、符号和 Provider Loader 行为。
- 解析 Header 并结合 Provider 行为决定 `boot`/`init_boot`/`vendor_boot`；不把仅修改的
  `init_boot` 直接当作 `fastboot boot` 的完整镜像。
- Provider 迁移时保护共享 `/data/adb` 与模块状态，将应用、staging、共享数据和模块清理分别授权。
- 将临时启动、永久刷写、清数据和重新锁定 BL 作为独立授权与停止关卡。
- 区分 Bootloader 临时启动路径失败与内核不兼容；在把非活动槽当作回滚方案前，先证明它能独立启动。
- 将“为了首次运行验证而刷写”的授权与“验证后保留为永久安装”的决定分开。

## 安全说明

读取信息、下载源码或完成编译，不代表已经授权执行解锁、清数据、临时启动、刷写或重新锁定
Bootloader。涉及真机变更时必须再次明确确认。

## 安装到 Codex

把完整的 `reproduce-android-kernel-builds/` 源码目录链接到用户 Skill 目录。链接目标的顶层必须
直接包含 `SKILL.md`；不要通过复制源码安装。

Windows PowerShell：

```powershell
$skillsRoot = Join-Path $HOME ".agents\skills"
$source = (Resolve-Path "<仓库根目录>\reproduce-android-kernel-builds").Path
$link = Join-Path $skillsRoot "reproduce-android-kernel-builds"
New-Item -ItemType Directory -Force -Path $skillsRoot | Out-Null
if (Test-Path -LiteralPath $link) { throw "目标已存在：$link" }
New-Item -ItemType Junction -Path $link -Target $source | Out-Null
```

macOS：

```bash
skills_root="$HOME/.agents/skills"
source_dir="$(cd "<仓库根目录>/reproduce-android-kernel-builds" && pwd)"
link_path="$skills_root/reproduce-android-kernel-builds"
mkdir -p "$skills_root"
if [ -e "$link_path" ] || [ -L "$link_path" ]; then echo "目标已存在：$link_path" >&2; exit 1; fi
ln -s "$source_dir" "$link_path"
```

Codex 通常会自动识别 Skill 变化；没有显示时重启 Codex。使用
`$reproduce-android-kernel-builds` 显式调用。需要跨 Agent 复用时，可在 CC Switch v3.13 或更高
版本中把 `~/.agents/skills` 设为共享来源，在 **Skills** 页面扫描/导入本地 Skill、启用目标 Agent
并同步。导入后重新检查设备授权、工具和安全关卡。

## 文件说明

- `SKILL.md`：完整工作流、安全边界和阶段关卡。
- `references/source-locks-and-profiles.md`：源码锁、设备 Profile 和 Adapter 设计。
- `references/validation-gates.md`：从设备识别到刷写和回滚的停止关卡。
- `references/vendor-source-and-prebuilt-fallback.md`：厂商源码缺口和第三方产物回退路线。
- `references/gki-lkm-ota-repack.md`：官方 Provider GKI/LKM、精确 OTA/实时 stock、KMI、分区、AVB、
  验证、迁移与清理规则。
- `scripts/verify_source_lock.py`：带并发上限地只读核对 Git HEAD、等价 Remote URL、工作树，以及可选的
  Commit 签名、Submodule 和 LFS Gate。
