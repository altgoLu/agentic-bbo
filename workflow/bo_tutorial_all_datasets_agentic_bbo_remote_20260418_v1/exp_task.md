# 实验任务单

更新时间：2026-04-18 CST

## 0. 任务定位

本任务用于驱动后续执行 agent，将论文 *Efficient and Principled Scientific Discovery through Bayesian Optimization: A Tutorial* 配套仓库中的全部数据集接入远程 `trxcc/agentic-bbo` benchmark。

本 workflow 是 smoke 级别的 benchmark 接入任务，不是论文完整复现实验。

## 1. 固定来源

### 1.1 论文

- 标题：
  - `Efficient and Principled Scientific Discovery through Bayesian Optimization: A Tutorial`
- 本地 PDF：
  - `D:\University\keyan\Benchmark\群聊文章\EFFICIENT AND PRINCIPLED SCIENTIFIC DISCOVERY THROUGH.pdf`

### 1.2 配套代码

- Source repo：
  - `https://github.com/zwyu-ai/BO-Tutorial-for-Sci`
- 必需参考路径：
  - `examples/HER/HER_virtual_data.csv`
  - `examples/HER/utils.py`
  - `examples/HEA/data/oracle_data.xlsx`
  - `examples/HEA/utils.py`
  - `examples/OER/OER.csv`
  - `examples/OER/OER_clean.csv`
  - `examples/OER/utils.py`
  - `examples/BH/BH_dataset.csv`
  - `examples/BH/utils.py`
  - `examples/Molecule/zinc.txt.gz`
  - `examples/Molecule/utils.py`

### 1.3 目标 benchmark

- Target repo：
  - `https://github.com/trxcc/agentic-bbo`
- 开始实现前必须在 `exp_result.md` 中补全：
  - remote host
  - remote repo path
  - remote branch
  - Python version
  - `uv` version 或等价环境管理方式
  - source repo ref
  - `agentic-bbo` base commit/ref
  - dataset cache root
  - artifacts root

## 2. 范围

### 2.1 必须完成

- 在 `agentic-bbo` 中新增 scientific discovery task family。
- 新增并注册五个 task：
  - `her_demo`
  - `hea_demo`
  - `oer_demo`
  - `bh_demo`
  - `molecule_qed_demo`
- 新增数据资产下载/cache 或等价手动放置契约。
- 新增 BO tutorial 相关 optional dependencies。
- 为五个 task 新增 task descriptions。
- 泛化 task 创建逻辑，使 `python -m bbo.run --task <scientific_task>` 能运行。
- 对每个 task 跑 3-evaluation `random_search` smoke。
- 将所有命令、输出、路径、commit 和 blocker 写入 `exp_result.md`。

### 2.2 明确不做

- 不跑论文完整实验。
- 不跑 `200 evaluations x 16 seeds`。
- 不比较 HEBO、BO-LCB、Random Search 或其他 baseline。
- 不声称完成论文 benchmark 复现。
- 不伪造缺失数据。
- 不 silent fallback 到随机数据。
- 不用假的函数替代 RDKit QED。
- 除非现有接口无法表达这些 task，否则不修改 `bbo/core/`。

## 3. 实现要求

### 3.1 推荐新增文件

新增：

```text
bbo/tasks/scientific/
  __init__.py
  registry.py
  data_assets.py
  tabular_oracles.py
  her.py
  hea.py
  oer.py
  bh.py
  molecule.py
```

`data_assets.py` 负责：

- source repo URL/ref 处理
- 原始文件下载或手动路径解析
- cache root 解析
- sha256 计算
- 数据集存在性检查
- 数据集 metadata 摘要

`tabular_oracles.py` 负责共享工具：

- `RandomForestRegressor` 构造
- one-hot 列对齐
- 目标列统计
- pandas / sklearn 缺失时的清晰错误信息

### 3.2 Registry 与 CLI

修改 `bbo/tasks/registry.py`：

- 新增 `TASK_REGISTRY`。
- 新增 `create_task(task_name, max_evaluations=None, seed=0, **kwargs)`。
- 保留 `create_demo_task`，兼容 synthetic demo。
- 在 `TASK_FAMILIES` 中新增 `scientific` family。

修改 `bbo/run.py`：

