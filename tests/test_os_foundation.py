"""
PR-OS-FOUNDATION acceptance tests — covers all 9 sub-items in one file.

Sub-items:
  1.1 ProspectRecord compliance fields
  1.2 Stage Machine v2 (14 stages, forward-only)
  1.3 Service Contracts (6 bundles + endpoint)
  1.4 Customer Workspace endpoint
  1.5 Approval Queue endpoints
  1.6 /api/v1/learning/weekly endpoint
  1.7 Company Brain (CustomerRecord 12 fields + GET/PATCH /brain)
  1.8 Verification tooling docs exist
  1.9 Forbidden Claims at draft generation
"""

from __future__ import annotations

from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]


# ── 1.1 ProspectRecord compliance fields ──────────────────────────


def test_1_1_prospect_compliance_fields_exist() -> None:
    from db.models import ProspectRecord
    cols = {c.name for c in ProspectRecord.__table__.columns}
    for required in (
        "source_type", "consent_status", "consent_source",
        "last_customer_inbound_at", "allowed_channels", "blocked_channels",
        "risk_reason", "human_approval_required",
    ):
        assert required in cols, f"ProspectRecord missing field {required}"


# ── 1.2 Stage Machine v2 ──────────────────────────────────────────


def test_1_2_stage_ladder_has_14_stages() -> None:
    from api.routers.prospects import _STATUS_LADDER
    assert len(_STATUS_LADDER) >= 13  # 14 incl. closed_lost
    for stage in (
        "new", "qualified", "messaged", "replied", "diagnostic_sent",
        "meeting_booked", "pilot_offered", "invoice_sent", "paid_or_committed",
        "closed_won", "proof_delivered", "retainer_offered", "retainer_won",
        "closed_lost",
    ):
        assert stage in _STATUS_LADDER, f"missing stage {stage}"


def test_1_2_legacy_alias_resolves() -> None:
    from api.routers.prospects import _resolve_status
    assert _resolve_status("identified") == "new"
    assert _resolve_status("meeting") == "meeting_booked"
    assert _resolve_status("pilot") == "pilot_offered"
    # Unknown alias passes through (lets unknown values surface as errors)
    assert _resolve_status("unknown") == "unknown"
    assert _resolve_status(None) is None


def test_1_2_two_new_rwus_in_catalog() -> None:
    from auto_client_acquisition.revenue_company_os.revenue_work_units import (
        RWU_CATALOG, is_valid_unit,
    )
    types = {r.unit_type for r in RWU_CATALOG}
    assert "prospect_qualified" in types
    assert "diagnostic_delivered" in types
    assert is_valid_unit("prospect_qualified")
    assert is_valid_unit("diagnostic_delivered")
    assert len(RWU_CATALOG) >= 14


# ── 1.3 Service Contracts ─────────────────────────────────────────


def test_1_3_all_6_bundles_have_contracts() -> None:
    from api.routers.services import CATALOG, SERVICE_CONTRACTS
    bundle_ids = {b["id"] for b in CATALOG}
    for bid in bundle_ids:
        assert bid in SERVICE_CONTRACTS, f"contract missing for bundle {bid}"
        contract = SERVICE_CONTRACTS[bid]
        for required in (
            "ideal_customer_ar", "required_inputs", "workflow_steps",
            "approval_points", "blocked_actions", "deliverables",
            "proof_metrics", "definition_of_done",
        ):
            assert required in contract, f"{bid} contract missing field {required}"


def test_1_3_growth_starter_has_real_workflow() -> None:
    from api.routers.services import SERVICE_CONTRACTS
    c = SERVICE_CONTRACTS["growth_starter"]
    assert len(c["workflow_steps"]) >= 5
    assert "cold_whatsapp" in c["blocked_actions"]
    assert "proof_pack_generated" in c["definition_of_done"]


def test_1_3_contract_endpoint_registered() -> None:
    from api.routers.services import router
    paths = {r.path for r in router.routes}
    assert "/api/v1/services/{bundle_id}/contract" in paths


# ── 1.4 Customer Workspace + 1.7 Brain endpoints ─────────────────


