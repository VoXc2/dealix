"""Per-target client pack — proposal markdown + deck notes (no auto-send)."""

from __future__ import annotations

import json
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from auto_client_acquisition.designops.generators.proposal_page import generate_proposal_page
from dealix.commercial_ops.paths import REPO_ROOT
from dealix.commercial_ops.targeting_csv import load_targets

CLIENT_PACKS_DIR = REPO_ROOT / "data" / "client_packs"
DECK_TEMPLATE = REPO_ROOT / "docs/commercial/ops_client_pack/dealix_ops_sales_kit_ar.pptx"
RUNBOOK_PATH = REPO_ROOT / "docs/commercial/ops_client_pack/dealix_ops_runbook_ar.md"

OFFER_LABELS: dict[str, tuple[str, str]] = {
    "ten_lead_audit": ("Ten Lead Audit", "499–1,500"),
    "agency_proof_pack": ("Agency Proof Pack", "1,500"),
    "governed_diagnostic": ("Governed Revenue Ops Diagnostic", "4,999–9,999"),
    "executive_diagnostic": ("Executive Diagnostic", "9,999–15,000"),
    "diagnostic_layer": ("Diagnostic Layer (Partner)", "4,999–9,999"),
    "partner_sprint": ("Partner Sprint", "499"),
}

DEFAULT_DELIVERABLES = [
    "Revenue Workflow Map",
    "Source Quality Review",
    "Pipeline Risk Map",
    "Follow-up Gap Analysis",
    "Decision Passport",
    "Proof-of-Value Opportunities",
]


def _slug(name: str) -> str:
    s = re.sub(r"[^\w\u0600-\u06FF]+", "-", name.strip(), flags=re.UNICODE)
    return (s.strip("-") or "client")[:80]


def find_target_row(*, company: str | None = None, lead_id: str | None = None) -> dict[str, str] | None:
    """Match CSV row by company name (case-insensitive) or synthetic lead id."""
    rows = load_targets()
    if company:
        key = company.strip().lower()
        for r in rows:
            if (r.get("company") or "").strip().lower() == key:
                return r
    if lead_id:
        for r in rows:
            slug = _slug(r.get("company") or "")
            if lead_id.lower() in {slug.lower(), (r.get("company") or "").strip().lower()}:
                return r
    return None


def build_client_pack_from_row(row: dict[str, str], *, write_disk: bool = True) -> dict[str, Any]:
    company = (row.get("company") or "عميل").strip()
    offer_id = (row.get("offer_id") or "governed_diagnostic").strip()
    label, price_band = OFFER_LABELS.get(offer_id, ("Governed Revenue Ops Diagnostic", "4,999–9,999"))
    pain = (row.get("pain_hypothesis") or "").strip()
    segment = (row.get("segment") or "agency_wedge").strip()
    contact = (row.get("contact") or "REPLACE:contact").strip()

    scope_ar = (
        f"تشخيص محكوم لـ {company} ({segment}): تحويل {pain or 'فجوات المتابعة والأدلة'} "
        "إلى workflow قابل للقياس خلال أسبوعين."
    )
    scope_en = (
        f"Governed diagnostic for {company} ({segment}): turn "
        f"{pain or 'follow-up and evidence gaps'} into measurable workflows within two weeks."
    )

    proposal = generate_proposal_page(
        customer_handle=company,
        recommended_service=label,
        scope_ar=scope_ar,
        scope_en=scope_en,
        deliverables=DEFAULT_DELIVERABLES,
        timeline_days=14,
        price_band_sar=price_band,
        blocked_actions=[
            "إرسال واتساب بارد",
            "LinkedIn آلي",
            "فواتير Moyasar live بدون موافقة",
        ],
        proof_plan=[
            "Risk Score مجاني أو Sample Proof على 10 leads",
            "Decision Passport في الاجتماع",
            "Evidence ledger بعد كل لمسة يدوية",
        ],
    )

    deck_notes = "\n".join(
        [
            f"# Deck customization — {company}",
            "",
            f"Template: {DECK_TEMPLATE.relative_to(REPO_ROOT)}",
            "",
            "Slides to edit (3–5):",
            f"1. Cover — {company}",
            f"2. Pain — {pain or '—'}",
            f"3. Segment — {segment} · Motion {row.get('motion', 'A')}",
            f"4. Offer — {label} ({price_band} SAR)",
            "5. Diagnostic scope — 14 days · founder manual send only",
            "",
            f"Contact placeholder: {contact}",
            "Demo: /ar/business-now#strategy (simulate sector/city/budget)",
        ]
    )

    runbook_hint = ""
    if RUNBOOK_PATH.is_file():
        runbook_hint = RUNBOOK_PATH.read_text(encoding="utf-8")[:1200]

    generated_at = datetime.now(UTC).isoformat()
    slug = _slug(company)
    out_dir = CLIENT_PACKS_DIR / slug

    paths: dict[str, str] = {}
    if write_disk:
        out_dir.mkdir(parents=True, exist_ok=True)
        prop_path = out_dir / "proposal.md"
        prop_path.write_text(
            proposal.get("markdown") or proposal.get("markdown_ar") or "",
            encoding="utf-8",
        )
        (out_dir / "deck_notes.md").write_text(deck_notes, encoding="utf-8")
        (out_dir / "runbook_excerpt.md").write_text(runbook_hint, encoding="utf-8")
        manifest = {
            "company": company,
            "offer_id": offer_id,
            "generated_at": generated_at,
            "deck_template": str(DECK_TEMPLATE.relative_to(REPO_ROOT)),
            "files": ["proposal.md", "deck_notes.md", "runbook_excerpt.md"],
        }
        (out_dir / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        def _rel(p: Path) -> str:
            try:
                return str(p.relative_to(REPO_ROOT))
            except ValueError:
                return str(p)

        paths = {k: _rel(out_dir / k) for k in manifest["files"]}
        paths["manifest"] = _rel(out_dir / "manifest.json")
        paths["directory"] = _rel(out_dir)

    return {
        "generated_at": generated_at,
        "company": company,
        "segment": segment,
        "offer_id": offer_id,
        "recommended_service": label,
        "price_band_sar": price_band,
        "proposal": proposal,
        "deck_notes": deck_notes,
        "deck_template": str(DECK_TEMPLATE.relative_to(REPO_ROOT)),
        "demo_path": "/ar/business-now#strategy",
        "paths": paths,
        "policy_ar": "حزمة للمراجعة والإرسال اليدوي فقط — لا إرسال آلي.",
    }


def build_client_pack(
    *,
    company: str | None = None,
    lead_id: str | None = None,
    row: dict[str, str] | None = None,
    write_disk: bool = True,
) -> dict[str, Any]:
    if row is None:
        row = find_target_row(company=company, lead_id=lead_id)
    if not row:
        raise ValueError("target_not_found")
    return build_client_pack_from_row(row, write_disk=write_disk)
