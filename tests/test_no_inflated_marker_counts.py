"""Doctrine-as-code: marker counters MUST equal len(entries).

This is the one cheat we explicitly block. If a future PR (or a
hand-edit) inflates `outreach_sent_count` or `invoice_sent_count`
without adding a matching entry, this test fails locally (via the
pre-commit hook) and in CI (via the doctrine-gate job).

Why this matters: those two integers separate **build-complete** from
**company-complete**. If they can be inflated, the verifier becomes
meaningless.
"""
from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def _load(rel: str) -> dict:
    p = REPO_ROOT / rel
    if not p.exists():
        return {"entries": []}
    return json.loads(p.read_text(encoding="utf-8"))


def test_partner_outreach_count_matches_entries():
    data = _load("data/partner_outreach_log.json")
    count = data.get("outreach_sent_count", 0)
    n = len(data.get("entries") or [])
    assert count == n, (
        f"outreach_sent_count={count} but len(entries)={n}. "
        "Hand-editing the counter without adding entries is a doctrine "
        "violation. Use scripts/log_partner_outreach.py instead."
    )


def test_first_invoice_count_matches_entries():
    data = _load("data/first_invoice_log.json")
    count = data.get("invoice_sent_count", 0)
    n = len(data.get("entries") or [])
    assert count == n, (
        f"invoice_sent_count={count} but len(entries)={n}. "
        "Hand-editing the counter without adding entries is a doctrine "
        "violation. Use scripts/log_invoice_event.py instead."
    )


def test_ceo_complete_matches_count():
    """`ceo_complete` is True iff at least one entry exists."""
    for rel, key in (
        ("data/partner_outreach_log.json", "outreach_sent_count"),
        ("data/first_invoice_log.json", "invoice_sent_count"),
    ):
        data = _load(rel)
        count = data.get(key, 0)
        ceo = bool(data.get("ceo_complete"))
        assert ceo == (count >= 1), (
            f"{rel}: ceo_complete={ceo} but {key}={count} (mismatch)"
        )
