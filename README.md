# AutoResearch Skills

> 把研究智能体从“一次性 prompt”升级为可设计、可隔离、可审计、可交接的工程系统。

[![CI](https://github.com/bosprimigenious/autoresearch-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/bosprimigenious/autoresearch-skills/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-7-7c3aed.svg)](skills)
[![Tests](https://img.shields.io/badge/tests-CI-0f766e.svg)](.github/workflows/ci.yml)

AutoResearch Skills 不是一组零散提示词，而是一套面向研究型 Coding Agent 的完整作业体系：从判断问题是否值得优化，到建立可信 Baseline、设计任务、隔离并发运行、审查证据，再到把上下文结构化交给下一个 Agent。

它解决的不是“怎样让 Agent 多跑几次”，而是更难也更重要的问题：**怎样让一次自动研究经得起复现、比较、审计与继续执行。**

```text
研究空间        基线质量        任务设计        运行隔离        证据验收        跨 Agent 交接
    │               │               │               │               │               │
    └───────────────┴───────────────┴───────► 可复现的 AutoResearch 闭环 ◄─────────────┘
```

## 为什么是一个系统，而不是七份 Prompt

- **先证明问题值得研究。** 区分真实方法空间与固定超参数搜索，避免把算力消耗包装成研究进展。
- **先把论文候选变成证据账本。** 多源检索、规范化去重、源码许可、资源预算、评测与权威题库查重必须分别留证，限流或缺权限不能写成“没有重复”。
- **把公平性写进流程。** Baseline、预算、指标、产物和复现条件在运行前明确，结果不能靠事后解释。
- **证据优先，默认拒绝含糊结论。** QA 以结构化门禁检查提交、容器路径、平台接口和成对证据；缺证据就不能冒充完成。
- **隔离不仅是目录隔离。** 同时约束运行环境、凭据、产物、时间和 Agent 上下文，降低并发研究互相污染的风险。
- **算力决策包含容量风险。** 小卡先清功能问题，目标卡按小时做端到端 pilot，再把重租概率、恢复损失和停止条件纳入小时/包日选择。
- **交接面向继续执行。** 输出的是下一位 Agent 可以直接接手的状态、证据、阻塞和动作，而不是一段看似完整的总结。
- **隐私是发布门禁。** 公开包、self-check、轨迹与附件逐件检查；CI 额外阻断本机路径、私有协作链接、邮箱、内网地址和常见凭据形态。

## 七个协同 Skill

| Skill | 负责什么 | 核心产出 |
|---|---|---|
| [`autoresearch-paper-discovery`](skills/autoresearch-paper-discovery) | 多源找论文并在投入实现前做候选预检 | 候选账本、权威查重状态与推荐/补证/拒绝结论 |
| [`autoresearch-optimization-surface`](skills/autoresearch-optimization-surface) | 判断任务是否存在足够的研究自由度 | 方法空间、固定项、可变项与反例 |
| [`autoresearch-baseline-quality`](skills/autoresearch-baseline-quality) | 审查基线是否合理、公平、可复现 | Baseline 质量结论与修复清单 |
| [`autoresearch-task-authoring`](skills/autoresearch-task-authoring) | 把论文或代码仓变成可执行的研究任务 | 任务契约、预算、指标、验收与交付结构 |
| [`autoresearch-run-isolation`](skills/autoresearch-run-isolation) | 设计双轨运行、GPU 租赁、恢复与隔离边界 | 容量计划、工作区、血缘、产物与时限约束 |
| [`autoresearch-task-qa`](skills/autoresearch-task-qa) | 对任务包和证据执行 fail-closed 审查 | 分层 QA 结论、失败项与可复核证据 |
| [`autoresearch-conversation-handoff`](skills/autoresearch-conversation-handoff) | 把本轮研究交给下一位 Agent 继续 | 可执行交接包，而非叙述性摘要 |

这些 Skill 可以独立使用，也可以按研究生命周期串联。推荐默认顺序：

```text
paper-discovery
  → optimization-surface
  → baseline-quality
  → task-authoring
  → run-isolation
  → task-qa
  → conversation-handoff
```

## 快速开始

克隆仓库：

```sh
git clone https://github.com/bosprimigenious/autoresearch-skills.git
cd autoresearch-skills
```

将需要的 Skill 软链到 Agent 的用户级 Skill 目录。以 Codex 为例：

```sh
ln -s "$PWD/skills/autoresearch-task-qa" \
  ~/.codex/skills/autoresearch-task-qa
```

重启 Agent，让它重新发现 Skill。随后可以直接用自然语言提出任务，例如：

```text
检查这个研究任务是否真的存在优化空间，并指出伪研究自由度。
审查这个 baseline 是否公平、可复现，缺什么证据就明确判失败。
把这个代码仓整理成可以交给多个 Agent 隔离运行的研究任务。
对交付包执行完整 QA，并生成下一位 Agent 能继续执行的交接。
```

仓库同时提供 `SKILL.md`、`AGENTS.md` 与 `CLAUDE.md` 派生格式，便于接入支持相应规则文件的 Coding Agent。不要复制多份后分别修改；选择一份工作树作为事实来源，其余目录使用软链。

## 可执行验证

项目不是靠 README 自证。仓库提供结构校验、派生格式漂移检查、隐私扫描、静态 QA 与回归测试：

```sh
python3 scripts/validate_skills.py
python3 scripts/sync_formats.py --check
python3 scripts/privacy_scan.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s skills/autoresearch-task-qa/scripts -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s skills/autoresearch-paper-discovery/scripts -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s skills/autoresearch-run-isolation/scripts -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s scripts -p 'test_*.py'
```

GitHub Actions 会在每次 push 和 pull request 上执行同一组检查。

`privacy_scan.py` 是 fail-closed 的公开发布门禁：除普通文本外，它会递归检查 ZIP、DOCX、PPTX、XLSX、ODF、JAR 与 wheel 的成员路径和内容，提取不透明二进制中的 ASCII/UTF-16 元数据，并阻断敏感文件名、凭据赋值、私有协作链接和带签名参数的 capability URL。损坏、加密、超限、嵌套过深或含符号链接的归档不会被静默跳过。诊断只输出类别、脱敏位置和行号，不输出命中值。`example.com` 邮箱、环境变量引用和 `YOUR_API_KEY` 一类显式占位符保留为合法公共示例；占位符不能用于豁免归档结构错误。

## 证据边界

这套仓库能够验证的是 Skill 结构、任务契约和静态 QA 逻辑。它**不会**把以下事项伪装成已经完成：

- Docker 镜像确实能够构建并运行；
- 外部研究平台或 Harbor 接口确实可用；
- 真实训练已经完成并达到目标指标；
- 数据、模型、许可证或第三方材料具备公开授权；
- 静态扫描能够替代人工隐私与商业秘密复核。

运行时成功必须由运行时证据证明；公开发布必须逐件检查主包、self-check、轨迹和证据附件。详细门禁见 [`privacy-and-portability.md`](skills/autoresearch-task-qa/references/privacy-and-portability.md)。

## 仓库结构

```text
autoresearch-skills/
├── skills/                  # 七个可组合的 AutoResearch Skill
│   └── <skill>/
│       ├── SKILL.md         # 唯一规则源
│       ├── AGENTS.md        # Agent 兼容格式
│       ├── CLAUDE.md        # Claude Code 兼容格式
│       ├── agents/          # Agent 元数据
│       ├── references/      # 规范、清单与方法参考
│       ├── assets/          # 可复制的通用模板（按需）
│       └── scripts/         # 静态 QA 与测试（按需）
├── scripts/
│   ├── validate_skills.py   # 仓库级结构校验
│   ├── sync_formats.py      # 从 SKILL.md 生成兼容格式
│   └── privacy_scan.py      # 不回显命中值的隐私门禁
└── .github/workflows/ci.yml # 持续集成门禁
```

仓库只包含通用规则、参考文档与静态检查代码，不包含真实任务包、对话记录、模型权重、凭据或私有平台附件。

## License

[MIT](LICENSE)
