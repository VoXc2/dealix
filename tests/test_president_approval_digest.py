from __future__ import annotations

import pytest

from dealix.president_approval_digest import (
    UNKNOWN,
    ApprovalRequest,
    MoneySnapshot,
    WipPolicy,
    WorkItem,
    build_president_digest,
)


POLICY = WipPolicy(
    max_company_p0s=3,
    max_build_prs_per_owner=2,
    max_experiments_per_funnel_stage=1,
    source_ref="data/commercial/package_routing_contract_v1.json#president_wip",
    evidence_refs=("evidence://portfolio-policy/1",),
)
EVALUATED_AT = "2026-08-29T10:00:00+03:00"


def _money(**overrides: object) -> MoneySnapshot:
    values: dict[str, object] = {
        "revenue_sar": 0.0,
        "paid_pilots": 0,
        "evidence_class": "PAYMENT_EVIDENCE",
        "evidence_refs": ("evidence://payment-snapshot/1",),
        "as_of": "2026-08-29T09:00:00+03:00",
    }
    values.update(overrides)
    return MoneySnapshot(**values)  # type: ignore[arg-type]


def _work(**overrides: object) -> WorkItem:
    values: dict[str, object] = {
        "work_id": "revenue-1",
        "kind": "other",
        "owner": "revenue",
        "status": "active",
        "next_action": "PREPARE_DIAGNOSTIC",
        "priority_score": 100,
        "evidence_refs": ("evidence://work/1",),
    }
    values.update(overrides)
    return WorkItem(**values)  # type: ignore[arg-type]


def _approval(**overrides: object) -> ApprovalRequest:
    values: dict[str, object] = {
        "approval_id": "approval-1",
        "action_fingerprint": "fp-1",
        "exact_scope": "send one named customer follow-up",
        "authority_class": "SPECIFIC_APPROVAL_REQUIRED",
        "evidence_refs": ("evidence://relationship/1",),
        "risk_class": "commercial_external",
        "expires_at": "2026-08-29T23:00:00+03:00",
        "approval_state": "PENDING",
        "state_checked_at": "2026-08-29T09:55:00+03:00",
        "approval_state_ref": "approval://state/1",
    }
    values.update(overrides)
    return ApprovalRequest(**values)  # type: ignore[arg-type]


def _digest(
    *,
    money: MoneySnapshot | None = None,
    work_items: tuple[WorkItem, ...] = (),
    approvals: tuple[ApprovalRequest, ...] = (),
    wip_policy: WipPolicy = POLICY,
):
    return build_president_digest(
        money=money or _money(),
        work_items=work_items,
        approvals=approvals,
        wip_policy=wip_policy,
        evaluated_at=EVALUATED_AT,
    )


def test_digest_exposes_only_five_surfaces_and_never_grants_authority() -> None:
    payload = _digest(work_items=(_work(),), approvals=(_approval(),)).to_dict()
    assert set(payload) == {"MONEY", "DECISIONS", "RISKS", "APPROVALS", "NEXT_ACTION"}
    assert payload["MONEY"]["verified_revenue_sar"] == 0
    assert payload["MONEY"]["truth_state"] == "VERIFIED_PAYMENT_EVIDENCE"
    assert payload["APPROVALS"][0]["actionable_pending"] is True
    assert payload["APPROVALS"][0]["approval_granted"] is False
    assert payload["APPROVALS"][0]["execution_performed"] is False
    assert payload["NEXT_ACTION"]["execution_authority"] is False


@pytest.mark.parametrize("evidence_class", ["INVOICE", "PROPOSAL", "CRM_AMOUNT", "ANALYTICS_EVENT", "UNKNOWN"])
def test_non_payment_amounts_never_become_verified_money(evidence_class: str) -> None:
    payload = _digest(
        money=_money(
            revenue_sar=999999.0,
            paid_pilots=99,
            evidence_class=evidence_class,
            evidence_refs=("evidence://not-payment/1",),
        )
    ).to_dict()
    assert payload["MONEY"]["verified_revenue_sar"] == UNKNOWN
    assert payload["MONEY"]["verified_paid_pilots"] == UNKNOWN
    assert payload["MONEY"]["truth_state"] == UNKNOWN


