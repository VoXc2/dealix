"""Safety: trust badges MUST NOT contain PII / pricing / partner names.

Even when the underlying marker logs contain commercial detail, the SVG
badges should only display: counts, PASS/FAIL, YES/NO. No partner names,
no buyer names, no amounts, no emails.
"""
from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

_SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "render_trust_badges.py"
_spec = importlib.util.spec_from_file_location("render_trust_badges_mod", _SCRIPT)
renderer = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(renderer)


def _seed_partner_log_with_pii(tmp_path: Path) -> Path:
    p = tmp_path / "partner_outreach_log.json"
    p.write_text(json.dumps({
        "log_id": "L",
        "outreach_sent_count": 1,
        "entries": [{
            "partner_name": "PII Partner Co.",
            "archetype": "Big 4 / Assurance Partner",
            "channel": "email",
            "git_author": "founder@dealix.sa",
            "entry_id": "deadbeef",
        }],
    }))
    return p


def _seed_invoice_log_with_amount(tmp_path: Path) -> Path:
    p = tmp_path / "first_invoice_log.json"
    p.write_text(json.dumps({
        "log_id": "L",
        "invoice_sent_count": 1,
        "entries": [{
            "buyer": "Bank of Saudi PII",
            "amount_sar_disclosed_internally": 25000,
            "entry_id": "cafe",
            "git_author": "founder@dealix.sa",
        }],
    }))
    return p


def test_badge_svgs_never_contain_partner_or_buyer_names(tmp_path, monkeypatch):
    po = _seed_partner_log_with_pii(tmp_path)
    inv = _seed_invoice_log_with_amount(tmp_path)
    # Redirect renderer to the synthetic data.
    monkeypatch.setattr(renderer, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(renderer, "REPORT_PATH", tmp_path / "absent_report.json")

    out = tmp_path / "out"
    renderer.render(out)

    forbidden = [
        "PII Partner Co.",
        "Bank of Saudi PII",
        "founder@dealix.sa",
        "25000",
        "25,000",
        "SAR",
    ]
    for p in out.glob("*.svg"):
        text = p.read_text()
        for bad in forbidden:
            assert bad not in text, f"badge {p.name} leaks {bad!r}"


def test_badge_svgs_have_no_email_or_phone_patterns(tmp_path, monkeypatch):
    monkeypatch.setattr(renderer, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(renderer, "REPORT_PATH", tmp_path / "absent_report.json")
    out = tmp_path / "out"
    renderer.render(out)
    email_rx = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
    phone_rx = re.compile(r"\+?966\d{8,9}")
    for p in out.glob("*.svg"):
        text = p.read_text()
        assert not email_rx.search(text), f"badge {p.name} has email"
        assert not phone_rx.search(text), f"badge {p.name} has phone"
