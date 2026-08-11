# gaiduo-ppt

[中文](README.md) | [English](README_en.md)

`gaiduo-ppt` 是一个用于 Codex 的自定义 Skill，目标是把用户提供的研究报告、商业分析、财报分析、行业报告、课程文档、Markdown / PDF / DOCX 等材料，制作成叙事清楚、视觉精美、高保真还原的 HTML 版 PPT。

它适合这类场景：

- 把一份未经演示化处理的研究报告转成可演示的 HTML 幻灯片；
- 为商业分析、品牌研究、行业报告、财报解读制作视觉化演示稿；
- 先探索多种视觉方向，再生成逐页高清视觉稿，最后还原成可在浏览器中播放的 HTML PPT；
- 希望最终页面既有较强设计感，又保留标题、正文、数字和图表文字的 HTML 可读性。

## 核心特点

- 四阶段工作流：演示大纲、视觉方向探索、逐页视觉定稿、HTML 混合还原。
- 内容先行：先把文档转成演示大纲，不提前限制视觉设计。
- Product Design 视觉探索：先生成 3 种完整视觉方向，供用户选择。
- 高保真混合还原：最终 HTML 不追求全部代码化，而是结合真实 HTML 文本、SVG / CSS 图表和局部图片模块。
- 防止视觉退化：禁止把阶段三整页视觉稿直接作为 HTML 页面背景。
- 细节保真：对小图标、虚线、引线、节点、飞轮、金字塔等细节建立专门检查机制。

## 安装方法

把 `gaiduo-ppt` 文件夹复制到 Codex 的 skills 目录下：

```bash
cp -R gaiduo-ppt ~/.codex/skills/gaiduo-ppt
```

如果已经安装过旧版本，可以用：

```bash
rsync -a --delete gaiduo-ppt/ ~/.codex/skills/gaiduo-ppt/
```

安装后重启 Codex，或开启新的 Codex 会话，即可用 `$gaiduo-ppt` 调用。

## 工作流程

### 阶段一：生成演示大纲

Codex 会先阅读源文档，把原始报告转化为适合 PPT 的演示大纲。

阶段一重点处理：

- 提炼整套演示的核心结论；
- 建立连贯叙事结构；
- 控制每页只表达一个核心观点；
- 输出每页标题、核心观点、页面内容和关键数据与证据；
- 不输出视觉建议，避免限制后续视觉设计。

阶段一完成后会暂停，等待用户确认大纲。

示例指令：

```text
使用 $gaiduo-ppt 将这份报告制作成 HTML 版 PPT。
```

或者更具体地说：

```text
使用 $gaiduo-ppt 阅读我上传的研究报告，先生成适合 HTML 版 PPT 的演示大纲。完成大纲后暂停，不要生成视觉稿或 HTML。
```

### 阶段二：探索视觉方向

大纲确认后，Codex 会使用 Product Design 为整套 PPT 探索 3 种不同视觉方向。

阶段二通常输出：

- 方向 1 拼图；
- 方向 2 拼图；
- 方向 3 拼图。

每张拼图覆盖整套 PPT 的全部页面，用于判断：

- 整体视觉风格；
- 页面节奏；
- 图表语言；
- 图片 / 插画 / 纹理语言；
- 主题匹配度；
- 是否有足够设计感。

阶段二只做视觉方向选择，不生成 HTML。

示例指令：

```text
大纲确认。使用 Product Design，根据已经确认的演示大纲，为这份 HTML 版 PPT 探索 3 种不同的完整视觉方向。只展示 3 张整套拼图，不要生成逐页高清视觉稿，也不要编写 HTML。
```

### 阶段三：生成逐页高清视觉稿和生产资料

用户选择一个视觉方向后，Codex 会把该方向产品化，生成可供 HTML 高保真还原的生产资料。

阶段三会输出：

- `final_content_spec.md`：最终文字、数据、单位和页面内容规范；
- `visual_lock_spec.md`：视觉锁定清单；
- `visual_detail_contract.md`：细节保真合同；
- `rendering_strategy.md`：HTML 混合还原策略；
- `asset_plan.json`：素材和元素实现计划；
- `slide_01.png`、`slide_02.png` 等逐页高清视觉稿；
- `assets/production/` 中的局部图片素材。

