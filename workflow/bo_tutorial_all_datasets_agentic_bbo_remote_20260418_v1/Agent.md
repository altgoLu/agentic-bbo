# Agent 指南

更新时间：2026-04-18 CST

## 0. 任务定位

本 workflow 用来驱动后续执行 agent，把论文 *Efficient and Principled Scientific Discovery through Bayesian Optimization: A Tutorial* 配套仓库中的全部数据集接入远程 `trxcc/agentic-bbo` benchmark。

本任务是 benchmark 接入和 smoke 验证，不是论文完整复现实验。

固定范围：

- 论文 PDF：`D:\University\keyan\Benchmark\群聊文章\EFFICIENT AND PRINCIPLED SCIENTIFIC DISCOVERY THROUGH.pdf`
- 配套代码仓库：`https://github.com/zwyu-ai/BO-Tutorial-for-Sci`
- 目标 benchmark：`https://github.com/trxcc/agentic-bbo`
- 数据集与 task：`her_demo`、`hea_demo`、`oer_demo`、`bh_demo`、`molecule_qed_demo`
- 验收方式：每个 task 跑 3 次 `random_search` evaluation
- 远程 benchmark 信息：创建 workflow 时未知，执行阶段必须补全

## 1. 执行前必读顺序

开始修改远程 benchmark 前，必须按顺序阅读：

1. `Agent.md`
2. `request.md`
3. `exp_task.md`
4. `dataset_manifest.md`
5. `dependency_manifest.md`
6. `exp_result.md`
7. `remote_codex_prompt.md`
8. 目标 benchmark 的 `README.md`
9. 目标 benchmark 的 `bbo/core/` task 和 trial 接口
10. 目标 benchmark 的 `bbo/tasks/registry.py`
11. 目标 benchmark 的 `bbo/run.py`

如果文件之间存在冲突，优先级如下：

1. `exp_task.md`
2. `dataset_manifest.md`
3. `dependency_manifest.md`
4. `request.md`
5. `Agent.md`
6. 目标 benchmark 原仓库源码

## 2. 执行规则

- 不允许伪造数据集。
- 不允许在数据缺失时 silent fallback 到随机数据或假数据。
- 不允许把 smoke 结果表述成论文复现实验结果。
- 不跑论文中的 `200 evaluations x 16 seeds` 完整设置。
- 本 workflow 不比较 HEBO、BO-LCB 或其他 baseline。
- 除非 smoke 证明现有接口无法表达这些任务，否则不修改 `bbo/core/`。
- 所有远程路径、commit、依赖安装动作、命令、失败原因都必须写入 `exp_result.md`。

## 3. 远程实现建议结构

推荐在 benchmark 中新增：

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

task description 必须新增到：

```text
bbo/task_descriptions/her_demo/
bbo/task_descriptions/hea_demo/
bbo/task_descriptions/oer_demo/
bbo/task_descriptions/bh_demo/
bbo/task_descriptions/molecule_qed_demo/
```

每个 task description 目录至少包含：

```text
background.md
goal.md
constraints.md
prior_knowledge.md
evaluation.md
environment.md
```

## 4. 完成定义

只有同时满足以下条件，本 workflow 才算完成：

1. 远程目标路径、分支和 commit 已记录。
2. 五个数据集均已下载或手动放置，并完成校验。
3. 依赖已通过 optional extra 或等价环境命令安装并记录。
4. 五个 scientific task 已注册，并可通过 `python -m bbo.run` 运行。
5. 五个 task 的 `sanity_check()` 均通过。
6. 五个 smoke 命令均完成至少 3 次 evaluation。
7. 每个 smoke run 都写出 `trials.jsonl` 和 `summary.json`。
8. 每个 summary 都包含 `best_primary_objective`。
9. JSONL、summary、plot 等产物路径已写入 `exp_result.md`。
10. `exp_result.md` 的状态已更新为 `completed`，或记录了明确 blocker。
