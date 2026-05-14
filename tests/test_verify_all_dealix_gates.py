"""Unit tests for the readiness-gate logic in ``scripts/verify_all_dealix.py``.

Locks the score-5 contracts and dishonesty-rejection behavior that the
matrix declares. These checks otherwise have no automated coverage —
which is how Codex was able to spot multiple gate-truth violations only
during review.
"""

from __future__ import annotations

import json
from pathlib import Path


def _load_verifier(monkeypatch, tmp_root: Path):
    """Import ``scripts.verify_all_dealix`` and point its ``REPO_ROOT`` at a
    fresh temporary tree for the duration of this test only.

    The previous implementation mutated the cached module's ``REPO_ROOT``
    by direct assignment. That leaked the temp path into other test files
    (e.g. ``tests/test_wave19_recovery_verifier.py``) which reuse the
    cached module via ``sys.modules`` — once the first test in this file
    ran, every later test that touched ``verify_all_dealix`` started
    reading fixtures from ``tmp_path``. ``monkeypatch.setattr`` reverts
    the attribute on teardown, so the cached module's ``REPO_ROOT`` is
    restored to the real repository root before the next test runs.
    """
    scripts_dir = Path(__file__).resolve().parent.parent / "scripts"
    monkeypatch.syspath_prepend(str(scripts_dir))
    import verify_all_dealix as mod  # type: ignore

    monkeypatch.setattr(mod, "REPO_ROOT", tmp_root)
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


def test_fcc_rejects_directory_as_page_artifact(
    monkeypatch, tmp_path: Path
) -> None:
    """A directory under the repo (e.g. ``docs/``) must NOT satisfy the
    founder-page gate — only a real file artifact does."""
    mod = _load_verifier(monkeypatch, tmp_path)
    (tmp_path / "data").mkdir(parents=True, exist_ok=True)
    (tmp_path / "data/founder_command_center_status.json").write_text(
        json.dumps({"deployment_marker": True, "page_path": "docs/"}),
        encoding="utf-8",
    )
    (tmp_path / "docs").mkdir(parents=True, exist_ok=True)  # dir exists
    result = mod.check_founder_command_center()
    assert result.pass_ is False
    assert "page artifact missing" in result.details


def test_partner_motion_strict_founder_confirmed_boolean(
    monkeypatch, tmp_path: Path
) -> None:
    """Truthy non-True values (``"false"``, ``1``, ``"yes"``) must NOT
    pass the founder-confirmed gate — only the boolean ``True`` does."""
    mod = _load_verifier(monkeypatch, tmp_path)
    _seed_partner_pipeline(tmp_path)
    (tmp_path / "data/partner_outreach_log.json").write_text(
        json.dumps(
            {
                "outreach_sent_count": 3,
                "entries": [
                    {"partner": "A", "founder_confirmed": "false"},
                    {"partner": "B", "founder_confirmed": "yes"},
                    {"partner": "C", "founder_confirmed": 1},
                ],
            }
        ),
        encoding="utf-8",
    )
    result = mod.check_partner_motion()
    assert result.score == 4
    assert "none founder-confirmed" in result.details


def test_first_invoice_strict_proof_target_string(
    monkeypatch, tmp_path: Path
) -> None:
    """Non-string sentinels (``None`` / ``False``) coerced via ``str(...)``
    must NOT satisfy the proof-target gate."""
    mod = _load_verifier(monkeypatch, tmp_path)
    _seed_first_invoice_log(
        tmp_path,
        {
            "invoice_sent_count": 2,
            "invoice_paid_count": 2,
            "entries": [
                {"invoice_no": "INV-1", "proof_target": None},
                {"invoice_no": "INV-2", "proof_target": False},
            ],
        },
    )
    result = mod.check_first_invoice_motion()
    assert result.score == 4
    assert "no entry carries proof_target evidence" in result.details


def test_ceo_complete_requires_partner_motion_score_5(
    monkeypatch, tmp_path: Path
) -> None:
    """At Partner Motion score 4 (outreach sent but no founder-confirmed),
    ``ceo_complete`` must be False — score 4 means the founder hasn't
    yet performed the confirming market action."""
    mod = _load_verifier(monkeypatch, tmp_path)

    class _R:
        def __init__(self, system, score, pass_):
            self.system = system
            self.score = score
            self.pass_ = pass_

    monkeypatch.setattr(
        mod,
        "CHECKS",
        [
            lambda: _R("Offer Ladder", 4, True),
            lambda: _R("Founder Command Center", 4, True),
            lambda: _R("Partner Motion", 4, True),       # outreach sent, not confirmed
            lambda: _R("First Invoice Motion", 4, True),  # sent, unpaid
            lambda: _R("Funding Pack", 4, True),
            lambda: _R("GCC Expansion", 4, True),
            lambda: _R("Open Doctrine", 4, True),
        ],
    )
    _, all_pass, ceo_complete = mod.run()
    assert all_pass is True
    assert ceo_complete is False, (
        "Partner Motion at 4 means no founder-confirmed entry; "
        "ceo_complete must NOT fire yet"
    )


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
