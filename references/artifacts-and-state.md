# 文件与状态约定

**分支说明：** 下方含 styleboards/reference/backgrounds/foregrounds 的目录结构仅对 A 适用。B 需要 `project.json`、双预览 `previews/B1.png`、`previews/B2.png`、用户确认状态，以及按选择生成的 `B1/slide-XX.png` 与/或 `B2/slide-XX.png`；双方选择 both 则有两套独立全页图片，不强制建立 A 的目录。见 [B 分支](image-fast-path.md)。

## 推荐项目目录（示例）

```
workspace/<project_id>/
  project.json                  # 唯一事实源（可使用 assets/project-template.json）
  styleboards/01.png ... 08.png
  reference/slide-01.png ...
  assets/backgrounds/*.png
  assets/foregrounds/*.png
  builds/<build_id>/deck.pptx
  builds/<build_id>/deck.pdf
  builds/<build_id>/preview/slide-01.png ...
  builds/<build_id>/qa-report.json
```

素材引用用相对路径；同一构建版本绑定同一 `build_id`。保存每个产物的 SHA-256，禁止拿旧 PDF/图片冒充最新 PPTX 的导出。可选 `manifest` 字段记录 `build_id`, `source_build_id`, `renderer`, `export_timestamp`, `actual_verification`。

## 各模式交付
- `workflow_branch=B`: 先双预览并由用户确认 B1/B2/both，再交付指定的一套或两套有序高清图片；both 需要两个独立版本目录与独立 QA；除非用户要求，否则不生成 PPTX/PDF，也不需要 A 的分层工程包。
- `editable`: 真实可编辑 `.pptx`、全页预览；按需 `.pdf`、可重建素材和动画描述。
- `image`（A 的图片模式或 B）：逐页图片是 B 的默认交付；仅在明确需要时封装为纯图片 `.pptx`（按需 PDF），必须明确“不能分层编辑”，禁止夸大。
- `hybrid`: `.pptx` 与按页的编辑性边界表，明确 `flattened` 素材。
- `pdf-only`: PDF 与按需预览，不声称 PPTX 已有。
- `review`: QA报告、已修改文件和差异说明；修改后仍执行受影响页面验证。

## 跨环境运行
工程所需生成/渲染/校验工具因Agent而异。优先使用实际可运行的工具组合；不把某一种Python/PPT生成库写死为工作流必要条件。若某项条件无法满足，精确说明影响范围并给出能诚实交付的产物。

## B v2.2 推荐文件结构

```text
workspace/<project_id>/
  project.json             # workflow_branch=B; b_generation_mode/B 预览与用户确认状态
  previews/B1.png          # 同一正式内容页的 B1（不加 Skill 内置画质约束）
  previews/B2.png          # 同页 B2（追加固定自然真实照片质感约束）
  B1/slide-01.png ...      # 仅 B1 或 both 选项时存在完整图片集
  B2/slide-01.png ...      # 仅 B2 或 both 选项时存在完整图片集
  qa-report.json           # 各版本独立检查结果
```

推荐使用 `assets/image-branch-template.json`（schema 1.2）；`gates.b_previews_generated` 表示两张预览实际生成，`gates.b_variant_confirmed` 表示用户看过预览并批准具体生成范围。不得在确认前为默认 both 预置已批准状态。
