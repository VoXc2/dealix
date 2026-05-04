"""
Phases 2 / 3 / 4 acceptance tests.

Phase 2 — Delivery Engine: full E2E sprint flow (start → 7 days → close-out)
Phase 3 — Learning skeleton: module imports + /api/v1/learning/playbook
Phase 4 — 6 product brand pages: files exist + correct data-product
"""

from __future__ import annotations

from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]


# ── Phase 2: Delivery Engine ──────────────────────────────────────


def test_phase_2_sprint_record_model() -> None:
    from db.models import SprintRecord
    cols = {c.name for c in SprintRecord.__table__.columns}
    for required in (
        "id", "customer_id", "service_id", "started_at",
        "current_day", "status", "contract_snapshot_json",
        "day_outputs", "completed_at", "proof_pack_event_id",
    ):
        assert required in cols, f"SprintRecord missing field {required}"


def test_phase_2_sprint_templates_importable() -> None:
    from auto_client_acquisition.delivery import (
        generate_close_out, generate_diagnostic, generate_meeting_prep,
        generate_message_pack, generate_opportunity_pack,
        generate_pipeline_review, generate_proof_draft,
    )
    # All 7 generators must accept brain dict + return dict
    brain = {"company_name": "T", "sector": "B2B", "city": "Riyadh"}
    for fn in (generate_diagnostic, generate_opportunity_pack,
               generate_message_pack, generate_meeting_prep):
        out = fn(brain)
        assert isinstance(out, dict)
        assert "day" in out


def test_phase_2_diagnostic_shape() -> None:
    from auto_client_acquisition.delivery import generate_diagnostic
    out = generate_diagnostic({"company_name": "Acme", "sector": "SaaS", "city": "Riyadh"})
    assert out["day"] == 1
    assert out["kind"] == "diagnostic"
    assert "best_segment_ar" in out
    assert "quick_wins" in out
    assert len(out["quick_wins"]) >= 3
    assert "risk_to_avoid_ar" in out


def test_phase_2_opportunity_pack_returns_10() -> None:
    from auto_client_acquisition.delivery import generate_opportunity_pack
    out = generate_opportunity_pack({"average_deal_value_sar": 5000, "company_name": "Acme",
                                     "sector": "B2B", "city": "Jeddah"})
    assert out["count"] == 10
    assert len(out["opportunities"]) == 10
    for opp in out["opportunities"]:
        assert "n" in opp
        assert "why_now_ar" in opp
        assert "recommended_channel_ar" in opp


def test_phase_2_message_pack_has_6_first_3_followups_2_objections() -> None:
    from auto_client_acquisition.delivery import generate_message_pack
    out = generate_message_pack({"company_name": "Acme", "offer_ar": "consulting", "sector": "B2B"})
    assert len(out["first_messages_ar"]) == 6
    assert len(out["follow_ups_ar"]) == 3
    assert len(out["objection_responses"]) == 2
    assert "blocked_phrases_ar" in out


def test_phase_2_close_out_has_upsell() -> None:
    from auto_client_acquisition.delivery import generate_close_out
    out = generate_close_out({"company_name": "Acme"}, proof_draft={"expected_revenue_impact_sar": 1000})
    assert out["day"] == 7
    upsell = out.get("upsell") or {}
    assert upsell.get("service_id") == "executive_growth_os"
    assert "2,999" in upsell.get("price_label", "")


def test_phase_2_router_registered() -> None:
    from api.routers.sprints import router
    paths = {r.path for r in router.routes}
    for required in (
        "/api/v1/sprints/start",
        "/api/v1/sprints/{sprint_id}",
        "/api/v1/sprints/by-customer/{customer_id}",
        "/api/v1/sprints/{sprint_id}/diagnostic/generate",
        "/api/v1/sprints/{sprint_id}/opportunities/generate",
        "/api/v1/sprints/{sprint_id}/messages/generate",
        "/api/v1/sprints/{sprint_id}/meeting-prep",
        "/api/v1/sprints/{sprint_id}/review",
        "/api/v1/sprints/{sprint_id}/proof/draft",
        "/api/v1/sprints/{sprint_id}/close-out",
    ):
        assert required in paths, f"sprints router missing {required}"


