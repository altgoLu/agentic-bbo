# 用户请求

更新时间：2026-04-18 CST

## 1. 原始需求

创建一个新的 workflow，用来指导后续 agent 将 BO tutorial 论文配套仓库中的全部数据集和相关依赖接入远程 `trxcc/agentic-bbo` benchmark。

后续执行 agent 需要完成：

- 将论文配套仓库中的全部数据集接入 `agentic-bbo`。
- 将必要依赖加入 benchmark，但不要污染基础安装。
- 在远程 benchmark 环境中部署或准备实现。
- 对每个数据集运行一个最小 smoke demo。
- 记录所有结果、产物路径和 blocker。

## 2. 固定决策

- Workflow 目录：
  - `D:\Users\Johnny\Documents\New project\workflow\bo_tutorial_all_datasets_agentic_bbo_remote_20260418_v1`
- 论文：
  - `Efficient and Principled Scientific Discovery through Bayesian Optimization: A Tutorial`
- 本地 PDF：
  - `D:\University\keyan\Benchmark\群聊文章\EFFICIENT AND PRINCIPLED SCIENTIFIC DISCOVERY THROUGH.pdf`
- 配套代码仓库：
  - `https://github.com/zwyu-ai/BO-Tutorial-for-Sci`
- 目标 benchmark：
  - `https://github.com/trxcc/agentic-bbo`
- 数据集范围：
  - HER
  - HEA
  - OER
  - BH
  - Molecule/QED
- Smoke 验证：
  - 使用 `random_search`
  - 每个 task 固定 `--max-evaluations 3`
  - 每个数据集跑一个 smoke run

## 3. 不做事项

- 不做论文完整复现。
- 不跑 `200 evaluations x 16 seeds`。
- 不做 HEBO、BO-LCB、Random Search 的完整比较。
- 不引入长跑实验矩阵。
- 不声称 smoke 结果代表科学性能。
- 不重写无关算法、logger 或 plotter。

## 4. 执行阶段必须补全的远程信息

创建 workflow 阶段尚不知道远程 host 和路径。执行 agent 必须在 `exp_result.md` 中补全：

- 远程 host
- 远程仓库路径
- 远程分支
- 远程 Python 版本
- 远程 `uv` 版本或环境管理方式
- `agentic-bbo` 基础 commit/ref
- `BO-Tutorial-for-Sci` source ref
- 数据集 cache root
- 实验 artifact root

## 5. 交付物

本 workflow 的交付物是一个有记录的远程 benchmark 接入与 smoke 验证结果，而不只是本地说明文档。

如果远程执行被阻塞，必须在 `exp_result.md` 中记录可恢复的 blocker，便于下一个 agent 接着做。
