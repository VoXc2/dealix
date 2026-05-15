"""Renders the enterprise layer validation report (text + JSON)."""

from __future__ import annotations

from typing import Any

from dealix.layer_validation.cross_layer import cross_layer_passed
from dealix.layer_validation.spec import ENTERPRISE_LAYERS
from dealix.layer_validation.validation_engine import READY, LayerResult, all_ready


def render_json(
    results: dict[str, LayerResult],
    cross_checks: list[dict[str, Any]],
) -> dict[str, Any]:
    """Machine-readable report."""
    return {
        "layers": [
            {
                "order": results[spec.id].order,
                "id": spec.id,
                "title": spec.title,
                "score": results[spec.id].score,
                "status": results[spec.id].status,
                "capped_by": results[spec.id].capped_by,
                "blockers": results[spec.id].blockers,
            }
            for spec in ENTERPRISE_LAYERS
        ],
        "cross_layer": cross_checks,
        "enterprise_layers_ready": all_ready(results) and cross_layer_passed(cross_checks),
    }


def render_report(
    results: dict[str, LayerResult],
    cross_checks: list[dict[str, Any]],
) -> str:
    """Human-readable layer-by-layer report (mirrors verify_dealix_ready.py)."""
    lines: list[str] = []
    lines.append("=== ENTERPRISE_LAYER_VALIDATION ===")
    for spec in ENTERPRISE_LAYERS:
        result = results[spec.id]
        name = spec.title.upper().replace(" & ", "_").replace(" ", "_")
        suffix = f" capped_by={result.capped_by}" if result.capped_by else ""
        lines.append(
            f"LAYER{result.order}_{name}={result.status} score={result.score}{suffix}"
        )

    lines.append("")
    lines.append("--- BLOCKERS ---")
    any_blockers = False
    for spec in ENTERPRISE_LAYERS:
        result = results[spec.id]
        if result.blockers:
            any_blockers = True
            lines.append(f"[{spec.id}]")
            for blocker in result.blockers:
                lines.append(f"  - {blocker}")
    if not any_blockers:
        lines.append("(none)")

    lines.append("")
    lines.append("--- CROSS_LAYER ---")
    for check in cross_checks:
        status = "PASS" if check["passed"] else "FAIL"
        lines.append(f"XLAYER_{check['gate']}={status} severity={check['severity']}")
        for blocker in check.get("blockers") or []:
            lines.append(f"  - {blocker}")

    ready = all_ready(results) and cross_layer_passed(cross_checks)
    lines.append("")
    built = sum(1 for r in results.values() if r.status == READY)
    lines.append(f"LAYERS_READY={built}/{len(ENTERPRISE_LAYERS)}")
    lines.append(f"ENTERPRISE_LAYERS_READY={'true' if ready else 'false'}")
    return "\n".join(lines)
