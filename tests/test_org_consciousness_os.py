"""Tests for org_consciousness_os — Systems 36-45.

Seeds real data through the real ledger APIs (friction_log, the revenue
event store, observability buffer, approval center) so every component is
exercised against real reads. Includes a doctrine-guard test.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta, timezone
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from auto_client_acquisition.approval_center.approval_store import (
    get_default_approval_store,
)
from auto_client_acquisition.approval_center.schemas import ApprovalRequest
from auto_client_acquisition.friction_log import store as friction_store
from auto_client_acquisition.friction_log.schemas import FrictionEvent
from auto_client_acquisition.friction_log.store import clear_for_test, emit
from auto_client_acquisition.observability_v10.buffer import (
    _reset_v10_buffer,
    record_v10_trace,
)
from auto_client_acquisition.observability_v10.schemas import TraceRecordV10
from auto_client_acquisition.org_consciousness_os import (
    benchmark_customer,
    build_causal_report,
    build_workforce_governance,
    compute_execution_health,
    compute_operational_value,
    compute_resilience,
    compute_trust,
    detect_learning_patterns,
    propose_optimizations,
    recommend_meta_orchestration,
    self_evolving,
    synthesize_consciousness,
)
from auto_client_acquisition.org_consciousness_os.schemas import (
    DOCTRINE_POSTURE,
    OrgConsciousnessSnapshot,
)
from auto_client_acquisition.proof_architecture_os.value_ledger import ValueLedgerEvent
from auto_client_acquisition.revenue_memory.event_store import (
    get_default_store,
    reset_default_store,
)
from auto_client_acquisition.revenue_memory.events import make_event

CUSTOMER = "cust_oc"


@pytest.fixture(autouse=True)
def _reset_stores():
    clear_for_test()
    reset_default_store()
    _reset_v10_buffer()
    get_default_approval_store().clear()
    yield
    clear_for_test()
    reset_default_store()
    _reset_v10_buffer()
    get_default_approval_store().clear()


# ── seed helpers ─────────────────────────────────────────────────


def _seed_event(
    event_type: str,
    *,
    subject_id: str = "t1",
    payload=None,
    correlation_id=None,
    customer_id: str = CUSTOMER,
) -> None:
    get_default_store().append(
        make_event(
            event_type=event_type,
            customer_id=customer_id,
            subject_type="agent_task",
            subject_id=subject_id,
            payload=payload or {},
            correlation_id=correlation_id,
        )
    )


def _seed_friction_at(
    *,
    kind: str,
    days_ago: float,
    workflow_id: str = "",
    cost_minutes: int = 0,
    customer_id: str = CUSTOMER,
) -> None:
    """Write a friction event with a backdated occurred_at directly to the log."""
    occurred = (datetime.now(UTC) - timedelta(days=days_ago)).isoformat()
    ev = FrictionEvent(
        customer_id=customer_id,
        kind=kind,
        workflow_id=workflow_id,
        cost_minutes=cost_minutes,
        occurred_at=occurred,
    )
    path: Path = friction_store._path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(ev.to_dict(), ensure_ascii=False) + "\n")


# ── System 36 — execution health ─────────────────────────────────


def test_execution_health_on_real_data():
    emit(customer_id=CUSTOMER, kind="approval_delay", cost_minutes=15)
    emit(customer_id=CUSTOMER, kind="schema_failure", cost_minutes=5)
    record_v10_trace(
        TraceRecordV10(
            correlation_id="c1", customer_id=CUSTOMER, estimated_cost_usd=0.02, latency_ms=120.0
        )
    )
    _seed_event("agent.action_executed")
    _seed_event("agent.action_failed")

    signal = compute_execution_health(customer_id=CUSTOMER, window_days=30)
    assert signal.friction_total == 2
    assert signal.friction_cost_minutes == 20
    assert signal.trace_count == 1
    assert signal.congestion_events["agent.action_failed"] == 1
    assert 0 <= signal.execution_health_score <= 100
    assert signal.health_band in {"healthy", "watch", "strained", "critical"}


def test_execution_health_empty_returns_zeroed_signal():
    signal = compute_execution_health(customer_id="nobody", window_days=30)
    assert signal.friction_total == 0
    assert signal.trace_count == 0
    assert signal.execution_health_score == 100
    assert signal.health_band == "healthy"


# ── System 37 — causal reasoning ─────────────────────────────────


def test_causal_links_friction_to_workflow_events():
    emit(customer_id=CUSTOMER, kind="approval_delay", workflow_id="wf1")
    _seed_event("agent.action_failed", subject_id="task_99", correlation_id="wf1")

    report = build_causal_report(customer_id=CUSTOMER, window_days=30)
    assert len(report.links) == 1
    link = report.links[0]
    assert link.workflow_id == "wf1"
    assert "task_99" in link.linked_task_ids
    assert link.confidence == "high"
    assert link.hypothesis
    assert report.top_root_causes[0][0] == "approval_delay"


def test_causal_unlinked_friction_is_low_confidence():
    emit(customer_id=CUSTOMER, kind="retry", workflow_id="orphan")
    report = build_causal_report(customer_id=CUSTOMER, window_days=30)
    assert report.links[0].confidence == "low"
    assert report.links[0].linked_task_ids == ()


# ── System 38 — digital workforce governance ─────────────────────


def test_workforce_governance_covers_all_agents():
    report = build_workforce_governance(customer_id=CUSTOMER)
    assert len(report.agents) == 12
    for agent in report.agents:
        assert 0 <= agent.risk_score <= 100
        assert agent.risk_band in {"low", "medium", "high", "restricted_not_allowed"}
        assert agent.auditability_card_valid is True
        assert agent.card_errors == ()
        assert agent.owner == "founder"
        assert agent.escalation_path.endswith("founder")
    assert report.agents_not_deploy_ready == 0


# ── System 39 — resilience ───────────────────────────────────────


def test_resilience_circuit_opens_under_failure_load():
    for _ in range(6):
        _seed_event("agent.action_failed", payload={"retries": 2, "max_retries": 2})
    _seed_event("agent.action_executed")

    signal = compute_resilience(customer_id=CUSTOMER, window_days=30)
    assert signal.total_failures == 6
    assert signal.executed == 1
    assert signal.retry_exhausted == 6
    assert signal.circuit_state == "open"
    assert signal.failover_recommended is True


def test_resilience_circuit_closed_when_healthy():
    for _ in range(10):
        _seed_event("agent.action_executed")
    signal = compute_resilience(customer_id=CUSTOMER, window_days=30)
    assert signal.circuit_state == "closed"
    assert signal.failover_recommended is False


# ── System 40 — trust infrastructure ─────────────────────────────


def test_trust_signal_is_governance_clean():
    store = get_default_approval_store()
    store.create(
        ApprovalRequest(
            object_type="lead",
            object_id="l1",
            action_type="follow_up_task",
            customer_id=CUSTOMER,
        )
    )
    signal = compute_trust(
        customer_id=CUSTOMER,
        tracked_audit_metrics=frozenset({"policy_checks_logged"}),
    )
    assert signal.pending_approvals == 1
    assert signal.governance_decision_sample["decision"] == "ALLOW"
    assert signal.reversibility_score == 100
    assert 0 <= signal.trust_index <= 100


# ── System 41 — operational value ────────────────────────────────


def _value_event(eid: str, *, valid: bool) -> ValueLedgerEvent:
    return ValueLedgerEvent(
        value_event_id=eid,
        project_id="p1",
        client_id=CUSTOMER,
        value_type="time_saved",
        metric="hours",
        before=10,
        after=4,
        evidence="ev" if valid else "",
        confidence="medium",
        limitations="estimate",
    )


def test_operational_value_excludes_invalid_events():
    signal = compute_operational_value(
        customer_id=CUSTOMER,
        value_events=[_value_event("v1", valid=True), _value_event("v2", valid=False)],
    )
    assert signal.value_events_count == 2
    assert signal.valid_value_events == 1
    assert signal.is_estimate is True
    assert "estimate" in signal.impact_summary.lower()


# ── System 42 — organizational learning fabric ───────────────────


def test_learning_detects_recurring_pattern_across_windows():
    # same kind in window 0 and window 2
    _seed_friction_at(kind="schema_failure", days_ago=2)
    _seed_friction_at(kind="schema_failure", days_ago=5)
    _seed_friction_at(kind="schema_failure", days_ago=65)

    report = detect_learning_patterns(customer_id=CUSTOMER, lookback_windows=4, window_days=30)
    keys = {p.pattern_key for p in report.recurring_patterns}
    assert "schema_failure" in keys
    pattern = next(p for p in report.recurring_patterns if p.pattern_key == "schema_failure")
    assert pattern.windows_seen >= 2
    assert pattern.trend in {"rising", "falling", "stable"}


def test_learning_ignores_single_window_friction():
    emit(customer_id=CUSTOMER, kind="retry")
    report = detect_learning_patterns(customer_id=CUSTOMER, window_days=30)
    assert report.recurring_patterns == ()


# ── System 43 — meta-orchestration ───────────────────────────────


def test_meta_orchestration_is_recommendation_only():
    _seed_event("agent.action_requested")
    _seed_event("agent.action_requested")
    _seed_event("agent.action_failed")

    rec = recommend_meta_orchestration(customer_id=CUSTOMER, window_days=30)
    assert rec.is_recommendation_only is True
    assert rec.workload_by_status["pending"] == 2
    assert all(isinstance(r, str) for r in rec.recommendations)
    assert 0 <= rec.imbalance_score <= 100


# ── System 44 — strategic intelligence ───────────────────────────


def test_strategic_benchmarks_against_cohort():
    cohort = {
        cid: compute_execution_health(customer_id=cid, window_days=30)
        for cid in (CUSTOMER, "peer_a", "peer_b")
    }
    report = benchmark_customer(customer_id=CUSTOMER, cohort_signals=cohort)
    assert report.cohort_size == 3
    assert len(report.benchmarks) == 4
    for b in report.benchmarks:
        assert 0 <= b.percentile <= 100
        assert b.direction in {"ahead", "behind", "at_median"}


def test_strategic_requires_customer_in_cohort():
    cohort = {"peer_a": compute_execution_health(customer_id="peer_a")}
    with pytest.raises(ValueError):
        benchmark_customer(customer_id=CUSTOMER, cohort_signals=cohort)


# ── System 45 — self-evolving core ───────────────────────────────


def test_self_evolving_proposals_are_draft_only():
    for _ in range(6):
        _seed_event("agent.action_failed")
    _seed_friction_at(kind="schema_failure", days_ago=2)
    _seed_friction_at(kind="schema_failure", days_ago=40)

    learning = detect_learning_patterns(customer_id=CUSTOMER, window_days=30)
    resilience = compute_resilience(customer_id=CUSTOMER, window_days=30)
    workforce = build_workforce_governance(customer_id=CUSTOMER)
    proposals = propose_optimizations(
        customer_id=CUSTOMER,
        learning=learning,
        resilience=resilience,
        workforce=workforce,
    )
    assert proposals  # circuit is open -> at least one proposal
    for p in proposals:
        assert p.status == "DRAFT"
        assert p.requires_human_approval is True
        assert p.auto_apply is False


# ── top-level synthesis ──────────────────────────────────────────


def test_synthesize_consciousness_is_complete_and_serializable():
    emit(customer_id=CUSTOMER, kind="approval_delay", cost_minutes=10)
    _seed_event("agent.action_executed")

    snapshot = synthesize_consciousness(customer_id=CUSTOMER, window_days=30)
    assert isinstance(snapshot, OrgConsciousnessSnapshot)
    assert snapshot.customer_id == CUSTOMER
    assert snapshot.doctrine == DOCTRINE_POSTURE
    # JSON-serializable end to end.
    json.dumps(snapshot.to_dict())


# ── doctrine guard ───────────────────────────────────────────────

_FORBIDDEN_TOKENS = (
    "send_email_live",
    "send_whatsapp_live",
    "charge_payment_live",
    "cold_whatsapp",
    "scrape_web",
    "linkedin_automation",
    "bulk_outreach",
    ".enqueue(",
    "run_workflow",
    "mark_executing",
)


def test_module_contains_no_live_action_tokens():
    pkg_dir = Path(self_evolving.__file__).resolve().parent
    offenders: list[str] = []
    for py in pkg_dir.glob("*.py"):
        text = py.read_text(encoding="utf-8")
        for token in _FORBIDDEN_TOKENS:
            if token in text:
                offenders.append(f"{py.name}:{token}")
    assert not offenders, f"forbidden tokens found: {offenders}"


def test_self_evolving_has_no_apply_path():
    for banned in ("apply", "execute", "commit", "run"):
        assert not hasattr(self_evolving, banned), f"self_evolving must not expose {banned}()"


def test_doctrine_posture_is_read_only():
    assert DOCTRINE_POSTURE == {
        "read_only": True,
        "no_live_send": True,
        "no_live_charge": True,
        "no_external_execution": True,
        "proposals_draft_only": True,
    }


# ── router smoke ─────────────────────────────────────────────────


def _client() -> TestClient:
    from api.routers.org_consciousness_os import router

    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


def test_router_endpoints_return_governance_decision():
    emit(customer_id=CUSTOMER, kind="approval_delay", cost_minutes=10)
    client = _client()

    get_paths = [
        "/api/v1/org-consciousness/status",
        f"/api/v1/org-consciousness/{CUSTOMER}",
        f"/api/v1/org-consciousness/{CUSTOMER}/execution-health",
        f"/api/v1/org-consciousness/{CUSTOMER}/causal",
        f"/api/v1/org-consciousness/{CUSTOMER}/workforce-governance",
        f"/api/v1/org-consciousness/{CUSTOMER}/resilience",
        f"/api/v1/org-consciousness/{CUSTOMER}/trust",
        f"/api/v1/org-consciousness/{CUSTOMER}/learning",
        f"/api/v1/org-consciousness/{CUSTOMER}/meta-orchestration",
        f"/api/v1/org-consciousness/{CUSTOMER}/evolution-proposals",
    ]
    for path in get_paths:
        resp = client.get(path)
        assert resp.status_code == 200, path
        assert resp.json()["governance_decision"] == "ALLOW", path


def test_router_value_and_strategic_post_endpoints():
    client = _client()

    value_resp = client.post(
        f"/api/v1/org-consciousness/{CUSTOMER}/value",
        json={
            "value_events": [
                {
                    "value_event_id": "v1",
                    "project_id": "p1",
                    "client_id": CUSTOMER,
                    "value_type": "time_saved",
                    "metric": "hours",
                    "before": 10,
                    "after": 4,
                    "evidence": "ev",
                    "confidence": "medium",
                    "limitations": "estimate",
                }
            ],
            "capital_events": [],
        },
    )
    assert value_resp.status_code == 200
    assert value_resp.json()["valid_value_events"] == 1

    strat_resp = client.post(
        "/api/v1/org-consciousness/strategic",
        json={"customer_id": CUSTOMER, "cohort_customer_ids": ["peer_a", "peer_b"]},
    )
    assert strat_resp.status_code == 200
    assert strat_resp.json()["cohort_size"] == 3
