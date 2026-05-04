"""
PR-VISION-CLOSE acceptance tests.

Asserts that the eleven items in the vision-close plan are present and wired:

  Acquisition surface:
    A1. Onboarding wizard HTML + JS + endpoint
    A2. 8 per-role landing pages + role-page.js
    A3. Proof Pack PDF generator + endpoints
    A4. WhatsApp brief preview JS

  Vision completeness:
    B1. Call & Meeting Intelligence OS module + meetings router
    B2. meeting_held + meeting_closed RWUs in the catalog
    B3. Role action guard middleware + policy table
    B4. risk_badge field on every Card

  Operating rhythm:
    C1. Daily-ops cron CLI + RAILWAY_CRON.md
    C2. self_growth_mode.loop_once function exists
    C3. why_now_ar enforced at Card schema level
"""

from __future__ import annotations

from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]


# ── Acquisition surface ───────────────────────────────────────────


def test_a1_onboarding_artifacts_exist() -> None:
    assert (REPO / "landing" / "onboarding.html").exists()
    assert (REPO / "landing" / "assets" / "js" / "onboarding-wizard.js").exists()
    assert (REPO / "api" / "routers" / "onboarding.py").exists()


def test_a1_onboarding_router_registered() -> None:
    from api.routers import onboarding  # noqa: F401
    assert hasattr(onboarding, "router")


def test_a1_onboarding_endpoints_present() -> None:
    from api.routers.onboarding import router
    paths = {r.path for r in router.routes}
    assert "/api/v1/onboarding/submit" in paths
    assert "/api/v1/onboarding/eta" in paths


def test_a2_role_pages_all_present() -> None:
    role_dir = REPO / "landing" / "role"
    assert role_dir.exists()
    for slug in ("ceo", "sales", "growth", "revops", "cs", "finance", "compliance", "partner"):
        f = role_dir / f"{slug}.html"
        assert f.exists(), f"missing role page: {f}"
        text = f.read_text(encoding="utf-8")
        assert f'data-role="{slug}"' in text, f"{f.name} missing data-role attr"
    assert (REPO / "landing" / "assets" / "js" / "role-page.js").exists()


def test_a3_proof_pack_pdf_module_exists() -> None:
    from auto_client_acquisition.revenue_company_os import proof_pack_pdf
    assert hasattr(proof_pack_pdf, "render_html")
    assert hasattr(proof_pack_pdf, "render_pdf")


def test_a3_proof_pack_template_exists() -> None:
    assert (REPO / "landing" / "templates" / "proof_pack_pdf.html").exists()


def test_a3_proof_pack_html_endpoint_registered() -> None:
    from api.routers.proof_ledger import router
    paths = {r.path for r in router.routes}
    assert "/api/v1/proof-ledger/customer/{customer_id}/pack.html" in paths
    assert "/api/v1/proof-ledger/customer/{customer_id}/pack.pdf" in paths


def test_a3_render_html_smoke() -> None:
    from auto_client_acquisition.revenue_company_os.proof_pack_builder import build_pack
    from auto_client_acquisition.revenue_company_os.proof_pack_pdf import render_html

    pack = build_pack([], customer_label="acme-co")
    html = render_html(pack, customer_label="acme-co", event_count=0)
    assert "<html" in html.lower()
    assert "acme-co" in html
    assert "Proof Pack" in html


def test_a4_whatsapp_preview_js_exists() -> None:
    assert (REPO / "landing" / "assets" / "js" / "whatsapp-preview.js").exists()


def test_a4_command_center_loads_preview_script() -> None:
    cc = (REPO / "landing" / "command-center.html").read_text(encoding="utf-8")
    assert "whatsapp-preview.js" in cc
    assert "data-whatsapp-preview" in cc


# ── Vision completeness ──────────────────────────────────────────


def test_b1_meeting_intelligence_module_exists() -> None:
    from auto_client_acquisition.revenue_company_os import call_meeting_intelligence_os as m
    assert hasattr(m, "build_brief")
    assert hasattr(m, "meeting_snapshot")
    assert hasattr(m, "top_decisions")


def test_b1_meeting_intelligence_role_supported() -> None:
    from auto_client_acquisition.revenue_company_os.role_brief_builder import SUPPORTED_ROLES, build
    assert "meeting_intelligence" in SUPPORTED_ROLES
    out = build("meeting_intelligence", data={"meetings": [], "proof_events": []})
    assert out["role"] == "meeting_intelligence"
    assert "top_decisions" in out
    assert "blocked_today_ar" in out


