"""Contracts for the OP2 Money Now reconciliation snapshot."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "data" / "commercial" / "op2_money_now_reconciliation_v1.json"


def _load_module():
    path = ROOT / "scripts" / "commercial" / "op2_money_now_reconciliation.py"
    spec = importlib.util.spec_from_file_location("op2_money_now", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


money = _load_module()


def _snapshot() -> dict:
    return json.loads(SNAPSHOT.read_text(encoding="utf-8"))


def test_snapshot_is_evidence_only() -> None:
    payload = _snapshot()
    assert payload["schema"] == "dealix.op2-money-now-reconciliation.v1"
    assert payload["counts_as_revenue"] is False
    assert payload["counts_as_pipeline"] is False
    assert payload["economic_truth"]["founder_income_is_not_dealix_revenue"] is True


def test_imini_is_negotiation_but_not_revenue() -> None:
    payload = _snapshot()
    imini = next(r for r in payload["relationships"] if r["entity"] == "iMini / Jannie")
    assert imini["stage"] == "NEGOTIATION"
    assert "NO_VERIFIED_PAYMENT" in imini["commercial_truth"]
    assert payload["economic_truth"]["verified_revenue_sar"] == 0


def test_outbound_contacts_are_not_promoted_to_warm() -> None:
    payload = _snapshot()
    by_entity = {r["entity"]: r for r in payload["relationships"]}
    for entity in ("Linnk Arabia", "Leap29 Saudi"):
        if entity in by_entity:
            assert by_entity[entity]["stage"] == "OUTBOUND_SENT_NO_REPLY"


def test_reconciliation_is_deterministic() -> None:
    rebuilt = money.build_reconciliation()
    stored = _snapshot()
    assert [r["entity"] for r in rebuilt["relationships"]] == [r["entity"] for r in stored["relationships"]]
    assert rebuilt["economic_truth"]["verified_revenue_sar"] == stored["economic_truth"]["verified_revenue_sar"]
