"""PR-LAUNCH-FINAL — verify the launch package is in place + green.

These tests ensure the artifacts that turn "code ready" into "launch ready"
all exist on disk and can be imported. They do NOT hit a deployed URL.
"""

from __future__ import annotations

import importlib
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]


# ── Frontend artifacts ───────────────────────────────────────────


def test_proof_pack_js_exists_and_nontrivial():
    p = REPO / "landing" / "assets" / "js" / "proof-pack.js"
    assert p.exists(), "landing/assets/js/proof-pack.js missing — broken reference in proof-pack.html"
    text = p.read_text(encoding="utf-8")
    assert len(text) > 500, "proof-pack.js should not be a stub"
    assert "/api/v1/proof-ledger" in text, "proof-pack.js must hit /api/v1/proof-ledger"


def test_command_center_widgets_js_exists():
    p = REPO / "landing" / "assets" / "js" / "command-center-widgets.js"
    assert p.exists()
    text = p.read_text(encoding="utf-8")
    assert "data-widget=\"daily-ops\"" in text or "daily-ops" in text
    assert "/api/v1/observability/costs/summary" in text
    assert "/api/v1/observability/unsafe/summary" in text
    assert "/api/v1/daily-ops/history" in text


def test_command_center_html_includes_widgets():
    p = REPO / "landing" / "command-center.html"
    text = p.read_text(encoding="utf-8")
    assert 'command-center-widgets.js' in text
    for marker in ('data-widget="daily-ops"', 'data-widget="cost-summary"', 'data-widget="unsafe-blocked"'):
        assert marker in text, f"missing widget placeholder: {marker}"


# ── Deployment artifacts ─────────────────────────────────────────


def test_dockerfile_exists():
    p = REPO / "Dockerfile"
    assert p.exists()
    text = p.read_text(encoding="utf-8")
    assert "FROM" in text and "python" in text.lower()
    assert "uvicorn" in text or "CMD" in text


def test_dockerignore_exists():
    p = REPO / ".dockerignore"
    assert p.exists()


def test_railway_json_valid():
    import json
    p = REPO / "railway.json"
    assert p.exists()
    data = json.loads(p.read_text(encoding="utf-8"))
    deploy = data.get("deploy") or {}
    assert deploy.get("healthcheckPath") == "/healthz"


def test_env_staging_example_covers_critical_vars():
    p = REPO / ".env.staging.example"
    assert p.exists()
    text = p.read_text(encoding="utf-8")
    required = (
        "APP_ENV", "DATABASE_URL", "ANTHROPIC_API_KEY",
        "WHATSAPP_ALLOW_LIVE_SEND", "GMAIL_ALLOW_LIVE_SEND",
        "MOYASAR_ALLOW_LIVE_CHARGE", "LINKEDIN_ALLOW_AUTO_DM",
        "RESEND_ALLOW_LIVE_SEND", "APP_SECRET_KEY",
    )
    for var in required:
        assert var in text, f"{var} not documented in .env.staging.example"


# ── Operations docs ──────────────────────────────────────────────


@pytest.mark.parametrize("doc", [
    "RUNBOOK.md",
    "OUTREACH_PLAYBOOK.md",
    "LAUNCH_DAY_CHECKLIST.md",
    "FIRST_PILOT_INTAKE.md",
])
def test_required_doc_exists(doc):
    p = REPO / "docs" / doc
    assert p.exists(), f"docs/{doc} missing — required for launch"
    assert p.stat().st_size > 1000, f"docs/{doc} looks like a stub"


def test_runbook_mentions_daily_ops_windows():
    text = (REPO / "docs" / "RUNBOOK.md").read_text(encoding="utf-8")
    for window in ("morning", "midday", "closing", "scorecard"):
        assert window in text, f"RUNBOOK missing window: {window}"


def test_outreach_playbook_has_six_templates():
    text = (REPO / "docs" / "OUTREACH_PLAYBOOK.md").read_text(encoding="utf-8")
    # 6 LinkedIn templates were planned; weak check: count headings
    assert text.count("Template ") >= 6


def test_launch_day_checklist_has_d_minus_7_to_d_plus_7():
    text = (REPO / "docs" / "LAUNCH_DAY_CHECKLIST.md").read_text(encoding="utf-8")
    for marker in ("D-7", "D-1", "D0", "D+1", "D+7"):
        assert marker in text, f"LAUNCH_DAY_CHECKLIST missing: {marker}"


def test_first_pilot_intake_has_definition_of_done():
    text = (REPO / "docs" / "FIRST_PILOT_INTAKE.md").read_text(encoding="utf-8")
    assert "Definition of Done" in text or "DoD" in text
    assert "499" in text  # the price point
    assert "/api/v1/proof-ledger" in text  # references the live API


# ── Tooling ──────────────────────────────────────────────────────


def test_staging_smoke_script_exists_and_imports():
    p = REPO / "scripts" / "staging_smoke.py"
    assert p.exists()
    mod = importlib.import_module("scripts.staging_smoke")
    assert hasattr(mod, "run_smoke")
    assert hasattr(mod, "PROBES")
    assert len(mod.PROBES) >= 12


def test_launch_checklist_script_exists_and_imports():
    p = REPO / "scripts" / "launch_checklist.py"
    assert p.exists()
    mod = importlib.import_module("scripts.launch_checklist")
    assert hasattr(mod, "run")


def test_launch_checklist_returns_launch_ready():
    """End-to-end: the LAUNCH_READY gate must still be green."""
    from scripts.launch_checklist import run
    report = run()
    failed = [c for c in report.checks if not c.passed]
    assert report.passed, "launch_checklist BLOCKED:\n" + "\n".join(
        f"  - {c.name}: {c.detail}" for c in failed
    )


# ── Single-source-of-truth invariants ────────────────────────────


def test_eight_live_action_gates_default_false():
    from core.config.settings import Settings
    s = Settings()
    gates = (
        "whatsapp_allow_live_send",
        "gmail_allow_live_send",
        "moyasar_allow_live_charge",
        "linkedin_allow_auto_dm",
        "resend_allow_live_send",
        "whatsapp_allow_internal_send",
        "whatsapp_allow_customer_send",
        "calls_allow_live_dial",
    )
    flipped = [g for g in gates if getattr(s, g, None) is True]
    assert not flipped, f"these gates must default False but are True: {flipped}"


def test_service_tower_all_sellable():
    from auto_client_acquisition.service_tower.excellence_score import all_excellence
    out = all_excellence()
    summary = out["summary"]
    assert summary["internal_only"] == 0
    assert summary["beta_only"] == 0
    assert summary["sellable"] == summary["total"]
