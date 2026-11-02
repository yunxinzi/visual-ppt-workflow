# Visual PPT Workflow

**A high-fidelity, editable presentation design workflow as a portable Agent Skill.**

[简体中文](#中文说明) · [English](#english) · [Gemini 安装指南](INSTALL_GEMINI.md) · [Agent Skill 规范](SKILL.md)

## 中文说明

这是一个基于真实 PPT 制作迭代经验构建的开源 Agent Skill，支持 **8 套可视化风格探索、完整图稿人工审核、复杂样页试装、真实分层可编辑 PPTX、动画预规划、逐页对照验收、断点续作**。

> 注意：它是**工作流与验收标准**，不是独立的图片生成模型或 PowerPoint 引擎。实际生图、PPTX 拼装、动画和实播测试取决于你使用的 Agent 工具；不得虚构未完成的步骤。

### Gemini CLI 一条命令安装

```bash
gemini skills install https://github.com/yunxinzi/visual-ppt-workflow.git
```

Gemini CLI 安装后运行 `/skills list` 验证，并在使用时批准技能激活。详细操作见 [INSTALL_GEMINI.md](INSTALL_GEMINI.md)。

### Gemini 网页版

Gemini Apps 支持上传包含根目录 `SKILL.md` 的 ZIP 来创建 Skill。**在网页聊天中粘贴 GitHub 链接不等于持久安装。** 下载此仓库并将所有文件打包（`SKILL.md` 必须处于 ZIP 根目录），在 `Customize → Skills → Create → Upload` 上传。

### 使用方式

直接告诉支持 Skill 的 Agent：“为我制作一份关于 XXX 的 12 页 PPT，启用 visual-ppt-workflow，先给我 8 套视觉预览供审核。”  

主要流程：**DEFINE → EXPLORE → PILOT → ARTWORK → REBUILD → VERIFY → DELIVER**

### 支持模式

- `editable`：可编辑原生文字、简单对象与独立前景（默认）。
- `image`：图像版 PPTX，明确声明不具有逐元素编辑性。
- `hybrid`：背景图片加可编辑文字与前景素材。
- `review`：已有幻灯片质量审查和局部优化。
- `pdf-only`：明确只需 PDF 时可直接交付该格式。

### 目录说明

- [SKILL.md](SKILL.md)：入口与不可跳过的阶段 Gate。
- [references/](references/)：视觉、分层、动画、验收与恢复规范。
- [scripts/](scripts/)：辅助结构审核及图像差异检测。
- [tests/](tests/)：标准库单元测试。
- [history/](history/)：原始工作流演进历史（供追溯，非现行规范）。
- [GEMINI_CHAT_PROMPT.md](GEMINI_CHAT_PROMPT.md)：可复制的安装提示词。

### 基础校验

```bash
python3 scripts/validate_skill.py .
python3 scripts/validate_project.py assets/project-template.json
python3 -m unittest discover -s tests -v
```

## English

An Agent Skills compatible workflow for faithful, high-quality slide design. It mandates eight genuinely different style previews, approval of the whole visual deck, genuine object layering, optional animation planning, incremental repairs, and verifiable final delivery.

**Install for Gemini CLI:**

```bash
gemini skills install https://github.com/yunxinzi/visual-ppt-workflow.git
```

For Gemini web, import a ZIP with `SKILL.md` at its root. Refer to [INSTALL_GEMINI.md](INSTALL_GEMINI.md) for setup and limitations.

## License

[MIT](LICENSE).
