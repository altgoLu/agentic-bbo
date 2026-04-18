# Exp Result

更新日期：`2026-04-18 CST`

状态：`completed`

## 0. 基本信息

- workflow root:
  - `D:\Users\Johnny\Documents\New project\workflow\bo_tutorial_her_agentic_bbo_demo_20260418_v1`
- target benchmark:
  - `https://github.com/trxcc/agentic-bbo`
- target task:
  - `her_demo`
- source paper PDF:
  - `D:\University\keyan\Benchmark\群聊文章\EFFICIENT AND PRINCIPLED SCIENTIFIC DISCOVERY THROUGH.pdf`
- source tutorial repo:
  - `https://github.com/zwyu-ai/BO-Tutorial-for-Sci`
- source dataset:
  - `examples/HER/HER_virtual_data.csv`
- source reference implementation:
  - `examples/HER/utils.py`

## 1. Benchmark Repo

- local_repo_path:
  - `/home/trx/cm/agentic-bbo`
- remote_url:
  - `https://github.com/trxcc/agentic-bbo.git`
- branch:
  - `main`
- commit_sha:
  - `64e0b81173bd0c1f9c1fbcb57c5bfcd7464cd452`
- dirty_before:
  - `true` (`workflow/` 与 `.codex` 在开始前已为未跟踪状态)
- dirty_after:
  - `true` (新增 her_demo 改动、workflow 日志与结果文件，未创建 git commit)
- package_manager:
  - `uv`
- python_version:
  - `3.11.5`

## 2. HER Dataset

### 2.1 数据获取

- dataset_strategy: `package_data`
- dataset_source_url:
  - `https://raw.githubusercontent.com/zwyu-ai/BO-Tutorial-for-Sci/main/examples/HER/HER_virtual_data.csv`
- local_dataset_path:
  - `bbo/tasks/scientific/data/HER_virtual_data.csv`
- download_or_copy_status:
  - `completed`；通过浅克隆 `zwyu-ai/BO-Tutorial-for-Sci` 到 `/tmp/bo_tutorial_her_source` 后，将 `examples/HER/HER_virtual_data.csv` 拷贝进包内数据目录
- checksum_or_size:
  - `sha256=1843a9247fb74a7df2b40088efb4e4d66f1fce5d788bfb10cf1423c31940bd5e`
  - `size_bytes=83252`

### 2.2 数据核验

- row_count:
  - `812`
- column_count:
  - `11`
- feature_columns:
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
- target_column: `Target`
- target_min:
  - `0.0`
- target_max:
  - `27.7041039`
- target_mean:
  - `7.443407453194581`
- target_std:
  - `5.648601683093673`
- regret_definition: `Target.max() - Target`
- dataset_qc_status:
  - `passed`；详见 `workflow/bo_tutorial_her_agentic_bbo_demo_20260418_v1/outputs/her_dataset_qc.json`

## 3. Implementation Status

### 3.1 Task implementation

- task_family_path:
  - `bbo/tasks/scientific`
- task_file:
  - `bbo/tasks/scientific/her.py`
- task_class_or_factory:
  - `HerTask / create_her_task`
- registered_task_name: `her_demo`
- search_space_status:
  - `passed`；10 个 `FloatParam`，范围均为 `[0, 5]`
- objective_status:
  - `passed`；primary objective=`regret`，direction=`minimize`
- random_forest_oracle_status:
  - `passed`；`RandomForestRegressor(n_estimators=100, random_state=<seed>)`
- task_sanity_status:
  - `passed`

### 3.2 Task description

- description_dir:
  - `bbo/task_descriptions/her_demo`
- background_md:
  - `bbo/task_descriptions/her_demo/background.md`
- goal_md:
  - `bbo/task_descriptions/her_demo/goal.md`
- constraints_md:
  - `bbo/task_descriptions/her_demo/constraints.md`
- prior_knowledge_md:
  - `bbo/task_descriptions/her_demo/prior_knowledge.md`
- evaluation_md:
  - `bbo/task_descriptions/her_demo/evaluation.md`
- environment_md:
  - `bbo/task_descriptions/her_demo/environment.md`
- description_sanity_status:
  - `passed`

### 3.3 CLI integration

- bbo_run_modified:
  - `true`；`bbo/run.py` 现通过通用 `create_task(...)` 创建任务，并对非 2D/无 `surface_grid()` 的任务只生成通用 trace/distribution plots
- task_registry_modified:
  - `true`；`bbo/tasks/registry.py` 与 `bbo/tasks/__init__.py` 已注册 `her_demo`
- cli_accepts_her_demo:
  - `true`
- non_synthetic_visualization_handling:
  - `generic trace/distribution enabled; 2D landscape only when dimension==2 and task exposes surface_grid()`

### 3.4 Dependencies

- sklearn_available:
  - `true` (`scikit-learn==1.8.0`)
- pandas_available:
  - `true` (`pandas==3.0.2`)
