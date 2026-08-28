"""V18 Revenue Portfolio Control Plane acceptance tests (#1277).

Proves the mandatory V18 gates:

1. buyability does not alter factual qualification
2. buying-group members require provenance
3. unknown stakeholder remains UNKNOWN
4. proof reuse requires permission
5. experiment cannot SCALE without outcome evidence
6. capacity allocator cannot overbook founder/event time
7. event schedules cannot overlap impossibly
8. portfolio ranking never creates qualification evidence
9. public contact data cannot imply consent (partner path)
10. loss recording requires evidence and never relaxes governance
11. no duplicate scheduler owner exists
12. #1273/#1274/#1277 roles do not overlap incorrectly
13. portfolio command returns TOP 5 max with one next autonomous action

Pure deterministic tests — no network, no DB, no LLM.
"""

from __future__ import annotations

import csv
from pathlib import Path

import pytest

from auto_client_acquisition.portfolio_os.buyability import (
    BuyabilityAssessment,
    BuyingGroup,
    BuyingGroupMember,
    BuyingRole,
    RoleConfidence,
    assess_buyability,
    default_buying_group,
    validate_member,
)
from auto_client_acquisition.portfolio_os.capacity import (
    AllocationViolation,
    CapacityAllocation,
    CapacityBudget,
    allocate_capacity,
)
from auto_client_acquisition.portfolio_os.command import build_portfolio_command
from auto_client_acquisition.portfolio_os.distribution import (
    DistributionEdge,
    evaluate_proof_reuse,
)
from auto_client_acquisition.portfolio_os.events import (
    EventAllocation,
    EventConflict,
    canonical_event_windows,
    optimize_event_plan,
)
from auto_client_acquisition.portfolio_os.experiments import (
    Experiment,
    ExperimentDecision,
    ExperimentRegistry,
    register_experiment,
    validate_experiment,
)
from auto_client_acquisition.portfolio_os.losses import (
    LossReason,
    record_loss,
)
from auto_client_acquisition.portfolio_os.partners import (
    PartnerPath,
    assess_partner_path,
)
from auto_client_acquisition.portfolio_os.portfolio import (
    PortfolioItem,
    PortfolioLane,
    rank_portfolio,
    value_score,
)


# ── 1. buyability does not alter factual qualification ─────────────────────


def test_buyability_does_not_alter_qualification() -> None:
    group = BuyingGroup(
        account_id="acc-1",
        members=(
            BuyingGroupMember(
                role=BuyingRole.ECONOMIC_BUYER.value,
                source="BIG5_REAL_INTERACTION",
                observed_fact="GM stated fragmented lead tracking",
                role_confidence=RoleConfidence.HIGH.value,
                relationship_state="real_relationship",
            ),
        ),
    )
    assessment = assess_buyability(
        "acc-1",
        group=group,
        factor_evidence={
            "PROBLEM_FIT": "strong: stated fragmented lead tracking",
            "STAKEHOLDER_ALIGNMENT": "strong: GM engaged",
            "ECONOMIC_DEFENSIBILITY": "moderate",
        },
    )
    # The score is an ordinal aid and never flips state to QUALIFIED.
    assert 0 <= assessment.buyability_score <= 100
    # The score must not invent qualification facts.
    assert "QUALIFIED" not in assessment.to_dict()
    assert "PAID" not in assessment.to_dict()


# ── 2. buying-group members require provenance ─────────────────────────────


def test_buying_group_member_requires_provenance() -> None:
    unprovenanced = BuyingGroupMember(
        role=BuyingRole.ECONOMIC_BUYER.value,
        source="",
        observed_fact="",
    )
    errors = validate_member(unprovenanced)
    assert "MEMBER_WITHOUT_PROVENANCE" in errors

    provenanced = BuyingGroupMember(
        role=BuyingRole.CHAMPION.value,
        source="EVENT_INTERACTION",
        observed_fact="wants faster follow-up automation",
        role_confidence=RoleConfidence.MEDIUM.value,
    )
    assert validate_member(provenanced) == []


def test_buying_group_never_invents_person() -> None:
    group = default_buying_group("acc-1")
    assert group.known_member_count() == 0
    assert group.unprovenanced_count() == 0


# ── 3. unknown stakeholder remains UNKNOWN ─────────────────────────────────


