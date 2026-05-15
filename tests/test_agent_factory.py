"""Tests for agent_factory — blueprint, builder gates, memory, eval, trace."""
from __future__ import annotations

import pytest
from pydantic import ValidationError

from auto_client_acquisition.agent_factory import (
    AgentBlueprint,
    AgentEvalCase,
    AgentEvalSuite,
    AgentMemoryBinding,
    AgentStepRecord,
    BuildOutcome,
    DocumentChunk,
    EscalationRule,
    EscalationTrigger,
    HashingEmbedder,
    SemanticChunkIndex,
    append_step,
    binding_valid,
    blueprint_structurally_valid,
    build_agent,
    build_retrieval_request,
    new_trace,
    retrieve_for_agent,
    run_eval_case,
    run_eval_suite,
    summarize_trace,
)
from auto_client_acquisition.agent_factory.trace import TraceStatus
from auto_client_acquisition.agent_os.agent_lifecycle import AgentLifecycleState
from auto_client_acquisition.agent_os.agent_registry import (
    clear_agent_registry_for_tests,
    get_agent,
)
from auto_client_acquisition.agent_os.autonomy_levels import AutonomyLevel
from auto_client_acquisition.agentic_operations_os.agent_permissions import ToolClass
from auto_client_acquisition.agentic_operations_os.agent_risk_score import AgentRiskDimensions
from auto_client_acquisition.knowledge_v10.schemas import SourceType


@pytest.fixture(autouse=True)
def _clear_registry():
    clear_agent_registry_for_tests()
    yield
    clear_agent_registry_for_tests()


def _risk(value: int = 10) -> AgentRiskDimensions:
    return AgentRiskDimensions(
        data_sensitivity=value,
        tool_risk=value,
        autonomy_level=value,
        external_action_exposure=value,
        human_oversight=value,
        audit_coverage=value,
        business_criticality=value,
    )


def _blueprint(**overrides) -> AgentBlueprint:
    base: dict = {
        "agent_id": "agent_rev_01",
        "name": "Revenue Analyst",
        "owner": "founder",
        "purpose": "analyze pipeline",
        "role": "revenue analyst",
        "goals": ["surface revenue leaks"],
        "autonomy_level": AutonomyLevel.DRAFT,
        "lifecycle_target": AgentLifecycleState.DRAFT,
        "tools": ["read", "analyze"],
        "tool_classes": [ToolClass.READ_ONLY, ToolClass.ANALYSIS],
        "risk_dimensions": _risk(10),
        "auditability_enabled": True,
        "audit_scope": ["actions", "decisions"],
    }
    base.update(overrides)
    return AgentBlueprint(**base)


def _escalation() -> EscalationRule:
    return EscalationRule(
        trigger=EscalationTrigger.LOW_CONFIDENCE,
        handoff_to="founder",
        required_action="human review",
    )


# ── Blueprint contract ──────────────────────────────────────────────

def test_blueprint_rejects_blank_owner():
    ok, errors = blueprint_structurally_valid(_blueprint(owner=" "))
    assert ok is False
    assert "owner_required" in errors


def test_blueprint_rejects_empty_goals():
    ok, errors = blueprint_structurally_valid(_blueprint(goals=[]))
    assert ok is False
    assert "at_least_one_goal_required" in errors


def test_blueprint_extra_field_forbidden():
    with pytest.raises(ValidationError):
        _blueprint(unexpected_field=1)


def test_blueprint_reuses_autonomy_enum():
    bp = _blueprint(autonomy_level=AutonomyLevel.DRAFT)
    assert bp.autonomy_level == AutonomyLevel.DRAFT
    with pytest.raises(ValidationError):
        _blueprint(autonomy_level=99)


# ── Builder happy path ──────────────────────────────────────────────

def test_build_agent_happy_path():
    result = build_agent(_blueprint())
    assert result.outcome == BuildOutcome.BUILT
    assert result.registered is True
    assert result.violations == ()
    card = get_agent("agent_rev_01")
    assert card is not None
    assert card.status == "built"


