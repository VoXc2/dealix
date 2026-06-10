"""Smoke tests for master-plan wave modules."""
from auto_client_acquisition.approval_center.postgres_store import PostgresApprovalStore
from auto_client_acquisition.approval_center.schemas import ApprovalRequest
from auto_client_acquisition.revenue_science.pricing_outcome import (
    PricingOutcomeInput,
    simulate_pricing_outcome,
)
from auto_client_acquisition.workflow_os_v10.service_session_executor import (
    execute_step,
    list_workflow_steps,
)
from dealix.commercial_ops.aeo_meta import build_aeo_snapshot
from dealix.commercial_ops.agent_eval_harness import run_agent_eval_harness
from dealix.commercial_ops.gtm_blitz_tracker import build_gtm_blitz_snapshot


def test_service_session_executor_lists_seven_steps():
    assert len(list_workflow_steps()) == 7
    assert execute_step("day_1_kickoff_diagnostic")["ok"]

def test_pricing_outcome_simulate_diagnostic():
    out = simulate_pricing_outcome(PricingOutcomeInput(sku="governed_diagnostic", proof_packs_delivered=1))
    assert out["ok"] and out["total_estimated_sar"] > out["base_sar"]

def test_agent_eval_harness_passes():
    assert run_agent_eval_harness()["verdict"] == "PASS"

def test_aeo_meta_has_learn_count():
    assert "learn_article_count" in build_aeo_snapshot()

def test_gtm_blitz_snapshot_shape():
    assert "verdict" in build_gtm_blitz_snapshot()

def test_postgres_approval_store_roundtrip():
    store = PostgresApprovalStore(database_url="sqlite:///:memory:")
    req = ApprovalRequest(object_type="lead", object_id="x", action_type="draft_email", summary_en="t")
    store.create(req)
    assert any(p.approval_id == req.approval_id for p in store.list_pending())
