"""Unit tests for dealix/prompts (T3b)."""

from __future__ import annotations

import pytest

from dealix.prompts import load, snapshot_all


@pytest.mark.parametrize("pid", ["proposal", "icp", "qualification", "reply"])
def test_each_prompt_loads_with_id_version_body(pid: str) -> None:
    p = load(pid)
    assert p.id == pid
    assert p.version
    assert p.body
    assert p.sha256 and len(p.sha256) == 64


def test_snapshot_all_covers_all_four() -> None:
    snap = snapshot_all()
    assert {"proposal", "icp", "qualification", "reply"}.issubset(set(snap.keys()))


def test_proposal_renders_template_variables() -> None:
    p = load("proposal")
    rendered = p.render(
        {
            "sector": "real-estate",
            "company_name": "Acme",
            "pain_points": "long cycles",
            "locale": "ar",
            "recipient_email": "buyer@acme.sa",
        }
    )
    assert "Acme" in rendered
    assert "buyer@acme.sa" in rendered
    # Unresolved $vars are left in safe_substitute by design.


def test_unknown_prompt_raises() -> None:
    with pytest.raises(FileNotFoundError):
        load("does_not_exist")