def test_payment_class_without_evidence_is_unknown_even_when_zero() -> None:
    payload = _digest(money=_money(evidence_refs=())).to_dict()
    assert payload["MONEY"]["verified_revenue_sar"] == UNKNOWN
    assert payload["MONEY"]["verified_paid_pilots"] == UNKNOWN


def test_unproven_positive_movement_cannot_evade_stop_rule() -> None:
    item = _work(
        work_id="stale-build",
        kind="build_pr",
        owner="engineering",
        verified_movement=100,
        movement_truth_class="UNKNOWN_NOT_EVIDENCE_BACKED",
        movement_evidence_refs=(),
        founder_minutes=90,
        review_after_founder_minutes=60,
    )
    payload = _digest(work_items=(item,)).to_dict()
    assert payload["DECISIONS"][0]["decision"] == "REVIEW_OR_STOP"
    assert payload["NEXT_ACTION"]["action"] == "REVIEW_OR_STOP"


def test_evidence_backed_movement_can_satisfy_stop_boundary() -> None:
    item = _work(
        verified_movement=1,
        movement_truth_class="VERIFIED_ECONOMIC_MOVEMENT",
        movement_evidence_refs=("evidence://movement/1",),
        founder_minutes=90,
        review_after_founder_minutes=60,
    )
    assert item.requires_review_or_stop() is False


@pytest.mark.parametrize(
    ("approval_state", "expires_at", "expected_state"),
    [
        ("REVOKED", "2026-08-29T23:00:00+03:00", "REVOKED"),
        ("EXPIRED", "2026-08-29T23:00:00+03:00", "EXPIRED"),
        ("UNKNOWN", "2026-08-29T23:00:00+03:00", "UNKNOWN"),
        ("PENDING", "2026-08-29T09:59:00+03:00", "EXPIRED"),
    ],
)
def test_non_current_approvals_remain_audit_only(
    approval_state: str,
    expires_at: str,
    expected_state: str,
) -> None:
    payload = _digest(
        approvals=(
            _approval(approval_state=approval_state, expires_at=expires_at),
        )
    ).to_dict()
    row = payload["APPROVALS"][0]
    assert row["lifecycle_state"] == expected_state
    assert row["actionable_pending"] is False
    assert row["approval_granted"] is False
    assert row["projection_only"] is True


def test_future_state_check_is_non_actionable_unknown() -> None:
    payload = _digest(
        approvals=(_approval(state_checked_at="2026-08-29T11:00:00+03:00"),)
    ).to_dict()
    assert payload["APPROVALS"][0]["lifecycle_state"] == "UNKNOWN"
    assert payload["APPROVALS"][0]["actionable_pending"] is False


def test_wip_limits_are_evidence_bound_inputs_not_digest_owned_constants() -> None:
    policy = WipPolicy(
        max_company_p0s=1,
        max_build_prs_per_owner=1,
        max_experiments_per_funnel_stage=1,
        source_ref="company-machine://policy/wip-v2",
        evidence_refs=("evidence://policy/v2",),
    )
    work = (
        _work(work_id="p0-1", kind="company_p0", owner="president"),
        _work(work_id="p0-2", kind="company_p0", owner="president"),
    )
    payload = _digest(work_items=work, wip_policy=policy).to_dict()
    risk = next(row for row in payload["RISKS"] if row["code"] == "COMPANY_P0_WIP_EXCEEDED")
    assert risk["limit"] == 1
    assert risk["policy_source_ref"] == "company-machine://policy/wip-v2"


def test_duplicate_action_fingerprint_fails_closed() -> None:
    with pytest.raises(ValueError, match="duplicate action_fingerprint"):
        _digest(
            approvals=(
                _approval(approval_id="a1", action_fingerprint="same"),
                _approval(approval_id="a2", action_fingerprint="same", approval_state_ref="approval://state/2"),
            )
        )


def test_work_and_wip_policy_require_source_refs() -> None:
    with pytest.raises(ValueError, match="work evidence_refs"):
        _work(evidence_refs=())
    with pytest.raises(ValueError, match="WIP policy evidence_refs"):
        WipPolicy(
            max_company_p0s=3,
            max_build_prs_per_owner=2,
            max_experiments_per_funnel_stage=1,
            source_ref="policy://1",
            evidence_refs=(),
        )