- `--task` choices 必须来自全部注册 task，而不是只来自 synthetic task。
- `run_single_experiment()` 必须调用 `create_task()`。
- `generate_visualizations()` 必须接受通用 `Task`。
- 只有 task 支持 numeric 2D surface 时才生成 landscape plot。scientific task 只要求 trace/distribution plot。
- `pycma` 可以继续只支持 numeric search space。带 categorical 的 scientific task smoke 固定使用 `random_search`。

### 3.3 依赖接入

新增 optional extras 或等价依赖机制：

- `bo-tutorial`
- `bo-tutorial-full`

以 `dependency_manifest.md` 为依赖来源。

Smoke 必须使用：

```bash
uv sync --extra dev --extra bo-tutorial
```

### 3.4 Task descriptions

每个 task 新增：

```text
bbo/task_descriptions/<task_name>/
  background.md
  goal.md
  constraints.md
  prior_knowledge.md
  evaluation.md
  environment.md
```

每个文件内容要求简洁且与 task 对应：

- `background.md`：科学场景和数据来源。
- `goal.md`：primary objective 与优化方向。
- `constraints.md`：搜索空间和 smoke 限制。
- `prior_knowledge.md`：只写论文和配套代码支持的信息。
- `evaluation.md`：oracle 和 objective 转换。
- `environment.md`：optional extra 和 dataset cache 说明。

## 4. Task 语义

以 `dataset_manifest.md` 为精确定义。

摘要如下：

- `her_demo`：10D 连续 `[0, 5]`，HER `Target.max() - predicted_Target`，最小化 regret。
- `hea_demo`：4D 连续 `[0, 1]`，映射为 5 金属组成，最小化 target regret。
- `oer_demo`：categorical/numeric 混合 OER 设计，最小化预测 overpotential。
- `bh_demo`：BH 选中特征组成的连续搜索空间，最小化转换后的 yield regret。
- `molecule_qed_demo`：SMILES categorical 搜索空间，最小化 `1 - QED`。

## 5. 必跑 smoke 命令

实现完成后，在远程 benchmark 上运行：

```bash
uv sync --extra dev --extra bo-tutorial
uv run python -m compileall -q bbo tests
uv run pytest
uv run python -m bbo.run --algorithm random_search --task her_demo --max-evaluations 3 --results-root artifacts/bo_tutorial_all_smoke
uv run python -m bbo.run --algorithm random_search --task hea_demo --max-evaluations 3 --results-root artifacts/bo_tutorial_all_smoke
uv run python -m bbo.run --algorithm random_search --task oer_demo --max-evaluations 3 --results-root artifacts/bo_tutorial_all_smoke
uv run python -m bbo.run --algorithm random_search --task bh_demo --max-evaluations 3 --results-root artifacts/bo_tutorial_all_smoke
uv run python -m bbo.run --algorithm random_search --task molecule_qed_demo --max-evaluations 3 --results-root artifacts/bo_tutorial_all_smoke
```

## 6. 验收标准

- 五个源数据集均存在并通过校验。
- 五个 scientific task 均已注册。
- 五个 task description 均通过 `sanity_check()`。
- 五个 task 的 smoke run 均至少完成 3 次 evaluation。
- 每个 run 写出 `trials.jsonl`。
- 每个 run 写出 `summary.json`。
- 每个 `summary.json` 包含 `best_primary_objective`。
- plotter 支持时生成 trace/distribution plot。
- 所有 artifact path 均写入 `exp_result.md`。
- 失败的 smoke 不得隐藏；blocker 必须包含命令、错误摘要、原因判断和下一步。

## 7. 结果记录要求

至少将以下内容写入 `exp_result.md`：

- 远程 benchmark 信息
- git branch 和 commit
- source repo ref
- 依赖安装命令与状态
- 依赖导入检查状态
- 数据集校验表
- 修改文件列表
- 每个 task 的 smoke 表
- JSONL 路径
- summary 路径
- plot 路径
- blockers
- next steps

如果远程环境因为 RDKit 阻塞 Molecule/QED，必须将 `molecule_qed_demo` 标记为 blocked，同时继续 HER/HEA/OER/BH。不能用 fake objective 替代 Molecule/QED。
