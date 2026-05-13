"""Board-Ready Roadmap — six canonical phases."""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum


class BoardReadyPhase(IntEnum):
    PROOF_ENGINE = 1
    RETAINER_ENGINE = 2
    PRODUCTIZATION_ENGINE = 3
    ENTERPRISE_TRUST_ENGINE = 4
    DISTRIBUTION_ENGINE = 5
    HOLDING_ENGINE = 6


BOARD_READY_PHASES: tuple[BoardReadyPhase, ...] = tuple(BoardReadyPhase)


_PHASE_DELIVERABLES: dict[BoardReadyPhase, tuple[str, ...]] = {
    BoardReadyPhase.PROOF_ENGINE: (
        "capability_diagnostic",
        "revenue_intelligence_sprint",
        "source_passport",
        "governance_runtime_basic",
        "proof_pack",
        "capital_ledger",
    ),
    BoardReadyPhase.RETAINER_ENGINE: (
        "monthly_revops_os",
        "client_health",
        "proof_timeline",
        "expansion_map",
        "founder_command_center",
    ),
    BoardReadyPhase.PRODUCTIZATION_ENGINE: (
        "data_readiness_engine",
        "account_scoring_module",
        "proof_pack_generator",
        "productization_ledger",
        "client_workspace_mvp",
    ),
    BoardReadyPhase.ENTERPRISE_TRUST_ENGINE: (
        "ai_run_ledger",
        "agent_registry",
        "approval_engine",
        "audit_exports",
        "incident_response",
        "trust_pack",
    ),
    BoardReadyPhase.DISTRIBUTION_ENGINE: (
        "dealix_method",
        "partner_program",
        "academy_tracks",
        "benchmark_reports",
        "certification",
    ),
    BoardReadyPhase.HOLDING_ENGINE: (
        "dealix_revenue_bu",
        "dealix_governance_bu",
        "business_unit_scorecards",
        "venture_signal_engine",
        "vertical_venture_candidates",
    ),
}


@dataclass(frozen=True)
class BoardReadyRoadmap:
    current_phase: BoardReadyPhase
    completed_deliverables: frozenset[str]

    def gap_in_current_phase(self) -> tuple[str, ...]:
        wanted = _PHASE_DELIVERABLES[self.current_phase]
        return tuple(d for d in wanted if d not in self.completed_deliverables)

    def is_phase_complete(self) -> bool:
        return not self.gap_in_current_phase()
