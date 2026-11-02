# Visual PPT Workflow

An [Agent Skills](https://agentskills.io/specification) compatible **two-branch workflow and QA toolkit** for slide creation. Every **new** presentation request first asks: **A — need animation?** Follow the original full workflow (8 style previews, approval, editable rebuild, animation). **B — no animation?** Directly batch-generate full-slide images; skip all A-specific gates and layer rebuilding. Image slides are not element-editable.

**This is not a turnkey AI slide generator.** It ships instructions, reference documents, and small standard-library audit utilities. Your agent must supply actual image-generation, PPTX editing/rendering, and PowerPoint/WPS playback tools. Do not claim validation that did not occur.

Workflow: **ROUTE → A: DEFINE → EXPLORE → PILOT → ARTWORK → REBUILD → VERIFY → DELIVER**, or **B: IMAGE_GENERATE → IMAGE_QA → IMAGE_DELIVER**. The eight-style and artwork approval gates apply to A only. Do not re-ask if a branch has already been chosen, or for review-only tasks. A flattened image PPTX/PDF is optional for B, not automatic.

Install by copying `visual-ppt-workflow/` into a supported Agent Skills directory (e.g., `.agents/skills/`). Read `SKILL.md` for the executable instructions. The full Chinese README explains the available modes: editable, image-only, hybrid, PDF-only, and review.

```bash
python3 scripts/validate_skill.py .
python3 scripts/validate_project.py assets/project-template.json
python3 scripts/validate_project.py assets/image-branch-template.json
python3 -m unittest discover -s tests -v
python3 scripts/audit_pptx.py /path/to/slides.pptx --mode editable
```

The PPTX tool is a structural risk scan, not a fidelity or editability certification; use actual target-application testing before asserting real compatibility.

License: MIT. Third-party assets must be licensed separately.