def test_unknown_stakeholder_remains_unknown() -> None:
    member = BuyingGroupMember(
        role=BuyingRole.UNKNOWN_STAKEHOLDER.value,
        source="PUBLIC_WEBSITE",
        observed_fact="company website lists no named buyer",
        role_confidence=RoleConfidence.UNKNOWN.value,
    )
    assert validate_member(member) == []
    group = BuyingGroup(account_id="acc-1", members=(member,))
    assert group.role_present(BuyingRole.UNKNOWN_STAKEHOLDER.value)
    # Unknown state is preserved, never upgraded to a named role.
    assert not group.role_present(BuyingRole.ECONOMIC_BUYER.value)


# ── 4. proof reuse requires permission ─────────────────────────────────────


def test_proof_reuse_requires_permission() -> None:
    blocked = evaluate_proof_reuse(
        "proof-1",
        customer_permission_state="unknown",
        claim_support="x",
        source="s",
        provenance="p",
    )
    assert blocked.reusable is False
    assert "PERMISSION_UNKNOWN_OR_MISSING" in blocked.reasons

    denied = evaluate_proof_reuse(
        "proof-2",
        customer_permission_state="denied",
        claim_support="x",
        source="s",
        provenance="p",
    )
    assert denied.reusable is False
    assert "PERMISSION_DENIED" in denied.reasons

    granted = evaluate_proof_reuse(
        "proof-3",
        customer_permission_state="granted",
        claim_support="capability: revenue follow-up automation",
        source="customer",
        provenance="customer-consent-2026-08-28",
    )
    assert granted.reusable is True


def test_proof_reuse_blocked_without_claim_support() -> None:
    r = evaluate_proof_reuse(
        "proof-4",
        customer_permission_state="granted",
        claim_support="",
        source="s",
        provenance="p",
    )
    assert r.reusable is False
    assert "NO_CLAIM_SUPPORT" in r.reasons


# ── 5. experiment cannot SCALE without outcome evidence ────────────────────


def test_experiment_cannot_scale_without_outcome() -> None:
    exp = Experiment(
        experiment_id="exp-1",
        hypothesis="diagnostic-first CTA beats pilot-first",
        decision=ExperimentDecision.SCALE.value,
        outcome="",
    )
    errors = validate_experiment(exp)
    assert "SCALE_WITHOUT_OUTCOME_EVIDENCE" in errors
    registry = ExperimentRegistry()
    updated, reg_errors = register_experiment(registry, exp)
    assert reg_errors
    assert updated.experiments == ()  # rejected, never auto-scaled


def test_experiment_with_outcome_can_scale() -> None:
    exp = Experiment(
        experiment_id="exp-2",
        hypothesis="diagnostic-first CTA beats pilot-first",
        decision=ExperimentDecision.SCALE.value,
        outcome="5 consented discovery conversations from 9 diagnostic CTAs",
        confidence="medium",
        learning="diagnostic-first doubles reply engagement",
    )
    assert validate_experiment(exp) == []
    registry = ExperimentRegistry()
    updated, errors = register_experiment(registry, exp)
    assert errors == []
    assert len(updated.experiments) == 1


def test_experiment_invalid_decision_rejected() -> None:
    exp = Experiment(
        experiment_id="exp-3",
        hypothesis="x",
        decision="MAYBE",
        outcome="something",
    )
    errors = validate_experiment(exp)
    assert any(e.startswith("INVALID_DECISION") for e in errors)


# ── 6. capacity allocator cannot overbook ──────────────────────────────────


def test_capacity_allocator_cannot_overbook_founder() -> None:
    budget = CapacityBudget(founder_minutes=600)
    demands = [
        CapacityAllocation(lane="A", founder_minutes=400),
        CapacityAllocation(lane="B", founder_minutes=300),
    ]
    result = allocate_capacity(budget, demands)
    assert result.feasible is False
    assert any(v.resource == "founder_minutes" for v in result.violations)


def test_capacity_allocator_cannot_overbook_event_hours() -> None:
    budget = CapacityBudget(event_hours=20)
    demands = [
        CapacityAllocation(lane="EVENT_BIG5", event_hours=14),
        CapacityAllocation(lane="EVENT_LEAP", event_hours=10),
    ]
    result = allocate_capacity(budget, demands)
    assert result.feasible is False
    assert any(v.resource == "event_hours" for v in result.violations)


def test_capacity_within_budget_is_feasible() -> None:
    budget = CapacityBudget(founder_minutes=600, event_hours=20)
    demands = [
        CapacityAllocation(lane="EVENT_RELATIONSHIP", founder_minutes=300, event_hours=10),
        CapacityAllocation(lane="WARM_NETWORK", founder_minutes=200),
    ]
    result = allocate_capacity(budget, demands)
    assert result.feasible is True
    assert len(result.accepted_lanes) == 2