# ── Builder governance gates ────────────────────────────────────────

def test_build_rejects_forbidden_tool():
    result = build_agent(_blueprint(tools=["send_email", "web_scrape"]))
    assert result.outcome == BuildOutcome.REJECTED
    assert "tool_forbidden:send_email" in result.violations
    assert result.registered is False
    assert get_agent("agent_rev_01") is None


def test_build_rejects_forbidden_tool_class():
    result = build_agent(_blueprint(tool_classes=[ToolClass.EXTERNAL_ACTION]))
    assert result.outcome == BuildOutcome.REJECTED
    assert "tool_class_blocked:E" in result.violations


def test_build_rejects_restricted_risk_band():
    result = build_agent(_blueprint(risk_dimensions=_risk(100)))
    assert result.outcome == BuildOutcome.REJECTED
    assert "risk_band_restricted" in result.violations


def test_no_unbounded_agents_requires_kill_switch_owner():
    rejected = build_agent(
        _blueprint(
            autonomy_level=AutonomyLevel.RECOMMEND,
            kill_switch_owner="",
            escalation_rules=[_escalation()],
        ),
    )
    assert rejected.outcome == BuildOutcome.REJECTED
    assert "no_unbounded_agents:kill_switch_owner_required" in rejected.violations

    built = build_agent(
        _blueprint(
            autonomy_level=AutonomyLevel.RECOMMEND,
            kill_switch_owner="founder",
            escalation_rules=[_escalation()],
        ),
    )
    assert built.outcome == BuildOutcome.BUILT


def test_no_unaudited_changes_requires_auditability():
    rejected = build_agent(_blueprint(auditability_enabled=False, audit_scope=[]))
    assert rejected.outcome == BuildOutcome.REJECTED
    assert "no_unaudited_changes:auditability_required" in rejected.violations

    built = build_agent(_blueprint())
    assert built.outcome == BuildOutcome.BUILT
    assert "no_unaudited_changes:auditability_required" not in built.violations


def test_no_silent_failures_rejection_has_codes():
    result = build_agent(_blueprint(tools=["send_email"]))
    assert result.outcome == BuildOutcome.REJECTED
    assert len(result.violations) >= 1
    assert all(v.strip() for v in result.violations)


def test_build_rejects_deploy_target_missing_prereqs():
    result = build_agent(
        _blueprint(
            lifecycle_target=AgentLifecycleState.PRODUCTION,
            auditability_enabled=False,
            audit_scope=[],
        ),
    )
    assert result.outcome == BuildOutcome.REJECTED
    assert any(v.startswith("deploy_prereq_missing:") for v in result.violations)


def test_high_autonomy_requires_escalation_rule():
    result = build_agent(
        _blueprint(
            autonomy_level=AutonomyLevel.RECOMMEND,
            kill_switch_owner="founder",
            escalation_rules=[],
        ),
    )
    assert result.outcome == BuildOutcome.REJECTED
    assert "escalation_rule_required" in result.violations


# ── Memory binding ──────────────────────────────────────────────────

def test_binding_invalid_when_enabled_without_customer():
    binding = AgentMemoryBinding(enabled=True, allowed_sources=[SourceType.INTERNAL_DOC])
    ok, errors = binding_valid(binding)
    assert ok is False
    assert "customer_handle_required" in errors


def test_build_retrieval_request_forces_customer_scope():
    binding = AgentMemoryBinding(
        enabled=True,
        customer_handle="ACME-SAUDI",
        allowed_sources=[SourceType.INTERNAL_DOC],
    )
    req = build_retrieval_request(binding, "what is our onboarding process")
    assert req.customer_handle == "ACME-SAUDI"