def test_1_4_companies_router_endpoints() -> None:
    from api.routers.companies import router
    paths = {r.path for r in router.routes}
    assert "/api/v1/companies/{customer_id}/workspace" in paths
    assert "/api/v1/companies/{customer_id}/brain" in paths


def test_1_7_customer_brain_fields_exist() -> None:
    from db.models import CustomerRecord
    cols = {c.name for c in CustomerRecord.__table__.columns}
    for required in (
        "company_name", "website", "sector", "city",
        "offer_ar", "ideal_customer_ar", "average_deal_value_sar",
        "approved_channels", "blocked_channels", "tone_ar",
        "forbidden_claims", "current_service_id",
    ):
        assert required in cols, f"CustomerRecord (Brain) missing field {required}"


# ── 1.5 Approval Queue ────────────────────────────────────────────


def test_1_5_actions_router_endpoints() -> None:
    from api.routers.actions import router
    paths = {r.path for r in router.routes}
    assert "/api/v1/actions/pending" in paths
    assert "/api/v1/actions/{event_id}/approve" in paths
    assert "/api/v1/actions/{event_id}/reject" in paths
    assert "/api/v1/actions/funnel" in paths


# ── 1.6 Learning ──────────────────────────────────────────────────


def test_1_6_learning_router_endpoints() -> None:
    from api.routers.learning import router
    paths = {r.path for r in router.routes}
    assert "/api/v1/learning/weekly" in paths
    assert "/api/v1/learning/today" in paths


# ── 1.8 Verification docs ─────────────────────────────────────────


def test_1_8_inventory_docs_exist() -> None:
    for fn in (
        "FEATURE_INVENTORY.md", "DEPENDENCY_MAP.md",
        "VERIFICATION_MATRIX.md", "SERVICE_TOWER_CONTRACTS.md",
    ):
        path = REPO / "docs" / fn
        assert path.exists(), f"missing doc: {path}"
        assert path.stat().st_size > 100, f"doc too small (likely empty): {path}"


def test_1_8_full_acceptance_script_executable() -> None:
    p = REPO / "scripts" / "full_acceptance.sh"
    assert p.exists()
    text = p.read_text(encoding="utf-8")
    # Layer-2 + Layer-5 markers that the v2 script adds
    assert "no empty files" in text or "empty_files" in text
    assert "no secrets" in text or "secrets" in text


# ── 1.9 Forbidden Claims at draft ────────────────────────────────


def test_1_9_forbidden_claim_active_raises() -> None:
    from auto_client_acquisition.compliance.forbidden_claims import (
        ForbiddenClaimError, assert_safe,
    )
    with pytest.raises(ForbiddenClaimError):
        assert_safe("نضمن لك نتائج خلال أسبوع")


def test_1_9_negated_claim_passes() -> None:
    from auto_client_acquisition.compliance.forbidden_claims import assert_safe
    # Should NOT raise — explicitly negated
    assert_safe("✗ لا نضمن نتائج محددة")
    assert_safe("we do not guarantee results")


def test_1_9_empty_text_passes() -> None:
    from auto_client_acquisition.compliance.forbidden_claims import assert_safe
    assert_safe("")
    assert_safe(None)  # type: ignore[arg-type]


def test_1_9_scan_returns_match_objects() -> None:
    from auto_client_acquisition.compliance.forbidden_claims import scan
    matches = scan("هذا النص نضمن نتائج محددة")
    assert len(matches) >= 1
    assert any(m.claim == "نضمن" and not m.is_negated for m in matches)


# ── Integration: prospects.advance() forward-only enforcement ────


@pytest.mark.asyncio
async def test_stage_machine_forward_only(async_client) -> None:
    """Create prospect, advance to messaged, then try to move backward → 400."""
    create = await async_client.post(
        "/api/v1/prospects",
        json={"name": "test", "company": "Test Co", "relationship_type": "warm_1st_degree"},
    )
    assert create.status_code == 200
    pid = create.json()["id"]

    advance = await async_client.post(
        f"/api/v1/prospects/{pid}/advance",
        json={"target_status": "messaged"},
    )
    assert advance.status_code == 200, advance.text

    backward = await async_client.post(
        f"/api/v1/prospects/{pid}/advance",
        json={"target_status": "new"},
    )
    assert backward.status_code == 400
    assert "cannot_move_backward" in backward.text


