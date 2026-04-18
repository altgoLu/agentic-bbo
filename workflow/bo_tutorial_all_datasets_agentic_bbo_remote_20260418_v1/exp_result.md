# 实验结果记录

更新时间：2026-04-18 CST

## 0. 状态

- 总体状态：`not_started`
- 当前阶段：workflow 已准备，远程 benchmark 接入尚未开始
- 执行 agent：TBD
- 最后更新：本地 workflow 起草 agent

## 1. 远程 Benchmark 信息

开始实现前必须补全：

| 字段 | 值 |
|---|---|
| remote host | TBD |
| remote repo path | TBD |
| remote branch | TBD |
| remote Python version | TBD |
| remote uv version | TBD |
| agentic-bbo base commit/ref | TBD |
| source repo ref | TBD |
| dataset cache root | TBD |
| artifact root | TBD |

## 2. 依赖安装记录

| 步骤 | 命令 | 状态 | 备注 |
|---|---|---|---|
| 安装 smoke 依赖 | `uv sync --extra dev --extra bo-tutorial` | not_started | smoke 前必须完成 |
| 导入检查 | `uv run python -c "import pandas, sklearn, scipy, openpyxl, tqdm; from rdkit import Chem; from rdkit.Chem import QED; print('bo-tutorial deps ok')"` | not_started | Molecule/QED smoke 前必须完成 |
| 完整依赖预留 | `uv sync --extra dev --extra bo-tutorial --extra bo-tutorial-full` | not_started | 本 workflow 不要求 |

## 3. 数据集校验记录

### 3.1 总表

| 数据集 | Task | Source path | Local/cache path | sha256 | 行数/items | 列数 | 状态 |
|---|---|---|---|---|---:|---:|---|
| HER | `her_demo` | `examples/HER/HER_virtual_data.csv` | TBD | TBD | TBD | TBD | not_started |
| HEA | `hea_demo` | `examples/HEA/data/oracle_data.xlsx` | TBD | TBD | TBD | TBD | not_started |
| OER | `oer_demo` | `examples/OER/OER.csv` | TBD | TBD | TBD | TBD | not_started |
| BH | `bh_demo` | `examples/BH/BH_dataset.csv` | TBD | TBD | TBD | TBD | not_started |
| Molecule/QED | `molecule_qed_demo` | `examples/Molecule/zinc.txt.gz` | TBD | TBD | TBD | N/A | not_started |

### 3.2 HER 详情

- 列名：TBD
- 10 个 feature 列是否完整：TBD
- 目标列：`Target`
- Target min/max/mean/std：TBD
- Regret 转换是否验证：TBD
- 备注：TBD

### 3.3 HEA 详情

- 列名：TBD
- 必需原始列 `Co`、`Fe`、`Mn`、`V`、`Cu`、`target` 是否存在：TBD
- Target min/max/mean/std：TBD
- `_phi_inv` transform 是否验证：TBD
- 金属比例 `[0.05, 0.35]` 是否验证：TBD
- 组成比例和约等于 `1.0` 是否验证：TBD
- 备注：TBD

### 3.4 OER 详情

- 原始列名：TBD
- 目标列 `Overpotential mV @10 mA cm-2` 是否存在：TBD
- 清洗后 target min/max/mean/std：TBD
- categorical values 摘要：TBD
- numeric bounds 摘要：TBD
- 清洗摘要：TBD
- 备注：TBD

### 3.5 BH 详情

- 原始列名：TBD
- 目标列 `yield` 是否存在：TBD
- 原始 yield min/max/mean/std：TBD
- regret yield min/max/mean/std：TBD
- feature selector 状态：TBD
- 选中特征：TBD
- 选中特征 bounds：TBD
- 备注：TBD

### 3.6 Molecule/QED 详情

- archive member `zinc.txt` 是否存在：TBD
- SMILES 数量：TBD
- 首个合法 SMILES smoke check：TBD
- RDKit 导入状态：TBD
- QED objective 状态：TBD
- 备注：TBD

## 4. 实现状态

| 组件 | 状态 | 文件/路径 | 备注 |
|---|---|---|---|
| scientific task package | not_started | `bbo/tasks/scientific/` | TBD |
| data assets helper | not_started | `bbo/tasks/scientific/data_assets.py` | TBD |
| shared oracle helper | not_started | `bbo/tasks/scientific/tabular_oracles.py` | TBD |
| HER task | not_started | `bbo/tasks/scientific/her.py` | TBD |
| HEA task | not_started | `bbo/tasks/scientific/hea.py` | TBD |
| OER task | not_started | `bbo/tasks/scientific/oer.py` | TBD |
| BH task | not_started | `bbo/tasks/scientific/bh.py` | TBD |
| Molecule task | not_started | `bbo/tasks/scientific/molecule.py` | TBD |
| task registry | not_started | `bbo/tasks/registry.py` | TBD |
| CLI factory | not_started | `bbo/run.py` | TBD |
| dependency extras | not_started | `pyproject.toml` | TBD |
| task descriptions | not_started | `bbo/task_descriptions/<task>/` | TBD |
| tests | not_started | `tests/` | TBD |

## 5. 验证命令记录

| 命令 | 状态 | 输出/log path | 备注 |
|---|---|---|---|
| `uv sync --extra dev --extra bo-tutorial` | not_started | TBD | TBD |
| `uv run python -m compileall -q bbo tests` | not_started | TBD | TBD |
| `uv run pytest` | not_started | TBD | TBD |
| `uv run python -m bbo.run --algorithm random_search --task her_demo --max-evaluations 3 --results-root artifacts/bo_tutorial_all_smoke` | not_started | TBD | TBD |
| `uv run python -m bbo.run --algorithm random_search --task hea_demo --max-evaluations 3 --results-root artifacts/bo_tutorial_all_smoke` | not_started | TBD | TBD |
| `uv run python -m bbo.run --algorithm random_search --task oer_demo --max-evaluations 3 --results-root artifacts/bo_tutorial_all_smoke` | not_started | TBD | TBD |
| `uv run python -m bbo.run --algorithm random_search --task bh_demo --max-evaluations 3 --results-root artifacts/bo_tutorial_all_smoke` | not_started | TBD | TBD |
| `uv run python -m bbo.run --algorithm random_search --task molecule_qed_demo --max-evaluations 3 --results-root artifacts/bo_tutorial_all_smoke` | not_started | TBD | TBD |

## 6. Smoke 产物

| Task | JSONL path | Summary path | Plot paths | best_primary_objective | 状态 |
|---|---|---|---|---:|---|
| `her_demo` | TBD | TBD | TBD | TBD | not_started |
| `hea_demo` | TBD | TBD | TBD | TBD | not_started |
| `oer_demo` | TBD | TBD | TBD | TBD | not_started |
| `bh_demo` | TBD | TBD | TBD | TBD | not_started |
| `molecule_qed_demo` | TBD | TBD | TBD | TBD | not_started |

## 7. 修改文件列表

实现后记录：

```text
TBD
```

## 8. 当前 Blockers

- 远程 benchmark host/path/branch 尚未填写。
- 远程依赖环境尚未准备。
- dataset source ref 和 sha256 尚未记录。
- 本 workflow 创建阶段尚未修改 benchmark 代码。

## 9. 下一步

1. 补全远程 benchmark 信息。
2. 固定 `BO-Tutorial-for-Sci` source ref。
3. 安装 `bo-tutorial` 依赖。
4. 实现 scientific task family。
5. 校验全部数据集。
6. 运行 compile、pytest 和五个 smoke 命令。
7. 用真实执行结果更新本文件。