def test_memory_binding_drops_blocked_sources():
    binding = AgentMemoryBinding(
        enabled=True,
        customer_handle="ACME-SAUDI",
        allowed_sources=[
            SourceType.INTERNAL_DOC,
            SourceType.BLOCKED_SCRAPING_SOURCE,
            SourceType.BLOCKED_PERSONAL_DATA_SOURCE,
        ],
    )
    req = build_retrieval_request(binding, "what is our pricing policy")
    assert SourceType.INTERNAL_DOC.value in req.allowed_sources
    assert SourceType.BLOCKED_SCRAPING_SOURCE.value not in req.allowed_sources
    assert SourceType.BLOCKED_PERSONAL_DATA_SOURCE.value not in req.allowed_sources


def test_retrieve_for_agent_returns_empty_stub():
    binding = AgentMemoryBinding(
        enabled=True,
        customer_handle="ACME-SAUDI",
        allowed_sources=[SourceType.INTERNAL_DOC],
    )
    assert retrieve_for_agent(binding, "how do we onboard a customer") == []


# ── Eval harness ────────────────────────────────────────────────────

def test_eval_case_pass_and_fail():
    case = AgentEvalCase(case_id="c1", expected_outcome="done", expected_escalation=False)
    ok = run_eval_case(case, observed_outcome="done", observed_escalation=False)
    assert ok.passed is True
    bad = run_eval_case(case, observed_outcome="other", observed_escalation=False)
    assert bad.passed is False
    assert bad.notes == "outcome_mismatch"


def test_eval_suite_pass_rate():
    suite = AgentEvalSuite(
        suite_id="s1",
        agent_id="agent_rev_01",
        cases=[
            AgentEvalCase(case_id="c1", expected_outcome="done"),
            AgentEvalCase(case_id="c2", expected_outcome="done"),
        ],
    )
    out = run_eval_suite(suite, {"c1": ("done", False), "c2": ("wrong", False)})
    assert out.pass_rate == 0.5


def test_eval_escalation_correctness():
    case = AgentEvalCase(case_id="c1", expected_outcome="done", expected_escalation=True)
    correct = run_eval_case(case, observed_outcome="done", observed_escalation=True)
    assert correct.escalation_correct is True
    assert correct.passed is True
    wrong = run_eval_case(case, observed_outcome="done", observed_escalation=False)
    assert wrong.escalation_correct is False
    assert wrong.passed is False


# ── Trace ───────────────────────────────────────────────────────────

def test_new_trace_starts_empty():
    trace = new_trace("trace_1", "agent_rev_01")
    assert trace.status == TraceStatus.STARTED
    assert trace.steps == []


def test_append_step_recomputes_totals():
    trace = new_trace("trace_1", "agent_rev_01")
    updated = append_step(
        trace,
        AgentStepRecord(step_id="s1", step_index=0, latency_ms=100.0),
    )
    updated = append_step(
        updated,
        AgentStepRecord(step_id="s2", step_index=1, latency_ms=50.0, escalated=True),
    )
    assert updated.total_latency_ms == 150.0
    assert updated.escalation_count == 1
    assert trace.steps == []  # original is unchanged


def test_summarize_trace():
    trace = new_trace("trace_1", "agent_rev_01")
    trace = append_step(
        trace,
        AgentStepRecord(step_id="s1", latency_ms=20.0, escalated=True),
    )
    trace = append_step(trace, AgentStepRecord(step_id="s2", latency_ms=20.0))
    summary = summarize_trace(trace)
    assert summary["step_count"] == 2
    assert summary["total_latency_ms"] == 40.0
    assert summary["escalation_rate"] == 0.5


# ── Knowledge OS semantic retrieval engine ──────────────────────────

def _chunk(
    chunk_id: str,
    text: str,
    *,
    customer: str = "ACME-SAUDI",
    document_id: str = "doc1",
    source: SourceType = SourceType.INTERNAL_DOC,
) -> DocumentChunk:
    return DocumentChunk(
        chunk_id=chunk_id,
        document_id=document_id,
        customer_handle=customer,
        source_type=source,
        text=text,
    )


