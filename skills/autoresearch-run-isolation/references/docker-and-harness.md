# Docker 执行与 Harness 边界

## 推荐拓扑

受信控制层持有 API/provider 凭据、调度与原始事件；两个无密钥 Agent sandbox 使用同一冻结任务镜像 digest 和不同可写卷；可信 evaluator 持有隐藏资产并生成 receipt/reward；公共模型与数据缓存只读共享。

- Agent 不挂载宿主 Docker socket、SSH 私钥、peer 卷、Reference 或隐藏 tests。
- 单卡通过受信锁串行分配 trainer/evaluator；双卡显式记录宿主 device ID 与容器可见设备。
- controller 若能执行任意 root shell，必须限制模型可调用的参数与路径，否则容器隔离只是表象。
- 镜像、代码、轨迹和正式证据同步到租赁节点之外的持久位置。

`assets/compose.yaml` 是普通 NVIDIA Docker 主机的开发模板。`lane-a`、`lane-b` 和 `evaluate` 是互斥 profile；单卡时由受信控制层一次只启动一个 profile，不能执行无 profile 的全量并发启动。运行前至少执行 Compose 配置解析、容器内 GPU 可见性和真实最小前后向；这些结果不能替代目标 Harness 的 parser/build/trial/verifier/reward 链。

平台或 Harbor 的 backend 支持会变化。Harbor 当前公开任务格式允许声明 `gpus`/`gpu_types`，Docker 环境也可读取 Dockerfile、镜像或 Compose，但资源执行方式随 provider 而异，许多云 sandbox 只接受 Dockerfile。每次固定目标版本与 provider，检查安装版本的命令帮助和官方文档；不能凭旧示例推定 GPU、Compose、挂载、工作目录或 reward 路径仍相同。Oracle 证明 reference solution 与 verifier 正向闭环，Starter/负例检查平凡满分和 reward hack，真实 Agent Trial 才证明实际 agent 路径。

## 外部依据

实现时优先核对一手文档，并在每次目标平台升级后重新确认：

- [Docker Compose GPU support](https://docs.docker.com/compose/how-tos/gpu-support/)
- [Docker Compose startup order](https://docs.docker.com/compose/how-tos/startup-order/)
- [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)
- [Harbor task structure and resource requirements](https://harborframework.com/docs/tasks)

这些链接只说明通用能力或当前公开接口，不是某次任务已经通过的证据。最终以目标版本、目标 backend 和真实 trial receipt 为准。