def test_b1_meetings_router_registered() -> None:
    from api.routers import meetings
    paths = {r.path for r in meetings.router.routes}
    assert "/api/v1/meetings/log" in paths
    assert "/api/v1/meetings/closed" in paths
    assert "/api/v1/meetings/brief" in paths


def test_b1_meeting_record_model_exists() -> None:
    from db.models import MeetingRecord
    assert MeetingRecord.__tablename__ == "meetings"
    cols = {c.name for c in MeetingRecord.__table__.columns}
    for required in ("id", "customer_id", "occurred_at", "outcome",
                     "follow_up_due_at", "next_action_ar"):
        assert required in cols, f"MeetingRecord missing column {required}"


def test_b2_two_new_rwus_in_catalog() -> None:
    from auto_client_acquisition.revenue_company_os.revenue_work_units import (
        RWU_CATALOG, base_revenue_impact, is_valid_unit, weight_for,
    )
    types = {r.unit_type for r in RWU_CATALOG}
    assert "meeting_held" in types
    assert "meeting_closed" in types
    assert is_valid_unit("meeting_held") is True
    assert is_valid_unit("meeting_closed") is True
    assert weight_for("meeting_closed") == 3.0
    assert base_revenue_impact("meeting_closed") == 5000.0
    assert len(RWU_CATALOG) >= 12


def test_b3_role_action_policy_blocks_known_combos() -> None:
    from auto_client_acquisition.revenue_company_os.role_action_policy import evaluate
    allowed, reason = evaluate("sales_manager", "POST", "/api/v1/payments/charge")
    assert allowed is False
    assert reason and "live charge" in reason or "live" in (reason or "")
    # Empty/None role is always allowed
    assert evaluate(None, "POST", "/api/v1/payments/charge") == (True, None)
    assert evaluate("", "POST", "/api/v1/payments/charge") == (True, None)
    # Unrelated role is allowed for that path
    allowed2, _ = evaluate("ceo", "POST", "/api/v1/payments/charge")
    assert allowed2 is True


def test_b3_middleware_class_importable() -> None:
    from api.middleware import RoleActionGuardMiddleware
    assert RoleActionGuardMiddleware is not None


def test_b4_card_has_risk_badge_field() -> None:
    from auto_client_acquisition.revenue_company_os.cards import Card, CardType, Role, RiskLevel
    c = Card(
        id="x", type=CardType.OPPORTUNITY, role=Role.CEO,
        title_ar="t", why_now_ar="why", recommended_action_ar="ra",
        risk=RiskLevel.HIGH,
    )
    assert c.risk_badge == "P1"
    d = c.to_dict()
    assert d["risk_badge"] == "P1"


# ── Operating rhythm ─────────────────────────────────────────────


def test_c1_cron_cli_exists_and_importable() -> None:
    cli = REPO / "scripts" / "cron_daily_ops.py"
    assert cli.exists()
    text = cli.read_text(encoding="utf-8")
    assert "--window" in text
    assert "morning" in text and "scorecard" in text


def test_c1_railway_cron_doc_exists() -> None:
    assert (REPO / "docs" / "RAILWAY_CRON.md").exists()


def test_c1_railway_json_has_cron_block() -> None:
    import json
    data = json.loads((REPO / "railway.json").read_text(encoding="utf-8"))
    assert "cron" in data
    assert isinstance(data["cron"], list)
    schedules = {entry.get("name") for entry in data["cron"]}
    for w in ("daily-ops-morning", "daily-ops-midday",
              "daily-ops-closing", "daily-ops-scorecard"):
        assert w in schedules, f"railway.json cron missing {w}"


def test_c2_self_growth_loop_once_exists() -> None:
    from auto_client_acquisition.revenue_company_os.self_growth_mode import loop_once
    import inspect
    assert inspect.iscoroutinefunction(loop_once)


def test_c3_card_schema_enforces_why_now() -> None:
    from auto_client_acquisition.revenue_company_os.cards import Card, CardType, Role
    with pytest.raises(ValueError, match="why_now"):
        Card(
            id="x", type=CardType.OPPORTUNITY, role=Role.CEO,
            title_ar="t", why_now_ar="", recommended_action_ar="ra",
        )
