from __future__ import annotations

import asyncio
from datetime import datetime

from self_evolving_os import (
    LEGACY_COMPATIBILITY_ONLY,
    UNKNOWN,
    AutoApplier,
    ImprovementGenerator,
    ImprovementProposal,
    ImprovementSignal,
    MetricObservation,
)


def run(coro):
    return asyncio.run(coro)


def test_missing_metric_provider_produces_no_real_improvements() -> None:
    generator = ImprovementGenerator()

    assert run(generator.scan_for_improvements()) == []
    assert run(generator._get_metric_value("avg_latency_ms")) is None


def test_synthetic_observation_cannot_create_proposal() -> None:
    async def provider(metric: str):
        return MetricObservation(
            value=9999.0,
            evidence_refs=("test://synthetic",),
            source=f"synthetic:{metric}",
            observed_at=datetime.utcnow(),
            synthetic=True,
        )

    generator = ImprovementGenerator(metric_provider=provider)
    assert run(generator.scan_for_improvements()) == []


def test_evidence_backed_metric_can_create_review_only_proposal() -> None:
    async def provider(metric: str):
        values = {
            "avg_latency_ms": 2500.0,
            "error_rate": 0.01,
            "cost_per_call": 0.01,
            "success_rate": 0.99,
        }
        return MetricObservation(
            value=values[metric],
            evidence_refs=(f"otel://metric/{metric}/window-1",),
            source="otel",
            observed_at=datetime.utcnow(),
        )

    proposals = run(ImprovementGenerator(metric_provider=provider).scan_for_improvements())

    assert len(proposals) == 1
    proposal = proposals[0]
    assert proposal.evidence_refs == ["otel://metric/avg_latency_ms/window-1"]
    assert proposal.auto_appliable is False
    assert proposal.authority_class == "APPROVAL_REQUIRED"


def test_manual_source_less_signal_is_rejected() -> None:
    signal = ImprovementSignal(
        metric="avg_latency_ms",
        current_value=2500,
        expected_value=1600,
        gap=0.25,
        evidence_state=UNKNOWN,
    )

    try:
        run(ImprovementGenerator().generate_proposal(signal))
    except ValueError as exc:
        assert "EVIDENCE_REQUIRED" in str(exc)
    else:
        raise AssertionError("source-less proposal must fail closed")


def test_legacy_auto_applier_is_permanently_deactivated() -> None:
    proposal = ImprovementProposal(
        title="test",
        evidence_refs=["issue://1331"],
        config_changes={"timeout_ms": 1000},
    )
    applier = AutoApplier(approval_required=False)

    assert LEGACY_COMPATIBILITY_ONLY is True
    assert run(applier.can_auto_apply(proposal)) is False
    first = run(applier.try_apply(proposal))
    approved = run(applier.apply_with_approval(proposal, approved=True, reviewer="founder"))

    assert first.success is False
    assert approved.success is False
    assert "LEGACY_SELF_EVOLVING_APPLIER_DEACTIVATED" in (first.error or "")
    assert run(applier.get_applied_count()) == 0


def test_duplicate_attempts_remain_idempotently_non_mutating() -> None:
    proposal = ImprovementProposal(title="duplicate", evidence_refs=["issue://1331"])
    applier = AutoApplier()

    first = run(applier.try_apply(proposal))
    second = run(applier.try_apply(proposal))

    assert first.success is False
    assert second.success is False
    assert run(applier.get_applied_count()) == 0
