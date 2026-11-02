# Visual PPT Workflow

**An A/B-routed Agent Skill for animated editable presentations OR direct high-quality slide images.**

[简体中文](#中文说明) · [English](#english) · [Gemini 安装指南](INSTALL_GEMINI.md) · [Agent Skill 规范](SKILL.md)

## 中文说明

这是基于真实 PPT 制作迭代经验的开源 Agent Skill。**新建 PPT 前先选 A/B；A 保留原完整流程，B 先生成同一代表页的 B1（无内置画质约束）和 B2（固定真实照片质感约束）两张预览，经用户确认后仅生成 B1、仅生成 B2，或默认同时生成两套完整图片。** 两种路线各有独立交付和验收规则。

> 注意：它是**工作流与验收标准**，不是独立的图片生成模型或 PowerPoint 引擎。实际生图、PPTX 拼装、动画和实播测试取决于你使用的 Agent 工具；不得虚构未完成的步骤。

### 核心改动：先选 A / B

每个新建 PPT 任务在任何制作动作之前，先向用户询问：

> **本次 PPT 是否需要做动效或动画？**
>
> **A｜需要动画**：进入原流程，包含 8 套真实风格预览、人工选版、完整图稿审核、真分层可编辑 PPTX、动画与逐页 QA。
>
> **B｜不需要动画**：先对同一页生成两张独立预览——B1 不添加任何 Skill 内置画质/风格约束，B2 追加一条固定的自然真实照片质感约束。展示后询问**仅 B1 / 仅 B2 / 同时 B1+B2（默认）**；**必须得到用户确认才批量生图**。跳过 A 的八套选版、全稿审批、分层与动画；纯图片不能逐元素编辑。

用户已有明确分支选择或正在续作时不重问，审阅/修订已有文件也不重复选择。详细见 [分支路由](references/branch-routing.md) 和 [B 直接生图](references/image-fast-path.md)。

### B 子分支：两张同页对照 + 二次确认

1. B1：同样的主题、文案、比例和生成工具，**不添加 Skill 内置视觉画质约束**。
2. B2：在与 B1 相同的基础提示词末尾完整追加：
   > 画面保持干净自然的真实照片质感：不要数字噪点与彩色噪点，不要颗粒覆盖，不要过度锐化，不要 HDR 与油腻高光，不要蜡质表面，不要脏灰色调，不要假细节与压缩伪影。
3. 显示同一页的 B1/B2 两张独立预览图后，固定显示：
   > 可选择仅开始 B1 分支或者仅开始 B2 分支，默认是同时开始 B1 和 B2 生成。
4. **等待用户确认**。仅 B1 或仅 B2 = 完整一套；双版本（默认、确认后）= 两套完整 PPT 图片，分别输出 `B1/` 和 `B2/`，每套独立 QA。

[二级分支规范](references/image-fast-path.md) · [B1/B2 状态与确认 Gate](references/branch-routing.md)

### Gemini CLI 一条命令安装

```bash
gemini skills install https://github.com/yunxinzi/visual-ppt-workflow.git
```

Gemini CLI 安装后运行 `/skills list` 验证，并在使用时批准技能激活。详细操作见 [INSTALL_GEMINI.md](INSTALL_GEMINI.md)。

### Gemini 网页版

Gemini Apps 支持上传包含根目录 `SKILL.md` 的 ZIP 来创建 Skill。**在网页聊天中粘贴 GitHub 链接不等于持久安装。** 下载此仓库并将所有文件打包（`SKILL.md` 必须处于 ZIP 根目录），在 `Customize → Skills → Create → Upload` 上传。

### 使用方式

直接告诉支持 Skill 的 Agent：“为我制作一份关于 XXX 的 12 页 PPT，启用 visual-ppt-workflow。请先问我是否需要动画，让我选择 A 或 B。”  

主要流程：**ROUTE A/B**；A：**DEFINE → EXPLORE → PILOT → ARTWORK → REBUILD → VERIFY → DELIVER**；B：**B1/B2_PREVIEW → CONFIRM → IMAGE_GENERATE → IMAGE_QA → IMAGE_DELIVER**

### 支持模式

- `A/editable`：A 的默认模式，可编辑原生文字、简单对象与独立前景。
- `B/image`：先双预览与用户确认，然后按选定 B1/B2/both 交付 1 套或 2 套图片集；用户如需 PPTX，仅封装图片，声明不具有逐元素编辑性。
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

An Agent Skills compatible presentation workflow. **Before a new deck, ask A (animated editable workflow) or B (static slide images). B generates two independent previews of the same page: B1 adds no built-in quality/style constraints; B2 appends an exact fixed natural-photograph quality constraint. Present both previews and wait for user confirmation: B1 only, B2 only, or both full decks (default only AFTER explicit confirmation).** No A-specific styleboard/rebuild pipeline in B. Images are not element-editable.

**Install for Gemini CLI:**

```bash
gemini skills install https://github.com/yunxinzi/visual-ppt-workflow.git
```

For Gemini web, import a ZIP with `SKILL.md` at its root. Refer to [INSTALL_GEMINI.md](INSTALL_GEMINI.md) for setup and limitations.

## License

[MIT](LICENSE).
