# Exp Task

更新日期：`2026-04-18 CST`

## 0. 任务定位

本任务用于驱动后续 agent 在 `trxcc/agentic-bbo` benchmark 中接入论文 *Efficient and Principled Scientific Discovery through Bayesian Optimization: A Tutorial* 的 HER 数据集，并完成最小 smoke demo。

本轮目标不是复现论文完整实验，而是先打通一条可维护的 dataset task 接入链路：

1. 获取或缓存 HER CSV。
2. 在 agentic-bbo 中新增 `her_demo` task。
3. 定义 HER 的 10 维连续搜索空间。
4. 使用随机森林 mock oracle 完成 `Task.evaluate()`。
5. 接入 task description。
6. 让 CLI 能运行 `her_demo`。
7. 跑 `random_search` 的 3-evaluation smoke demo。
8. 把执行结果记录到 `exp_result.md`。

## 1. 固定来源

### 1.1 论文

- 标题：
  - `Efficient and Principled Scientific Discovery through Bayesian Optimization: A Tutorial`
- 本地 PDF：
  - `D:\University\keyan\Benchmark\群聊文章\EFFICIENT AND PRINCIPLED SCIENTIFIC DISCOVERY THROUGH.pdf`
- 论文中的 HER case：
  - `5.1 Catalyst Design for Photocatalytic Water Splitting`

### 1.2 配套代码

- Source repo:
  - `https://github.com/zwyu-ai/BO-Tutorial-for-Sci`
- HER dataset:
  - `examples/HER/HER_virtual_data.csv`
- HER reference implementation:
  - `examples/HER/utils.py`

### 1.3 目标 benchmark

- Target repo:
  - `https://github.com/trxcc/agentic-bbo`
- 核心参考文件：
  - `bbo/core/task.py`
  - `bbo/core/trial.py`
  - `bbo/core/experimenter.py`
  - `bbo/tasks/registry.py`
  - `bbo/tasks/synthetic/base.py`
  - `bbo/run.py`

## 2. 明确范围

### 2.1 本轮只做

- HER / Photocatalytic Hydrogen Evolution Reaction。
- `her_demo` 一个 task。
- smoke demo。

### 2.2 本轮不做

- 不跑论文完整实验。
- 不跑 `200 evaluations x 16 seeds`。
- 不接入 HEA。
- 不接入 OER。
- 不接入 BH。
- 不接入 Molecule/QED。
- 不引入 RDKit / ZINC。
- 不改 agentic-bbo 的 algorithm 设计。
- 不改 `bbo/core/`，除非现有接口无法表达 HER task。

## 3. HER 数据集定义

HER CSV 固定包含 10 个输入特征和 1 个目标列。

### 3.1 搜索空间

所有输入变量均为连续变量，范围固定为 `[0, 5]`：

| 参数名 | 类型 | low | high |
|---|---:|---:|---:|
| `AcidRed871_0gL` | float | 0 | 5 |
| `L-Cysteine-50gL` | float | 0 | 5 |
| `MethyleneB_250mgL` | float | 0 | 5 |
| `NaCl-3M` | float | 0 | 5 |
| `NaOH-1M` | float | 0 | 5 |
| `P10-MIX1` | float | 0 | 5 |
| `PVP-1wt` | float | 0 | 5 |
| `RhodamineB1_0gL` | float | 0 | 5 |
| `SDS-1wt` | float | 0 | 5 |
| `Sodiumsilicate-1wt` | float | 0 | 5 |

### 3.2 目标列

- 原始目标列：
  - `Target`
- 参考代码将 HER maximization 转换为 minimization regret：
  - `regret = Target.max() - Target`
- agentic-bbo 中的 primary objective 固定为：
  - name: `regret`
  - direction: `minimize`

### 3.3 Mock oracle

参考 `examples/HER/utils.py`：

1. 读取 CSV。
2. 将 `Target` 替换为 `Target.max() - Target`。
3. 输入特征为除 `Target` 外的 10 个变量。
4. 用 `RandomForestRegressor(n_estimators=100, random_state=<seed>)` 拟合 mock oracle。
5. `Task.evaluate()` 对输入 config 预测 regret。

推荐把 oracle 训练逻辑封装在 HER task family 内，而不是放入 `bbo/core/`。

## 4. agentic-bbo 改动要求

### 4.1 推荐新增结构

优先采用以下结构，除非目标仓库已有更合适的本地模式：

```text
bbo/tasks/scientific/
  __init__.py
  her.py
```

其中 `her.py` 至少提供：

- `HER_FEATURES`
- `HER_DATASET_FILENAME`
- `HER_DEFINITION` 或等价 task definition
- `HerTask` 或等价 `Task` subclass
- `create_her_task(...)`

### 4.2 TaskSpec 要求

`her_demo` 的 `TaskSpec` 必须包含：

- `name="her_demo"`
- 10 维 `SearchSpace`
- `ObjectiveSpec("regret", ObjectiveDirection.MINIMIZE)`
- `max_evaluations` 默认可设为 `40` 或更小，但 CLI 的 `--max-evaluations 3` 必须能覆盖
- `description_ref=TaskDescriptionRef.from_directory("her_demo", <description_dir>)`
- metadata 至少包含：
  - `display_name`
  - `source_paper`
  - `source_repo`
  - `dataset_name`
  - `dimension`
  - `oracle_type`

