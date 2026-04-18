# Remote Codex Prompt

请你执行本 workflow：

```text
D:\Users\Johnny\Documents\New project\workflow\bo_tutorial_her_agentic_bbo_demo_20260418_v1
```

或远程同步后的同名目录。

## 必读文件

请按顺序阅读：

1. `Agent.md`
2. `request.md`
3. `exp_task.md`
4. `exp_result.md`

## 任务目标

把论文 *Efficient and Principled Scientific Discovery through Bayesian Optimization: A Tutorial* 的 HER 数据集接入 `trxcc/agentic-bbo` benchmark，新增 `her_demo` task，并完成最小 smoke demo。

固定范围：

- 只接入 HER。
- 不接入 HEA/OER/BH/Molecule。
- 不复现论文完整实验。
- smoke demo 只需 3 次 random search evaluation。

## 关键实现要求

- HER 数据来自 `zwyu-ai/BO-Tutorial-for-Sci/examples/HER/HER_virtual_data.csv`。
- 搜索空间为 10 个连续变量，范围全是 `[0, 5]`。
- primary objective 为 `regret`，方向 `minimize`。
- regret 定义为 `Target.max() - Target`。
- mock oracle 使用 `RandomForestRegressor(n_estimators=100, random_state=<seed>)`。
- `Task.evaluate()` 返回标准 `EvaluationResult`。
- task description 放到 `bbo/task_descriptions/her_demo/`。
- CLI 必须支持：

```bash
uv run python -m bbo.run --algorithm random_search --task her_demo --max-evaluations 3 --results-root artifacts/her_demo_smoke
```

## 必跑验证

```bash
uv run python -m compileall -q bbo examples tests
uv run pytest
uv run python -m bbo.run --algorithm random_search --task her_demo --max-evaluations 3 --results-root artifacts/her_demo_smoke
```

## 完成后

请更新 `exp_result.md`：

- repo path / commit
- HER 数据核验信息
- modified files
- validation commands and statuses
- JSONL / summary / plot paths
- blockers 或 completed 状态

不要伪造结果；如果 smoke 失败，记录失败命令、错误摘要、原因判断和下一步。
