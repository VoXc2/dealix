"""The Dealix Promise — public manifesto endpoint (Wave 17).

Surfaces the 11 non-negotiables as a public, read-only commitment the
buyer's CISO / SAMA / NDMO reviewer can read directly. NO admin gate —
this IS the marketing surface.

Pattern mirrors `api/routers/commercial_map.py`. Source of truth is
`auto_client_acquisition/governance_os/non_negotiables.py` so the
manifesto and the test surface can never drift.

Endpoints:
  GET /api/v1/dealix-promise            → JSON of 11 commitments
  GET /api/v1/dealix-promise/markdown   → bilingual AR+EN markdown
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

from auto_client_acquisition.governance_os.non_negotiables import (
    NON_NEGOTIABLES,
)


router = APIRouter(prefix="/api/v1/dealix-promise", tags=["dealix-promise"])


def _to_dict(n) -> dict[str, Any]:
    return {
        "id": n.id,
        "title_en": n.title_en,
        "title_ar": n.title_ar,
        "promise_en": n.promise_en,
        "promise_ar": n.promise_ar,
        "refusal_en": n.refusal_en,
        "refusal_ar": n.refusal_ar,
        "enforced_by": list(n.enforced_by),
    }


def _build_payload() -> dict[str, Any]:
    return {
        "version": "1.0",
        "wave": "17",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_of_truth": (
            "auto_client_acquisition/governance_os/non_negotiables.py "
            "(canonical text in docs/00_constitution/NON_NEGOTIABLES.md)"
        ),
        "commitments_count": len(NON_NEGOTIABLES),
        "commitments": [_to_dict(n) for n in NON_NEGOTIABLES],
        "audit_chain_endpoint": "GET /api/v1/audit/{handle}/control-graph/markdown",
        "trust_pack_endpoint": "GET /api/v1/value/trust-pack/{handle}/pdf",
        "commercial_map_endpoint": "GET /api/v1/commercial-map/markdown",
        "governance_decision": "allow",
        "is_estimate": False,
    }


@router.get("")
async def dealix_promise_json() -> dict[str, Any]:
    """JSON — 11 commitments + tested-by file references."""
    return _build_payload()


@router.get("/markdown", response_class=PlainTextResponse)
async def dealix_promise_markdown() -> str:
    """Bilingual AR+EN markdown render — same source as docs/THE_DEALIX_PROMISE.md."""
    payload = _build_payload()
    lines: list[str] = []
    lines.append("# The Dealix Promise — وعد Dealix")
    lines.append("")
    lines.append(f"_Version {payload['version']} · Wave {payload['wave']}_")
    lines.append(f"_Generated: {payload['generated_at']}_")
    lines.append(
        f"_Source of truth: `{payload['source_of_truth'].split(' ', 1)[0]}` "
        f"({payload['commitments_count']} commitments)_"
    )
    lines.append("")
    lines.append(
        "These eleven commitments define the perimeter Dealix operates inside. "
        "Every one is enforced by tests, middleware, or governance modules in "
        "the codebase. If we ever ship code that violates one, our CI catches "
        "it before deploy."
    )
    lines.append("")
    lines.append(
        "هذه الالتزامات الإحدى عشرة تحدّد المحيط الذي يعمل Dealix داخله. "
        "كل واحد منها مفروض بواسطة اختبارات أو middleware أو وحدات حوكمة في "
        "قاعدة الكود. لو شُحن كود يخرق أحدها، يلتقطه CI قبل النشر."
    )
    lines.append("")
    lines.append("---")
    lines.append("")

    for i, n in enumerate(payload["commitments"], start=1):
        lines.append(f"## {i}. {n['title_en']} — {n['title_ar']}")
        lines.append("")
        lines.append(f"- **Commitment ID:** `{n['id']}`")
        lines.append("")
        lines.append(f"**Promise (EN):** {n['promise_en']}")
        lines.append("")
        lines.append(f"**التزامنا (AR):** {n['promise_ar']}")
        lines.append("")
        lines.append(f"**Refusal (EN):** {n['refusal_en']}")
        lines.append("")
        lines.append(f"**ما نرفضه (AR):** {n['refusal_ar']}")
        lines.append("")
        lines.append("**Enforced by:**")
        for path in n["enforced_by"]:
            lines.append(f"  - `{path}`")
        lines.append("")
        lines.append("---")
        lines.append("")

    lines.append("## Why this matters for your CISO · لماذا يهم هذا CISO شركتك")
    lines.append("")
    lines.append(
        "- Every commitment maps to a passing test in our CI pipeline. "
        "Demand the test file path; we send it on the same call."
    )
    lines.append(
        "- Every external action is logged with an approver identity and "
        "timestamp. The audit chain is exportable as a Trust Pack PDF."
    )
    lines.append(
        "- Every numeric promise carries `is_estimate=True`. We commit to "
        "commitments, not to guarantees."
    )
    lines.append("")
    lines.append("**Verify yourself:**")
    lines.append("")
    lines.append("```bash")
    lines.append("# JSON manifest (machine-readable)")
    lines.append("curl https://api.dealix.me/api/v1/dealix-promise | jq .commitments")
    lines.append("")
    lines.append("# Audit chain (per customer)")
    lines.append("curl https://api.dealix.me/api/v1/audit/{handle}/control-graph/markdown")
    lines.append("")
    lines.append("# Trust Pack PDF (per customer)")
    lines.append("curl https://api.dealix.me/api/v1/value/trust-pack/{handle}/pdf")
    lines.append("```")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(
        "_Estimated outcomes are not guaranteed outcomes / "
        "النتائج التقديرية ليست نتائج مضمونة._"
    )
    return "\n".join(lines)
