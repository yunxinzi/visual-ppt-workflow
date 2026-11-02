# 发给 Gemini CLI 或 Antigravity 的安装请求（复制整段）

请安装公开的 GitHub Agent Skill：https://github.com/yunxinzi/visual-ppt-workflow 。它的入口为 `SKILL.md`，Skill 名称为 `visual-ppt-workflow`。若你使用 Gemini CLI，执行 `gemini skills install https://github.com/yunxinzi/visual-ppt-workflow.git`；若使用 Antigravity，请按官方 Skills 目录放置。安装前让我审核权限和来源。完成后用技能列表确认成功，加载 SKILL.md 与所需 references，报告当前真正可用和缺失的图片生成、PPTX 编辑、渲染、动画与实播工具。不允许声称未验证的事情。然后我会提供 PPT 主题。请先问我是否需要动画，要求明确选择 A 或 B；A 再按原七阶段执行，B 不进入原七阶段；须先为同一页生成 B1（无额外内置视觉约束）和 B2（追加固定自然真实照片质感约束）两张真实预览并展示，随后等待我确认仅 B1、仅 B2，或者默认双版本同时生成，不能先生成整套图片。

**说明：** Gemini 网页版请使用 Skills 导入 ZIP 的方式。聊天中阅读 GitHub 链接不等于安装持久 Skill。