阶段三不是重新设计，而是高保真延展用户选定的阶段二方向。

它会特别锁定：

- 页面构图；
- 主视觉；
- 图表类型；
- 图片和品牌素材；
- 小图标；
- 虚线、引线、端点、箭头；
- 金字塔、飞轮、漏斗、循环图等几何关系。

阶段三完成后会暂停，等待用户确认。

示例指令：

```text
我选择方向 1。请使用 $gaiduo-ppt 根据选定视觉方向生成全部页面的独立高清视觉稿，并建立 final_content_spec.md、visual_lock_spec.md、visual_detail_contract.md、rendering_strategy.md 和 asset_plan.json。完成后暂停，不要生成 HTML。
```

### 阶段四：生成 HTML 版 PPT

阶段三确认后，Codex 会根据高清视觉稿和生产资料生成 HTML 项目。

阶段四会连续完成：

- 提取 HTML 设计系统；
- 实现页面；
- 用真实 HTML 承载标题、正文、数字和单位；
- 用 SVG / CSS / Canvas 实现可控图表；
- 对复杂插画、产品图、地图、场景、纹理等使用局部图片模块保真嵌入；
- 截图对比阶段三高清视觉稿；
- 修复 P0 / P1 / P2 问题；
- 测试翻页、页码、全屏和窗口缩放；
- 输出完整 HTML 项目和 QA 记录。

阶段四禁止：

- 把整页高清视觉稿直接作为 HTML 页面背景；
- 用透明文字层伪装成真实 HTML；
- 把复杂视觉模块重画成简化图标；
- 用汉字、emoji、符号代替信息型小图标；
- 省略虚线、引线、端点、节点锚点；
- 让金字塔、飞轮等几何图形角度不统一或闭合关系错误。

示例指令：

```text
阶段三视觉稿确认。请使用 $gaiduo-ppt 根据已经确认的逐页高清视觉稿和生产资料，完成整套 HTML 版 PPT。阶段之间不要暂停，完成后交付 HTML 项目、截图和 QA 记录。不要发布到互联网。
```

## 典型使用方式

最简单的用法是直接把报告发给 Codex，并说：

```text
使用 $gaiduo-ppt 将这份报告制作成 HTML 版 PPT。
```

更推荐的方式是分阶段确认：

1. 上传报告，让 Codex 生成演示大纲；
2. 确认或修改大纲；
3. 让 Codex 生成 3 种视觉方向；
4. 选择一个视觉方向；
5. 生成逐页高清视觉稿和生产资料；
6. 确认视觉稿；
7. 生成最终 HTML 版 PPT。

这种方式更适合追求视觉效果和高保真还原的 PPT 制作场景。

## 输出目录

默认输出结构类似：

```text
outputs/<project-slug>/
├── gaiduo_ppt_state.md
├── source/
├── outline/
├── stage2_visual/
├── stage3_production/
│   ├── final_content_spec.md
│   ├── visual_lock_spec.md
│   ├── visual_detail_contract.md
│   ├── rendering_strategy.md
│   ├── asset_plan.json
│   ├── slides/
│   └── assets/production/
└── html/
    ├── index.html
    ├── assets/
    ├── screenshots/
    └── qa.md
```

## 适合与不适合的场景

适合：

- 商业研究报告；
- 行业分析；
- 公司案例拆解；
- 财报分析；
- 品牌研究；
- 课程讲义；
- 需要较强视觉表达的 HTML 演示稿。

不太适合：

- 只需要简单文字转网页；
- 不需要视觉设计的普通文档排版；
- 必须输出 `.pptx` 文件的场景；
- 要求所有图形都 100% 可编辑、不能使用任何图片模块的场景。

## 设计取向

`gaiduo-ppt` 的取向是：

> 视觉效果优先，HTML 可编辑性第二；标题、正文、数字必须是真 HTML；复杂插画、产品图、地图、场景、纹理可以作为图片模块保真嵌入。

也就是说，它不是把 PPT 全部转成纯代码图形，而是尽量在“高保真视觉效果”和“关键内容 HTML 化”之间取得平衡。
