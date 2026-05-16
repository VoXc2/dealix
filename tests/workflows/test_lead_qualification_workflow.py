from __future__ import annotations

from dealix.contracts.audit_log import AuditAction
from dealix.workflows.lead_qualification import (
    ActorContext,
    CompanyContext,
    InMemoryCRMStore,
    InMemoryRollbackJournal,
    InMemoryTenantContextStore,
    LeadInput,
    LeadQualificationWorkflow,
    WORKFLOW_STEP_SEQUENCE,
    load_lead_qualification_workflow_definition,
)


def _build_workflow() -> LeadQualificationWorkflow:
    context_store = InMemoryTenantContextStore()
    context_store.upsert(
        "tenant-a",
        CompanyContext(
            company="Acme",
            summary="شركة لديها فريق مبيعات نشط وتبحث عن تسريع التأهيل.",
            signals=("existing_customer", "high_intent"),
        ),
    )
    return LeadQualificationWorkflow(
        context_store=context_store,
        crm_store=InMemoryCRMStore(),
        rollback_journal=InMemoryRollbackJournal(),
    )


def test_workflow_definition_matches_required_step_sequence() -> None:
    definition = load_lead_qualification_workflow_definition()
    steps = tuple(step["step_id"] for step in definition["steps"])
    assert steps == WORKFLOW_STEP_SEQUENCE
    assert definition["tenant_required"] is True
    assert definition["rollback_supported"] is True


def test_tenant_isolation_prevents_cross_tenant_execution() -> None:
    workflow = _build_workflow()
    lead = LeadInput(
        lead_id="lead-001",
        tenant_id="tenant-b",
        company="Acme",
        name="Noura",
        email="noura@example.sa",
        message="Need urgent demo and integration plan.",
        budget_sar=80_000,
    )
    actor = ActorContext(actor_id="user-01", tenant_id="tenant-a", roles=("tenant_admin",))

    result = workflow.run(lead, actor)

    assert result.status == "denied"
    assert "tenant isolation" in result.reason
    assert AuditAction.ACCESS_DENIED in {entry.action for entry in result.audit_entries}


def test_rbac_denies_execution_for_viewer_role() -> None:
    workflow = _build_workflow()
    lead = LeadInput(
        lead_id="lead-002",
        tenant_id="tenant-a",
        company="Acme",
        name="Omar",
        email="omar@example.sa",
        message="Please send a pilot proposal.",
        budget_sar=30_000,
    )
    actor = ActorContext(actor_id="user-02", tenant_id="tenant-a", roles=("viewer",))

    result = workflow.run(lead, actor)

    assert result.status == "denied"
    assert "rbac denied" in result.reason
    assert result.rollback_token is None


def test_high_risk_path_requests_approval_and_skips_crm_update() -> None:
    crm_store = InMemoryCRMStore()
    workflow = _build_workflow()
    workflow.crm_store = crm_store

    lead = LeadInput(
        lead_id="lead-003",
        tenant_id="tenant-a",
        company="Acme",
        name="Maha",
        email="maha@example.sa",
        message="Legal complaint refund request with personal data issue.",
        budget_sar=2_000,
    )
    actor = ActorContext(actor_id="risk-owner", tenant_id="tenant-a", roles=("tenant_admin",))

    result = workflow.run(lead, actor)

    assert result.status == "pending_approval"
    assert result.approval_required is True
    assert crm_store.get("tenant-a", "lead-003") is None
    assert AuditAction.APPROVAL_REQUESTED in {entry.action for entry in result.audit_entries}


def test_completed_flow_updates_crm_and_supports_rollback() -> None:
    crm_store = InMemoryCRMStore()
    rollback = InMemoryRollbackJournal()
    workflow = _build_workflow()
    workflow.crm_store = crm_store
    workflow.rollback_journal = rollback

    crm_store.upsert(
        "tenant-a",
        "lead-004",
        {
            "lead_id": "lead-004",
            "qualification": "warm",
            "lead_score": 52.0,
        },
    )
    lead = LeadInput(
        lead_id="lead-004",
        tenant_id="tenant-a",
        company="Acme",
        name="Sara",
        email="sara@example.sa",
        message="We are ready for a demo and integration workshop next week.",
        budget_sar=90_000,
    )
    actor = ActorContext(actor_id="rev-op", tenant_id="tenant-a", roles=("revenue_operator",))

    result = workflow.run(lead, actor)

    assert result.status == "completed"
    assert result.rollback_token is not None
    assert result.metrics["workflow_total_ms"] > 0
    assert result.metrics["status_completed"] == 1.0
    updated = crm_store.get("tenant-a", "lead-004")
    assert updated is not None
    assert updated["qualification"] == "hot"
    assert updated["lead_score"] >= 70

    rolled_back = rollback.rollback(result.rollback_token or "", crm_store)
    restored = crm_store.get("tenant-a", "lead-004")
    assert rolled_back is True
    assert restored is not None
    assert restored["qualification"] == "warm"