@pytest.mark.asyncio
async def test_phase_2_full_e2e_sprint(async_client) -> None:
    """End-to-end: prospect → closed_won (auto-creates Customer with Brain) →
    start sprint → run all 7 days → close-out emits proof event."""
    # 1. Create + advance prospect
    create = await async_client.post(
        "/api/v1/prospects",
        json={
            "name": "sprint_e2e",
            "company": "Sprint Test Co",
            "sector": "B2B SaaS",
            "city": "Riyadh",
            "expected_value_sar": 499.0,
            "relationship_type": "warm_1st_degree",
        },
    )
    pid = create.json()["id"]
    for target in ("messaged", "replied", "meeting_booked",
                   "pilot_offered", "invoice_sent",
                   "paid_or_committed", "closed_won"):
        r = await async_client.post(
            f"/api/v1/prospects/{pid}/advance",
            json={"target_status": target},
        )
        assert r.status_code == 200, f"advance to {target} failed"

    p = await async_client.get(f"/api/v1/prospects/{pid}")
    cust_id = p.json()["customer_id"]
    assert cust_id

    # 2. Start sprint
    start = await async_client.post(
        "/api/v1/sprints/start",
        json={"customer_id": cust_id, "service_id": "growth_starter"},
    )
    assert start.status_code == 200, start.text
    sprint_id = start.json()["sprint_id"]
    assert sprint_id

    # 3. Run all 7 days
    day1 = await async_client.post(f"/api/v1/sprints/{sprint_id}/diagnostic/generate")
    assert day1.status_code == 200
    assert day1.json()["day"] == 1
    assert "best_segment_ar" in day1.json()["output"]

    day2 = await async_client.post(f"/api/v1/sprints/{sprint_id}/opportunities/generate")
    assert day2.status_code == 200
    assert day2.json()["output"]["count"] == 10

    day3 = await async_client.post(f"/api/v1/sprints/{sprint_id}/messages/generate")
    assert day3.status_code == 200
    assert len(day3.json()["output"]["first_messages_ar"]) == 6

    day4 = await async_client.post(f"/api/v1/sprints/{sprint_id}/meeting-prep")
    assert day4.status_code == 200
    assert "meeting_agenda" in day4.json()["output"]

    day5 = await async_client.get(f"/api/v1/sprints/{sprint_id}/review")
    assert day5.status_code == 200
    assert "summary" in day5.json()["output"]

    day6 = await async_client.post(f"/api/v1/sprints/{sprint_id}/proof/draft")
    assert day6.status_code == 200
    assert "expected_revenue_impact_sar" in day6.json()["output"]

    day7 = await async_client.post(f"/api/v1/sprints/{sprint_id}/close-out", json={})
    assert day7.status_code == 200
    body7 = day7.json()
    assert body7["status"] == "completed"
    assert body7["output"]["day"] == 7
    assert body7["output"]["upsell"]["service_id"] == "executive_growth_os"

    # 4. Final state shows all 7 days
    final = await async_client.get(f"/api/v1/sprints/{sprint_id}")
    body = final.json()
    assert body["status"] == "completed"
    assert body["current_day"] == 7
    for d in range(1, 8):
        assert f"day_{d}" in body["day_outputs"], f"missing day_{d} output"


# ── Phase 3: Learning skeleton ────────────────────────────────────


def test_phase_3_modules_importable() -> None:
    from auto_client_acquisition.learning import (
        analyze_channels, mine_objections, score_messages,
    )
    # Empty input → empty result, no crash
    assert mine_objections([])["library"] == []
    assert score_messages([])["experiments_count"] == 0
    assert analyze_channels([])["channels_count"] == 0


@pytest.mark.asyncio
async def test_phase_3_playbook_endpoint(async_client) -> None:
    r = await async_client.get("/api/v1/learning/playbook?days=30")
    assert r.status_code == 200
    body = r.json()
    for k in ("channel_performance", "message_experiments", "objection_library", "phase"):
        assert k in body
    assert body["phase"] == "phase_3_skeleton"


# ── Phase 4: Product brand pages ──────────────────────────────────


def test_phase_4_product_pages_all_present() -> None:
    products_dir = REPO / "landing" / "products"
    assert products_dir.exists()
    for slug in ("command", "sell", "grow", "serve", "partner", "proof"):
        f = products_dir / f"{slug}.html"
        assert f.exists(), f"missing product page: {f}"
        text = f.read_text(encoding="utf-8")
        assert f'data-product="{slug}"' in text, f"{f.name} missing data-product attr"
        assert "product-page.js" in text


def test_phase_4_product_page_js_exists() -> None:
    p = REPO / "landing" / "assets" / "js" / "product-page.js"
    assert p.exists()
    text = p.read_text(encoding="utf-8")
    # All 6 brands referenced
    for slug in ("command", "sell", "grow", "serve", "partner", "proof"):
        assert slug in text, f"product-page.js missing brand {slug}"
