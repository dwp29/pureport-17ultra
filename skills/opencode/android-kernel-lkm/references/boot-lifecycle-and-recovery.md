# 加载时机、启动保护与恢复 / Load Timing, Boot Guards and Recovery

模块能 `insmod`、参数节点能读，不代表它在正确的启动阶段加载。需要早于 Android
用户空间初始化生效的 hook，如果放到 `service.sh`，通常已经错过目标初始化路径。
A module that can `insmod` is not necessarily loaded at the right boot stage. A hook that must
exist before Android user-space initialization will usually miss its target if loaded from
`service.sh`.

## 1. 先确定最早安全加载点 / Find the earliest safe load point

按目标数据流，不按脚本名字选阶段：
Choose by dependency and consumer timing, not by script name:

| 条件 / Condition | 优先阶段 / Preferred stage |
|---|---|
| 目标消费者在 Android 启动早期读取状态、建表或枚举对象 / the consumer reads state, builds tables, or enumerates objects during Android early boot | `post-fs-data.sh` |
| 目标驱动已经在内核或 ramdisk 中加载，只等用户空间服务 / the driver is already loaded; only a later user-space service is involved | `service.sh` |
| 依赖模块在启动后期才出现 / required modules appear later | `service.sh`，有明确上限的等待 / bounded wait |
| 同一模块既需要早期安装又需要后期确认 / early installation plus late confirmation | 早期只加载一次，`service.sh` 只验证和收尾 / load once early; verify in `service.sh` |

判断证据：
Evidence:

1. 从日志确认消费者何时首次读取目标状态。
   Confirm from logs when the consumer first reads the target state.
2. 在 `/sys/module/<dependency>` 确认依赖已经存在。
   Confirm the dependency exists under `/sys/module/<dependency>`.
3. 比较 `post-fs-data`、`service` 两种加载点的行为差异，而不是反复猜测 hook。
   Compare the two load stages instead of repeatedly guessing hook points.

`post-fs-data.sh` 会阻塞启动流程。这里不要放长时间等待、无限重试或高成本探测。
`post-fs-data.sh` blocks the boot sequence. Do not put long waits, unbounded retries, or expensive
probing there.

## 2. 安装门禁和启动门禁要同时存在 / Gate at both install and boot

安装时检查只能阻止明显错误包；系统升级、回滚或恢复镜像仍可能让旧模块留在数据分区，
所以每次启动必须重新检查。
An install-time check catches an obviously wrong package. OTA upgrades, rollbacks, and restored
images can still leave an old module in the data partition, so every boot must check again.

```sh
EXPECTED_KERNEL_RELEASE="<exact release used to build>"
CURRENT_KERNEL_RELEASE="$(uname -r 2>/dev/null)"

if [ "$CURRENT_KERNEL_RELEASE" != "$EXPECTED_KERNEL_RELEASE" ]; then
    log_message "RESULT=FAILED stage=kernel_check actual=${CURRENT_KERNEL_RELEASE:-unknown}"
    self_disable
    exit 0
fi
```

`customize.sh` 中也做同样比较，并直接 `abort`。不要把 `/proc/version` 的展示文本当作
release；比较 `uname -r` 或已加载 vendor KO 的 vermagic 真值。
Apply the same comparison in `customize.sh` and `abort` on mismatch. Do not use the display text
from `/proc/version` as the release; compare `uname -r` or the vermagic truth from a loaded vendor
KO.

## 3. 启动事务标记 / Boot transaction marker

在 `insmod` 前持久化一个带 `boot_id` 的 guard。只有同一个 boot 里，模块已驻留并完成
`service.sh` 验收后，才删除 guard。下一次启动看到旧 `boot_id` 的 guard，说明上一轮没有
完整走完，直接自禁用，避免连环重启。
Persist a guard containing the current `boot_id` before `insmod`. Clear it only in the same boot,
after the module is resident and `service.sh` verification passes. A guard from a different boot
means the previous transaction never completed; self-disable instead of rebooting forever.

```sh
BOOT_ID="$(cat /proc/sys/kernel/random/boot_id 2>/dev/null)"
LOAD_GUARD="$MODDIR/load_in_progress"
DISABLE_MARKER="$MODDIR/disable"

self_disable() {
    touch "$DISABLE_MARKER"
    chmod 0644 "$DISABLE_MARKER" 2>/dev/null
    sync
}

if [ -f "$LOAD_GUARD" ]; then
    GUARD_BOOT_ID="$(sed -n 's/^boot_id=//p' "$LOAD_GUARD" 2>/dev/null | head -n 1)"
    if [ -n "$GUARD_BOOT_ID" ] && [ "$GUARD_BOOT_ID" != "$BOOT_ID" ]; then
        # collect previous-boot evidence here
        self_disable
        exit 0
    fi

    # Same-boot duplicate execution or an unfinished transaction: do not loop.
    self_disable
    exit 0
fi

{
    echo "boot_id=${BOOT_ID:-unavailable}"
    echo "stage=post-fs-data"
    echo "started=$(date '+%Y-%m-%d %H:%M:%S')"
} > "$LOAD_GUARD"
sync
```