@pytest.mark.asyncio
async def test_stage_machine_blocks_large_jump(async_client) -> None:
    """Reject a 2-stage skip unless allow_skip=True. The ladder is:
    new(0) → qualified(1) → messaged(2) → replied(3) → diagnostic_sent(4) →
    meeting_booked(5) → ... A 1-stage skip (delta=2) is allowed by default
    (warm intros are pre-qualified). A 2-stage skip (delta=3) requires
    allow_skip=True."""
    create = await async_client.post(
        "/api/v1/prospects",
        json={"name": "test_jump", "relationship_type": "warm_1st_degree"},
    )
    pid = create.json()["id"]

    # new → messaged (delta=2, 1-stage skip) is allowed by default
    r1 = await async_client.post(
        f"/api/v1/prospects/{pid}/advance",
        json={"target_status": "messaged"},
    )
    assert r1.status_code == 200, r1.text

    # messaged → meeting_booked (delta=3, 2-stage skip) → 400 without allow_skip
    r2 = await async_client.post(
        f"/api/v1/prospects/{pid}/advance",
        json={"target_status": "meeting_booked"},
    )
    assert r2.status_code == 400
    assert "jump_too_large" in r2.text

    # With allow_skip=True → 200
    r3 = await async_client.post(
        f"/api/v1/prospects/{pid}/advance",
        json={"target_status": "meeting_booked", "allow_skip": True},
    )
    assert r3.status_code == 200


@pytest.mark.asyncio
async def test_workspace_returns_full_shape(async_client) -> None:
    """End-to-end: prospect → closed_won → CustomerRecord auto-created
    with Brain populated → workspace returns the 9 sections."""
    create = await async_client.post(
        "/api/v1/prospects",
        json={
            "name": "workspace_test",
            "company": "Acme Workspace Co",
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
        assert r.status_code == 200, f"advance to {target} failed: {r.text}"

    p = await async_client.get(f"/api/v1/prospects/{pid}")
    cust_id = p.json().get("customer_id")
    assert cust_id, "closed_won should have auto-created a customer"

    brain = await async_client.get(f"/api/v1/companies/{cust_id}/brain")
    assert brain.status_code == 200
    data = brain.json()
    assert data["company_name"] == "Acme Workspace Co"
    assert data["sector"] == "B2B SaaS"
    assert data["city"] == "Riyadh"
    assert "approved_channels" in data
    assert "blocked_channels" in data
    assert "tone_ar" in data
    assert "proof_summary" in data

    ws = await async_client.get(f"/api/v1/companies/{cust_id}/workspace")
    assert ws.status_code == 200
    body = ws.json()
    for section in (
        "current_sprint", "open_decisions", "opportunities_count",
        "drafts_count", "meetings", "invoices", "proof_packs",
        "risks_blocked", "next_7_days_plan",
    ):
        assert section in body, f"workspace missing section {section}"


@pytest.mark.asyncio
async def test_actions_pending_endpoint(async_client) -> None:
    r = await async_client.get("/api/v1/actions/pending")
    assert r.status_code == 200
    body = r.json()
    assert "count" in body
    assert "items" in body


@pytest.mark.asyncio
async def test_learning_weekly_endpoint(async_client) -> None:
    r = await async_client.get("/api/v1/learning/weekly?days=7")
    assert r.status_code == 200
    body = r.json()
    for k in ("totals_by_unit", "bottleneck_ar", "next_experiment_ar",
              "no_unsafe_action_executed"):
        assert k in body, f"weekly learning missing key {k}"


@pytest.mark.asyncio
async def test_service_contract_endpoint(async_client) -> None:
    r = await async_client.get("/api/v1/services/growth_starter/contract")
    assert r.status_code == 200
    body = r.json()
    assert body["bundle_id"] == "growth_starter"
    contract = body["contract"]
    assert "workflow_steps" in contract
    assert "definition_of_done" in contract
    assert "cold_whatsapp" in contract["blocked_actions"]
