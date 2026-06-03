"""Delivery pipelines must never start before client inputs are received."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
POST_INTAKE = {"build", "review", "handoff", "value_report", "closed"}


def test_no_delivery_before_inputs():
    path = ROOT / "data/delivery/pipelines.jsonl"
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert rows, "expected at least one delivery pipeline"
    for p in rows:
        if p.get("stage") in POST_INTAKE:
            assert p.get("inputs_received") is True, f"{p['client']} advanced without inputs"
