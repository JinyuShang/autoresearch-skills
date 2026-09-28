# AutoResearch Skills

一组可复用的 AutoResearch 任务设计、运行隔离、质量审查和交接 skill。仓库只包含通用规则、参考文档与静态检查脚本，不包含真实任务包、对话记录、模型权重或私有平台附件。

## Skills

- `autoresearch-optimization-surface`：判断研究任务是否具有真实方法空间，而非仅搜索固定超参数。
- `autoresearch-baseline-quality`：审查 Baseline 的合理性、公平预算与可复现性。
- `autoresearch-task-authoring`：把论文或代码仓整理成可交付的工程研究任务。
- `autoresearch-run-isolation`：隔离多 Agent 运行、凭据、证据和有效时长。
- `autoresearch-task-qa`：审查研究门槛、提交结构、Docker/Harbor 路径和成对证据。
- `autoresearch-conversation-handoff`：生成可继续执行的跨 Agent 交接。

## 安装

克隆仓库后，将需要的 skill 目录软链到工具的用户级 skill 目录。以 Codex 为例：

```sh
git clone https://github.com/bosprimigenious/autoresearch-skills.git
ln -s /absolute/path/autoresearch-skills/skills/autoresearch-task-qa ~/.codex/skills/autoresearch-task-qa
```

不要复制多份后分别修改；选择一份工作树作为事实来源，其余工具目录使用软链。

## 验证

```sh
python3 scripts/validate_skills.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s skills/autoresearch-task-qa/scripts -p 'test_*.py'
```

测试验证 skill 结构与静态 QA 逻辑，不代表外部 Harbor 平台、Docker 构建或真实训练已经运行成功。

## 隐私边界

公开材料必须逐件检查，不能用主包通过替代 self-check、轨迹或证据附件。详细门禁见 [`privacy-and-portability.md`](skills/autoresearch-task-qa/references/privacy-and-portability.md)。许可证、数据授权、真实身份信息和商业秘密仍需人工复核。

## License

[MIT](LICENSE)
