"""Tests for scripts/dealix_invoice.py (P3 — admin Moyasar CLI).

Verifies:
  - Refuses to run when MOYASAR_SECRET_KEY is unset
  - Refuses sk_live_ keys without --allow-live
  - Computes amount_halalas correctly (sar × 100)
  - Calls MoyasarClient.create_invoice with the right args
  - Prints the founder-friendly summary by default
  - --json prints the full response as JSON
  - Caps abusively-large amounts (>50_000 SAR)
"""
from __future__ import annotations

import asyncio
import json
import sys
from io import StringIO
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "dealix_invoice.py"
sys.path.insert(0, str(REPO))

# Import the script's main + helpers as a module via runpy-style trick.
import importlib.util


def _load():
    spec = importlib.util.spec_from_file_location(
        "dealix_invoice_cli", str(SCRIPT)
    )
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


cli = _load()


# ─── Argparse + safety checks ───────────────────────────────────────


def test_is_live_key_helper():
    assert cli._is_live_key("sk_live_abc") is True
    assert cli._is_live_key("sk_live_") is True
    assert cli._is_live_key("sk_test_xyz") is False
    assert cli._is_live_key("") is False


def test_unset_secret_key_raises_system_exit(monkeypatch):
    monkeypatch.delenv("MOYASAR_SECRET_KEY", raising=False)

    class _Args:
        email = "x@y.sa"
        amount_sar = 499.0
        description = "test"
        customer_handle = ""
        service_id = "growth_starter"
        callback_url = ""
        allow_live = False
        json = False

    with pytest.raises(SystemExit) as exc:
        asyncio.run(cli._create(_Args()))
    assert "MOYASAR_SECRET_KEY" in str(exc.value)


def test_live_key_without_flag_raises(monkeypatch):
    monkeypatch.setenv("MOYASAR_SECRET_KEY", "sk_live_realdangerous")

    class _Args:
        email = "x@y.sa"
        amount_sar = 499.0
        description = "test"
        customer_handle = ""
        service_id = "growth_starter"
        callback_url = ""
        allow_live = False
        json = False

    with pytest.raises(SystemExit) as exc:
        asyncio.run(cli._create(_Args()))
    assert "live" in str(exc.value).lower()


def test_live_key_with_flag_proceeds(monkeypatch):
    """If founder explicitly passes --allow-live, the safety check
    yields to the underlying API call (which we mock)."""
    monkeypatch.setenv("MOYASAR_SECRET_KEY", "sk_live_real")

    class _Args:
        email = "x@y.sa"
        amount_sar = 499.0
        description = "test"
        customer_handle = ""
        service_id = "growth_starter"
        callback_url = ""
        allow_live = True
        json = False

    fake = {"id": "inv_live", "amount": 49900, "url": "https://x"}
    with patch.object(cli, "MoyasarClient") as MockClient:
        MockClient.return_value.create_invoice = AsyncMock(return_value=fake)
        result = asyncio.run(cli._create(_Args()))
    assert result == fake


def test_amount_halalas_conversion(monkeypatch):
    monkeypatch.setenv("MOYASAR_SECRET_KEY", "sk_test_xyz")

    class _Args:
        email = "x@y.sa"
        amount_sar = 499.0
        description = "Pilot"
        customer_handle = "ACME-001"
        service_id = "growth_starter"
        callback_url = ""
        allow_live = False
        json = False

    captured = {}

    async def _capture(**kwargs):
        captured.update(kwargs)
        return {"id": "inv_test", "amount": kwargs["amount_halalas"], "url": "https://x"}

    with patch.object(cli, "MoyasarClient") as MockClient:
        MockClient.return_value.create_invoice = AsyncMock(side_effect=_capture)
        asyncio.run(cli._create(_Args()))

    assert captured["amount_halalas"] == 49900  # 499 SAR × 100
    assert captured["currency"] == "SAR"
    assert captured["description"] == "Pilot"
    md = captured["metadata"]
    assert md["customer_email"] == "x@y.sa"
    assert md["customer_handle"] == "ACME-001"
    assert md["service_id"] == "growth_starter"
    assert md["created_by"] == "dealix_invoice_cli"


def test_amount_zero_or_negative_rejected(monkeypatch):
    monkeypatch.setenv("MOYASAR_SECRET_KEY", "sk_test_x")

    class _Args:
        email = "x@y.sa"
        amount_sar = 0.0
        description = "x"
        customer_handle = ""
        service_id = "growth_starter"
        callback_url = ""
        allow_live = False
        json = False

    with pytest.raises(SystemExit):
        asyncio.run(cli._create(_Args()))


def test_amount_over_50k_rejected(monkeypatch):
    monkeypatch.setenv("MOYASAR_SECRET_KEY", "sk_test_x")

    class _Args:
        email = "x@y.sa"
        amount_sar = 100000.0
        description = "x"
        customer_handle = ""
        service_id = "growth_starter"
        callback_url = ""
        allow_live = False
        json = False

    with pytest.raises(SystemExit) as exc:
        asyncio.run(cli._create(_Args()))
    assert "50,000" in str(exc.value) or "50000" in str(exc.value)


# ─── Argparse parser shape ──────────────────────────────────────────


def test_parser_has_required_args(monkeypatch):
    monkeypatch.setattr(
        sys, "argv",
        ["dealix_invoice.py", "--email", "a@b.sa", "--amount-sar", "499", "--description", "x"],
    )
    args = cli.parse_args()
    assert args.email == "a@b.sa"
    assert args.amount_sar == 499.0
    assert args.description == "x"
    assert args.allow_live is False
    assert args.json is False


# ─── Output rendering ───────────────────────────────────────────────


def test_main_prints_founder_friendly_summary(monkeypatch, capsys):
    monkeypatch.setenv("MOYASAR_SECRET_KEY", "sk_test_x")
    monkeypatch.setattr(
        sys, "argv",
        ["dealix_invoice.py", "--email", "a@b.sa", "--amount-sar", "499", "--description", "Pilot"],
    )

    fake = {
        "id": "inv_print_test",
        "amount": 49900,
        "url": "https://checkout.moyasar.com/inv_print_test",
    }
    with patch.object(cli, "MoyasarClient") as MockClient:
        MockClient.return_value.create_invoice = AsyncMock(return_value=fake)
        rc = cli.main()

    out = capsys.readouterr().out
    assert rc == 0
    assert "INVOICE_ID=inv_print_test" in out
    assert "PAYMENT_URL=https://checkout.moyasar.com/inv_print_test" in out
    assert "499 SAR" in out
    assert "manually" in out  # safety reminder line


def test_main_json_mode_prints_raw(monkeypatch, capsys):
    monkeypatch.setenv("MOYASAR_SECRET_KEY", "sk_test_x")
    monkeypatch.setattr(
        sys, "argv",
        [
            "dealix_invoice.py",
            "--email", "a@b.sa",
            "--amount-sar", "499",
            "--description", "Pilot",
            "--json",
        ],
    )

    fake = {"id": "inv_json", "amount": 49900, "url": "https://x", "extra": True}
    with patch.object(cli, "MoyasarClient") as MockClient:
        MockClient.return_value.create_invoice = AsyncMock(return_value=fake)
        rc = cli.main()

    out = capsys.readouterr().out
    assert rc == 0
    parsed = json.loads(out)
    assert parsed == fake
