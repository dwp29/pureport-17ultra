# 显示模式与时序生效验证 / Display Mode and Timing Validation

显示超频或新增模式不是“把模式加进列表”。必须沿完整路径逐层证明数据没有丢失：
Display overclocking or adding modes is not "append an entry to the mode list". Prove that each
layer of the path preserves the intended change:

```text
panel source mode
  -> DRM mode list
  -> user-space mode selection
  -> kernel mode-set / commit
  -> vendor panel params
  -> DSI command, clock and lane rate
  -> physical panel behavior
```

任何一层成功都不能代替最终效果。
Success at one layer never substitutes for the final effect.

## 1. 固化原厂基线 / Capture the stock baseline

修改前保存：
Before modifying, record:

- 面板名、分辨率、物理尺寸、连接类型。
  Panel name, resolution, physical size, and connection type.
- 原厂全部模式的 mode ID、pixel clock、H/V active、H/V porches、sync width、vrefresh。
  Every stock mode's ID, pixel clock, H/V active, H/V porches, sync widths, and vrefresh.
- 每种模式实际使用的 panel params、DSI data rate、lane count 和动态刷新参数。
  The panel params, DSI data rate, lane count, and dynamic-refresh values actually used per mode.
- 切换前、切换中、切换后的厂商日志。
  Vendor logs before, during, and after switching.

每个自定义模式必须有独立的参数存储，不能复用会被其他模式同时读写的临时 buffer。
Each custom mode needs independent backing storage. Do not share a mutable temporary buffer that
another mode can read or overwrite concurrently.

## 2. 四个不同状态 / Four distinct states

报告结果时必须区分：
Report these states separately:

| 状态 / State | 证据 / Evidence |
|---|---|
| 枚举可见 / enumerated | DRM mode list、`dumpsys display` 或 UI 中出现目标模式 / mode appears in DRM list, `dumpsys display`, or UI |
| 选择到达内核 / selection reached kernel | mode-set / atomic commit hook 收到正确 mode ID / hook receives the intended mode ID |
| 时序已编程 / timing programmed | vendor params、porch、clock、data rate、DSI 命令确实更新 / params, porches, clock, data rate, and DSI commands updated |
| 面板实际生效 / panel effective | 实际刷新率、帧间隔、持续运行稳定，无 timeout/underrun/花屏/黑屏 / actual refresh, frame cadence, sustained stability, no timeout/underrun/corruption/blanking |

只看到第一个状态，绝不能汇报“生效”。
Seeing only the first state must never be reported as "working".

## 3. 常见失败形态 / Common failure shapes

| 现象 / Symptom | 优先检查 / Check first |
|---|---|
| UI 有新模式，实际仍为旧刷新率 / new mode visible, actual refresh unchanged | 只拦截了枚举路径；mode-set/params/commit 路径未覆盖 / only enumeration is hooked; mode-set, params, or commit path is not |
| 切换命令成功但参数未变化 / switch returns success, params unchanged | 厂商前置检查 early-return、mode ID 映射错误、参数指针仍是原模式 / vendor guard, wrong mode-ID mapping, params still point to stock mode |
| 中间档位正常，最高或最低档异常 / middle rates work; extreme or stock mode corrupts | porch、VFP/HFP、data rate 边界或原厂恢复路径错误 / porch, VFP/HFP, data-rate limit, or stock-restore path |
| 切换后过几秒恢复 / works briefly then reverts | 后续 commit、frame timing update 或 userspace policy 覆盖了设置 / a later commit, frame-timing update, or user-space policy overwrites it |
| 休眠唤醒后失效或花屏 / breaks after suspend/resume | 只在启动枚举时应用，没有处理 resume/re-enumeration / only applied during boot enumeration; resume or re-enumeration is unhandled |
| 同一模式偶发命中错误时序 / same mode intermittently uses wrong timing | mode ID 或参数存储不唯一，存在竞争/复用 / non-unique mode ID or shared mutable params |

## 4. 自定义模式不变量 / Custom-mode invariants

- mode ID、mode name 和参数索引必须稳定且唯一。
  Mode ID, mode name, and parameter index must be stable and unique.
