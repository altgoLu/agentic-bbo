# 远程 Codex 执行 Prompt

请执行以下 workflow：

```text
D:\Users\Johnny\Documents\New project\workflow\bo_tutorial_all_datasets_agentic_bbo_remote_20260418_v1
```

或同步到远程后的同名目录。

## 1. 必读文件

请按顺序阅读：

1. `Agent.md`
2. `request.md`
3. `exp_task.md`
4. `dataset_manifest.md`
5. `dependency_manifest.md`
6. `exp_result.md`

## 2. 任务目标

把论文 *Efficient and Principled Scientific Discovery through Bayesian Optimization: A Tutorial* 配套仓库中的五个数据集全部接入 `trxcc/agentic-bbo`，并让它们成为可 smoke 运行的 benchmark task。

目标仓库：

```text
https://github.com/trxcc/agentic-bbo
```

数据来源仓库：

```text
https://github.com/zwyu-ai/BO-Tutorial-for-Sci
```

需要新增的 task：

```text
her_demo
hea_demo
oer_demo
bh_demo
molecule_qed_demo
```

## 3. 开始修改前必须做

先在 `exp_result.md` 中补全：

- remote host
- remote repo path
- remote branch
- Python version
- `uv` version
- `agentic-bbo` base commit/ref
- `BO-Tutorial-for-Sci` source ref
- dataset cache root
- artifact root

## 4. 必须实现

- 新增 `bbo/tasks/scientific/`。
- 新增 downloader/cache 和数据校验逻辑。
- 新增 optional dependency extra：`bo-tutorial`。
- 新增 optional dependency extra：`bo-tutorial-full`，供后续完整 baseline 使用。
- 通过通用 task registry 注册五个 task。
- 保持 synthetic task 兼容。
- 让 `python -m bbo.run --task <task>` 能运行 scientific task。
- 为五个 task 新增 task descriptions。
- 所有 smoke 都使用 `random_search`。

不允许伪造数据。不允许 silent fallback。不可用假函数替代 RDKit QED。

## 5. 必跑验证

运行：

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

## 6. 完成后必须更新

更新 `exp_result.md`：

- 依赖安装状态
- 数据集校验详情
- 修改文件列表
- 验证命令状态
- JSONL 路径
- summary 路径
- plot 路径
- blocker 或 completed 状态

如果只有 RDKit 阻塞 `molecule_qed_demo`，记录该 blocker，并继续 HER/HEA/OER/BH。除非五个 task 均 completed，或明确记录了可接受 blocker，否则不要把整个 workflow 标记为 completed。
