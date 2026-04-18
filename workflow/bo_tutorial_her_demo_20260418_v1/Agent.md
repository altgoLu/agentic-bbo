# Agent Guide

更新日期：`2026-04-18 CST`

## 0. 任务定位

本 workflow 用于把论文 *Efficient and Principled Scientific Discovery through Bayesian Optimization: A Tutorial* 中的首个科学发现数据集接入 `trxcc/agentic-bbo` benchmark。

本轮只做 HER 数据集的最小可运行接入：

- 数据集：`examples/HER/HER_virtual_data.csv`
- 目标 task：`her_demo`
- 目标 benchmark：`https://github.com/trxcc/agentic-bbo`
- 验收级别：smoke demo

本 workflow 不是论文完整复现实验，不跑 200 evaluations / 16 seeds，不接入 HEA、OER、BH、Molecule/QED。

## 1. 执行前必须先读

后续执行 agent 必须按顺序阅读：

1. 本文件 `Agent.md`
2. `request.md`
3. `exp_task.md`
4. `exp_result.md`
5. 若已存在执行记录：`summary/`、`logs/`、`outputs/`
6. 目标 benchmark 的 `README.md`
7. 目标 benchmark 的 `bbo/core/DEVELOPER_GUIDE_zh.md` 或同等开发说明
8. 目标 benchmark 的 `bbo/tasks/registry.py`
9. 目标 benchmark 的 `bbo/run.py`
10. 目标 benchmark 中已有 synthetic task 实现

如果文件之间存在冲突，优先级如下：

1. `exp_task.md`
2. `request.md`
3. `Agent.md`
4. benchmark 原仓库文档

## 2. 固定输入

- 论文 PDF：
  - `D:\University\keyan\Benchmark\群聊文章\EFFICIENT AND PRINCIPLED SCIENTIFIC DISCOVERY THROUGH.pdf`
- 论文配套仓库：
  - `https://github.com/zwyu-ai/BO-Tutorial-for-Sci`
- HER 数据源：
  - `examples/HER/HER_virtual_data.csv`
- HER 参考实现：
  - `examples/HER/utils.py`
- 目标 benchmark：
  - `https://github.com/trxcc/agentic-bbo`

## 3. 设计原则

- 不优先改 `bbo/core/`。HER 是任务级 evaluator，应放在 `bbo/tasks/` 和 `bbo/task_descriptions/`。
- 保持 agentic-bbo 现有 ask/evaluate/tell、JSONL logging、replay/resume 语义。
- `Task.evaluate()` 必须返回标准 `EvaluationResult`。
- HER oracle 采用教程配套代码中的随机森林 mock oracle 语义。
- demo 只验证接入链路能跑通，不声明复现论文结果。

## 4. Definition of Done

只有同时满足以下条件，本 workflow 才算完成：

1. `her_demo` 已在 agentic-bbo 中注册。
2. HER CSV 可以被稳定加载或缓存。
3. 10 个 HER 连续变量的搜索空间定义正确，范围均为 `[0, 5]`。
4. `Target` 已按 `Target.max() - Target` 转换为 minimization regret。
5. 随机森林 mock oracle 可以训练并被 `Task.evaluate()` 调用。
6. `her_demo.sanity_check()` 通过。
7. `uv run python -m bbo.run --algorithm random_search --task her_demo --max-evaluations 3 --results-root artifacts/her_demo_smoke` 成功完成。
8. JSONL、summary、必要 plots 路径已记录到 `exp_result.md`。
9. `exp_result.md` 状态更新为 `completed` 或明确记录 blocker。

## 5. 不要做的事

- 不跑完整论文 benchmark。
- 不接入 HEA/OER/BH/Molecule/QED。
- 不把 Molecule/RDKit/ZINC 依赖带入本轮。
- 不引入长跑实验矩阵。
- 不把 smoke demo 结论写成论文复现结论。
- 不重构无关算法、logger 或 plotting 代码。
