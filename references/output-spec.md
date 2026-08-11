# 输出规范

## 项目状态

文件产出任务必须创建或更新 `gaiduo_ppt_state.md`，记录：

- 项目名称和输出目录；
- 当前阶段；
- 源文档路径；
- 已确认的大纲、视觉方向、高清稿和 HTML 产物；
- 用户最新决策；
- 未解决问题；
- 下一步。

## 建议目录

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

## 文件命名

- 阶段二拼图：`direction_1.png`、`direction_2.png`、`direction_3.png`
- 阶段三高清稿：`slide_01.png`、`slide_02.png`
- HTML 截图：`html_slide_01.png`、`html_slide_02.png`

## QA 记录

QA 记录要区分 P0、P1、P2、P3，并说明每个问题的处理结果。

不要把未经过截图对比的结果称为“最终完成”。
