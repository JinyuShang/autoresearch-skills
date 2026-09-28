# 出题合同

## 必须先回答

- 参赛者能修改什么文件、函数和语义？
- 哪些资产、数据、seed、预算和评测逻辑冻结？
- Baseline 为什么合理，Reference 为什么不是泄题？
- 主指标如何从候选运行重新计算，失败如何关闭？
- 质量、速度、显存、稳定性分别是目标还是硬门？
- 证据由哪个步骤生成，路径、schema 和哈希是什么？

## 交付目录职责

- `workspace/`：参赛者可见且可执行的题目。
- `expert_evidence/`：专家说明、轨迹与汇总结论。
- `optimization_evidence/`：Baseline/Reference 成对原始结果、日志、模型索引和比较。

平台若要求单业务外层目录，ZIP 根只能有一个目录，该目录内再放以上三项。

## 完成标准

- Starter、Baseline、Reference 都能在声明环境运行。
- B/R 使用同协议，结果可从原始值复算。
- 评分器拒绝旧结果、缺文件、篡改资产和不完整 case。
- instruction 不泄露 Hidden、Reference 代码或作者路径。
- 代码、文档、JSON 和哈希在同一次构建中生成，不靠手工补数字。