单次加载失败就自禁用，不要在同一 boot 中无限重试。加载成功但状态未达到预期，
也应自禁用并保留状态输出。
Self-disable after a single load failure; do not retry forever in the same boot. If the module
loads but its required state is not reached, self-disable and preserve the status output.

`service.sh` 成功收尾时：
On successful service-stage completion:

```sh
GUARD_BOOT_ID="$(sed -n 's/^boot_id=//p' "$LOAD_GUARD" 2>/dev/null | head -n 1)"
if [ "$GUARD_BOOT_ID" != "$BOOT_ID" ]; then
    self_disable
    exit 0
fi

rm -f "$LOAD_GUARD"
sync
```

## 4. Guard 必须真的可写且可持久化 / The guard must persist

常见错误是 guard 写在只读模块镜像、临时目录或错误的 `MODDIR`：
A common failure is writing the guard into the read-only module image, `/tmp`, or the wrong
`MODDIR`:

- `MODDIR=${0%/*}` 后先打印并确认路径。
  Resolve and log `MODDIR=${0%/*}` before relying on it.
- 写文件后检查退出码，写入后 `sync`。
  Check the write result and `sync` after writing.
- 下次启动必须能读到上次写入的内容，否则保护等于不存在。
  The next boot must be able to read what was written; otherwise the guard does not exist.

不要依赖模块管理器一定自动禁用故障模块。管理器策略、执行顺序和版本行为并不相同。
Do not rely on the module manager to automatically disable a failing module. Policies, ordering,
and behavior vary by manager and version.

## 5. 日志策略 / Logging policy

默认只输出状态变化和错误，详细路径日志必须由参数或文件开关启用：
By default, log only state transitions and errors. Gate detailed path logging behind a module
parameter or marker file:

- 基础：版本、KO SHA-256、内核匹配、依赖就绪、加载结果、`installed/active` 状态。
  Basic: version, KO SHA-256, kernel match, dependencies, load result, `installed/active` state.
- 详细：完整时序、指针、模式表、厂商命令、切换路径。
  Verbose: full timings, pointers, mode tables, vendor commands, and switch paths.
- 热路径使用 `pr_info_ratelimited()` 或等价限频；错误日志不受 verbose 开关影响。
  Use `pr_info_ratelimited()` or equivalent in hot paths; errors must not depend on verbose mode.
- 日志轮转只保留当前和上一轮，避免占满模块目录。
  Keep only current and previous boot logs so the module directory cannot grow without bound.

## 6. `invalid module format` 的固定排查顺序 / Fixed triage for `invalid module format`

不要先改源码。先保存 `insmod` stderr 和紧随其后的内核日志：
Do not edit the source first. Preserve the `insmod` stderr and the immediately following kernel log:

```sh
INSMOD_OUTPUT="$(insmod "$KO" 2>&1)"
INSMOD_RC=$?
echo "$INSMOD_OUTPUT"
dmesg | tail -n 80
```

然后依次核对：
Then check in order:

1. 设备当前 release 是否与构建基线一致。
   Is the current device release identical to the build baseline?
2. 候选 KO 和已加载 vendor KO 的 vermagic 是否逐字节一致。
   Is the candidate vermagic byte-for-byte identical to a loaded vendor KO?
3. 是否误用了另一系统版本的头文件、CRC 或模块链接脚本。
   Were headers, CRCs, or the module linker script taken from another system version?
4. 内核日志是否明确给出 `version magic ... should be ...`。有这一行时以它为准。
   Does dmesg contain `version magic ... should be ...`? Use that exact line when present.
5. 以上都匹配仍报格式错误时，再检查 ELF class、重定位、section 布局和 KCFI/ABI section。
   If all match, inspect ELF class, relocations, section layout, and KCFI/ABI sections.

## 7. 交付前检查 / Pre-delivery checklist

- 消费者第一次读取目标状态时，模块已经驻留。
  The module is resident before the consumer first snapshots the target state.
- 安装和每次启动都检查内核 release。
  Kernel release is checked both at install and every boot.
- `load_in_progress` 在 `insmod` 前落盘，验收成功后才删除。
  `load_in_progress` is durable before `insmod` and removed only after verification.
- 上一轮中断会在下一轮自禁用，并留下可读证据。
  An interrupted transaction self-disables next boot and leaves readable evidence.
- 失败路径只加载一次，不形成重启循环。
  Failure paths load once and cannot form a reboot loop.
- 基础日志足以判断 loaded、installed、active、failed 四个状态。
  Basic logs can distinguish loaded, installed, active, and failed.
