"""Integration tests for the POST /api/v1/skills/{id}/run endpoint."""

from __future__ import annotations

import pytest


@pytest.mark.asyncio
async def test_handlers_list_returns_registered_ids(async_client) -> None:
    r = await async_client.get("/api/v1/skills/handlers")
    assert r.status_code == 200
    ids = set(r.json()["handlers"])
    # The four real handlers shipped in T8a.
    assert {"sales_qualifier", "lead_scorer", "content_generator_ar", "ar_en_translator"} <= ids


@pytest.mark.asyncio
async def test_skill_list_carries_executable_flag(async_client) -> None:
    r = await async_client.get("/api/v1/skills")
    assert r.status_code == 200
    by_id = {s["id"]: s for s in r.json()["skills"]}
    assert by_id["sales_qualifier"]["executable"] is True
    # A stub skill that has no handler yet.
    assert by_id["proposal_writer"]["executable"] is False


@pytest.mark.asyncio
async def test_run_sales_qualifier_full_bant(async_client) -> None:
    r = await async_client.post(
        "/api/v1/skills/sales_qualifier/run",
        json={
            "inputs": {
                "lead_snapshot": {
                    "budget": "100000 SAR",
                    "authority": "CFO",
                    "need": "AI sales automation",
                    "timeline": "Q3 2026",
                },
                "compliance_signals": {"has_pdpl_consent": True, "dnc_listed": False},
                "locale": "ar",
            }
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert body["skill_id"] == "sales_qualifier"
    assert body["result"]["score"] == 1.0
    assert body["result"]["recommended_action"] == "qualify_and_book_meeting"
    assert body["elapsed_ms"] >= 0


@pytest.mark.asyncio
async def test_run_sales_qualifier_pdpl_gate_caps_score(async_client) -> None:
    r = await async_client.post(
        "/api/v1/skills/sales_qualifier/run",
        json={
            "inputs": {
                "lead_snapshot": {
                    "budget": "yes", "authority": "yes",
                    "need": "yes", "timeline": "yes",
                },
                "compliance_signals": {"has_pdpl_consent": False, "dnc_listed": True},
            }
        },
    )
    assert r.status_code == 200
    # PDPL gate fails → score capped at 0.30.
    assert r.json()["result"]["score"] <= 0.30
    assert r.json()["result"]["gates"]["pdpl"] is False


@pytest.mark.asyncio
async def test_run_lead_scorer_returns_components(async_client) -> None:
    r = await async_client.post(
        "/api/v1/skills/lead_scorer/run",
        json={
            "inputs": {
                "lead": {
                    "industry": "real-estate",
                    "company_size": "enterprise",
                    "role": "CTO",
                    "signals": {"urgency": 0.9, "intent": 0.85},
                }
            }
        },
    )
    assert r.status_code == 200
    res = r.json()["result"]
    assert 0 < res["score"] <= 1.0
    assert set(res["components"]) == {"fit", "urgency", "intent", "sector"}
    assert res["weights_applied"]["fit"] == 0.30


@pytest.mark.asyncio
async def test_run_content_generator_ar_includes_cta_and_hashtags(async_client) -> None:
    r = await async_client.post(
        "/api/v1/skills/content_generator_ar/run",
        json={
            "inputs": {
                "product_name": "Dealix",
                "hook": "نمو B2B بدون فوضى.",
                "audience": "فرق المبيعات",
                "length": "long",
                "tone": "urgent",
            }
        },
    )
    assert r.status_code == 200
    res = r.json()["result"]
    assert "PDPL" in res["copy"]
    assert "ZATCA" in res["copy"]
    assert res["call_to_action"]
    assert len(res["hashtags"]) >= 3


@pytest.mark.asyncio
async def test_run_ar_en_translator_glossary_substitution(async_client) -> None:
    r = await async_client.post(
        "/api/v1/skills/ar_en_translator/run",
        json={"inputs": {"text": "احتاج عرض سعر وفاتورة ZATCA", "from": "ar", "to": "en"}},
    )
    assert r.status_code == 200
    res = r.json()["result"]
    assert "quotation" in res["translated"]
    assert "invoice" in res["translated"]
    assert res["from"] == "ar"
    assert res["to"] == "en"


@pytest.mark.asyncio
async def test_run_skill_404_for_unknown_id(async_client) -> None:
    r = await async_client.post(
        "/api/v1/skills/not-a-real-skill/run", json={"inputs": {}}
    )
    assert r.status_code == 404
    assert r.json()["detail"] == "skill_not_found"


@pytest.mark.asyncio
async def test_run_skill_501_for_skill_without_handler(async_client) -> None:
    # proposal_writer is in the catalogue but no handler registered yet.
    r = await async_client.post(
        "/api/v1/skills/proposal_writer/run", json={"inputs": {}}
    )
    assert r.status_code == 501
    assert r.json()["detail"] == "skill_handler_not_implemented"
