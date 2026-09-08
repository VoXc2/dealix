#!/usr/bin/env python3
"""Fail-closed verification for legacy self-improvement quarantine."""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

# Entry-point invariant: this verifier must work from any cwd.  Running a file
# under scripts/ops directly makes Python place scripts/ops (not the repository
# root) on sys.path, so project imports would otherwise depend on PYTHONPATH.
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from self_evolving_os import (  # noqa: E402
    LEGACY_COMPATIBILITY_ONLY,
    AutoApplier,
    ImprovementGenerator,
    ImprovementProposal,
    MetricObservation,
)


def run(coro):
    return asyncio.run(coro)


def main() -> int:
    generator = ImprovementGenerator()
    assert run(generator.scan_for_improvements()) == []
    assert run(generator._get_metric_value("avg_latency_ms")) is None

    async def synthetic_provider(metric: str):
        return MetricObservation(
            value=9999.0,
            evidence_refs=(f"synthetic://{metric}",),
            source="verification_fixture",
            synthetic=True,
        )

    assert run(ImprovementGenerator(synthetic_provider).scan_for_improvements()) == []

    proposal = ImprovementProposal(title="verification", evidence_refs=["issue://1331"])
    applier = AutoApplier(approval_required=False)
    assert LEGACY_COMPATIBILITY_ONLY is True
    assert run(applier.can_auto_apply(proposal)) is False
    assert run(applier.try_apply(proposal)).success is False
    assert run(applier.apply_with_approval(proposal, approved=True)).success is False
    assert run(applier.get_applied_count()) == 0

    generator_source = (ROOT / "self_evolving_os" / "improvement_generator.py").read_text(encoding="utf-8")
    applier_source = (ROOT / "self_evolving_os" / "auto_applier.py").read_text(encoding="utf-8")
    profile_source = (ROOT / ".github" / "agents" / "dealix-engineer.md").read_text(encoding="utf-8")

    assert '"avg_latency_ms": 1500.0' not in generator_source
    assert 'AUTO_APPLY_RISK_LEVELS = ["low"]' not in applier_source
    assert "LEGACY_SELF_EVOLVING_APPLIER_DEACTIVATED" in applier_source
    assert "git push" in profile_source
    assert "SPECIFIC_APPROVAL_REQUIRED" in profile_source

    print("DEALIX_SELF_IMPROVEMENT_TRUTH_QUARANTINE=PASS")
    print("SIMULATED_METRICS_AUTHORITY=BLOCKED")
    print("LEGACY_AUTO_APPLY=DEACTIVATED")
    print("CUSTOM_ENGINEER_PROFILE=BOUNDED")
    print("MAIN_MERGE_AUTHORITY=FALSE")
    print("EXTERNAL_EXECUTION_AUTHORITY=FALSE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