### 4.3 数据资产策略

允许两种实现方式，优先采用更适合目标仓库的方式：

1. 小数据直接纳入包内，例如：
   - `bbo/tasks/scientific/data/HER_virtual_data.csv`
2. 首次运行从 source repo raw URL 下载到 cache。

若采用包内数据：

- 需要检查 `pyproject.toml` 的 package-data 是否包含 CSV。
- 如果未包含，需要补充 package data。

若采用下载/cache：

- 必须记录 raw URL。
- 必须有清晰错误信息。
- 不允许 silent fallback 到随机生成数据。

### 4.4 CLI 接入

当前 agentic-bbo 的 `bbo.run` 如果只从 `SYNTHETIC_PROBLEM_REGISTRY` 读取任务，则必须泛化 task factory：

- `--task her_demo` 必须合法。
- `run_single_experiment(... task_name="her_demo" ...)` 必须能创建 HER task。
- `generate_visualizations()` 不得强依赖 `SyntheticFunctionTask` 或 `surface_grid()`。
- HER smoke 不要求 landscape plot，只要求 trace/distribution 如可用。

## 5. Task description 要求

新增目录：

```text
bbo/task_descriptions/her_demo/
```

至少包含：

```text
background.md
goal.md
constraints.md
prior_knowledge.md
evaluation.md
environment.md
```

各文件内容要求：

- `background.md`：说明 HER 是 photocatalytic water splitting 中的 catalyst composition optimization。
- `goal.md`：说明目标是最小化 `Target.max() - predicted Target`，等价于寻找高 HER。
- `constraints.md`：说明 10 个输入变量均在 `[0, 5]`；本轮只用 mock oracle，不做真实实验。
- `prior_knowledge.md`：概述 10 种材料/添加剂及其可能作用，不做超出论文/教程的强结论。
- `evaluation.md`：说明随机森林 mock oracle、regret objective、smoke demo 预算。
- `environment.md`：说明需要 Python、numpy、pandas、scikit-learn，以及 agentic-bbo 基础依赖。

## 6. Smoke test

后续执行 agent 至少运行：

```bash
uv run python -m compileall -q bbo examples tests
uv run pytest
uv run python -m bbo.run --algorithm random_search --task her_demo --max-evaluations 3 --results-root artifacts/her_demo_smoke
```

### 6.1 Smoke 通过标准

- HER CSV 可加载。
- 10 个输入字段完整。
- `Target` 列存在且可转换为 regret。
- mock oracle 可训练。
- `her_demo.sanity_check()` 通过。
- 3 次 random search evaluation 成功完成。
- JSONL history 写出。
- summary 写出。
- summary 包含 `best_primary_objective`。
- 产物路径写入 `exp_result.md`。

### 6.2 Smoke 失败处理

如果 smoke 失败：

1. 不允许跳过失败直接写 completed。
2. 必须在 `exp_result.md` 记录：
   - command
   - error summary
   - suspected cause
   - next action
3. 若问题是依赖缺失，记录需要安装的依赖。
4. 若问题是 agentic-bbo CLI 仍只支持 synthetic task，优先修 CLI factory。

## 7. 结果产物

后续执行完成后，至少应记录：

- agentic-bbo repo path
- git commit/ref
- HER CSV source path
- HER row count
- HER columns
- Target min / max / mean / std
- modified files
- smoke command
- smoke status
- JSONL path
- summary path
- plot paths

推荐产物位置：

- workflow 本地记录：
  - `summary/`
  - `logs/`
  - `outputs/`
- benchmark 运行产物：
  - `artifacts/her_demo_smoke/`

## 8. 执行顺序

1. 确认 agentic-bbo 仓库位置；若本地没有，获取 `https://github.com/trxcc/agentic-bbo`。
2. 阅读目标仓库 README、core developer guide、现有 synthetic task。
3. 获取 HER CSV 与参考 `examples/HER/utils.py`。
4. 新增 HER task implementation。
5. 新增 `her_demo` task descriptions。
6. 注册 `her_demo`。
7. 泛化 CLI 使 `--task her_demo` 可运行。
8. 如需，补充 `scikit-learn` 依赖。
9. 运行 compileall。
10. 运行 pytest。
11. 运行 HER smoke。
12. 更新 `exp_result.md`。
13. 如有必要，在 `summary/` 写一份简短执行总结。

## 9. Definition of Done

本任务完成必须满足：

1. `her_demo` 已接入 agentic-bbo。
2. HER 数据加载与 mock oracle 可复现。
3. CLI smoke command 成功。
4. JSONL、summary、plots 路径已记录。
5. `exp_result.md` 已从 `not_started` 更新为实际状态。

## 10. 禁止事项

- 不要伪造 smoke 结果。
- 不要用随机数据代替 HER CSV。
- 不要把 `Target` 当成 minimization objective 直接用；必须按参考逻辑转换为 regret。
- 不要把 Molecule/QED 依赖带入本轮。
- 不要将本轮 smoke 结果表述为论文 benchmark 复现。
