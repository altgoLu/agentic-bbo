# Request

更新日期：`2026-04-18 CST`

## 0. 用户需求

用户希望创建一个 workflow 目录，用于驱动后续 agent 根据论文 *Efficient and Principled Scientific Discovery through Bayesian Optimization: A Tutorial*，把文章中需要用到的数据集部署到 `trxcc/agentic-bbo` benchmark 上，并完成简单 demo 测试。

经过前置确认，本轮范围收敛为：

- 只做一个数据集。
- 首个数据集选择 HER / Photocatalytic Hydrogen Evolution Reaction。
- 目标 benchmark 是 `trxcc/agentic-bbo`。
- demo 深度为 smoke test。

## 1. Workflow 目录

本地 workflow 根目录固定为：

```text
D:\Users\Johnny\Documents\New project\workflow\bo_tutorial_her_agentic_bbo_demo_20260418_v1
```

应包含：

```text
Agent.md
request.md
exp_task.md
exp_result.md
remote_codex_prompt.md
logs/
outputs/
summary/
```

## 2. 任务边界

本轮要做：

- 在 agentic-bbo 中新增 `her_demo` task。
- 接入 HER CSV 数据。
- 用 10 个连续变量定义搜索空间。
- 用随机森林 mock oracle 作为 evaluator。
- 返回标准 `EvaluationResult`。
- 跑最小 smoke demo。

本轮不做：

- 不复现论文完整实验表。
- 不跑 200 evaluations / 16 seeds。
- 不接入 HEA、OER、BH、Molecule/QED。
- 不修改 `bbo/core/`，除非 smoke 证明现有接口无法表达 HER 接入。

## 3. 重要来源

- PDF：
  - `D:\University\keyan\Benchmark\群聊文章\EFFICIENT AND PRINCIPLED SCIENTIFIC DISCOVERY THROUGH.pdf`
- 论文配套仓库：
  - `https://github.com/zwyu-ai/BO-Tutorial-for-Sci`
- HER 数据：
  - `https://github.com/zwyu-ai/BO-Tutorial-for-Sci/blob/main/examples/HER/HER_virtual_data.csv`
- HER 参考代码：
  - `https://github.com/zwyu-ai/BO-Tutorial-for-Sci/blob/main/examples/HER/utils.py`
- agentic-bbo：
  - `https://github.com/trxcc/agentic-bbo`

## 4. 用户期望产出

- 一个完整 workflow 目录。
- `exp_task.md` 能清楚告诉执行 agent 需要跑什么。
- `exp_result.md` 能记录完成了哪些实验。
- 后续执行 agent 能按此目录直接开始实现 HER 接入与 smoke demo。
