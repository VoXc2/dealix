"""Agentic Enterprise — AI Operating Fabric router.

Exposes the 12-layer fabric: the organizational nervous-system index that
maps each layer of the agentic enterprise to the packages implementing it,
with a real, on-disk health signal (no fake proof).

Endpoints:
  GET /api/v1/agentic-enterprise/fabric          → full 12-layer rollup
  GET /api/v1/agentic-enterprise/layers          → static layer descriptors
  GET /api/v1/agentic-enterprise/layers/{number} → one layer + health
  GET /api/v1/agentic-enterprise/maturity        → maturity score + grade
  GET /api/v1/agentic-enterprise/markdown        → bilingual AR+EN render
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse

from auto_client_acquisition.agentic_enterprise_os import (
    FABRIC_LAYERS,
    fabric_status,
    layer_by_number,
    layer_to_dict,
    maturity_score,
    resolve_layer_health,
)

router = APIRouter(
    prefix="/api/v1/agentic-enterprise", tags=["agentic-enterprise"]
)


@router.get("/fabric")
async def get_fabric() -> dict[str, Any]:
    """Full 12-layer rollup with per-layer health and overall maturity."""
    return fabric_status()


@router.get("/layers")
async def list_layers() -> dict[str, Any]:
    """Static descriptors for all 12 fabric layers."""
    return {
        "layer_count": len(FABRIC_LAYERS),
        "layers": [layer_to_dict(layer) for layer in FABRIC_LAYERS],
        "governance_decision": "allow",
    }


@router.get("/layers/{number}")
async def get_layer(number: int) -> dict[str, Any]:
    """One layer: static descriptor + resolved on-disk health."""
    layer = layer_by_number(number)
    if layer is None:
        raise HTTPException(status_code=404, detail="layer_not_found")
    return {
        **layer_to_dict(layer),
        "health": resolve_layer_health(layer),
        "governance_decision": "allow",
    }


@router.get("/maturity")
async def get_maturity() -> dict[str, Any]:
    """Overall fabric maturity score and grade."""
    status = fabric_status()
    return {
        "maturity_score": maturity_score(),
        "maturity_grade": status["maturity_grade"],
        "layer_count": status["layer_count"],
        "layers_operational": status["layers_operational"],
        "governance_decision": "allow",
    }


@router.get("/markdown", response_class=PlainTextResponse)
async def fabric_markdown() -> str:
    """Bilingual AR+EN render of the 12-layer operating fabric."""
    status = fabric_status()
    lines: list[str] = []
    lines.append("# Dealix AI Operating Fabric — نسيج التشغيل الذكي")
    lines.append("")
    lines.append(
        f"_Maturity: {status['maturity_score']} · "
        f"Grade: {status['maturity_grade']} · "
        f"{status['layers_operational']}/{status['layer_count']} layers operational_"
    )
    lines.append("")
    lines.append(
        "The 12-layer index that turns scattered OS packages into one "
        "governed organizational nervous system. Humans stay over the loop."
    )
    lines.append("")
    lines.append("---")
    lines.append("")

    health_by_number = {ly["number"]: ly for ly in status["layers"]}
    for layer in FABRIC_LAYERS:
        health = health_by_number[layer.number]
        lines.append(
            f"## Layer {layer.number} — {layer.title_en} · {layer.title_ar}"
        )
        lines.append("")
        lines.append(
            f"- **Status:** {health['status']} "
            f"({health['packages_present']}/{health['packages_total']} packages)"
        )
        lines.append(f"- **Mandate (EN):** {layer.mandate_en}")
        lines.append(f"- **التفويض (AR):** {layer.mandate_ar}")
        lines.append("- **Packages:**")
        for pkg, present in health["packages"].items():
            mark = "✓" if present else "✗"
            lines.append(f"  - `{pkg}` {mark}")
        lines.append(f"- **Capabilities:** {', '.join(layer.capabilities)}")
        lines.append("")
        lines.append("---")
        lines.append("")

    lines.append(
        "_Estimated outcomes are not guaranteed outcomes / "
        "النتائج التقديرية ليست نتائج مضمونة._"
    )
    return "\n".join(lines)