- dependency_file_modified:
  - `pyproject.toml`, `uv.lock`
- dependency_notes:
  - `uv sync --extra dev` 安装了 `pandas`、`scikit-learn` 及其依赖，并同步更新 lockfile；包数据已通过 `pyproject.toml` 纳入 `bbo/tasks/scientific/data/*.csv`

## 4. Validation

### 4.1 compileall

- command:
  - `uv run python -m compileall -q bbo examples tests`
- status: `passed`
- log_path:
  - `workflow/bo_tutorial_her_agentic_bbo_demo_20260418_v1/logs/compileall.log`
- notes:
  - `compileall` 成功，stdout 为空

### 4.2 pytest

- command:
  - `uv run pytest`
- status: `passed`
- log_path:
  - `workflow/bo_tutorial_her_agentic_bbo_demo_20260418_v1/logs/pytest.log`
- notes:
  - `9 passed in 3.65s`

### 4.3 HER smoke

- command:
  - `uv run python -m bbo.run --algorithm random_search --task her_demo --max-evaluations 3 --results-root artifacts/her_demo_smoke`
- status: `passed`
- log_path:
  - `workflow/bo_tutorial_her_agentic_bbo_demo_20260418_v1/logs/her_smoke.log`
- results_root:
  - `artifacts/her_demo_smoke`
- trials_jsonl:
  - `artifacts/her_demo_smoke/her_demo/random_search/seed_7/trials.jsonl`
- summary_json:
  - `artifacts/her_demo_smoke/her_demo/random_search/seed_7/summary.json`
- plot_paths:
  - `artifacts/her_demo_smoke/her_demo/random_search/seed_7/plots/trace.png`
  - `artifacts/her_demo_smoke/her_demo/random_search/seed_7/plots/distribution.png`
- trial_count:
  - `3`
- best_primary_objective:
  - `25.76106351365`
- stop_reason:
  - `task_budget`

## 5. Output Artifacts

- benchmark_artifacts_root:
  - `artifacts/her_demo_smoke`
- workflow_logs:
  - `workflow/bo_tutorial_her_agentic_bbo_demo_20260418_v1/logs`
- workflow_outputs:
  - `workflow/bo_tutorial_her_agentic_bbo_demo_20260418_v1/outputs`
- workflow_summary:
  - `workflow/bo_tutorial_her_agentic_bbo_demo_20260418_v1/summary`
- copied_summary_files:
  - `workflow/bo_tutorial_her_agentic_bbo_demo_20260418_v1/summary/her_demo_smoke_summary.json`
  - `workflow/bo_tutorial_her_agentic_bbo_demo_20260418_v1/outputs/her_dataset_qc.json`

## 6. Modified Files

- added_files:
  - `bbo/tasks/scientific/__init__.py`
  - `bbo/tasks/scientific/her.py`
  - `bbo/tasks/scientific/data/HER_virtual_data.csv`
  - `bbo/task_descriptions/her_demo/background.md`
  - `bbo/task_descriptions/her_demo/goal.md`
  - `bbo/task_descriptions/her_demo/constraints.md`
  - `bbo/task_descriptions/her_demo/prior_knowledge.md`
  - `bbo/task_descriptions/her_demo/evaluation.md`
  - `bbo/task_descriptions/her_demo/environment.md`
  - `tests/test_her_task.py`
  - `workflow/bo_tutorial_her_agentic_bbo_demo_20260418_v1/logs/compileall.log`
  - `workflow/bo_tutorial_her_agentic_bbo_demo_20260418_v1/logs/pytest.log`
  - `workflow/bo_tutorial_her_agentic_bbo_demo_20260418_v1/logs/her_smoke.log`
  - `workflow/bo_tutorial_her_agentic_bbo_demo_20260418_v1/outputs/her_dataset_qc.json`
  - `workflow/bo_tutorial_her_agentic_bbo_demo_20260418_v1/summary/her_demo_smoke_summary.json`
- modified_files:
  - `bbo/run.py`
  - `bbo/tasks/__init__.py`
  - `bbo/tasks/registry.py`
  - `pyproject.toml`
  - `uv.lock`
  - `workflow/bo_tutorial_her_agentic_bbo_demo_20260418_v1/exp_result.md`
- deleted_files:
  - `none`
- notes:
  - `workflow/` 与 `.codex` 在开始前已是未跟踪目录；本次未改动 `.codex`，仅在 workflow 目录内新增执行记录与汇总文件

## 7. Blockers

当前：

- 无阻塞；本轮固定范围内目标已完成

后续如遇 blocker，在此追加：

- `none`

## 8. Next Steps

1. 如需扩展论文数据接入，可按同样模式继续新增 `HEA`、`OER`、`BH` 或 molecule/QED task。
2. 如需更严格验证，可在 `her_demo` 上增加多 seed smoke、resume 测试或 `pycma` 基线运行。
