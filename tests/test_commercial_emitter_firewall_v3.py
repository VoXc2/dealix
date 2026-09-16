from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest

from api.routers.revenue_metrics import RECURRING_METRICS_STATUS, _compute_dashboard
from dealix.commercial.upsell_engine import UpsellEngine
from dealix.payments.payment_link import (
    LEGACY_FIXED_PRICE_TIER_KEYS,
    SERVICE_TIERS,
    PaymentLinkError,
    PaymentLinkRequest,
    create_payment_link,
)

ROOT = Path(__file__).resolve().parents[1]

ACTIVE_EMITTERS = (
    "api/routers/prospect.py",
    "api/routers/outreach.py",
    "api/routers/autonomous.py",
    "api/routers/revenue.py",
    "api/routers/automation.py",
    "api/routers/dominance.py",
    "auto_client_acquisition/email/reply_classifier.py",
    "auto_client_acquisition/email/daily_targeting.py",
    "auto_client_acquisition/email/research_agent.py",
    "auto_client_acquisition/intelligence/offers.py",
    "auto_client_acquisition/agents/rules_router.py",
    "auto_client_acquisition/whatsapp_client_os/assessment.py",
    "scripts/dealix_reply_classifier.py",
    "scripts/generate_daily_mass_drafts.py",
    "scripts/dealix_ai_ops_diagnostic.py",
    "dealix/business_now/commercial_strategy.py",
    "dealix/commercial_persuasion.py",
)

FORBIDDEN = (
    "Starter 999",
    "Growth 2,999",
    "Scale 7,999",
    "pilot بريال",
    "1 SAR × 7 days",
    "45 ثانية",
    "25% MRR",
    "10% MRR",
    "20-30% MRR",
    "PDPL-compliant",
    "Pilot لمدة 30 يوم",
    "30-day Revenue Command Pilot",
)


def test_active_emitters_cannot_restore_retired_commercial_authority() -> None:
    text = "\n".join((ROOT / path).read_text(encoding="utf-8") for path in ACTIVE_EMITTERS)
    folded = text.casefold()
    for token in FORBIDDEN:
        assert token.casefold() not in folded, token


def test_autonomous_outbound_policy_is_fail_closed() -> None:
    text = (ROOT / "api/routers/autonomous.py").read_text(encoding="utf-8")
    assert '"auto_send_allowed": []' in text
    assert '"email_cold": "blocked"' in text
    assert "auto_send = False" in text
    assert "human_required = True" in text
    assert "approval_required=True" in text
    assert '"recommended_action": "QUEUE_FOR_HUMAN"' in text


@pytest.mark.asyncio
async def test_legacy_fixed_price_tier_cannot_create_payment_link() -> None:
    assert SERVICE_TIERS == {}
    assert "sprint_499" in LEGACY_FIXED_PRICE_TIER_KEYS
    with pytest.raises(PaymentLinkError, match="retired"):
        await create_payment_link(
            PaymentLinkRequest(service_tier="sprint_499", customer_name="Example")
        )


def test_upsell_engine_emits_scope_not_price() -> None:
    result = UpsellEngine().check(
        account_id="a1",
        company_name="Example",
        proof_event_count=6,
        proof_level="L2",
    )
    blob = result.model_dump_json()
    assert result.is_eligible is True
    assert result.price_authority == "customer_specific_quote_after_review"
    assert "2,999" not in blob
    assert "4,999" not in blob
    assert "15,000" not in blob
    assert "automatic expansion" in blob.lower() or "توسع تلقائي" in blob


def test_revenue_metrics_never_mint_mrr_from_legacy_plan_label() -> None:
    now = datetime.now(UTC)
    result = _compute_dashboard(
        [
            {
                "customer_handle": "customer-1",
                "plan": "growth",
                "amount_halalas": 123_456,
                "currency": "SAR",
                "last_event_type": "payment_paid",
                "created_at": now,
            }
        ]
    )
    assert result["verified_cash"]["total_halalas"] == 123_456
    assert result["verified_cash"]["total_sar"] == pytest.approx(1234.56)
    assert result["mrr"]["sar"] is None
    assert result["arr"]["sar"] is None
    assert result["nrr_pct"] is None
    assert result["churn_pct_monthly"] is None
    assert result["recurring_metrics_status"] == RECURRING_METRICS_STATUS
    assert result["plan_distribution_authority"] == "classification_only_no_price_or_revenue_authority"
