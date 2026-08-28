"""Tests for scripts/dealix_invoice.py test-only payment compatibility CLI."""
from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "dealix_invoice.py"
sys.path.insert(0, str(REPO))

import importlib.util


def _load():
    spec = importlib.util.spec_from_file_location("dealix_invoice_cli", str(SCRIPT))
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


cli = _load()


class _BaseArgs:
    email = "x@y.sa"
    amount_sar = 1200.0
    description = "Customer-specific quote test"
    customer_handle = "ACME-001"
    service_id = "customer_specific_quote_test"
    quote_evidence_id = "quote-test-001"
    callback_url = ""
    allow_live = False
    json = False


def test_key_helpers():
    assert cli._is_live_key("sk_live_abc") is True
    assert cli._is_live_key("sk_test_xyz") is False
    assert cli._is_test_key("sk_test_xyz") is True
    assert cli._is_test_key("sk_live_abc") is False


def test_unset_secret_key_raises_system_exit(monkeypatch):
    monkeypatch.delenv("MOYASAR_SECRET_KEY", raising=False)
    with pytest.raises(SystemExit) as exc:
        asyncio.run(cli._create(_BaseArgs()))
    assert "sk_test" in str(exc.value)


def test_live_key_is_always_blocked_even_if_legacy_flag_true(monkeypatch):
    monkeypatch.setenv("MOYASAR_SECRET_KEY", "sk_live_realdangerous")

    class _Args(_BaseArgs):
        allow_live = True

    with pytest.raises(SystemExit) as exc:
        asyncio.run(cli._create(_Args()))
    assert "live_invoice_blocked" in str(exc.value).lower()


def test_unknown_key_class_is_blocked(monkeypatch):
    monkeypatch.setenv("MOYASAR_SECRET_KEY", "secret_unknown")
    with pytest.raises(SystemExit) as exc:
        asyncio.run(cli._create(_BaseArgs()))
    assert "sk_test" in str(exc.value).lower()


def test_test_invoice_amount_and_metadata(monkeypatch):
    monkeypatch.setenv("MOYASAR_SECRET_KEY", "sk_test_xyz")
    captured = {}

    async def _capture(**kwargs):
        captured.update(kwargs)
        return {"id": "inv_test", "amount": kwargs["amount_halalas"], "url": "https://x"}

    with patch.object(cli, "MoyasarClient") as MockClient:
        MockClient.return_value.create_invoice = AsyncMock(side_effect=_capture)
        result = asyncio.run(cli._create(_BaseArgs()))

    assert result["id"] == "inv_test"
    assert captured["amount_halalas"] == 120000
    assert captured["currency"] == "SAR"
    metadata = captured["metadata"]
    assert metadata["customer_email"] == "x@y.sa"
    assert metadata["customer_handle"] == "ACME-001"
    assert metadata["service_id"] == "customer_specific_quote_test"
    assert metadata["quote_evidence_id"] == "quote-test-001"
    assert metadata["commercial_truth"] == "TEST_ONLY_NOT_PAYMENT_OR_REVENUE"
    assert metadata["created_by"] == "dealix_invoice_cli_test_only"


def test_amount_zero_or_negative_rejected(monkeypatch):
    monkeypatch.setenv("MOYASAR_SECRET_KEY", "sk_test_x")

    class _Args(_BaseArgs):
        amount_sar = 0.0

    with pytest.raises(SystemExit):
        asyncio.run(cli._create(_Args()))


def test_amount_over_50k_rejected(monkeypatch):
    monkeypatch.setenv("MOYASAR_SECRET_KEY", "sk_test_x")

    class _Args(_BaseArgs):
        amount_sar = 100000.0

    with pytest.raises(SystemExit) as exc:
        asyncio.run(cli._create(_Args()))
    assert "50,000" in str(exc.value) or "50000" in str(exc.value)


def test_parser_default_is_non_live_customer_specific_test(monkeypatch):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "dealix_invoice.py",
            "--email", "a@b.sa",
            "--amount-sar", "1200",
            "--description", "Quote test",
        ],
    )
    args = cli.parse_args()
    assert args.amount_sar == 1200.0
    assert args.allow_live is False
    assert args.service_id == "customer_specific_quote_test"
    assert args.quote_evidence_id == ""


def test_main_legacy_allow_live_flag_fails_closed(monkeypatch, capsys):
    monkeypatch.setenv("MOYASAR_SECRET_KEY", "sk_live_x")
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "dealix_invoice.py",
            "--email", "a@b.sa",
            "--amount-sar", "1200",
            "--description", "Quote",
            "--allow-live",
        ],
    )
    rc = cli.main()
    captured = capsys.readouterr()
    assert rc == 2
    assert "LIVE_INVOICE_BLOCKED" in captured.err


def test_dry_run_is_explicitly_non_authoritative(monkeypatch, capsys):
    monkeypatch.delenv("MOYASAR_SECRET_KEY", raising=False)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "dealix_invoice.py",
            "--email", "a@b.sa",
            "--amount-sar", "1200",
            "--description", "Quote preview",
            "--quote-evidence-id", "quote-123",
            "--dry-run",
        ],
    )
    rc = cli.main()
    out = capsys.readouterr().out
    assert rc == 0
    assert "DRY_RUN=true" in out
    assert "COMMERCIAL_AUTHORITY=NONE_PREVIEW_ONLY" in out
    assert "LIVE_INVOICE_ALLOWED=false" in out
    assert "REFUND_OR_REMEDY_AUTHORIZED=false" in out
    assert "PAYMENT_PROOF_CREATED=false" in out
    assert "REVENUE_CREATED=false" in out
    assert "quote-123" in out
    assert "7-day" not in out.lower()
    assert "growth_starter" not in out.lower()


def test_main_test_invoice_prints_test_only_summary(monkeypatch, capsys):
    monkeypatch.setenv("MOYASAR_SECRET_KEY", "sk_test_x")
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "dealix_invoice.py",
            "--email", "a@b.sa",
            "--amount-sar", "1200",
            "--description", "Quote test",
            "--quote-evidence-id", "quote-123",
        ],
    )

    fake = {
        "id": "inv_print_test",
        "amount": 120000,
        "url": "https://checkout.moyasar.com/inv_print_test",
    }
    with patch.object(cli, "MoyasarClient") as MockClient:
        MockClient.return_value.create_invoice = AsyncMock(return_value=fake)
        rc = cli.main()

    out = capsys.readouterr().out
    assert rc == 0
    assert "TEST_ONLY=true" in out
    assert "INVOICE_ID=inv_print_test" in out
    assert "TEST_PAYMENT_URL=https://checkout.moyasar.com/inv_print_test" in out
    assert "AMOUNT_SAR=1200" in out
    assert "LIVE_INVOICE_ALLOWED=false" in out
    assert "PAYMENT_PROOF_CREATED=false" in out
    assert "REVENUE_CREATED=false" in out


def test_main_json_mode_prints_raw_test_response(monkeypatch, capsys):
    monkeypatch.setenv("MOYASAR_SECRET_KEY", "sk_test_x")
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "dealix_invoice.py",
            "--email", "a@b.sa",
            "--amount-sar", "1200",
            "--description", "Quote test",
            "--json",
        ],
    )

    fake = {"id": "inv_json", "amount": 120000, "url": "https://x", "extra": True}
    with patch.object(cli, "MoyasarClient") as MockClient:
        MockClient.return_value.create_invoice = AsyncMock(return_value=fake)
        rc = cli.main()

    out = capsys.readouterr().out
    assert rc == 0
    assert json.loads(out) == fake
