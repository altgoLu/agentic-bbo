## Agentbbo 中的 knob（参数）surrogate 实验

本文介绍如何在本仓库中运行 **knob（数据库参数调优）surrogate 实验**。

这些任务是 **离线（offline）** benchmark：底层是序列化的 sklearn 模型（`*.joblib`）。它把归一化后的 knob 向量 \(x \in [0,1]^d\) 映射为预测指标（例如 throughput 或 latency）。**不需要真实数据库实例**。

### 你会用到的入口

- **Task family**: surrogate knob tasks under `bbo/tasks/surrogate/`
- **Examples**: `examples/run_knob_surrogate_demo.py`
- **统一运行入口**：`python -m bbo.run`（推荐）或 `bbo.run.run_single_experiment()`
- **输出位置**：默认写到 `runs/demo/` 下的 JSONL trial 日志（`trials.jsonl`）和汇总（`summary.json`）

### 前置条件

- **Python 环境**：推荐用仓库管理的环境（`uv`）
- **surrogate 依赖**：环境里必须有 `joblib`、`scikit-learn`
- **模型 checkpoint**：需要一个可用的 `*.joblib`（Sysbench-5 支持仓库自带的 placeholder）

用 `uv` 安装（推荐）：

```bash
uv sync --extra dev --extra surrogate
```

### 可用的 surrogate knob 任务

用 Python 列出 task id：

```bash
uv run python -c "from bbo.tasks import SURROGATE_TASK_IDS; print('\\n'.join(SURROGATE_TASK_IDS))"
```

常见 task id（示例）：

- `knob_surrogate_sysbench_5`
- `knob_surrogate_sysbench_all`
- `knob_surrogate_job_5`
- `knob_surrogate_job_all`
- `knob_surrogate_pg_5`
- `knob_surrogate_pg_20`

### 准备 `*.joblib` surrogate 文件

真实的大模型 checkpoint 不会提交到仓库。你有两种方式：

- **方式 A（推荐）**：把文件复制到 `bbo/tasks/surrogate/assets/`，并使用约定的文件名
- **方式 B**：设置环境变量，指向该 `.joblib` 的绝对路径

文件名 ↔ `task_id` ↔ 环境变量的对应关系见 `bbo/tasks/surrogate/assets/README.md`。

#### 示例：Sysbench 5-knob RF

复制到 assets（不需要环境变量）：

```bash
cp <KnobsTuningEA>/autotune/tuning_benchmark/surrogate/RF_SYSBENCH_5knob.joblib \
  bbo/tasks/surrogate/assets/RF_SYSBENCH_5knob.joblib
```

或用环境变量覆盖路径：

```bash
export AGENTIC_BBO_SYSBENCH5_SURROGATE=/absolute/path/to/RF_SYSBENCH_5knob.joblib
```

### 运行 knob 实验（推荐用 `bbo.run`）

跑 random-search baseline：

```bash
uv run python -m bbo.run \
  --task knob_surrogate_sysbench_5 \
  --algorithm random_search \
  --seed 1 \
  --max-evaluations 60
```

跑 CMA-ES（需要你环境里额外安装 `cma` / `pycma` 相关依赖）：

```bash
uv run python -m bbo.run \
  --task knob_surrogate_sysbench_5 \
  --algorithm pycma \
  --seed 1 \
  --max-evaluations 60 \
  --sigma-fraction 0.18 \
  --popsize 6
```

从命令行覆盖 joblib/knobs 路径（可选）：

```bash
uv run python -m bbo.run \
  --task knob_surrogate_sysbench_5 \
  --algorithm random_search \
  --seed 1 \
  --max-evaluations 60 \
  --surrogate-path /abs/path/to/RF_SYSBENCH_5knob.joblib \
  --knobs-json-path bbo/tasks/surrogate/assets/knobs_SYSBENCH_top5.json
```

### 运行示例脚本

`examples/run_knob_surrogate_demo.py` 本质上只是对 `run_single_experiment()` 的轻量封装：

```bash
uv run python examples/run_knob_surrogate_demo.py \
  --task knob_surrogate_sysbench_5 \
  --algorithm random_search \
  --seed 1 \
  --max-evaluations 60
```

### 输出：结果写到哪里

默认输出目录结构如下：

```text
runs/demo/<task>/<algorithm>/seed_<seed>/
  trials.jsonl
  summary.json
```

- **`trials.jsonl`**：每次评估（trial）一行 JSON 记录
- **`summary.json`**：聚合后的最优值、incumbents、以及 logger 汇总

### 常见问题排查

- **`joblib.load` 报 `EOF` / `reading array data`**
  - 通常是 `.joblib` 文件不完整（复制了一半、或 Git LFS 没拉全）。请重新拷贝完整的 `*.joblib`。
- **`ModuleNotFoundError: joblib` 或 `sklearn`**
  - 安装 surrogate 依赖：`uv sync --extra surrogate`
- **使用 `--algorithm pycma` 时提示 `ModuleNotFoundError: cma`**
  - 你需要先在环境里安装 `cma` 依赖，然后再使用 `pycma`。

