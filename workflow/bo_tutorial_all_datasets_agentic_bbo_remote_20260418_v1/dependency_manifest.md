# 依赖清单

更新时间：2026-04-18 CST

本 workflow 需要把 BO tutorial 相关依赖加入 benchmark，但不能让 `agentic-bbo` 的基础安装变重。

## 1. 推荐 optional extras

建议在 `pyproject.toml` 或等价依赖机制中新增 optional extras。

### `bo-tutorial`

五个 smoke task 需要的依赖：

```toml
bo-tutorial = [
  "pandas>=1.0.1",
  "scikit-learn>=0.22",
  "scipy>=1.1",
  "openpyxl>=3.1",
  "tqdm",
  "rdkit",
]
```

用途：

- `pandas`：读取 CSV/XLSX，并完成 OER one-hot 编码。
- `scikit-learn`：随机森林 mock oracle 和 BH 特征选择。
- `scipy`：保持配套科学计算栈兼容。
- `openpyxl`：读取 HEA XLSX 文件。
- `tqdm`：兼容配套工具和后续脚本。
- `rdkit`：支持 Molecule/QED task。

### `bo-tutorial-full`

为后续完整论文 baseline 扩展预留：

```toml
bo-tutorial-full = [
  "hebo",
  "torch>=1.9.0",
  "gpytorch>=1.4.0",
  "pymoo==0.6.1.6",
  "catboost>=0.24.4",
  "disjoint-set",
]
```

用途：

- 保持 smoke 接入与 HEBO/BO-LCB 复现实验解耦。
- 为后续 v3 或完整复现实验记录 tutorial 全依赖栈。

## 2. Smoke 环境安装命令

远程环境推荐执行：

```bash
uv sync --extra dev --extra bo-tutorial
```

如果目标环境无法通过当前 package index 安装 RDKit，必须把精确失败信息写入 `exp_result.md`，并采用以下明确 fallback 之一：

- 使用目标环境支持的 conda/mamba channel 安装 RDKit，然后继续执行同一组 smoke 命令。
- 只将 `molecule_qed_demo` 标记为 blocked，并继续 HER/HEA/OER/BH 四个 task 的 smoke。

不允许用假的 objective 替代 RDKit QED。

## 3. 依赖导入验证

安装后必须验证：

```bash
uv run python -c "import pandas, sklearn, scipy, openpyxl, tqdm; from rdkit import Chem; from rdkit.Chem import QED; print('bo-tutorial deps ok')"
```

完整 optional dependencies 只有在明确要求时才验证：

```bash
uv sync --extra dev --extra bo-tutorial --extra bo-tutorial-full
uv run python -c "import hebo, torch, gpytorch, pymoo, catboost; import disjoint_set; print('bo-tutorial-full deps ok')"
```

## 4. 规则

- 不要把这些依赖放入基础 `[project].dependencies`。
- smoke 不要求安装 `bo-tutorial-full`。
- `random_search` smoke 不应依赖 `hebo`。
- 不要跳过依赖记录；安装命令、状态和 import check 摘要必须写入 `exp_result.md`。
