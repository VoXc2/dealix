"""System 45 — Self-Evolving Organizational Core.

Turns learning, resilience and workforce-governance signals into
optimization proposals. Every proposal is a DRAFT requiring human
approval — there is intentionally no ``apply`` / ``execute`` function in
this module. Doctrine-critical: the core proposes, humans dispose.
"""

from __future__ import annotations

from uuid import uuid4

from auto_client_acquisition.org_consciousness_os.schemas import (
    EvolutionProposal,
    LearningFabricReport,
    ResilienceSignal,
    WorkforceGovernanceReport,
)


def _proposal(
    *,
    target: str,
    change_summary: str,
    rationale: str,
    evidence_refs: tuple[str, ...],
) -> EvolutionProposal:
    return EvolutionProposal(
        proposal_id=f"evo_{uuid4().hex[:12]}",
        target=target,
        change_summary=change_summary,
        rationale=rationale,
        evidence_refs=evidence_refs,
        status="DRAFT",
        requires_human_approval=True,
        auto_apply=False,
    )


def propose_optimizations(
    *,
    customer_id: str,
    learning: LearningFabricReport,
    resilience: ResilienceSignal,
    workforce: WorkforceGovernanceReport,
) -> list[EvolutionProposal]:
    """Propose (DRAFT-only) optimizations from organizational signals."""
    proposals: list[EvolutionProposal] = []

    for pattern in learning.recurring_patterns:
        if pattern.trend == "rising":
            proposals.append(
                _proposal(
                    target=f"workflow:{pattern.pattern_key}",
                    change_summary=(
                        f"Harden the workflow path responsible for "
                        f"'{pattern.pattern_key}' friction."
                    ),
                    rationale=(
                        f"'{pattern.pattern_key}' friction is rising — seen "
                        f"in {pattern.windows_seen} windows, "
                        f"{pattern.occurrences} occurrences."
                    ),
                    evidence_refs=tuple(pattern.sample_workflows),
                )
            )

    if resilience.circuit_state == "open":
        proposals.append(
            _proposal(
                target="resilience:failover",
                change_summary=(
                    "Add a failover/circuit-breaker path for the failing " "action types."
                ),
                rationale=(
                    f"Circuit is OPEN — {resilience.total_failures} failures "
                    f"vs {resilience.executed} executions."
                ),
                evidence_refs=tuple(sorted(resilience.by_action_type)),
            )
        )

    for agent in workforce.agents:
        if not agent.deploy_ready:
            proposals.append(
                _proposal(
                    target=f"agent:{agent.agent_id}",
                    change_summary=(
                        f"Complete deploy prerequisites for "
                        f"{agent.agent_id} before further use."
                    ),
                    rationale=("Missing prerequisites: " + ", ".join(agent.missing_prerequisites)),
                    evidence_refs=tuple(agent.missing_prerequisites),
                )
            )

    return proposals


__all__ = ["propose_optimizations"]
