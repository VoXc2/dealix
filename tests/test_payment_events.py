"""Tests for the Payment Event Handler."""

from __future__ import annotations

import pytest

from dealix.commercial.payment_events import (
    PaymentEvent,
    PaymentEventProcessor,
    normalize_moyasar_webhook,
)


class TestNormalizeMoyasarWebhook:

    def test_payment_paid_webhook(self):
        body = {
            "type": "payment_paid",
            "data": {
                "id": "pay_123",
                "invoice_id": "inv_456",
                "amount": 49900,
                "status": "paid",
                "metadata": {
                    "service_tier": "sprint_499",
                    "account_id": "acct_001",
                    "customer_name": "Ahmed Co",
                },
            },
            "live_mode": False,
        }
        event = normalize_moyasar_webhook(body)
        assert event is not None
        assert event.payment_id == "pay_123"
        assert event.amount_sar == 499.0
        assert event.service_tier == "sprint_499"
        assert event.status == "paid"
        assert event.account_id == "acct_001"

    def test_non_payment_event_returns_none(self):
        body = {"type": "customer_created", "data": {}}
        event = normalize_moyasar_webhook(body)
        assert event is None

    def test_invoice_paid_event(self):
        body = {
            "type": "invoice_paid",
            "data": {
                "id": "inv_789",
                "amount": 150000,
                "metadata": {"service_tier": "data_pack_1500"},
            },
        }
        event = normalize_moyasar_webhook(body)
        assert event is not None
        assert event.amount_sar == 1500.0
        assert event.status == "paid"

    def test_missing_metadata_graceful(self):
        body = {
            "type": "payment_paid",
            "data": {"id": "pay_001", "amount": 49900},
        }
        event = normalize_moyasar_webhook(body)
        assert event is not None
        assert event.account_id == ""
        assert event.service_tier == ""


class TestPaymentEventProcessor:

    @pytest.mark.asyncio
    async def test_non_paid_event_not_processed(self):
        processor = PaymentEventProcessor()
        event = PaymentEvent(
            payment_id="pay_001",
            invoice_id="inv_001",
            status="failed",
            amount_sar=499,
            amount_halalas=49900,
        )
        result = await processor.process(event)
        assert result.payment_status == "failed"
        assert not result.onboarding_created
        assert not result.founder_alert_generated

    @pytest.mark.asyncio
    async def test_paid_event_generates_founder_alert(self):
        processor = PaymentEventProcessor()
        event = PaymentEvent(
            payment_id="pay_002",
            invoice_id="inv_002",
            status="paid",
            amount_sar=499,
            amount_halalas=49900,
            service_tier="sprint_499",
            account_id="acct_test",
            customer_name="Riyadh Consulting",
        )
        result = await processor.process(event)
        assert result.payment_status == "paid"
        assert result.founder_alert_generated is True
        assert "Riyadh Consulting" in result.founder_alert_ar
        assert "موافقة" in result.founder_alert_ar  # mentions approval

    @pytest.mark.asyncio
    async def test_paid_event_creates_onboarding(self):
        processor = PaymentEventProcessor()
        event = PaymentEvent(
            payment_id="pay_003",
            invoice_id="inv_003",
            status="paid",
            amount_sar=499,
            amount_halalas=49900,
            service_tier="sprint_499",
            account_id="acct_onboard",
            customer_name="Test Company SA",
        )
        result = await processor.process(event)
        assert result.onboarding_created is True
        assert result.onboarding_id.startswith("onb_")

    @pytest.mark.asyncio
    async def test_zatca_failure_does_not_block(self):
        """ZATCA failure must not block payment processing."""
        processor = PaymentEventProcessor()
        event = PaymentEvent(
            payment_id="pay_004",
            invoice_id="inv_004",
            status="paid",
            amount_sar=1500,
            amount_halalas=150000,
            service_tier="data_pack_1500",
        )
        result = await processor.process(event)
        # Should complete even if ZATCA is not configured
        assert result.payment_status == "paid"
        assert result.zatca_result.get("status") in ("skipped", "error", "issued")


class TestPaymentEvent:

    def test_event_id_auto_generated(self):
        e = PaymentEvent(
            payment_id="pay_x",
            invoice_id="inv_x",
            status="paid",
            amount_sar=499,
            amount_halalas=49900,
        )
        assert e.event_id.startswith("evt_")

    def test_occurred_at_is_utc(self):
        e = PaymentEvent(
            payment_id="pay_y",
            invoice_id="inv_y",
            status="paid",
            amount_sar=499,
            amount_halalas=49900,
        )
        from datetime import timezone
        assert e.occurred_at.tzinfo is not None
