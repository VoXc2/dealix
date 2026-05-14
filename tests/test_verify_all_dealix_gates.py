"""Unit tests for the readiness-gate logic in ``scripts/verify_all_dealix.py``.

Locks the score-5 contracts and dishonesty-rejection behavior that the
matrix declares. These checks otherwise have no automated coverage —
which is how Codex was able to spot multiple gate-truth violations only
during review.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def _load_verifier(monkeypatch, tmp_root: Path):
    """Import ``scripts.verify_all_dealix`` with REPO_ROOT pointed at a
    fresh temporary tree, so we can stage minimal fixtures per test."""
    scripts_dir = Path(__file__).resolve().parent.parent / "scripts"
    monkeypatch.syspath_prepend(str(scripts_dir))
    sys.modules.pop("verify_all_dealix", None)
    import verify_all_dealix as mod  # type: ignore

    mod.REPO_ROOT = tmp_root
    return mod


def _seed_partner_pipeline(tmp_root: Path) -> None:
    docs = tmp_root / "docs/sales-kit"
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "ANCHOR_PARTNER_OUTREACH.md").write_text("# anchor outreach", encoding="utf-8")
    data = tmp_root / "data"
    data.mkdir(parents=True, exist_ok=True)
    (data / "anchor_partner_pipeline.json").write_text(
        json.dumps({"partner_archetypes": ["TIER1_SI", "TIER1_RESELLER"]}),
        encoding="utf-8",
    )


def _seed_first_invoice_log(tmp_root: Path, log: dict) -> None:
    docs = tmp_root / "docs/ops"
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "FIRST_INVOICE_UNLOCK.md").write_text("# first invoice", encoding="utf-8")
    data = tmp_root / "data"
    data.mkdir(parents=True, exist_ok=True)
    (data / "first_invoice_log.json").write_text(json.dumps(log), encoding="utf-8")


# ── check_founder_command_center ─────────────────────────────────


def test_fcc_marker_without_page_is_now_failing(monkeypatch, tmp_path: Path) -> None:
    mod = _load_verifier(monkeypatch, tmp_path)
    (tmp_path / "data").mkdir(parents=True, exist_ok=True)
    (tmp_path / "data/founder_command_center_status.json").write_text(
        json.dumps({"deployment_marker": True, "page_path": "no/such/page.html"}),
        encoding="utf-8",
    )
    result = mod.check_founder_command_center()
    assert result.pass_ is False
    assert "page artifact missing" in result.details


def test_fcc_page_path_must_stay_inside_repo(monkeypatch, tmp_path: Path) -> None:
    mod = _load_verifier(monkeypatch, tmp_path)
    (tmp_path / "data").mkdir(parents=True, exist_ok=True)
    (tmp_path / "data/founder_command_center_status.json").write_text(
        json.dumps({"deployment_marker": True, "page_path": "/etc/hosts"}),
        encoding="utf-8",
    )
    result = mod.check_founder_command_center()
    assert result.pass_ is False


# ── check_partner_motion ─────────────────────────────────────────


def test_partner_motion_score5_requires_founder_confirmed(
    monkeypatch, tmp_path: Path
) -> None:
    mod = _load_verifier(monkeypatch, tmp_path)
    _seed_partner_pipeline(tmp_path)
    (tmp_path / "data/partner_outreach_log.json").write_text(
        json.dumps(
            {
                "outreach_sent_count": 2,
                "entries": [
                    {"partner": "A", "founder_confirmed": False},
                    {"partner": "B", "founder_confirmed": False},
                ],
            }
        ),
        encoding="utf-8",
    )
    result = mod.check_partner_motion()
    assert result.score == 4
    assert "none founder-confirmed" in result.details


def test_partner_motion_score5_with_founder_confirmed(
    monkeypatch, tmp_path: Path
) -> None:
    mod = _load_verifier(monkeypatch, tmp_path)
    _seed_partner_pipeline(tmp_path)
    (tmp_path / "data/partner_outreach_log.json").write_text(
        json.dumps(
            {
                "outreach_sent_count": 1,
                "entries": [{"partner": "A", "founder_confirmed": True}],
            }
        ),
        encoding="utf-8",
    )
    result = mod.check_partner_motion()
    assert result.score == 5


def test_partner_motion_rejects_dishonest_ceo_complete(
    monkeypatch, tmp_path: Path
) -> None:
    mod = _load_verifier(monkeypatch, tmp_path)
    _seed_partner_pipeline(tmp_path)
    (tmp_path / "data/partner_outreach_log.json").write_text(
        json.dumps(
            {
                "outreach_sent_count": 0,
                "ceo_complete": True,
                "entries": [],
            }
        ),
        encoding="utf-8",
    )
    result = mod.check_partner_motion()
    assert result.pass_ is False
    assert "dishonest" in result.details


# ── check_first_invoice_motion ───────────────────────────────────


def test_first_invoice_score5_requires_proof_target(
    monkeypatch, tmp_path: Path
) -> None:
    mod = _load_verifier(monkeypatch, tmp_path)
    _seed_first_invoice_log(
        tmp_path,
        {
            "invoice_sent_count": 1,
            "invoice_paid_count": 1,
            "entries": [{"invoice_no": "INV-1"}],  # no proof_target
        },
    )
    result = mod.check_first_invoice_motion()
    assert result.score == 4
    assert "proof_target" in result.details


def test_first_invoice_score5_with_proof_target(
    monkeypatch, tmp_path: Path
) -> None:
    mod = _load_verifier(monkeypatch, tmp_path)
    _seed_first_invoice_log(
        tmp_path,
        {
            "invoice_sent_count": 1,
            "invoice_paid_count": 1,
            "entries": [
                {"invoice_no": "INV-1", "proof_target": "case_study_alpha"}
            ],
        },
    )
    result = mod.check_first_invoice_motion()
    assert result.score == 5


# ── check_open_doctrine ──────────────────────────────────────────


def test_open_doctrine_scans_all_markdown_in_dir(
    monkeypatch, tmp_path: Path
) -> None:
    mod = _load_verifier(monkeypatch, tmp_path)
    doctrine = tmp_path / "open-doctrine"
    doctrine.mkdir(parents=True)
    (doctrine / "README.md").write_text("# doctrine", encoding="utf-8")
    (doctrine / "11_NON_NEGOTIABLES.md").write_text("# rules", encoding="utf-8")
    (doctrine / "CONTROL_MAPPING.md").write_text("# mapping", encoding="utf-8")
    # New file (not in the hardcoded list) that contains a leak
    (doctrine / "FRESH_PAGE.md").write_text(
        "the Password for admin is leaked here", encoding="utf-8"
    )
    result = mod.check_open_doctrine()
    assert result.pass_ is False
    assert "FRESH_PAGE" in result.details
    assert "password" in result.details
