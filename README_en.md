# gaiduo-ppt

[中文](README.md) | [English](README_en.md)

`gaiduo-ppt` is a custom Codex skill for turning source documents—such as research reports, business analyses, financial reports, industry reports, course materials, Markdown, PDF, or DOCX files—into narrative, visually polished, high-fidelity HTML presentations.

It is designed for users who want more than a plain document-to-webpage conversion: the workflow first builds a presentation outline, then explores visual directions, produces high-resolution page references, and finally implements a browser-based HTML slide deck.

## Key Features

- Four-stage workflow: outline, visual exploration, production design, and HTML hybrid rendering.
- Content-first process: the outline stage focuses on narrative and slide copy without constraining visual design too early.
- Product Design visual exploration: generate multiple full-deck visual directions before choosing one.
- High-fidelity hybrid rendering: final slides combine visible HTML text, SVG / CSS / Canvas charts, and local image modules.
- Anti-regression rules: Stage 3 full-page reference images must not be used as full-page HTML backgrounds.
- Detail fidelity: micro-icons, dotted lines, leader lines, nodes, flywheels, pyramids, and other structural details are explicitly checked.

## Installation

In Codex, ask Codex to install this skill directly from the GitHub repository:

```text
Install this skill:
https://github.com/gaiduo/gaiduo-ppt
```

Restart Codex, or start a new Codex session, then invoke the skill with `$gaiduo-ppt`.

## Workflow

### Stage 1: Presentation Outline

Codex reads the source document and turns it into a slide-ready presentation outline.

This stage focuses on:

- identifying the core conclusion of the deck;
- building a coherent narrative structure;
- keeping each slide focused on one main idea;
- writing slide titles, key points, page content, and supporting evidence;
- avoiding visual suggestions so later visual exploration remains unconstrained.

Stage 1 pauses for user confirmation before moving forward.

Example prompt:

```text
Use $gaiduo-ppt to turn this report into an HTML presentation.
```

### Stage 2: Visual Direction Exploration

After the outline is confirmed, Codex uses Product Design to explore three distinct full-deck visual directions.

This stage usually outputs:

- direction 1 mosaic;
- direction 2 mosaic;
- direction 3 mosaic.

Each mosaic covers the full deck and helps the user judge the overall visual system, slide rhythm, chart language, image style, topic fit, and design quality.

Stage 2 does not generate HTML.

### Stage 3: High-Resolution Page References and Production Materials

After the user selects a visual direction, Codex turns that direction into production-ready materials for high-fidelity HTML implementation.

Stage 3 outputs:

- `final_content_spec.md`;
- `visual_lock_spec.md`;
- `visual_detail_contract.md`;
- `rendering_strategy.md`;
- `asset_plan.json`;
- high-resolution page references such as `slide_01.png`;
- local image assets under `assets/production/`.

This stage is not a redesign step. It locks the selected direction and prepares the materials needed for faithful implementation.

### Stage 4: HTML Presentation Implementation

After Stage 3 is confirmed, Codex builds the final HTML slide deck.

Stage 4 includes:

- extracting the HTML design system;
- implementing slides;
- using visible HTML for titles, body text, numbers, and units;
- implementing controllable charts with SVG / CSS / Canvas when appropriate;
- embedding complex illustrations, product images, maps, scenes, textures, or brand visuals as local image modules;
- comparing browser screenshots against Stage 3 references;
- fixing P0 / P1 / P2 issues;
- testing navigation, page numbers, fullscreen mode, and scaling.

Stage 4 must not:

- use full-page Stage 3 references as HTML backgrounds;
- hide real text in a transparent semantic layer;
- replace complex visuals with simplified icons;
- replace information icons with plain text, emoji, or punctuation;
- omit dotted lines, leader lines, endpoints, or node anchors;
- break the geometry of pyramids, flywheels, funnels, or loop diagrams.

## Typical Usage

The simplest way to use the skill is:

```text
Use $gaiduo-ppt to turn this report into an HTML presentation.
```

For better results, use staged confirmation:

1. Upload the source document and generate the presentation outline.
2. Confirm or revise the outline.
3. Generate three visual directions.
4. Select one direction.
5. Generate high-resolution page references and production materials.
6. Confirm the page references.
7. Generate the final HTML presentation.

## Output Structure

Typical output structure:

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

## Design Philosophy

`gaiduo-ppt` follows this principle:

> Visual quality first, HTML editability second. Titles, body text, and numbers must be real visible HTML; complex illustrations, product images, maps, scenes, and textures may be embedded as local image modules for fidelity.

In short, the skill aims to balance presentation-grade visual quality with reliable HTML-based content.
