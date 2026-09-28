---
name: autoresearch-task-authoring
description: 从论文与代码仓设计可交付的 AutoResearch 工程题，确定 Starter、Baseline、Reference、评分器、Harbor 结构和证据契约。用于出题、改题或审题；不替代提交包最终 QA。
---

# AutoResearch 出题

先读任务平台最新规则、项目示例和目标论文，再读 [authoring-contract.md](references/authoring-contract.md)。不得从旧题或别的仓库复制未经验证的结构。

1. 建立题目合同：允许修改面、冻结面、输入输出、预算、质量门、主指标方向和 0/1 锚点。
2. Starter 必须朴素、可运行且不故意削弱；Baseline 必须来自正式实现并能解释。
3. Reference 只能证明题目有改进空间，不能把算法答案写进 instruction；正式 B/R 使用相同数据、seed、预算和评测器。
4. 评分器从候选代码重新运行并独立计算结果，不采信候选自报分数；成功结果用同文件系统 stage 后原子替换。
5. 将作者材料、参赛者 workspace 和优化证据分开。Docker COPY、WORKDIR、入口与选定的平台 profile 必须形成一条可执行路径。
6. 先做小规模成对实跑，再决定是否值得开展双轨迹长跑。没有动态证据时明确写“未验证运行”。
7. 交付前调用 `autoresearch-task-qa` 做独立静态审查；三门或 21 项有失败即 NOT READY。
8. 开源或外发前对主包、QA/self-check、轨迹和证据附件分别做隐私与可移植性检查；生成报告不得保留作者 home、凭据值或私有文件链接。

输出至少包括题面、接口、Starter、Baseline、Reference、评分器、冻结清单、证据清单、构建说明和验收命令。
