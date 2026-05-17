"""Registry invariants — the fake-green tripwire.

If any machine claims a maturity score it cannot evidence, or the registry
drifts out of shape, these tests fail loudly in CI.
"""
from __future__ import annotations

import pytest

from auto_client_acquisition.execution_assurance_os import (
    EXPECTED_MACHINE_IDS,
    aggregate_score,
    build_full_ops_health,
    evaluate_acceptance_gate,
    evaluate_dod,
    load_machine_registry,
    score_machine,
    validate_registry,
)
from auto_client_acquisition.execution_assurance_os.registry import (
    CANONICAL_EVIDENCE_EVENTS,
)

pytestmark = pytest.mark.unit


def test_registry_loads_and_validates() -> None:
    reg = load_machine_registry()
    ok, errors = validate_registry(reg)
    assert ok, f"registry invalid: {errors}"


def test_all_ten_machines_present() -> None:
    reg = load_machine_registry()
    assert set(reg.ids) == set(EXPECTED_MACHINE_IDS)
    assert len(reg.machines) == 10


def test_no_dod_item_is_met_without_evidence() -> None:
    """The core anti-fake-green invariant."""
    reg = load_machine_registry()
    for m in reg.machines:
        for d in m.definition_of_done:
            if d.met:
                assert d.evidence_ref.strip(), (
                    f"{m.id}/{d.id} claims met:true with no evidence_ref"
                )


def test_every_machine_has_owner_goal_and_gate() -> None:
    reg = load_machine_registry()
    for m in reg.machines:
        assert m.owner.strip(), f"{m.id} has no owner"
        assert m.goal.strip(), f"{m.id} has no goal"
        assert m.acceptance_gate, f"{m.id} has no acceptance gate"
        assert m.definition_of_done, f"{m.id} has no Definition of Done"
        assert m.failure_modes, f"{m.id} has no declared failure modes"


def test_scores_within_zero_to_five() -> None:
    reg = load_machine_registry()
    for m in reg.machines:
        assert 0 <= m.maturity_score <= 5
        assert 0 <= m.scorecard_target <= 5


def test_evidence_event_names_are_canonical() -> None:
    reg = load_machine_registry()
    for m in reg.machines:
        for event in m.evidence_event_names:
            assert event in CANONICAL_EVIDENCE_EVENTS, (
                f"{m.id} references unknown evidence event '{event}'"
            )


def test_docs_only_machines_score_honestly_low() -> None:
    """Marketing, Affiliate and Media are docs-only — they must not read green."""
    reg = load_machine_registry()
    for machine_id in ("marketing_factory", "affiliate_machine", "media_engine"):
        spec = reg.get(machine_id)
        assert spec is not None
        assert spec.maturity_score <= 1, (
            f"{machine_id} claims maturity {spec.maturity_score} — fake green"
        )


def test_scorecard_never_raises_and_is_consistent() -> None:
    reg = load_machine_registry()
    portfolio = aggregate_score(reg)
    assert portfolio.machines_total == 10
    assert 0.0 <= portfolio.percentage <= 100.0
    for spec in reg.machines:
        score = score_machine(spec)
        dod = evaluate_dod(spec)
        gate = evaluate_acceptance_gate(spec)
        assert score.declared_score == spec.maturity_score
        assert 0.0 <= dod.pct <= 100.0
        assert isinstance(gate.passed, bool)


def test_no_inconsistent_maturity_claims() -> None:
    """Declared maturity must not drift wildly from DoD completion."""
    reg = load_machine_registry()
    portfolio = aggregate_score(reg)
    inconsistent = [
        s.machine_id for s in portfolio.machines if s.consistency == "inconsistent"
    ]
    assert not inconsistent, f"inconsistent maturity claims: {inconsistent}"


def test_full_ops_health_builds() -> None:
    reg = load_machine_registry()
    health = build_full_ops_health(reg)
    assert len(health.machine_rows) == 10
    assert len(health.kpis) == 10
    assert health.hard_gates["no_fake_green"] is True
    assert health.critical_kpi["target"] == "0%"