- 自定义模式必须能被后续路径重新找到；不能只在枚举回调里临时存在。
  Later paths must resolve the custom mode again; it cannot exist only inside the enumeration callback.
- 所有读取 panel params 的厂商入口必须返回同一个自定义模式对应的数据。
  Every vendor entry that returns panel params must return data for the same custom mode.
- 切换失败时保持或恢复原厂模式，不能留下半套参数。
  On switch failure, remain on or restore the exact stock mode; never leave half-applied params.
- 原厂模式由原厂数据恢复，不要重新合成一个“看起来相同”的模式。
  Restore a stock mode from its original vendor data. Do not synthesize a lookalike mode.
- 不在未知 DDIC/DCS 上试命令。先确认命令、参数长度和返回语义。
  Do not probe unknown DDIC/DCS commands. Confirm the command, payload length, and response first.

## 5. 验收命令 / Verification commands

具体节点因平台而异；优先使用厂商 debugfs 和模块 `status`，其次才是 UI。
Nodes vary by platform. Prefer vendor debugfs and the module's `status`; UI is the last resort.

```sh
# userspace 当前模式 / current user-space mode
adb shell dumpsys display | grep -Ei 'mode|refresh|fps' | head -80

# 模块状态：至少包含 requested / installed / active / actual
adb shell su -c 'cat /sys/module/<module>/parameters/status'

# 厂商显示日志，tag 按目标平台替换
adb shell su -c "dmesg | grep -Ei '<vendor-display-tags>' | tail -160"
```

模块的 `status` 至少应区分：
The module `status` should distinguish at least:

```text
loaded=1 installed=1 requested=165 active=165 actual=165 result=ok
loaded=1 installed=1 requested=165 active=144 actual=144 result=no_effect
```

不要把 `requested` 复制成 `actual`。`actual` 必须来自驱动状态、commit 结果或可验证的
帧时序测点。
Do not copy `requested` into `actual`. `actual` must come from driver state, commit results, or a
verifiable frame-cadence measurement.

## 6. 持续稳定性和边界测试 / Sustained stability and boundaries

每个档位至少验证：
For every rate, verify:

1. 冷启动后首次切换。
   First switch after cold boot.
2. 在该模式持续运行一段时间，不只看切换瞬间。
   Sustained operation, not only the instant after switching.
3. 切回原厂模式。
   Switch back to the exact stock mode.
4. 息屏/亮屏。
   Screen off/on.
5. 休眠/唤醒。
   Suspend/resume.
6. 旋转、分辨率变化或 HDR/色彩模式变化（若目标平台支持）。
   Rotation, resolution changes, or HDR/color-mode changes when supported.
7. 重复切换全部档位至少一轮。
   Cycle through every mode at least once.

只验证中间档位不能证明极值档安全；只验证极值档也不能证明原厂恢复路径安全。
Testing only middle rates cannot prove the extremes are safe. Testing only the extremes cannot
prove stock restoration is safe.

## 7. 日志开关 / Logging switch

- 默认：加载结果、依赖、panel 匹配、模式切换结果、`requested/active/actual`、错误。
  Default: load result, dependencies, panel match, switch result, requested/active/actual, errors.
- 详细：porch、clock、data rate、mode ID、参数地址、厂商命令。只在测试时开启。
  Verbose: porches, clock, data rate, mode ID, parameter addresses, vendor commands. Test builds only.
- 高频回调使用限频日志；状态变化用一次性日志。
  Rate-limit high-frequency callbacks; log state transitions once.
- `status` 是首要排障接口，不能要求每次都抓完整 dmesg。
  `status` is the primary diagnostic interface; not every report should require a full dmesg.

## 8. 完成标准 / Completion criteria

- 枚举、内核选择、时序编程、实际刷新率四层证据齐全。
  Evidence exists for enumeration, kernel selection, timing programming, and actual refresh.
- 每个档位和原厂恢复都通过持续运行测试。
  Every rate and stock restoration passes sustained testing.
- 失败切换不会留下半套参数或错误状态。
  A failed switch leaves no half-applied params or incorrect state.
- 输出中同时记录 KO SHA-256 和实际测试档位。
  The report records both the KO SHA-256 and the rates actually tested.
