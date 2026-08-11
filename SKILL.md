---
name: gaiduo-ppt
description: "将用户提供的 Markdown、PDF、DOCX、研究报告、商业分析、财报分析、行业报告、课程文档或其他材料制作成叙事清楚、视觉精美、高保真还原的 HTML 版 PPT。Use when the user asks to create, continue, revise, audit, or fix an HTML presentation, HTML slide deck, browser-based PPT, Product Design visual exploration, production visual references, or high-fidelity hybrid HTML implementation from a source document."
---

# gaiduo-ppt

`gaiduo-ppt` 用四阶段流程把文档制作成 HTML 版 PPT：演示大纲、视觉方向探索、视觉定稿与生产资料、HTML 混合还原。

## 底层原则

1. 内容先行：阶段一只做叙事和页面文案，不输出视觉建议。
2. 视觉大胆：阶段二只判断视觉方向、题材匹配、页面节奏和设计感，不因为 HTML 难做而提前降低设计质量。
3. 定稿保真：阶段三不是重新设计，而是把用户选定的阶段二方向高保真产品化。
4. 混合还原：最终 HTML 不是全部代码化。标题、正文、数字、单位必须是真 HTML；复杂插画、产品图、地图、场景、纹理、品牌视觉可以作为图片模块保真嵌入。
5. 执行分工：阶段四只执行，不重新设计。为了可编辑性牺牲已确认视觉质感属于失败。

## 阶段判断

根据用户请求和已有产物判断当前阶段，不要重启已完成工作：

1. 阶段一：已有源文档，但没有确认的演示大纲。
2. 阶段二：演示大纲已确认，但没有选定视觉方向。
3. 阶段三：视觉方向已选定，需要生成逐页高清视觉稿、视觉锁定清单、素材和混合还原策略。
4. 阶段四：阶段三产物已确认，需要生成 HTML 项目并逐页 QA。

如果用户只是咨询、分析或复盘问题，直接回答，不创建文件。

## 必读参考

只读取当前阶段所需文件，避免把旧规则全部塞进上下文：

- 阶段一：`references/stage-1-outline.md`
- 阶段二：`references/stage-2-visual-exploration.md`，以及 `references/visual-quality-standards.md`
- 阶段三：`references/stage-3-production-design.md`，以及 `references/hybrid-rendering.md`、`references/visual-detail-fidelity.md`
- 阶段四：`references/stage-4-html-rendering.md`，以及 `references/hybrid-rendering.md`、`references/visual-detail-fidelity.md`
- 所有文件产出任务：`references/output-spec.md`

读取所选参考文件后再行动。

## 阶段闸门

- 阶段一完成后展示演示大纲并暂停，等待用户确认。
- 阶段二完成后只展示 3 张视觉方向拼图并暂停，等待用户选择或修改。
- 阶段三完成后展示逐页高清视觉稿、视觉锁定清单、素材清单和混合还原策略并暂停，等待用户确认。
- 阶段四连续完成 HTML、截图、对比、修复和交付；只有文件缺失、权限不足、用户重大选择缺失时才暂停。

不得擅自跨越阶段闸门。

## Product Design 和图片生成

- 阶段二使用 Product Design 进行视觉方向探索。
- 阶段三使用 Product Design 或图像生成能力制作逐页高清视觉稿和缺失的生产素材，但必须以阶段二选定方向为视觉合同。
- 阶段四不得重新生成或替换已确认视觉素材；如素材不足，回到阶段三补齐。

## 输出目录

默认把项目产物放在：

`outputs/<project-slug>/`

创建或更新 `gaiduo_ppt_state.md`，记录当前阶段、确认产物、用户选择、待解决问题和下一步。

## 完成标准

最终 HTML 版 PPT 只有在以下条件满足时才算完成：

- 页面数量和顺序正确；
- 标题、正文、数字、单位和口径来自确认内容；
- 最终 HTML 与阶段三高清视觉稿逐页对比无 P0/P1/P2 问题；
- 复杂视觉模块没有被简化、重画或替换；
- 翻页、页码、全屏、窗口缩放和刷新状态正常；
- 交付 HTML 项目、素材、逐页最终截图、QA 记录和使用说明。

## 辅助脚本

- `scripts/validate_asset_plan.py`：检查阶段三的混合还原/素材计划是否存在缺失来源、可疑简化或不允许的重新生成。
- `scripts/validate_html_rendering.py`：检查阶段四 HTML 是否违规引用整页阶段三视觉稿、整页图片层或隐藏语义文字层。
