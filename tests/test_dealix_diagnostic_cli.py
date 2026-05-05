"""Tests for scripts/dealix_diagnostic.py.

Pure local generation. NO LLM, NO live sends. The output is a
markdown brief intended for the founder's manual review before
any external send.
"""
from __future__ import annotations

import io
import json
import sys
from contextlib import redirect_stdout
from pathlib import Path

import pytest


SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
SCRIPT = SCRIPTS_DIR / "dealix_diagnostic.py"


def _import_module():
    sys.path.insert(0, str(SCRIPTS_DIR))
    try:
        import dealix_diagnostic  # type: ignore[import-not-found]
        return dealix_diagnostic
    finally:
        sys.path.pop(0)


def test_diagnostic_script_exists_and_has_shebang():
    assert SCRIPT.exists()
    assert SCRIPT.read_text(encoding="utf-8").startswith("#!/usr/bin/env python3")


def test_list_bundles_runs_without_company_arg(capsys):
    mod = _import_module()
    rc = mod.main(["--list-bundles"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "growth_starter" in out
    assert "Available bundles" in out
    assert "Sector → bundle defaults" in out


def test_diagnostic_markdown_includes_bilingual_sections(capsys):
    mod = _import_module()
    rc = mod.main([
        "--company", "ACME Saudi Co.",
        "--sector", "b2b_services",
        "--region", "riyadh",
        "--pipeline-state", "WhatsApp incoming, founder responds at night",
    ])
    out = capsys.readouterr().out
    assert rc == 0
    # Bilingual structure
    assert "القراءة السريعة" in out
    assert "Executive summary (English)" in out
    # Company name preserved verbatim
    assert "ACME Saudi Co." in out
    # Pricing visible
    assert "499" in out
    # Hard rules surfaced — both languages
    assert "no scraping" in out.lower() or "scraping" in out.lower()
    assert "موافقة" in out or "موافقتكم" in out  # consent language
    # Founder review banner
    assert "Founder review required" in out


def test_diagnostic_recommends_bundle_per_sector():
    mod = _import_module()
    matrix = mod._load_matrix()

    md_b2b = mod.render_markdown(
        company="X",
        sector="b2b_services",
        region="ksa",
        pipeline_state="—",
        matrix=matrix,
    )
    md_agency = mod.render_markdown(
        company="X",
        sector="agency",
        region="ksa",
        pipeline_state="—",
        matrix=matrix,
    )
    assert "growth_starter" in md_b2b
    assert "partnership_growth" in md_agency


def test_diagnostic_unknown_sector_falls_back_to_growth_starter():
    mod = _import_module()
    bundle = mod._recommended_bundle("totally_unknown_sector")
    assert bundle == "growth_starter"


def test_diagnostic_json_mode_carries_guardrails(capsys):
    mod = _import_module()
    rc = mod.main([
        "--company", "ACME",
        "--sector", "b2b_services",
        "--region", "riyadh",
        "--pipeline-state", "—",
        "--json",
    ])
    out = capsys.readouterr().out
    assert rc == 0
    payload = json.loads(out)

    assert payload["company"] == "ACME"
    assert payload["recommended_bundle"] == "growth_starter"
    assert payload["approval_status"] == "approval_required"

    g = payload["guardrails"]
    assert g["no_live_send"] is True
    assert g["no_scraping"] is True
    assert g["no_cold_outreach"] is True
    assert g["no_revenue_guarantee"] is True
    assert g["manual_review_before_send"] is True


def test_diagnostic_markdown_never_promises_revenue_or_ranking():
    """Hard rule: the brief must NEVER contain forbidden marketing
    claims. If a future contributor adds 'نضمن' or 'guaranteed' to
    the template, this test fails immediately."""
    mod = _import_module()
    matrix = mod._load_matrix()
    md = mod.render_markdown(
        company="ACME Saudi Co.",
        sector="b2b_services",
        region="riyadh",
        pipeline_state="—",
        matrix=matrix,
    )
    forbidden = [
        "نضمن لكم",      # we guarantee you
        "guaranteed revenue",
        "guaranteed ranking",
        "blast",          # mass outreach
    ]
    for token in forbidden:
        assert token.lower() not in md.lower(), (
            f"diagnostic brief contains forbidden token {token!r}"
        )


def test_diagnostic_requires_company_flag(capsys):
    mod = _import_module()
    with pytest.raises(SystemExit):
        mod.main([
            "--sector", "b2b_services",
            "--region", "riyadh",
        ])
