"""Per-company Revenue Command Pilot pack — internal review only, no auto-send."""

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
LEGACY_DECK_TEMPLATE = REPO_ROOT / "docs/commercial/ops_client_pack/dealix_ops_sales_kit_ar.pptx"
RUNBOOK_PATH = REPO_ROOT / "docs/commercial/ops_client_pack/dealix_ops_runbook_ar.md"
CURRENT_SERVICE = "Revenue Command Pilot"
CURRENT_TIMELINE_DAYS = 30
PRICE_AUTHORITY = "quote_after_discovery"
DECK_TEMPLATE_STATUS = "quarantined_until_current_commercial_authority_review"

# Existing targeting rows can carry historical offer_ids. They remain accepted
# as input metadata only; none of them can recreate a separate priced offer.
LEGACY_OFFER_IDS = {
    "ten_lead_audit",
    "agency_proof_pack",
    "governed_diagnostic",
    "executive_diagnostic",
    "diagnostic_layer",
    "partner_sprint",
    "growth_starter",
    "data_to_revenue",
}

DEFAULT_DELIVERABLES = [
    "One approved revenue workflow",
    "Baseline + source / missing-evidence report",
    "Pipeline and decision-risk view",
    "Approval path + acceptance criteria",
    "Weekly Proof Pack",
    "Weekly executive readout",
    "Final Proof Pack + stop / expand / redesign review",
]


def _slug(name: str) -> str:
    s = re.sub(r"[^\w\u0600-\u06FF]+", "-", name.strip(), flags=re.UNICODE)
    return (s.strip("-") or "client")[:80]


def find_target_row(*, company: str | None = None, lead_id: str | None = None) -> dict[str, str] | None:
    """Match a company row without importing contact details into the pack."""
    rows = load_targets()
    if company:
        key = company.strip().lower()
        for row in rows:
            if (row.get("company") or "").strip().lower() == key:
                return row
    if lead_id:
        for row in rows:
            slug = _slug(row.get("company") or "")
            if lead_id.lower() in {
                slug.lower(),
                (row.get("company") or "").strip().lower(),
            }:
                return row
    return None


def build_client_pack_from_row(row: dict[str, str], *, write_disk: bool = True) -> dict[str, Any]:
    """Build one minimum-data, quote-only Pilot pack from a company row."""
    company = (row.get("company") or "عميل").strip()
    legacy_offer_id = (row.get("offer_id") or "").strip()
    pain = (row.get("pain_hypothesis") or "").strip()
    segment = (row.get("segment") or "b2b").strip()

    scope_ar = (
        f"Revenue Command Pilot محكوم لمدة 30 يومًا لـ {company} ({segment}): "
        f"تحويل {pain or 'فجوة إيرادية/تشغيلية محددة'} إلى workflow واحد قابل للقياس، "
        "مع baseline ومصدر وowner وحدود بيانات وموافقات ومعايير قبول وProof."
    )
    scope_en = (
        f"Governed 30-day Revenue Command Pilot for {company} ({segment}): turn "
        f"{pain or 'one specific revenue/operating gap'} into one measurable workflow "
        "with a baseline/source, owner, data boundary, approvals, acceptance criteria, and Proof."
    )

    proposal = generate_proposal_page(
        customer_handle=company,
        recommended_service=CURRENT_SERVICE,
        scope_ar=scope_ar,
        scope_en=scope_en,
        deliverables=DEFAULT_DELIVERABLES,
        timeline_days=CURRENT_TIMELINE_DAYS,
        price_band_sar=PRICE_AUTHORITY,
        blocked_actions=[
            "Cold WhatsApp",
            "Mass LinkedIn automation",
            "Unapproved external send",
            "Live checkout/charge without the separate payment gate",
            "Unverified customer, revenue, ROI, or compliance claims",
        ],
        proof_plan=[
            "Baseline + first-party source or explicit missing-evidence state",
            "Weekly Proof Pack + weekly executive readout",
            "Final Proof Pack with Delivery/Payment/Revenue/Customer Value kept separate",
            "Final stop / expand / redesign decision from evidence",
        ],
    )

    deck_notes = "\n".join(
        [
            f"# Deck customization — {company}",
            "",
            "Deck template: QUARANTINED — legacy PPTX has not been validated against the current quote-only launch authority.",
            "Do not attach or send the legacy deck until it passes current commercial/content QA.",
            "",
            "Slides/content to create after template QA (internal draft):",
            f"1. Cover — {company}",
            f"2. Pain hypothesis — {pain or 'TBD from qualified discovery'}",
            f"3. Segment — {segment}",
            "4. Product — Dealix · Revenue + Proof + Command",
            "5. Pilot — one workflow · 30 days · quote after qualified discovery",
            "6. Proof — weekly + final evidence and stop / expand / redesign decision",
            "",
            "Contact: intentionally not copied into this minimum-data pack.",
            "Price: customer-specific quote after qualified discovery and approval.",
            "Send: blocked until action-specific approval; this pack has no send authority.",
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
            "product": CURRENT_SERVICE,
            "timeline_days": CURRENT_TIMELINE_DAYS,
            "price_authority": "customer_specific_quote_after_qualified_discovery",
            "legacy_offer_id_input": legacy_offer_id if legacy_offer_id in LEGACY_OFFER_IDS else None,
            "generated_at": generated_at,
            "deck_template": None,
            "deck_template_status": DECK_TEMPLATE_STATUS,
            "legacy_deck_reference": str(LEGACY_DECK_TEMPLATE.relative_to(REPO_ROOT)),
            "files": ["proposal.md", "deck_notes.md", "runbook_excerpt.md"],
            "safe_to_send": False,
        }
        (out_dir / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
        )

        def _rel(path: Path) -> str:
            try:
                return str(path.relative_to(REPO_ROOT))
            except ValueError:
                return str(path)

        paths = {name: _rel(out_dir / name) for name in manifest["files"]}
        paths["manifest"] = _rel(out_dir / "manifest.json")
        paths["directory"] = _rel(out_dir)

    return {
        "generated_at": generated_at,
        "company": company,
        "segment": segment,
        "offer_id": "revenue_command_pilot_30d",
        "legacy_offer_id_input": legacy_offer_id if legacy_offer_id in LEGACY_OFFER_IDS else None,
        "recommended_service": CURRENT_SERVICE,
        "price_band_sar": PRICE_AUTHORITY,
        "price_authority": "customer_specific_quote_after_qualified_discovery",
        "timeline_days": CURRENT_TIMELINE_DAYS,
        "proposal": proposal,
        "deck_notes": deck_notes,
        "deck_template": None,
        "deck_template_status": DECK_TEMPLATE_STATUS,
        "legacy_deck_reference": str(LEGACY_DECK_TEMPLATE.relative_to(REPO_ROOT)),
        "paths": paths,
        "safe_to_send": False,
        "policy_ar": (
            "حزمة minimum-data للمراجعة الداخلية فقط — لا إرسال أو Quote أو Invoice أو "
            "Payment request أو نشر دون موافقة الإجراء المناسبة."
        ),
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
