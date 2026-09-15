"""Active founder/commercial surfaces must follow the current one-product launch path.

This intentionally checks only runtime/operator surfaces consumed by current code.
Historical/archival strategy documents are not silently promoted to launch authority.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ACTIVE_SURFACES = (
    ROOT / "dealix/commercial_ops/first_paid_tracker.py",
    ROOT / "dealix/commercial_ops/daily_pack.py",
    ROOT / "dealix/commercial_ops/value_map_status.py",
    ROOT / "docs/commercial/operations/FIRST_PAID_DIAGNOSTIC_DOD_AR.md",
    ROOT / "dealix/commercial_ops/motion_a_pipeline.py",
    ROOT / "dealix/commercial_ops/value_plan.py",
    ROOT / "dealix/commercial_ops/expansion_status.py",
    ROOT / "dealix/commercial_ops/weekly_scorecard_commercial.py",
    ROOT / "dealix/commercial_ops/full_ops_autopilot.py",
)

RETIRED_FIXED_PRICE_TOKENS = (
    "4,999",
    "15,000",
    "2,999",
    "499 SAR",
    "7-Day",
    "7-day",
)


def test_active_commercial_surfaces_use_quote_only_customer_specific_pilot() -> None:
    combined = "\n".join(path.read_text(encoding="utf-8") for path in ACTIVE_SURFACES)

    assert "customer-specific quote" in combined
    assert "source-backed Proof" in combined
    assert "30-day Revenue Command Pilot" not in combined
    assert "30 يومًا" not in combined

    for token in RETIRED_FIXED_PRICE_TOKENS:
        assert token not in combined, f"retired launch token returned in active surface: {token}"



def test_active_operator_copy_does_not_charge_for_diagnostics() -> None:
    combined = "\n".join(path.read_text(encoding="utf-8") for path in ACTIVE_SURFACES)
    forbidden = ("Diagnostic مدفوع", "فاتورة Diagnostic", "First paid Diagnostic")
    for token in forbidden:
        assert token not in combined, f"retired diagnostic-pricing copy returned: {token}"

def test_first_paid_tracker_returns_current_launch_path_not_price_ladder() -> None:
    text = (ROOT / "dealix/commercial_ops/first_paid_tracker.py").read_text(
        encoding="utf-8"
    )

    assert "Free Execution Diagnostic" in text
    assert "qualified discovery" in text
    assert "customer-specific quote/intervention" in text
    assert "30-day Revenue Command Pilot" not in text
    assert "stop / expand / redesign" in text


def test_first_close_dod_keeps_payment_proof_states_separate() -> None:
    text = (
        ROOT / "docs/commercial/operations/FIRST_PAID_DIAGNOSTIC_DOD_AR.md"
    ).read_text(encoding="utf-8")

    assert "invoice intent" in text
    assert "ليست Revenue" in text
    assert "payment_received" in text
    assert "proof_pack_delivered" in text
    assert "Publication Permission" in text
    assert "customer-specific quote" in text


def test_value_map_runtime_does_not_route_to_legacy_price_ladder_doc() -> None:
    text = (ROOT / "dealix/commercial_ops/value_map_status.py").read_text(
        encoding="utf-8"
    )

    assert 'VALUE_MAP_DOC = REPO_ROOT / "docs/DEALIX_BUSINESS_MODEL.md"' in text
    assert 'COMMERCIAL_IDENTITY_DOC = REPO_ROOT / "COMMERCIAL_IDENTITY.md"' in text
    assert 'FIRST_LAUNCH_GATE = REPO_ROOT / "dealix/config/first_launch_offer_gate.yaml"' in text
    assert 'VALUE_MAP_DOC = REPO_ROOT / "docs/commercial/COMMERCIAL_VALUE_MAP_AR.md"' not in text


def test_first_launch_gate_is_the_current_price_authority_boundary() -> None:
    gate = (ROOT / "dealix/config/first_launch_offer_gate.yaml").read_text(
        encoding="utf-8"
    )

    assert "quote_only_after_discovery: true" in gate
    assert "public_amount_sar: null" in gate
    assert "canonical_price_source_after_approval: founder_approved_named_customer_quote" in gate
    assert "live_checkout: blocked" in gate
