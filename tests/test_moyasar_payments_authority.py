import json

from company.automation import moyasar_payments as module


def test_create_payment_link_never_posts_even_when_configured(monkeypatch):
    monkeypatch.setenv("MOYASAR_API_KEY", "pk_test_configured")
    monkeypatch.setenv("MOYASAR_API_SECRET", "sk_live_must_not_authorize")
    monkeypatch.setenv("MOYASAR_LIVE_MODE", "true")

    def fail_if_posted(*args, **kwargs):
        raise AssertionError("legacy Moyasar adapter must never POST")

    monkeypatch.setattr(module.requests, "post", fail_if_posted)
    client = module.MoyasarPayments()
    result = client.create_payment_link(
        customer_email="buyer@example.invalid",
        customer_phone="+966000000000",
        customer_name="Test Buyer",
        description="Customer-specific quote",
        amount_sar=1234,
        pilot_id="pilot-test",
    )

    assert result["status"] == "blocked"
    assert result["reason"] == module.PAYMENT_WRITE_BLOCK_REASON
    assert result["provider_write_executed"] is False
    assert result["execution_authority_created"] is False
    assert result["payment_proof_created"] is False
    assert result["revenue_created"] is False
    assert result["payment_url"] is None


def test_pilot_invoice_has_no_retired_fixed_price_or_duration(monkeypatch):
    monkeypatch.delenv("MOYASAR_API_KEY", raising=False)
    monkeypatch.delenv("MOYASAR_API_SECRET", raising=False)
    client = module.MoyasarPayments()

    result = client.create_pilot_invoice(
        customer_name="Test Buyer",
        company_name="Example Co",
        customer_email="buyer@example.invalid",
        customer_phone="+966000000000",
        pilot_id="pilot-test",
    )
    rendered = json.dumps(result, sort_keys=True).lower()

    assert result["status"] == "blocked"
    assert result["amount_sar"] is None
    assert "499" not in rendered
    assert "7-day" not in rendered
    assert "14-day" not in rendered
    assert "growth_starter" not in rendered


class _FakeResponse:
    def raise_for_status(self):
        return None

    def json(self):
        return {
            "invoice": {
                "id": "inv-test",
                "status": "paid",
                "amount": 10000,
                "paid_amount": 10000,
                "customer": {"name": "Test Buyer"},
                "created_at": "2026-08-28T00:00:00Z",
                "updated_at": "2026-08-28T00:01:00Z",
            }
        }


def test_provider_paid_status_is_not_revenue_truth(monkeypatch):
    monkeypatch.setenv("MOYASAR_API_KEY", "pk_test_configured")
    monkeypatch.setenv("MOYASAR_API_SECRET", "sk_test_configured")
    monkeypatch.setattr(module.requests, "get", lambda *args, **kwargs: _FakeResponse())

    result = module.MoyasarPayments().check_payment_status("inv-test")

    assert result["status"] == "paid"
    assert result["evidence_class"] == "PROVIDER_STATUS_NOT_REVENUE_PROOF"
    assert result["revenue_verified"] is False