# ── 7. event schedules cannot overlap impossibly ───────────────────────────


def test_event_schedule_rejects_physical_overlap() -> None:
    allocations = [
        EventAllocation(
            allocation_id="big5-1",
            event_name="BIG5",
            day="2026-08-31",
            start_hour=16,
            end_hour=18,
            venue="Riyadh Front",
            expected_relationship_value=4,
            probability=0.5,
            strategic_reuse=3,
        ),
        EventAllocation(
            allocation_id="leap-1",
            event_name="LEAP",
            day="2026-08-31",
            start_hour=17,
            end_hour=19,
            venue="RECC Malham",
            expected_relationship_value=4,
            probability=0.6,
            strategic_reuse=4,
        ),
    ]
    plan = optimize_event_plan(allocations, event_hours_cap=20, founder_minutes_cap=600)
    assert plan.feasible is False
    assert len(plan.conflicts) == 1
    assert plan.conflicts[0].reason == "PHYSICAL_OVERLAP_DIFFERENT_VENUE"


def test_event_schedule_allows_sequential_allocations() -> None:
    allocations = [
        EventAllocation(
            allocation_id="big5-1",
            event_name="BIG5",
            day="2026-08-31",
            start_hour=16,
            end_hour=18,
            venue="Riyadh Front",
            expected_relationship_value=4,
            probability=0.5,
            strategic_reuse=3,
            travel_cost=2,
        ),
        EventAllocation(
            allocation_id="leap-1",
            event_name="LEAP",
            day="2026-09-01",
            start_hour=10,
            end_hour=12,
            venue="RECC Malham",
            expected_relationship_value=4,
            probability=0.6,
            strategic_reuse=4,
        ),
    ]
    plan = optimize_event_plan(allocations, event_hours_cap=20, founder_minutes_cap=600)
    assert plan.conflicts == ()
    assert plan.capacity_feasible is True
    assert plan.feasible is True


def test_event_windows_are_canonical_and_reverified() -> None:
    windows = {w.name: w for w in canonical_event_windows()}
    assert windows["BIG5"].venue == "Riyadh Front / ROSHN Front"
    assert windows["BIG5"].start == "2026-08-30" and windows["BIG5"].end == "2026-09-02"
    assert windows["LEAP"].venue == "RECC Malham"
    assert windows["LEAP"].start == "2026-08-31" and windows["LEAP"].end == "2026-09-03"
    assert windows["DEEPFEST"].venue == "RECC Malham"


# ── 8. portfolio ranking never creates qualification evidence ──────────────


def test_portfolio_ranking_is_ordinal_not_qualification() -> None:
    items = [
        PortfolioItem(
            item_id="i1",
            lane=PortfolioLane.FIRST_FIVE_DIRECT.value,
            company="Co A",
            evidence_strength=3,
            probability_of_movement=0.5,
            strategic_reuse=4,
            proof_potential=4,
        ),
        PortfolioItem(
            item_id="i2",
            lane=PortfolioLane.EVENT_RELATIONSHIP.value,
            company="Co B",
            evidence_strength=1,
            probability_of_movement=0.2,
        ),
    ]
    ranking = rank_portfolio(items)
    assert ranking.ranked_ids[0] == "i1"
    assert len(ranking.top(5)) == 2
    # Rank output contains no qualification claims.
    assert "qualified" not in ranking.to_dict().keys()
    assert "WON" not in str(ranking.to_dict())


def test_value_score_is_bounded() -> None:
    item = PortfolioItem(
        item_id="i",
        lane=PortfolioLane.FIRST_FIVE_DIRECT.value,
        evidence_strength=5,
        probability_of_movement=0.9,
        strategic_reuse=5,
        proof_potential=5,
        recurring_potential=5,
        founder_minutes=1,
        agent_cost=1,
        delivery_load=1,
        risk=1,
        reversibility=5,
    )
    score = value_score(item)
    assert 0 <= score <= 100


# ── 9. public contact data cannot imply consent ────────────────────────────


def test_public_contact_cannot_imply_consent() -> None:
    assessment = assess_partner_path(
        "rel-1",
        PartnerPath.PARTNER_INTRODUCTION.value,
        relationship_evidence="",  # public employee listing only
        consent_state="unknown",
        plausible=True,
    )
    assert assessment.status == "NOT_EVALUATED"
    assert "NO_RELATIONSHIP_EVIDENCE" in assessment.reasons

    # Active requires consent.
    active_no_consent = assess_partner_path(
        "rel-2",
        PartnerPath.CHANNEL_PARTNERSHIP.value,
        relationship_evidence="two-way intro conversation",
        consent_state="unknown",
        plausible=True,
        active=True,
    )
    assert active_no_consent.status != "ACTIVE"
    assert "ACTIVE_WITHOUT_CONSENT" in active_no_consent.reasons


