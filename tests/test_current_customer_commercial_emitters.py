from __future__ import annotations

import json
from pathlib import Path

from auto_client_acquisition.designops.generators.proposal_page import generate_proposal_page
from dealix.commercial_ops.client_pack import build_client_pack_from_row

ROOT = Path(__file__).resolve().parents[1]
SOURCE_FORBIDDEN = (
    "30-day revenue command pilot", "30-day pilot",
    "12,000 sar", "25,000 sar", "15,000 sar",
    "18,000 sar", "9,000 sar", "2,999 sar", "1,500 sar", "990 sar",
)


def _assert_output_has_no_fixed_authority(text: str) -> None:
    folded = text.casefold()
    for token in (*SOURCE_FORBIDDEN, "30 days", "30 يومًا"):
        assert token.casefold() not in folded


def test_proposal_ignores_legacy_duration_and_price_inputs() -> None:
    payload = generate_proposal_page(
        customer_handle="Example Co", recommended_service="Legacy Sprint",
        scope_ar="نطاق تجريبي", scope_en="Example scope", deliverables=[],
        timeline_days=30, price_band_sar="12000 SAR", blocked_actions=[], proof_plan=[],
    )
    text = json.dumps(payload, ensure_ascii=False)
    assert payload["manifest"]["timeline_days"] is None
    assert payload["manifest"]["price_authority"] == "customer_specific_quote_after_qualified_discovery"
    assert "customer-specific duration" in text.casefold()
    _assert_output_has_no_fixed_authority(text)


def test_client_pack_has_customer_specific_duration_and_quote() -> None:
    payload = build_client_pack_from_row(
        {"company_name": "Example Co", "segment": "b2b", "pain_hypothesis": "follow-up gap"},
        write_disk=False,
    )
    text = json.dumps(payload, ensure_ascii=False)
    assert payload["timeline_days"] is None
    assert payload["price_authority"] == "customer_specific_quote_after_qualified_discovery"
    _assert_output_has_no_fixed_authority(text)


def test_active_customer_emitters_do_not_embed_fixed_commercial_authority() -> None:
    paths = [
        "api/routers/drafts.py", "api/routers/sales_os.py",
        "auto_client_acquisition/customer_loop/customer_journey.py",
        "auto_client_acquisition/diagnostic_engine/engine.py",
        "auto_client_acquisition/vertical_playbooks/catalog.py",
        "dealix/commercial/warm_intro_generator.py", "dealix/commercial_ops/client_pack.py",
        "scripts/dealix_call_sheet.py", "scripts/dealix_diagnostic.py",
        "apps/web/lib/hubspot-commercial-os.ts", "scripts/commercial/generate_hubspot_commercial_os.py",
    ]
    text = "\n".join((ROOT / path).read_text(encoding="utf-8") for path in paths).casefold()
    for token in SOURCE_FORBIDDEN:
        assert token.casefold() not in text, f"fixed commercial authority returned: {token}"


def test_hubspot_daily_generator_keeps_crm_as_mirror_not_truth_owner() -> None:
    source = (ROOT / "scripts/commercial/generate_hubspot_commercial_os.py").read_text(encoding="utf-8")
    assert "HubSpot should be used as the CRM source of truth" not in source
    assert "HubSpot is an operational CRM mirror only" in source
    assert "not verified revenue" in source
    assert "canonical payment evidence" in source
