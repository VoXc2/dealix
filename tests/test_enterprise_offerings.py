"""Enterprise transformation catalog — registry, API, and tiered proposals.

Dealix sells governed AI transformation programs (tiered, thousands of SAR),
not chatbots. These tests lock the enterprise offer model + proposal flow.
"""
from __future__ import annotations

import re

from fastapi.testclient import TestClient

from api.main import app
from auto_client_acquisition.sales_os.proposal_renderer import (
    EnterpriseProposalContext,
    render_enterprise_proposal,
)
from auto_client_acquisition.service_catalog import (
    get_enterprise_offering,
    get_enterprise_tier,
    list_enterprise_offerings,
)

client = TestClient(app)

_GUARANTEE = re.compile(r"\bguarantee(d|s)?\b|نضمن", re.IGNORECASE)


def test_six_enterprise_offerings_each_with_three_tiers() -> None:
    offerings = list_enterprise_offerings()
    assert len(offerings) == 6
    for o in offerings:
        assert len(o.tiers) == 3, f"{o.id} must have 3 tiers"
        assert o.name_ar.strip() and o.name_en.strip()
        assert o.workstreams, f"{o.id} has no workstreams"


def test_enterprise_pricing_is_thousands_of_riyals() -> None:
    """Enterprise = large contracts, not 1,500 SAR services."""
    for o in list_enterprise_offerings():
        for t in o.tiers:
            assert t.setup_sar >= 25_000, f"{o.id}/{t.id} setup too small"
            assert t.setup_sar <= 250_000
            assert t.monthly_sar >= 0
            assert t.is_estimate is True


def test_no_guaranteed_language_in_enterprise_registry() -> None:
    """Article 8 — commitment language only, never 'guaranteed'/'نضمن'."""
    for o in list_enterprise_offerings():
        blob = " ".join(
            [o.name_ar, o.name_en, o.summary_ar, o.summary_en]
            + [t.kpi_commitment_ar + " " + t.kpi_commitment_en for t in o.tiers]
        )
        m = _GUARANTEE.search(blob)
        assert m is None, f"{o.id}: forbidden token {m.group(0)!r}"


def test_action_modes_never_live_send_or_charge() -> None:
    forbidden = {"live_send", "live_charge", "auto_send", "auto_charge"}
    for o in list_enterprise_offerings():
        assert not (set(o.action_modes_used) & forbidden), o.id
        assert "no_live_send" in o.hard_gates
        assert "no_live_charge" in o.hard_gates


def test_flagship_transformation_sprint_present() -> None:
    flagship = get_enterprise_offering("enterprise_transformation_sprint")
    assert flagship is not None
    tier_ids = {t.id for t in flagship.tiers}
    assert {"sprint_basic", "sprint_growth", "sprint_enterprise"} == tier_ids
    growth = get_enterprise_tier("enterprise_transformation_sprint", "sprint_growth")
    assert growth is not None and growth.setup_sar == 75_000


def test_enterprise_catalog_endpoint() -> None:
    resp = client.get("/api/v1/services/enterprise/catalog")
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["count"] == 6
    assert "chatbot" in body["positioning"].lower()


def test_enterprise_offering_detail_endpoint() -> None:
    resp = client.get("/api/v1/services/enterprise/ai_operating_system")
    assert resp.status_code == 200, resp.text
    offering = resp.json()["offering"]
    assert len(offering["tiers"]) == 3

    missing = client.get("/api/v1/services/enterprise/does_not_exist")
    assert missing.status_code == 404


def test_flat_catalog_still_returns_seven() -> None:
    """The original 7-offering ladder must remain intact."""
    resp = client.get("/api/v1/services/catalog")
    assert resp.status_code == 200
    assert resp.json()["count"] == 7


def test_enterprise_proposal_renders_all_tiers() -> None:
    offering = get_enterprise_offering("ai_revenue_transformation")
    assert offering is not None
    ctx = EnterpriseProposalContext(
        customer_name="شركة الواحة",
        customer_handle="alwaha",
        sector="real_estate",
        city="Riyadh",
        engagement_id="ENG-100",
        offering=offering,
        recommended_tier_id="rev_growth",
    )
    md = render_enterprise_proposal(ctx)
    assert "55,000" in md  # Growth setup
    assert "recommended" in md or "موصى به" in md
    assert "chatbot" in md.lower()  # the positioning line
    assert _GUARANTEE.search(md) is not None  # only the negation disclaimer


def test_enterprise_proposal_endpoint() -> None:
    resp = client.post(
        "/api/v1/service-setup/enterprise-proposal/acme",
        json={
            "customer_name": "ACME Corp",
            "customer_handle": "acme",
            "sector": "b2b_services",
            "city": "Jeddah",
            "engagement_id": "ENG-200",
            "offering_id": "enterprise_transformation_sprint",
            "recommended_tier_id": "sprint_growth",
        },
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["offering_id"] == "enterprise_transformation_sprint"
    assert len(body["tiers"]) == 3
    assert body["is_estimate"] is True
    assert "proposal_markdown" in body


def test_enterprise_proposal_endpoint_rejects_unknown_offering() -> None:
    resp = client.post(
        "/api/v1/service-setup/enterprise-proposal/acme",
        json={
            "customer_name": "ACME",
            "customer_handle": "acme",
            "engagement_id": "ENG-201",
            "offering_id": "not_a_real_offering",
        },
    )
    assert resp.status_code == 404
