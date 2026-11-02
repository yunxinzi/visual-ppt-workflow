# Visual PPT Workflow

**An A/B-routed Agent Skill for animated editable presentations OR direct high-quality slide images.**

[简体中文](#中文说明) · [English](#english) · [Gemini 安装指南](INSTALL_GEMINI.md) · [Agent Skill 规范](SKILL.md)

## 中文说明

这是基于真实 PPT 制作迭代经验的开源 Agent Skill。**新建 PPT 前先问是否需要动画，由用户选择 A/B；A 执行原完整流程，B 跳过原流程，直接批量生成整页图片。** 两种路线各有独立交付和验收规则。

> 注意：它是**工作流与验收标准**，不是独立的图片生成模型或 PowerPoint 引擎。实际生图、PPTX 拼装、动画和实播测试取决于你使用的 Agent 工具；不得虚构未完成的步骤。

### 核心改动：先选 A / B

每个新建 PPT 任务在任何制作动作之前，先向用户询问：

> **本次 PPT 是否需要做动效或动画？**
>
> **A｜需要动画**：进入原流程，包含 8 套真实风格预览、人工选版、完整图稿审核、真分层可编辑 PPTX、动画与逐页 QA。
>
> **B｜不需要动画**：推荐直接批量生图。无需将画面拆成可动画对象，通常能更完整保留画质与细节；**不再执行 A 的八套选版、完整图稿审批、可编辑拼装和动画流程**。默认交付逐页高质量图片集；仅当用户要求时才按每页一图封装 PPTX/PDF。图片页无法逐项编辑。

用户已有明确分支选择或正在续作时不重问，审阅/修订已有文件也不重复选择。详细见 [分支路由](references/branch-routing.md) 和 [B 直接生图](references/image-fast-path.md)。

### Gemini CLI 一条命令安装

```bash
gemini skills install https://github.com/yunxinzi/visual-ppt-workflow.git
```

Gemini CLI 安装后运行 `/skills list` 验证，并在使用时批准技能激活。详细操作见 [INSTALL_GEMINI.md](INSTALL_GEMINI.md)。

### Gemini 网页版

Gemini Apps 支持上传包含根目录 `SKILL.md` 的 ZIP 来创建 Skill。**在网页聊天中粘贴 GitHub 链接不等于持久安装。** 下载此仓库并将所有文件打包（`SKILL.md` 必须处于 ZIP 根目录），在 `Customize → Skills → Create → Upload` 上传。

### 使用方式

直接告诉支持 Skill 的 Agent：“为我制作一份关于 XXX 的 12 页 PPT，启用 visual-ppt-workflow。请先问我是否需要动画，让我选择 A 或 B。”  

主要流程：**ROUTE A/B**；A：**DEFINE → EXPLORE → PILOT → ARTWORK → REBUILD → VERIFY → DELIVER**；B：**IMAGE_GENERATE → IMAGE_QA → IMAGE_DELIVER**

### 支持模式

- `A/editable`：A 的默认模式，可编辑原生文字、简单对象与独立前景。
- `B/image`：B 的默认交付为图片集；用户如需 PPTX，仅封装图片，声明不具有逐元素编辑性。
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
python3 scripts/validate_project.py assets/image-branch-template.json
python3 -m unittest discover -s tests -v
```

## English

An Agent Skills compatible presentation workflow. **Before creating a new deck, ask the user to choose A (animation; original multi-gate editable workflow) or B (no animation; directly batch-generate finished slide images, bypassing the original workflow).** B produces non-editable image slides unless explicitly converted to flattened PPTX/PDF.

**Install for Gemini CLI:**

```bash
gemini skills install https://github.com/yunxinzi/visual-ppt-workflow.git
```

For Gemini web, import a ZIP with `SKILL.md` at its root. Refer to [INSTALL_GEMINI.md](INSTALL_GEMINI.md) for setup and limitations.

## License

[MIT](LICENSE).
