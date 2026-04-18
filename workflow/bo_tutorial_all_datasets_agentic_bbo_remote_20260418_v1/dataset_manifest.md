# 数据集清单

更新时间：2026-04-18 CST

配套代码仓库：`https://github.com/zwyu-ai/BO-Tutorial-for-Sci`

执行 agent 必须先固定 source repo ref，再下载或同步数据。ref、下载路径和 sha256 必须写入 `exp_result.md`。

## 1. HER

- Task 名称：`her_demo`
- 源文件路径：`examples/HER/HER_virtual_data.csv`
- 数据类型：CSV 表格回归数据
- 输入特征：
  - `AcidRed871_0gL`
  - `L-Cysteine-50gL`
  - `MethyleneB_250mgL`
  - `NaCl-3M`
  - `NaOH-1M`
  - `P10-MIX1`
  - `PVP-1wt`
  - `RhodamineB1_0gL`
  - `SDS-1wt`
  - `Sodiumsilicate-1wt`
- 搜索空间：10 个连续变量，每个范围均为 `[0, 5]`
- 原始目标列：`Target`
- Benchmark objective：`regret = Target.max() - predicted_Target`
- 优化方向：minimize
- Oracle：`sklearn.ensemble.RandomForestRegressor(n_estimators=100, random_state=<seed>)`

## 2. HEA

- Task 名称：`hea_demo`
- 源文件路径：`examples/HEA/data/oracle_data.xlsx`
- 数据类型：XLSX 表格回归数据
- 原始列：
  - `Co`
  - `Fe`
  - `Mn`
  - `V`
  - `Cu`
  - `target`
- 暴露给 optimizer 的搜索空间：
  - `x1`、`x2`、`x3`、`x4`，均为连续变量 `[0, 1]`
- 内部变换：
  - 使用配套代码中的 `_phi_inv` 逻辑，将 `x1..x4` 映射为 `Co/Fe/Mn/V/Cu`。
  - 每个金属比例必须在 `[0.05, 0.35]`。
  - 五个金属比例之和必须约等于 `1.0`。
- Benchmark objective：`regret = target.max() - predicted_target`
- 优化方向：minimize
- Oracle：`sklearn.ensemble.RandomForestRegressor(n_estimators=100, random_state=<seed>)`
- 注意：配套代码默认路径中有 `example/HEA/...` 拼写问题，实际应使用 `examples/HEA/data/oracle_data.xlsx`。

## 3. OER

- Task 名称：`oer_demo`
- Canonical 源文件路径：`examples/OER/OER.csv`
- 可参考的 clean 文件：`examples/OER/OER_clean.csv`
- 数据类型：categorical + numeric 混合表格回归数据
- 目标列：`Overpotential mV @10 mA cm-2`
- 优化方向：minimize
- Categorical 特征：
  - `Metal_1`
  - `Metal_2`
  - `Metal_3`
- Numerical 特征：
  - `Metal_1_Proportion`
  - `Metal_2_Proportion`
  - `Metal_3_Proportion`
  - `Hydrothermal Temp degree`
  - `Hydrothermal Time min`
  - `Annealing Temp degree`
  - `Annealing Time min`
  - `Proton Concentration M`
  - `Catalyst_Loading mg cm -2`
- 搜索空间：
  - 3 个 categorical 参数，取清洗后金属唯一值，必要时包含 `None`。
  - 金属比例为连续变量 `[0, 100]`。
  - 水热/退火温度和时间为整数变量，范围来自清洗后数据的 min/max。
  - 质子浓度和催化剂负载为连续变量，范围来自清洗后数据的 min/max。
- Oracle：
  - 使用 `pandas.get_dummies` 编码 categorical 特征。
  - 训练 `RandomForestRegressor(n_estimators=200, max_depth=15, min_samples_split=5, min_samples_leaf=2, random_state=42, n_jobs=-1)`。
- Smoke 可以跳过 cross-validation 输出，但清洗逻辑和 one-hot 对齐必须与配套代码一致。

## 4. BH

- Task 名称：`bh_demo`
- 源文件路径：`examples/BH/BH_dataset.csv`
- 数据类型：CSV 表格回归数据
- 原始目标列：`yield`
- 预处理：
  - 转换为 regret：`yield = yield.max() - yield`
  - 如存在 `cost` 和 `new_index`，需要丢弃
- 特征选择：
  - `feature_selector="random_forest"`
  - `min_imp=0.01`
  - `max_cum_imp=0.8`
  - `max_n=20`
- 搜索空间：
  - 对选中特征建立连续参数。
  - 每个参数范围取该特征在处理后数据中的 min/max。
- Benchmark objective：`regret`
- 优化方向：minimize
- Oracle：`sklearn.ensemble.RandomForestRegressor(n_estimators=100, random_state=<seed>)`

## 5. Molecule/QED

- Task 名称：`molecule_qed_demo`
- 源文件路径：`examples/Molecule/zinc.txt.gz`
- 数据类型：gzip tar archive，内部包含 `zinc.txt`
- 搜索空间：
  - 一个 categorical 参数：`SMILES`
  - choices 来自读取出的 ZINC SMILES 列表
- Objective：
  - 使用 RDKit `Chem.MolFromSmiles`。
  - 对合法 molecule 计算 `rdkit.Chem.QED.qed(mol)`。
  - 非法 SMILES 的原始 QED 分数记为 `0.0`。
  - Benchmark primary objective 为 `qed_loss = 1.0 - qed`。
- 优化方向：minimize
- Metadata：
  - 在 evaluation metadata 中记录原始 `qed`。
  - 记录 archive member 名称 `zinc.txt`。

## 6. 必须记录的数据校验项

每个数据集都必须在 `exp_result.md` 中记录：

- 解析后的本地路径
- 下载 URL 或手动放置来源
- source repo ref
- sha256
- 文件大小
- 行数或 item 数
- 表格数据的列名
- 表格数据的目标列统计
- 数据清洗或特征选择摘要

必要字段缺失时，不允许继续 task smoke。
