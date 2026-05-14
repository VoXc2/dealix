"""GCC Market Intel — Wave 19 (public endpoint).

Surfaces Dealix's posture across the 4 priority GCC markets so any
buyer's procurement / legal team can see whether Dealix already maps to
their jurisdiction's PDPL-equivalent.

Reads from `auto_client_acquisition.governance_os.gcc_markets` so the
markdown can never drift from the constants file.

Endpoints:
  GET /api/v1/gcc-markets            → JSON of 4 markets + regulatory + status
  GET /api/v1/gcc-markets/markdown   → bilingual AR+EN markdown
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

from auto_client_acquisition.governance_os.gcc_markets import GCC_MARKETS

router = APIRouter(prefix="/api/v1/gcc-markets", tags=["gcc-markets"])


def _to_dict(m) -> dict[str, Any]:
    return {
        "country": m.country,
        "country_ar": m.country_ar,
        "country_en": m.country_en,
        "regulator": m.regulator,
        "framework": m.framework,
        "framework_articles": list(m.framework_articles),
        "dealix_status": m.dealix_status,
        "local_payment_processor": m.local_payment_processor,
        "local_invoicing_standard": m.local_invoicing_standard,
        "language_priority": m.language_priority,
        "notes": m.notes,
    }


def _build_payload() -> dict[str, Any]:
    markets = [_to_dict(m) for m in GCC_MARKETS]
    return {
        "version": "1.0",
        "wave": "19",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_of_truth": (
            "auto_client_acquisition/governance_os/gcc_markets.py"
        ),
        "market_count": len(markets),
        "active_count": sum(1 for m in markets if m["dealix_status"] == "active"),
        "pilot_ready_count": sum(
            1 for m in markets if m["dealix_status"] == "pilot_ready"
        ),
        "future_market_count": sum(
            1 for m in markets if m["dealix_status"] == "future_market"
        ),
        "markets": markets,
        "doctrine_endpoint": "GET /api/v1/dealix-promise/markdown",
        "commercial_map_endpoint": "GET /api/v1/commercial-map/markdown",
        "governance_decision": "allow",
        "is_estimate": False,
    }


@router.get("")
async def gcc_markets_json() -> dict[str, Any]:
    """JSON — 4 markets + regulatory framework + Dealix coverage status."""
    return _build_payload()


@router.get("/markdown", response_class=PlainTextResponse)
async def gcc_markets_markdown() -> str:
    """Bilingual AR+EN markdown render — same source as docs/strategic/GCC_EXPANSION_STRATEGY.md."""
    payload = _build_payload()
    status_label = {
        "active": "🟢 Active",
        "pilot_ready": "🟡 Pilot-ready",
        "future_market": "⚪ Future market",
    }
    lines: list[str] = []
    lines.append("# Dealix — GCC Market Posture — موقفنا الإقليمي")
    lines.append("")
    lines.append(f"_Version {payload['version']} · Wave {payload['wave']}_")
    lines.append(f"_Generated: {payload['generated_at']}_")
    lines.append(f"_Source of truth: `{payload['source_of_truth']}` ({payload['market_count']} markets)_")
    lines.append("")
    lines.append(
        "Dealix's governance pack (PDPL + NDMO + audit chain + Trust Pack) "
        "maps natively to each priority GCC market's data-protection statute. "
        "Saudi is the active beachhead; UAE is pilot-ready; Qatar + Kuwait "
        "are documented as future markets and will open after a published "
        "Saudi flagship Sprint case study."
    )
    lines.append("")
    lines.append(
        "حزمة الحوكمة لـ Dealix (PDPL + NDMO + سلسلة التدقيق + Trust Pack) "
        "ترتبط بشكل طبيعي بكل قانون حماية بيانات في أسواق دول الخليج الأربعة "
        "ذات الأولوية. السعودية هي القاعدة النشطة؛ الإمارات جاهزة للتجريب؛ "
        "قطر والكويت موثّقتان كأسواق مستقبلية تُفتح بعد نشر دراسة حالة لسبرنت "
        "رئيسي سعودي."
    )
    lines.append("")
    lines.append(
        f"**Summary:** {payload['active_count']} active · "
        f"{payload['pilot_ready_count']} pilot-ready · "
        f"{payload['future_market_count']} future market(s)"
    )
    lines.append("")
    lines.append("---")
    lines.append("")
    for m in payload["markets"]:
        lines.append(f"## {m['country_en']} ({m['country']}) — {m['country_ar']}")
        lines.append("")
        lines.append(f"- **Status:** {status_label.get(m['dealix_status'], m['dealix_status'])}")
        lines.append(f"- **Regulator:** {m['regulator']}")
        lines.append(f"- **Framework:** {m['framework']}")
        lines.append("- **Framework articles mapped:**")
        for art in m["framework_articles"]:
            lines.append(f"  - {art}")
        lines.append(f"- **Local payment processor:** {m['local_payment_processor']}")
        lines.append(f"- **Local invoicing standard:** {m['local_invoicing_standard']}")
        lines.append(f"- **Language priority:** {m['language_priority']}")
        lines.append("")
        lines.append(f"_{m['notes']}_")
        lines.append("")
        lines.append("---")
        lines.append("")
    lines.append(
        "_Estimated outcomes are not guaranteed outcomes / "
        "النتائج التقديرية ليست نتائج مضمونة._"
    )
    return "\n".join(lines)
