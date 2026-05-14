"""Capital Assets — Wave 19 (public + admin endpoints).

Surfaces Dealix's strategic Capital Asset registry. The PUBLIC endpoint
exposes ONLY assets explicitly marked `public=True` — what reviewers,
investors, and partners are allowed to see. The admin endpoint exposes
everything.

Endpoints:
  GET /api/v1/capital-assets               → admin: full registry
  GET /api/v1/capital-assets/public        → public: only public=True assets
  GET /api/v1/capital-assets/public/markdown → bilingual markdown of public assets
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse

from api.security.api_key import require_admin_key
from auto_client_acquisition.capital_os.capital_asset_registry import (
    CAPITAL_ASSETS,
    list_public_capital_assets,
)


router = APIRouter(prefix="/api/v1/capital-assets", tags=["capital-assets"])


def _asset_to_public_dict(a) -> dict[str, Any]:
    """Public exposure: omit any field that could leak commercial-sensitive data."""
    return {
        "asset_id": a.asset_id,
        "name": a.name,
        "type": a.type,
        "strategic_role": a.strategic_role,
        "buyer_relevance": list(a.buyer_relevance),
        "maturity": a.maturity,
        "proof_level": a.proof_level,
        "linked_non_negotiables": list(a.linked_non_negotiables),
        "last_reviewed": a.last_reviewed,
        # NOTE: file_paths + commercial_use intentionally omitted from PUBLIC view.
    }


def _asset_to_admin_dict(a) -> dict[str, Any]:
    return {
        "asset_id": a.asset_id,
        "name": a.name,
        "type": a.type,
        "strategic_role": a.strategic_role,
        "file_paths": list(a.file_paths),
        "buyer_relevance": list(a.buyer_relevance),
        "commercial_use": list(a.commercial_use),
        "maturity": a.maturity,
        "linked_non_negotiables": list(a.linked_non_negotiables),
        "proof_level": a.proof_level,
        "last_reviewed": a.last_reviewed,
        "public": a.public,
    }


@router.get("", dependencies=[Depends(require_admin_key)])
async def capital_assets_admin() -> dict[str, Any]:
    """Admin-gated full registry."""
    return {
        "version": "1.0",
        "wave": "19",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "asset_count": len(CAPITAL_ASSETS),
        "assets": [_asset_to_admin_dict(a) for a in CAPITAL_ASSETS],
        "governance_decision": "allow",
        "is_estimate": False,
    }


@router.get("/public")
async def capital_assets_public() -> dict[str, Any]:
    """Public — only assets explicitly marked public=True.

    Surfaces strategic-role + buyer-relevance + maturity + proof-level +
    linked non-negotiables. Does NOT expose file paths or commercial use
    (those stay in the admin view + the on-disk registry).
    """
    public_assets = list_public_capital_assets()
    return {
        "version": "1.0",
        "wave": "19",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "public_asset_count": len(public_assets),
        "assets": [_asset_to_public_dict(a) for a in public_assets],
        "governance_decision": "allow",
        "is_estimate": False,
    }


@router.get("/public/markdown", response_class=PlainTextResponse)
async def capital_assets_public_markdown() -> str:
    public_assets = list_public_capital_assets()
    lines: list[str] = []
    lines.append("# Dealix Public Capital Assets — الأصول الرأسمالية العامة")
    lines.append("")
    lines.append(
        f"_Generated: {datetime.now(timezone.utc).isoformat()} · "
        f"{len(public_assets)} public-safe assets_"
    )
    lines.append("")
    lines.append(
        "The strategic Capital Assets Dealix has built that reviewers, "
        "partners, and investors are welcome to inspect. Internal assets "
        "are not listed here."
    )
    lines.append("")
    lines.append(
        "الأصول الرأسمالية الاستراتيجية لـ Dealix المتاحة للمراجعين والشركاء "
        "والمستثمرين. الأصول الداخلية غير مدرجة هنا."
    )
    lines.append("")
    lines.append("---")
    lines.append("")
    for a in public_assets:
        lines.append(f"## {a.asset_id} — {a.name}")
        lines.append("")
        lines.append(f"- **Type:** `{a.type}`")
        lines.append(f"- **Maturity:** {a.maturity}")
        lines.append(f"- **Proof level:** {a.proof_level}")
        lines.append(f"- **Last reviewed:** {a.last_reviewed}")
        lines.append(f"- **Buyer relevance:** {', '.join(a.buyer_relevance)}")
        lines.append(f"- **Linked non-negotiables:** {len(a.linked_non_negotiables)}")
        lines.append("")
        lines.append(f"_{a.strategic_role}_")
        lines.append("")
        lines.append("---")
        lines.append("")
    lines.append(
        "_Estimated outcomes are not guaranteed outcomes / "
        "النتائج التقديرية ليست نتائج مضمونة._"
    )
    return "\n".join(lines)
