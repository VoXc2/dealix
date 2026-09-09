"""Current operator/agent/template surfaces must not act from retired sales authority."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def _assert_current_agent_authority(text: str) -> None:
    low = text.lower()
    assert "customer-specific quote" in low or "customer_specific_quote" in low
    assert "30-day revenue command pilot" in low or "30_day_revenue_command_pilot" in low
    assert "invoice != payment" in low or "invoice intent or link creation is not revenue" in low
    for retired in (
        "7-day revenue intelligence sprint",
        "sprint 499",
        "revenue intelligence sprint | 499",
        "data-to-revenue pack | 1,500",
        "managed revenue ops | 2,999",
        "custom ai service setup | 5,000",
        "diagnostic brief includes proposal for 499",
        "50% invoice via moyasar",
        "moyasar_live_cutover.py",
    ):
        assert retired not in low


def test_claude_sales_agent_is_draft_only_quote_only() -> None:
    text = _read(".claude/agents/dealix-sales.md")
    _assert_current_agent_authority(text)
    assert "NO_LIVE_SEND" in text
    assert "NO_LIVE_CHARGE" in text
    assert "Never make a live payment" in text
    for token in ("4,999", "15,000", "2,999", "499 ر.س", "10 leads"):
        assert token not in text


def test_codex_sales_agent_uses_current_quote_only_authority() -> None:
    text = _read(".codex/agents/dealix-sales.toml")
    _assert_current_agent_authority(text)
    assert "no public fixed-price ladder" in text.lower()
    assert "payment execution authority" in text.lower()
    assert "founder linkedin is manual_native" in text.lower()


def test_codex_pm_does_not_resurrect_retired_sales_ladder() -> None:
    text = _read(".codex/agents/dealix-pm.toml")
    _assert_current_agent_authority(text)
    assert "primary wip = 1" in text.lower()
    assert "current repo authority wins" in text.lower()
    assert "verified revenue requires payment evidence" in text.lower()


def test_claude_pm_does_not_resurrect_retired_sales_ladder() -> None:
    text = _read(".claude/agents/dealix-pm.md")
    _assert_current_agent_authority(text)
    assert "Global primary WIP = 1" in text
    assert "verified revenue requires payment evidence" in text.lower()


def test_cursor_founder_sales_is_quote_only_and_evidence_first() -> None:
    text = _read(".cursor/rules/dealix-founder-sales.mdc")
    _assert_current_agent_authority(text)
    assert "لا توجد حاليًا سلطة عامة" in text
    assert "MANUAL_NATIVE" in text
    assert "quote authority ليست payment execution authority" in text


def test_codex_delivery_is_30_day_evidence_first_and_no_auto_retainer() -> None:
    text = _read(".codex/agents/dealix-delivery.toml")
    _assert_current_agent_authority(text)
    low = text.lower()
    assert "activity != delivery != payment != revenue != customer value != publication permission" in low
    assert "no automatic retainer/expansion offer" in low
    assert "historical 499/7-day playbooks" in low


def test_claude_delivery_is_30_day_evidence_first_and_no_auto_retainer() -> None:
    text = _read(".claude/agents/dealix-delivery.md")
    _assert_current_agent_authority(text)
    assert "Activity != Delivery != Payment != Revenue != Customer Value != Publication Permission" in text
    assert "No automatic retainer or expansion offer" in text
    assert "historical 499 SAR / 7-day playbooks" in text


def test_token_optimizer_commercial_context_points_to_current_authority() -> None:
    text = _read("token-optimizer/02-claude-md/skills/commercial.md")
    assert "COMMERCIAL_IDENTITY.md" in text
    assert "dealix/config/first_launch_offer_gate.yaml" in text
    assert "30-day Revenue Command Pilot" in text
    assert "NO_LIVE_SEND" in text
    assert "NO_LIVE_CHARGE" in text
    assert "Do not treat their presence as launch authority" in text


def test_today_page_does_not_authorize_send_payment_or_production() -> None:
    text = _read("docs/ops/TODAY.md")
    low = text.lower()
    semantic = low.replace("**", "")
    assert "customer-specific quote" in low
    assert "30-day revenue command pilot" in low
    assert "does not authorize external sending" in semantic
    assert "Do not create or send a payment request" in text
    assert "action-specific production approval" in text
    for token in ("Growth 2999", "Scale 7999", "999 ر.س", "5 warm contacts"):
        assert token not in text


def test_proof_template_separates_truth_states_and_has_no_auto_upsell() -> None:
    text = _read("data/templates/proof_pack_ar.md")
    assert "Activity ≠ Delivery ≠ Payment ≠ Revenue ≠ Customer Value ≠ Publication Permission" in text
    assert "customer-specific quote" in text
    assert "no automatic upsell" in text.lower() or "لا يوجد Managed Ops price tier عام تلقائي" in text
    assert "لا يدّعي" in text
    for token in ("2,999", "4,999", "7-day", "7-Day"):
        assert token not in text


def test_managed_ops_agent_has_no_public_price_or_auto_expansion_authority() -> None:
    text = _read("dealix/hermes/agents/managed_ops.py")
    assert "customer-specific approved quote/contract" in text
    assert "do not infer pricing or expansion authority" in text
    assert "never infer authority for external customer/prospect send" in text
    assert "4,999" not in text


def test_commercial_router_hard_blocks_payment_and_automatic_upsell() -> None:
    text = _read("api/routers/commercial.py")
    assert 'status_code=409' in text
    assert '"code": "NO_LIVE_CHARGE"' in text
    assert '"tiers": []' in text
    assert '"eligible_for_automatic_expansion": False' in text
    assert '"offer": None' in text
    assert '"price_sar": None' in text
    assert '"public_fixed_price": False' in text
    assert '"quote_only": True' in text
    assert 'founder_approved_named_customer_quote' in text
    assert "dealix_monthly_fee_sar" not in text
    assert "cost_fields_exposed" not in text


def test_pilot_delivery_requires_current_start_refs_and_has_30_day_outcome_review() -> None:
    text = _read("dealix/commercial/pilot_delivery.py")
    for ref in (
        "approved_scope_ref",
        "baseline_source_ref",
        "approved_data_boundary_ref",
        "approval_path_ref",
        "acceptance_criteria_ref",
        "customer_specific_quote_ref",
        "customer_acceptance_ref",
        "start_condition_ref",
    ):
        assert ref in text
    assert "(30," in text
    assert '"Final outcome review"' in text
    assert "STOP / EXPAND / REDESIGN" in text
    assert "external_send_allowed: bool = False" in text
    assert "live_charge_allowed: bool = False" in text
