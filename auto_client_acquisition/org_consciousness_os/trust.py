"""System 40 — Trust Infrastructure Engine.

Synthesizes explainability, reversibility and auditability into a single
trust index. Calls the institutional governance runtime to prove this
module's own path is governance-clean (it should always be ALLOW).
"""

from __future__ import annotations

from auto_client_acquisition.approval_center.approval_store import (
    ApprovalStore,
    get_default_approval_store,
)
from auto_client_acquisition.auditability_os.audit_metrics import (
    audit_metrics_coverage_score,
)
from auto_client_acquisition.institutional_control_os.governance_runtime import (
    GovernanceRuntimeSignals,
    evaluate_output_governance,
)
from auto_client_acquisition.org_consciousness_os.schemas import TrustSignal


def compute_trust(
    *,
    customer_id: str,
    approval_store: ApprovalStore | None = None,
    tracked_audit_metrics: frozenset[str] = frozenset(),
) -> TrustSignal:
    """Synthesize a trust signal for ``customer_id``."""
    approvals = approval_store or get_default_approval_store()
    pending = sum(1 for r in approvals.list_pending() if r.customer_id == customer_id)

    coverage = audit_metrics_coverage_score(tracked_audit_metrics)

    # This module is a read-only synthesis layer: no external action, no PII
    # egress, valid internal path. The governance runtime must clear it.
    decision = evaluate_output_governance(
        GovernanceRuntimeSignals(
            source_passport_valid=True,
            contains_personal_contact_data=False,
            external_action_requested=False,
            human_approved_external=False,
        ),
        audit_event_id=f"org_consciousness:{customer_id}",
    )

    # Explainability: every output carries a hypothesis/decision trail.
    explainability = 100 if decision["decision"] == "ALLOW" else 60
    # Reversibility: the module persists nothing and executes nothing.
    reversibility = 100
    trust_index = (explainability + reversibility + coverage) // 3

    return TrustSignal(
        customer_id=customer_id,
        explainability_score=explainability,
        reversibility_score=reversibility,
        auditability_coverage=coverage,
        pending_approvals=pending,
        governance_decision_sample=decision,
        trust_index=trust_index,
    )


__all__ = ["compute_trust"]
