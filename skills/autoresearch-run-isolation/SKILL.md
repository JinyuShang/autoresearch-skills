---
name: autoresearch-run-isolation
description: 为 AutoResearch 的 GPT/Seed 双轨迹、付费 GPU 长跑、评测与打包建立共享协议和隔离边界。用于接入模型、启动或恢复 campaign、设计证据与防止题目或轨迹串用；不替代具体任务算法。
---

# AutoResearch 运行协议与隔离

先读 [protocol-and-isolation.md](references/protocol-and-isolation.md)。优先复用 `autoresearch-run-protocol` 包；每题只实现任务适配器与可信评测器。

运行前冻结任务树并计算逐文件哈希；GPT 与 Seed 使用独立 workspace、控制目录、端口、凭据和轨迹目录。候选进程只能看到 Starter 与公开资产，Reference、专家证据和另一条轨迹不得进入其挂载范围。

每轮保存原始 RPC、命令、评测摘要、receipt 和来源哈希。有效时长以闭合 turn 窗口为基础，未闭合、排队、安装、阻塞、睡眠和故障不计。两条轨迹分别达门槛，不能相加。

把外部模型数据流纳入隔离合同：明确会发送的 prompt、工具结果和评测摘要；子进程环境使用最小白名单，凭据只以显式环境变量注入。落盘前按真实 secret 值和通用 token 形态脱敏，但不得把脱敏当作零外发。公开轨迹只保留完成审计所需字段，不发布原始 RPC、作者路径、主机信息或 capability 链接。

恢复运行前比较任务摘要、driver capability、已完成轮和远端 lease；不复用旧 PID 或不明控制目录。付费运行必须有磁盘、预算、备份失败和停止条件。

打包只从冻结源和显式白名单构建；构建后解压到新目录，比较完整路径集合与 SHA256，再交给 QA。主包、自检、轨迹和证据附件分别执行隐私检查，任一附件失败都不能发布。