def test_hashing_embedder_deterministic():
    embedder = HashingEmbedder()
    assert embedder.embed("pilot pricing") == embedder.embed("pilot pricing")
    assert embedder.embed("pilot pricing") != embedder.embed("onboarding agenda")


def test_index_rejects_blocked_source():
    index = SemanticChunkIndex()
    with pytest.raises(ValueError, match="blocked_source_type"):
        index.add_chunk(_chunk("c1", "anything", source=SourceType.BLOCKED_SCRAPING_SOURCE))
    assert index.chunk_count() == 0


def test_index_empty_returns_empty():
    index = SemanticChunkIndex()
    assert index.search("what is the pilot pricing") == []


def test_index_search_ranks_by_overlap():
    index = SemanticChunkIndex()
    index.add_chunks([
        _chunk("c1", "pilot pricing sprint costs 499 saudi riyal"),
        _chunk("c2", "onboarding kickoff call agenda for next meeting"),
    ])
    results = index.search("what is the pilot pricing")
    assert len(results) == 1
    assert results[0].chunk_id == "c1"
    assert results[0].score > 0.0


def test_index_search_filters_by_customer():
    index = SemanticChunkIndex()
    index.add_chunk(_chunk("c1", "pilot pricing details", customer="ACME-SAUDI"))
    assert index.search("pilot pricing", customer_handle="OTHER-CO") == []
    assert len(index.search("pilot pricing", customer_handle="ACME-SAUDI")) == 1


def test_index_search_filters_by_allowed_sources():
    index = SemanticChunkIndex()
    index.add_chunk(_chunk("c1", "pilot pricing details", source=SourceType.OFFICIAL_PUBLIC_SITE))
    assert index.search("pilot pricing", allowed_sources=[SourceType.INTERNAL_DOC]) == []
    assert index.search("pilot pricing", allowed_sources=[SourceType.OFFICIAL_PUBLIC_SITE])


def test_index_search_respects_top_k():
    index = SemanticChunkIndex()
    index.add_chunks([
        _chunk("c1", "pilot pricing one"),
        _chunk("c2", "pilot pricing two"),
        _chunk("c3", "pilot pricing three"),
    ])
    assert len(index.search("pilot pricing", top_k=2)) == 2


def test_retrieve_for_agent_semantic_mode_uses_index():
    index = SemanticChunkIndex()
    index.add_chunk(_chunk("c1", "pilot pricing sprint 499 saudi riyal"))
    binding = AgentMemoryBinding(
        enabled=True,
        customer_handle="ACME-SAUDI",
        allowed_sources=[SourceType.INTERNAL_DOC],
        retrieval_mode="semantic_pending",
    )
    results = retrieve_for_agent(binding, "what is the pilot pricing", index=index)
    assert len(results) == 1
    assert results[0].chunk_id == "c1"


def test_retrieve_for_agent_stub_mode_ignores_index():
    index = SemanticChunkIndex()
    index.add_chunk(_chunk("c1", "pilot pricing sprint"))
    binding = AgentMemoryBinding(
        enabled=True,
        customer_handle="ACME-SAUDI",
        allowed_sources=[SourceType.INTERNAL_DOC],
    )
    assert retrieve_for_agent(binding, "what is the pilot pricing", index=index) == []


def test_retrieve_for_agent_semantic_drops_out_of_scope_source():
    index = SemanticChunkIndex()
    index.add_chunk(_chunk("c1", "pilot pricing sprint", source=SourceType.OFFICIAL_PUBLIC_SITE))
    binding = AgentMemoryBinding(
        enabled=True,
        customer_handle="ACME-SAUDI",
        allowed_sources=[SourceType.INTERNAL_DOC],
        retrieval_mode="semantic_pending",
    )
    assert retrieve_for_agent(binding, "what is the pilot pricing", index=index) == []