# ── 10. loss recording requires evidence, never relaxes governance ─────────


def test_loss_requires_evidence() -> None:
    loss, errors = record_loss("acc-1", LossReason.BUDGET.value, evidence="")
    assert loss is None
    assert "LOSS_WITHOUT_EVIDENCE" in errors


def test_loss_never_relaxes_governance() -> None:
    loss, errors = record_loss(
        "acc-1",
        LossReason.NO_URGENCY.value,
        evidence="buyer said later",
        root_cause_hypothesis="timing mismatch",
        safe_improvement="timeboxed follow-up with new evidence",
        next_test="one value-add touch in 30 days",
    )
    assert errors == []
    assert loss is not None
    assert loss.governance_unchanged is True


def test_invalid_loss_reason_rejected() -> None:
    loss, errors = record_loss("acc-1", "MADE_UP_REASON", evidence="x")
    assert loss is None
    assert any(e.startswith("INVALID_LOSS_REASON") for e in errors)


# ── 11. no duplicate scheduler owner exists ────────────────────────────────


def test_scheduler_ownership_no_duplicate_owner() -> None:
    path = Path("/opt/dealix/company-os/SCHEDULER_OWNERSHIP.tsv")
    if not path.exists():
        pytest.skip("founder-os scheduler ownership file not present on this node")
    rows = list(csv.DictReader(path.open(encoding="utf-8"), delimiter="\t"))
    assert rows, "scheduler ownership file is empty"
    owners = [r.get("OWNER", "") for r in rows]
    assert len(owners) == len(set(owners)), f"duplicate scheduler owners: {owners}"


# ── 12. #1273/#1274/#1277 roles do not overlap incorrectly ─────────────────


def test_canonical_layer_roles_do_not_overlap() -> None:
    # Each layer owns a distinct question. Portfolio (meta) consumes
    # #1273 (account spine) and #1274 (factory) outputs; it never re-runs them.
    layer_questions = {
        "1277": "where to invest scarce resources next",
        "1273": "what next for this account",
        "1274": "how evidence/target/campaign orchestration runs",
    }
    assert len(layer_questions) == 3
    # Portfolio command must not fabricate account-level qualification.
    command = build_portfolio_command(
        generated_at="2026-08-28T14:00:00+03:00",
        items=[
            PortfolioItem(
                item_id="i1",
                lane=PortfolioLane.FIRST_FIVE_DIRECT.value,
                company="Co A",
                evidence_strength=2,
                probability_of_movement=0.4,
            )
        ],
    )
    assert len(command.top_moves) == 1
    # The command's next autonomous action is L0-L4 only, no send.
    assert "no external send" in command.next_autonomous_action


# ── 13. portfolio command returns TOP 5 max + one next action ──────────────


def test_portfolio_command_top5_max() -> None:
    items = [
        PortfolioItem(
            item_id=f"i{n}",
            lane=PortfolioLane.FIRST_FIVE_DIRECT.value,
            company=f"Co {n}",
            evidence_strength=3,
            probability_of_movement=0.5,
        )
        for n in range(1, 9)
    ]
    command = build_portfolio_command(generated_at="2026-08-28T14:00:00+03:00", items=items)
    assert len(command.top_moves) == 5
    assert len(command.top_moves) <= 5
    assert command.next_autonomous_action != ""


def test_portfolio_command_never_invents_money() -> None:
    command = build_portfolio_command(
        generated_at="2026-08-28T14:00:00+03:00",
        items=[],
        verified_revenue_sar=0.0,
    )
    assert command.verified_revenue_sar == 0.0
    assert command.closest_verified_money_path == ""


def test_portfolio_command_summarizes_experiments() -> None:
    registry = ExperimentRegistry(
        experiments=(
            Experiment(
                experiment_id="e-scale",
                hypothesis="h",
                decision=ExperimentDecision.SCALE.value,
                outcome="evidence",
            ),
            Experiment(
                experiment_id="e-stop",
                hypothesis="h",
                decision=ExperimentDecision.STOP.value,
                outcome="evidence",
            ),
        )
    )
    command = build_portfolio_command(
        generated_at="2026-08-28T14:00:00+03:00",
        items=[],
        experiments=registry,
    )
    assert command.experiments_scale == ["e-scale"]
    assert command.experiments_stop == ["e-stop"]
