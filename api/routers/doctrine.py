"""Open Governed AI Operations Doctrine — Wave 19 (public).

The category-creating public endpoint. Surfaces the 11 non-negotiables
AS AN OPEN FRAMEWORK other AI ops operators can adopt. Dealix is the
reference implementation.

Distinct from `/api/v1/dealix-promise` (which is Dealix's commitment to
its OWN customers). `/api/v1/doctrine` is the open-framework positioning:
Dealix maintains it, others adopt it.

Endpoints:
  GET /api/v1/doctrine            → JSON of the open framework
  GET /api/v1/doctrine/controls   → JSON of the control mapping
  GET /api/v1/doctrine/markdown   → bilingual AR+EN open framework markdown

NO admin gate — this IS the public surface that makes Dealix the standard.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

from auto_client_acquisition.governance_os.non_negotiables import NON_NEGOTIABLES


router = APIRouter(prefix="/api/v1/doctrine", tags=["doctrine"])


def _to_control(n) -> dict[str, Any]:
    """Map a non-negotiable to a Control row (open-framework framing)."""
    return {
        "id": f"NN-{n.id}",
        "name_en": n.title_en,
        "name_ar": n.title_ar,
        "control_summary_en": n.promise_en,
        "control_summary_ar": n.promise_ar,
        "refusal_en": n.refusal_en,
        "refusal_ar": n.refusal_ar,
        "evidence_artifact": _evidence_for(n.id),
        "test_reference": list(n.enforced_by),
    }


def _evidence_for(nn_id: str) -> str:
    """The artifact category that proves compliance with this control."""
    mapping = {
        "no_scraping": "Source Passport record",
        "no_cold_whatsapp": "Channel Policy decision log",
        "no_linkedin_automation": "Channel Policy decision log",
        "no_unsourced_claims": "Claim review log + Source Passport",
        "no_guaranteed_outcomes": "Claim review log",
        "no_pii_in_logs": "BOPLA redaction middleware log",
        "no_sourceless_ai": "Source Passport record",
        "no_external_action_without_approval": "Approval record + Audit Chain",
        "no_agent_without_identity": "Agent Card + Agent Registry record",
        "no_project_without_proof_pack": "Proof Pack PDF (14 sections)",
        "no_project_without_capital_asset": "Capital Ledger record",
    }
    return mapping.get(nn_id, "doctrine-specific evidence")


def _build_payload() -> dict[str, Any]:
    return {
        "name": "Governed AI Operations Doctrine",
        "version": "0.1.0",
        "maintainer": "Dealix",
        "license_doctrine": "CC BY 4.0 (Creative Commons Attribution 4.0)",
        "license_code_examples": "MIT",
        "trademark_note": "The Dealix name and logo are reserved; the doctrine text is open.",
        "non_negotiables_count": len(NON_NEGOTIABLES),
        "public_framework": True,
        "commercial_reference_implementation": "Dealix",
        "open_doctrine_repo_path": "open-doctrine/",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_of_truth": "auto_client_acquisition/governance_os/non_negotiables.py",
        "controls": [_to_control(n) for n in NON_NEGOTIABLES],
        "category": "governed AI operations",
        "designed_for": [
            "AI consultancies",
            "enterprise AI teams",
            "regulated operators",
            "GCC + MENA digital transformation teams",
            "founders building AI-enabled services",
        ],
        "explicitly_not": [
            "a compliance certification",
            "legal advice",
            "a substitute for jurisdictional law (PDPL / GDPR / NDMO / etc.)",
        ],
        "governance_decision": "allow",
        "is_estimate": False,
    }


@router.get("")
async def doctrine_json() -> dict[str, Any]:
    """JSON — the open framework + control mapping + license posture."""
    return _build_payload()


@router.get("/controls")
async def doctrine_controls() -> dict[str, Any]:
    """JSON — just the control rows. Useful for adopter integration tests."""
    payload = _build_payload()
    return {
        "version": payload["version"],
        "name": payload["name"],
        "controls_count": len(payload["controls"]),
        "controls": payload["controls"],
    }


@router.get("/markdown", response_class=PlainTextResponse)
async def doctrine_markdown() -> str:
    """Bilingual AR+EN open framework markdown."""
    payload = _build_payload()
    lines: list[str] = []
    lines.append("# Governed AI Operations Doctrine — دستور تشغيل AI المحوكم")
    lines.append("")
    lines.append(
        f"_Version {payload['version']} · Maintained by {payload['maintainer']} · "
        f"Doctrine: {payload['license_doctrine']} · Code: {payload['license_code_examples']}_"
    )
    lines.append("")
    lines.append(
        "An open doctrine for teams building responsible, evidence-backed AI "
        "operations. Created and maintained by Dealix. Dealix is the commercial "
        "reference implementation; the framework itself is open."
    )
    lines.append("")
    lines.append(
        "دستور مفتوح للفِرق التي تبني عمليات AI مسؤولة ومستندة إلى الأدلة. "
        "أنشأته وتشرف عليه شركة Dealix. تُعدّ Dealix النموذج المرجعي التجاري، "
        "أما الإطار نفسه فمفتوح للتبنّي."
    )
    lines.append("")
    lines.append(
        f"**Trademark note:** {payload['trademark_note']}"
    )
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Control Mapping — جدول الضوابط")
    lines.append("")
    lines.append("| # | Control (EN / AR) | Evidence Artifact | Test Reference |")
    lines.append("|---|---|---|---|")
    for i, c in enumerate(payload["controls"], start=1):
        ref = ", ".join(f"`{p}`" for p in c["test_reference"])
        lines.append(
            f"| {i} | **{c['name_en']}** / {c['name_ar']} "
            f"| {c['evidence_artifact']} | {ref} |"
        )
    lines.append("")
    lines.append("---")
    lines.append("")
    for i, c in enumerate(payload["controls"], start=1):
        lines.append(f"## {i}. {c['name_en']} — {c['name_ar']}")
        lines.append("")
        lines.append(f"- **Control ID:** `{c['id']}`")
        lines.append(f"- **Evidence artifact:** {c['evidence_artifact']}")
        lines.append("")
        lines.append(f"**Control (EN):** {c['control_summary_en']}")
        lines.append("")
        lines.append(f"**الضابط (AR):** {c['control_summary_ar']}")
        lines.append("")
        lines.append(f"**Refusal (EN):** {c['refusal_en']}")
        lines.append("")
        lines.append(f"**ما نرفضه (AR):** {c['refusal_ar']}")
        lines.append("")
        lines.append("**Test references:**")
        for t in c["test_reference"]:
            lines.append(f"  - `{t}`")
        lines.append("")
        lines.append("---")
        lines.append("")
    lines.append("## Explicitly NOT")
    lines.append("")
    for item in payload["explicitly_not"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append(
        "_Estimated outcomes are not guaranteed outcomes / "
        "النتائج التقديرية ليست نتائج مضمونة._"
    )
    return "\n".join(lines)
