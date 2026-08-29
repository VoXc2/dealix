#!/usr/bin/env python3
"""Standalone invariant verifier for the Dealix President approval digest."""

from __future__ import annotations

from dealix.president_approval_digest import (
    UNKNOWN,
    ApprovalRequest,
    MoneySnapshot,
    WipPolicy,
    WorkItem,
    build_president_digest,
)


def main() -> int:
    policy = WipPolicy(
        max_company_p0s=3,
        max_build_prs_per_owner=2,
        max_experiments_per_funnel_stage=1,
        source_ref="data/commercial/package_routing_contract_v1.json#president_wip",
        evidence_refs=("evidence://portfolio-policy/verify",),
    )
    digest = build_president_digest(
        money=MoneySnapshot(
            revenue_sar=0,
            paid_pilots=0,
            evidence_class="PAYMENT_EVIDENCE",
            evidence_refs=("evidence://payment-snapshot/verify",),
            as_of="2026-08-29T09:00:00+03:00",
        ),
        evaluated_at="2026-08-29T10:00:00+03:00",
        wip_policy=policy,
        work_items=(
            WorkItem(
                work_id="verify-revenue",
                kind="other",
                owner="revenue",
                status="active",
                next_action="PREPARE_EVIDENCE_BOUND_DIAGNOSTIC",
                priority_score=100,
                evidence_refs=("evidence://work/verify",),
            ),
            WorkItem(
                work_id="verify-stale",
                kind="build_pr",
                owner="engineering",
                status="active",
                next_action="BUILD_MORE",
                priority_score=50,
                evidence_refs=("evidence://work/stale",),
                verified_movement=100,
                movement_truth_class="UNKNOWN_NOT_EVIDENCE_BACKED",
                founder_minutes=90,
                review_after_founder_minutes=60,
            ),
        ),
        approvals=(
            ApprovalRequest(
                approval_id="verify-approval",
                action_fingerprint="verify-fingerprint",
                exact_scope="one named external action",
                authority_class="SPECIFIC_APPROVAL_REQUIRED",
                evidence_refs=("evidence://verify/1",),
                risk_class="l5_external",
                expires_at="2026-08-29T23:00:00+03:00",
                approval_state="PENDING",
                state_checked_at="2026-08-29T09:55:00+03:00",
                approval_state_ref="approval://state/verify",
            ),
            ApprovalRequest(
                approval_id="revoked-approval",
                action_fingerprint="revoked-fingerprint",
                exact_scope="revoked named external action",
                authority_class="SPECIFIC_APPROVAL_REQUIRED",
                evidence_refs=("evidence://verify/revoked",),
                risk_class="l5_external",
                expires_at="2026-08-29T23:00:00+03:00",
                approval_state="REVOKED",
                state_checked_at="2026-08-29T09:55:00+03:00",
                approval_state_ref="approval://state/revoked",
            ),
        ),
    ).to_dict()

    assert set(digest) == {"MONEY", "DECISIONS", "RISKS", "APPROVALS", "NEXT_ACTION"}
    assert digest["MONEY"]["verified_revenue_sar"] == 0
    assert digest["MONEY"]["truth_state"] == "VERIFIED_PAYMENT_EVIDENCE"
    assert any(row["decision"] == "REVIEW_OR_STOP" for row in digest["DECISIONS"])
    current = next(row for row in digest["APPROVALS"] if row["approval_id"] == "verify-approval")
    revoked = next(row for row in digest["APPROVALS"] if row["approval_id"] == "revoked-approval")
    assert current["actionable_pending"] is True
    assert revoked["actionable_pending"] is False
    assert all(row["approval_granted"] is False for row in digest["APPROVALS"])
    assert all(row["execution_performed"] is False for row in digest["APPROVALS"])
    assert digest["NEXT_ACTION"]["execution_authority"] is False

    non_payment = build_president_digest(
        money=MoneySnapshot(
            revenue_sar=999999,
            paid_pilots=99,
            evidence_class="CRM_AMOUNT",
            evidence_refs=("crm://amount/verify",),
            as_of="2026-08-29T09:00:00+03:00",
        ),
        evaluated_at="2026-08-29T10:00:00+03:00",
        wip_policy=policy,
        work_items=(),
        approvals=(),
    ).to_dict()
    assert non_payment["MONEY"]["verified_revenue_sar"] == UNKNOWN
    assert non_payment["MONEY"]["verified_paid_pilots"] == UNKNOWN

    print("DEALIX_PRESIDENT_APPROVAL_DIGEST=PASS")
    print("FOUNDER_SURFACES=MONEY,DECISIONS,RISKS,APPROVALS,NEXT_ACTION")
    print("PAYMENT_EVIDENCE_REQUIRED_FOR_VERIFIED_MONEY=1")
    print("UNPROVEN_MOVEMENT_CAN_BYPASS_STOP=0")
    print("REVOKED_OR_EXPIRED_APPROVAL_ACTIONABLE=0")
    print("WIP_POLICY_IS_EVIDENCE_BOUND_INPUT=1")
    print("APPROVALS_GRANTED=0")
    print("EXTERNAL_EXECUTION_PERFORMED=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
