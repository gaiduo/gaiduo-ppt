#!/usr/bin/env python3
"""Validate a gaiduo-ppt Stage 3 asset/rendering plan."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

IMAGE_METHODS = {"raster", "visual-module"}
METHODS = {"html-text", "chart", "svg-css", "raster", "visual-module"}
SLIDE_REFERENCE_RE = re.compile(r"(^|/)(stage3_production/)?slides/slide_\d+\.(png|jpg|jpeg|webp)$", re.I)
SLIDE_BASENAME_RE = re.compile(r"^slide_\d+\.(png|jpg|jpeg|webp)$", re.I)
CANVAS_WIDTH = 1920
CANVAS_HEIGHT = 1080


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("plan", help="asset_plan.json path")
    parser.add_argument("--project-root", default=".", help="Project root for source path checks")
    parser.add_argument("--allow-planned", action="store_true")
    return parser.parse_args()


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def is_stage3_slide_reference(source: str) -> bool:
    normalized = source.replace("\\", "/")
    return bool(SLIDE_REFERENCE_RE.search(normalized) or SLIDE_BASENAME_RE.match(Path(normalized).name))


def is_near_full_slide_box(box: Any) -> bool:
    if not (isinstance(box, list) and len(box) == 4 and all(isinstance(v, (int, float)) for v in box)):
        return False
    _x, _y, width, height = box
    return width >= CANVAS_WIDTH * 0.88 and height >= CANVAS_HEIGHT * 0.88


def has_detail_contract(element: dict[str, Any]) -> bool:
    contract = element.get("detail_contract")
    if not isinstance(contract, dict):
        return False
    keys = {"micro_icons", "connectors", "geometry_topology", "topology", "qa_items"}
    return any(contract.get(key) for key in keys)


def main() -> int:
    args = parse_args()
    plan_path = Path(args.plan)
    root = Path(args.project_root)
    plan = json.loads(plan_path.read_text(encoding="utf-8"))

    pages = as_list(plan.get("pages"))
    failures: list[str] = []
    user_authorized_full_slide_raster = bool(plan.get("user_authorized_full_slide_raster"))
    full_slide_reason = str(plan.get("full_slide_raster_reason", "")).strip()

    if not pages:
        failures.append("asset_plan.json must contain non-empty pages[]")

    if user_authorized_full_slide_raster and len(full_slide_reason) < 12:
        failures.append("user_authorized_full_slide_raster=true requires a clear full_slide_raster_reason")

    for page in pages:
        page_id = page.get("page_id", "unknown-page")
        elements = as_list(page.get("elements"))
        if not elements:
            failures.append(f"{page_id}: elements[] is empty")
            continue

        primary = [e for e in elements if e.get("role") == "primary"]
        if not primary:
            failures.append(f"{page_id}: no primary element")

        for element in elements:
            element_id = element.get("id", "unknown-element")
            label = f"{page_id}/{element_id}"
            method = element.get("method")
            role = element.get("role")
            status = element.get("status", "planned")

            if method not in METHODS:
                failures.append(f"{label}: invalid method {method!r}")
            if role not in {"primary", "supporting", "decorative"}:
                failures.append(f"{label}: invalid role {role!r}")
            if status not in {"planned", "ready"}:
                failures.append(f"{label}: invalid status {status!r}")
            if status != "ready" and not args.allow_planned:
                failures.append(f"{label}: status is not ready")

            box = element.get("target_box")
            if not (isinstance(box, list) and len(box) == 4 and all(isinstance(v, (int, float)) for v in box)):
                failures.append(f"{label}: target_box must be [x, y, width, height]")

            simplification_allowed = element.get("simplification_allowed")
            regeneration_allowed = element.get("regeneration_allowed")
            fidelity_critical = bool(element.get("fidelity_critical"))

            if method in IMAGE_METHODS:
                source = element.get("source")
                if not source:
                    failures.append(f"{label}: image/module element missing source")
                else:
                    if is_stage3_slide_reference(str(source)) and not user_authorized_full_slide_raster:
                        failures.append(f"{label}: cannot use Stage 3 full-slide reference as runtime asset: {source}")
                    if status == "ready" and not (root / source).exists():
                        failures.append(f"{label}: source file not found: {source}")
                if element.get("fit") not in {"contain", "cover", "stretch-forbidden"}:
                    failures.append(f"{label}: image/module fit must be contain, cover, or stretch-forbidden")
                if regeneration_allowed is not False:
                    failures.append(f"{label}: image/module must set regeneration_allowed=false")
                if is_near_full_slide_box(box) and not user_authorized_full_slide_raster:
                    failures.append(f"{label}: near full-slide image/module is forbidden without user_authorized_full_slide_raster=true")
                if role in {"primary", "supporting"} and method in IMAGE_METHODS and element.get("source_role") == "stage3-reference" and not user_authorized_full_slide_raster:
                    failures.append(f"{label}: source_role=stage3-reference cannot be used as runtime asset")

            if role in {"primary", "supporting"} and simplification_allowed is not False and fidelity_critical:
                failures.append(f"{label}: fidelity-critical element cannot allow simplification")

            if method == "html-text" and element.get("source"):
                failures.append(f"{label}: html-text should not point to an image source")

            if method in {"chart", "svg-css"} and fidelity_critical and role in {"primary", "supporting"}:
                if not has_detail_contract(element):
                    failures.append(f"{label}: fidelity-critical chart/svg-css requires non-empty detail_contract")
                contract = element.get("detail_contract") if isinstance(element.get("detail_contract"), dict) else {}
                if contract.get("text_substitution_forbidden") is False:
                    failures.append(f"{label}: detail_contract cannot allow text substitution for fidelity-critical chart/svg-css")

    if failures:
        print("FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
