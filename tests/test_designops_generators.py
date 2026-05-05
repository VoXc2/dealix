"""Tests for the DesignOps generators (Phase 5+6+7).

Pure unit tests — no network, no LLM, no DB. Each generator must:
  - return a dict with markdown_ar, markdown_en, html, manifest
  - manifest.safe_to_send must be False (always)
  - manifest.approval_status must be "approval_required"
  - Arabic primary block must be present in the html
  - no forbidden marketing tokens may appear in any rendered surface
"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from api.main import create_app
from auto_client_acquisition.designops.generators import (
    generate_customer_room_dashboard,
    generate_executive_weekly_pack,
    generate_mini_diagnostic,
    generate_pricing_page,
    generate_proof_pack,
    generate_proposal_page,
    html_renderer,
    markdown_renderer,
)


_FORBIDDEN_TOKENS = ("نضمن", "guaranteed", "blast", "scrape")


def _assert_safe_artifact(art: dict, *, expect_keys: bool = True) -> None:
    if expect_keys:
        assert "markdown_ar" in art
        assert "markdown_en" in art
        assert "html" in art
        assert "manifest" in art
    manifest = art["manifest"]
    assert manifest["safe_to_send"] is False
    assert manifest["approval_status"] == "approval_required"
    # Arabic primary signal: html starts with the AR-tagged document.
    assert '<html lang="ar" dir="rtl">' in art["html"]
    # Approval banner present in HTML.
    assert "approval_required" in art["html"]
    # Forbidden tokens must not leak.
    blob = (
        art.get("markdown_ar", "")
        + "\n"
        + art.get("markdown_en", "")
        + "\n"
        + art.get("markdown", "")
        + "\n"
        + art["html"]
    )
    for tok in _FORBIDDEN_TOKENS:
        assert tok not in blob, f"forbidden token leaked: {tok!r}"


# ── Renderer unit tests ────────────────────────────────────────────


def test_html_renderer_basic_structure() -> None:
    html = html_renderer.render_artifact_html(
        title_ar="عنوان",
        title_en="Title",
        sections_ar=[{"title": "قسم", "body": "محتوى"}],
        sections_en=[{"title": "Section", "body": "content"}],
        approval_status="approval_required",
        audience="internal_review",
        evidence_refs=["ref:1"],
    )
    assert '<html lang="ar" dir="rtl">' in html
    assert "approval_required" in html
    assert "internal_review" in html
    assert "ref:1" in html
    assert "Founder approval required" in html
    # No external CDN.
    assert "cdn." not in html.lower()
    assert "https://" not in html  # all assets inline


def test_markdown_renderer_arabic_first_separator_then_english() -> None:
    md = markdown_renderer.render_artifact_markdown(
        title_ar="عنوان",
        title_en="Title",
        sections_ar=[{"title": "قسم", "body": "محتوى"}],
        sections_en=[{"title": "Section", "body": "content"}],
        approval_status="approval_required",
        audience="internal_review",
        evidence_refs=["ref:1"],
    )
    # Arabic title appears before English title (Arabic primary).
    ar_idx = md.index("عنوان")
    en_idx = md.index("Title")
    assert ar_idx < en_idx
    assert "---" in md
    assert "approval_required" in md
    assert "Founder approval required" in md


# ── Mini diagnostic ────────────────────────────────────────────────


def test_generate_mini_diagnostic_returns_safe_artifact() -> None:
    art = generate_mini_diagnostic(
        company="ACME Saudi Co.",
        sector="b2b_services",
        region="riyadh",
        pipeline_state="WhatsApp incoming, founder responds at night",
    )
    _assert_safe_artifact(art)
    assert art["manifest"]["artifact_type"] == "mini_diagnostic"
    assert "ACME" in art["html"]


def test_generate_mini_diagnostic_internal_review_audience() -> None:
    art = generate_mini_diagnostic(
        company="X Co",
        sector="b2b_saas",
        region="ksa",
        pipeline_state="",
    )
    assert art["manifest"]["audience"] == "internal_review"
    assert isinstance(art["manifest"]["evidence_refs"], list)


# ── Proof pack ─────────────────────────────────────────────────────


def test_generate_proof_pack_no_consent_is_internal_only() -> None:
    events = [
        {
            "event_type": "delivery_complete",
            "service_id": "growth_starter",
            "outcome_metric": "qualified_leads",
            "outcome_value": "10",
            "consent_for_publication": False,
            "customer_anonymized": "Saudi B2B customer",
        }
    ]
    art = generate_proof_pack(
        customer_handle="Saudi B2B customer",
        events=events,
        period_label="2026-W18",
    )
    _assert_safe_artifact(art)
    assert art["manifest"]["audience"] == "internal_only"


def test_generate_proof_pack_empty_events_still_safe() -> None:
    art = generate_proof_pack(
        customer_handle="anon",
        events=[],
    )
    _assert_safe_artifact(art)
    assert art["manifest"]["artifact_type"] == "proof_pack"


# ── Executive weekly pack ──────────────────────────────────────────


def test_generate_executive_weekly_pack_safe_artifact() -> None:
    art = generate_executive_weekly_pack(week_label="2026-W18")
    _assert_safe_artifact(art)
    assert art["manifest"]["artifact_type"] == "executive_weekly_pack"
    assert "2026-W18" in art["html"] or "2026-W18" in art["markdown_ar"]


# ── Proposal ───────────────────────────────────────────────────────


def test_generate_proposal_page_safe_artifact() -> None:
    art = generate_proposal_page(
        customer_handle="ACME",
        recommended_service="growth_starter",
        scope_ar="مساعدة الفريق على إغلاق صفقات B2B خلال 7 أيّام.",
        scope_en="Help the team close B2B deals within 7 days.",
        deliverables=["10 Arabic drafts", "Follow-up plan"],
        timeline_days=7,
        price_band_sar="499",
        blocked_actions=["No cold WhatsApp"],
        proof_plan=["Daily ledger entries"],
    )
    _assert_safe_artifact(art)
    assert art["manifest"]["artifact_type"] == "proposal_page"


# ── Pricing ────────────────────────────────────────────────────────


def test_generate_pricing_page_safe_artifact() -> None:
    art = generate_pricing_page()
    _assert_safe_artifact(art)
    assert art["manifest"]["artifact_type"] == "pricing_page"
    assert art["manifest"]["tier_count"] >= 7


# ── Customer room ──────────────────────────────────────────────────


def test_generate_customer_room_dashboard_safe_artifact() -> None:
    art = generate_customer_room_dashboard(
        customer_handle="ACME",
        customer_payload={"stage": "pilot", "active_services": ["growth_starter"]},
    )
    _assert_safe_artifact(art)
    assert art["manifest"]["artifact_type"] == "customer_room_dashboard"


# ── Router smoke ───────────────────────────────────────────────────


@pytest.fixture(scope="module")
def client() -> TestClient:
    return TestClient(create_app())


def test_designops_status_endpoint(client: TestClient) -> None:
    resp = client.get("/api/v1/designops/status")
    assert resp.status_code == 200
    body = resp.json()
    assert body["module"] == "designops"
    g = body["guardrails"]
    assert g["no_llm_call"] is True
    assert g["no_external_http"] is True
    assert g["safe_to_send_default"] is False


def test_designops_skills_endpoint_defensive(client: TestClient) -> None:
    resp = client.get("/api/v1/designops/skills")
    assert resp.status_code == 200
    body = resp.json()
    assert "skills" in body
    assert isinstance(body["skills"], list)


def test_designops_generate_mini_diagnostic_endpoint(client: TestClient) -> None:
    resp = client.post(
        "/api/v1/designops/generate/mini-diagnostic",
        json={
            "company": "ACME",
            "sector": "b2b_services",
            "region": "ksa",
            "pipeline_state": "manual handoff",
        },
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["manifest"]["safe_to_send"] is False
    assert body["manifest"]["approval_status"] == "approval_required"


def test_designops_generate_pricing_page_endpoint(client: TestClient) -> None:
    resp = client.post(
        "/api/v1/designops/generate/pricing-page",
        json={"highlight": "growth_starter"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["manifest"]["artifact_type"] == "pricing_page"
    assert body["manifest"]["safe_to_send"] is False
