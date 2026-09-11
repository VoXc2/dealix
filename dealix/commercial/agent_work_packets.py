"""Agent Work Packets — bounded work for five logical agents.

Each packet includes:
- objective
- evidence
- constraints
- inputs
- expected output
- acceptance
- budget
- stop condition
- authority level
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from dealix.commercial.economic_cell import EconomicCell, LifecycleState


class AgentRole(StrEnum):
    PM = "dealix-pm"
    SALES = "dealix-sales"
    DELIVERY = "dealix-delivery"
    ENGINEER = "dealix-engineer"
    CONTENT = "dealix-content"


class AuthorityLevel(StrEnum):
    L0_OBSERVE = "L0_observe"
    L1_ANALYZE = "L1_analyze"
    L2_DRAFT = "L2_draft"
    L3_INTERNAL_EXECUTE = "L3_internal_execute"
    L4_REPO_EXECUTE = "L4_repo_execute"
    L5_MATERIAL_EXTERNAL = "L5_material_external"


class PacketStatus(StrEnum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    FAILED = "failed"


# Top3Selection defined locally to avoid circular import
class Top3Selection(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    rank: int
    cell_id: str
    canonical_name: str
    economic_score: float
    confidence: str
    evidence_class: str
    why_selected: str
    evidence_refs: list[str]
    economic_hypothesis: str
    expected_movement: str
    next_measurable_event: str
    owner: str
    resource_budget: str
    stop_loss: str
    why_not_competitors: list[str]


class WorkPacket(BaseModel):
    """Bounded work packet for an agent."""

    model_config = ConfigDict(extra="forbid")

    packet_id: str
    agent_role: AgentRole
    top3_selection: Top3Selection | None = None
    cell_id: str | None = None

    # Objective
    objective: str
    success_criteria: list[str] = Field(default_factory=list)

    # Evidence & Context
    evidence_refs: list[str] = Field(default_factory=list)
    context: dict[str, Any] = Field(default_factory=dict)

    # Constraints
    constraints: list[str] = Field(default_factory=list)
    authority_level: AuthorityLevel = AuthorityLevel.L2_DRAFT
    max_founder_minutes: float = 30.0
    max_cost_sar: float = 0.0
    max_duration_hours: float = 4.0

    # Inputs
    inputs: dict[str, Any] = Field(default_factory=dict)

    # Expected Output
    expected_output: dict[str, Any] = Field(default_factory=dict)
    deliverables: list[str] = Field(default_factory=list)

    # Acceptance
    acceptance_criteria: list[str] = Field(default_factory=list)
    verification_method: str = "human_review"

    # Stop Conditions
    stop_conditions: list[str] = Field(default_factory=list)
    stop_loss: str = ""

    # Status
    status: PacketStatus = PacketStatus.PENDING
    assigned_at: str | None = None
    started_at: str | None = None
    completed_at: str | None = None
    result: dict[str, Any] | None = None

    # Metadata
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    created_by: str = "president_command"


# ─── Packet Builders for Each Agent ────────────────────────────────────


class AgentPacketBuilder:
    """Build work packets for the five logical agents."""

    def __init__(self) -> None:
        pass

    def build_pm_packets(self, top3: list[Top3Selection], portfolio_snapshot: dict[str, Any]) -> list[WorkPacket]:
        """dealix-pm: company truth, portfolio allocation, Top 3, blockers, approvals."""
        packets = []

        # Packet 1: Portfolio Review & Allocation
        packets.append(WorkPacket(
            packet_id=f"pm_portfolio_{datetime.now(UTC).strftime('%Y%m%d')}",
            agent_role=AgentRole.PM,
            objective="Review portfolio state, validate Top 3, manage WIP slots, surface decisions",
            success_criteria=[
                "Portfolio snapshot verified",
                "Top 3 confirmed or adjusted with reasoning",
                "WIP slots allocated per DEEP_WIP_MAX",
                "Blockers and approvals surfaced",
            ],
            evidence_refs=[s.cell_id for s in top3],
            context={"portfolio_snapshot": portfolio_snapshot, "top3": [s.model_dump() for s in top3]},
            authority_level=AuthorityLevel.L3_INTERNAL_EXECUTE,
            max_founder_minutes=15.0,
            inputs={"registry_state": "current", "wip_status": "current"},
            expected_output={
                "validated_top3": "list",
                "wip_allocation": "dict",
                "blockers": "list",
                "approval_requests": "list",
            },
            deliverables=["validated_top3.json", "wip_allocation.json", "pm_brief.md"],
            acceptance_criteria=[
                "Top 3 matches president command output or has documented override",
                "WIP count ≤ 3",
                "All blockers have owner and next action",
            ],
            stop_conditions=["wip_exceeded", "no_valid_candidates"],
            stop_loss="revert_to_previous_top3",
        ))

        return packets

    def build_sales_packets(self, top3: list[Top3Selection], cells: list[EconomicCell]) -> list[WorkPacket]:
        """dealix-sales: qualified relationship movement, diagnostic, discovery, commercial drafts."""
        packets = []
        cell_map = {c.identity.cell_id: c for c in cells}

        for selection in top3:
            cell = cell_map.get(selection.cell_id)
            if not cell:
                continue

            # Diagnostic/Discovery packet
            packets.append(WorkPacket(
                packet_id=f"sales_diag_{selection.cell_id}_{datetime.now(UTC).strftime('%Y%m%d')}",
                agent_role=AgentRole.SALES,
                top3_selection=selection,
                cell_id=selection.cell_id,
                objective=f"Run diagnostic for {cell.identity.canonical_name}: qualify problem, buyer, access",
                success_criteria=[
                    "Problem quantified with measurable loss",
                    "Economic buyer identified and verified",
                    "Distribution path confirmed (warm/relationship)",
                    "Consent state assessed",
                    "Commercial draft prepared (if qualified)",
                ],
                evidence_refs=cell.evidence.evidence_sources,
                context={"cell": cell.model_dump(mode="json")},
                authority_level=AuthorityLevel.L2_DRAFT,
                max_founder_minutes=30.0,
                inputs={
                    "problem_class": cell.problem.problem_class.value,
                    "buyer_group": cell.buyer.buyer_group.value,
                    "sector": cell.market.sector.value,
                },
                expected_output={
                    "diagnostic_report": "dict",
                    "qualified": "bool",
                    "commercial_draft": "dict | null",
                    "next_action": "str",
                },
                deliverables=["diagnostic_report.md", "commercial_draft.json"],
                acceptance_criteria=[
                    "Problem statement has measurable loss type",
                    "Economic buyer named with verification ref",
                    "Relationship path documented",
                    "If qualified: commercial draft with acceptance criteria",
                ],
                stop_conditions=["no_buyer_identified", "no_relationship_path", "procurement_blocked"],
                stop_loss="return_to_research",
            ))

        return packets

    def build_delivery_packets(self, top3: list[Top3Selection], cells: list[EconomicCell]) -> list[WorkPacket]:
        """dealix-delivery: acceptance criteria, pilot execution, proof capture."""
        packets = []
        cell_map = {c.identity.cell_id: c for c in cells}

        for selection in top3:
            cell = cell_map.get(selection.cell_id)
            if not cell:
                continue

            if cell.portfolio.lifecycle_state in {LifecycleState.ACTIVE_DEEP, LifecycleState.DELIVERING}:
                packets.append(WorkPacket(
                    packet_id=f"delivery_exec_{selection.cell_id}_{datetime.now(UTC).strftime('%Y%m%d')}",
                    agent_role=AgentRole.DELIVERY,
                    top3_selection=selection,
                    cell_id=selection.cell_id,
                    objective=f"Execute delivery for {cell.identity.canonical_name}: pilot, proof, acceptance",
                    success_criteria=[
                        "Pilot plan executed per day-plan",
                        "Weekly proof captured",
                        "Customer acceptance criteria measured",
                        "Expansion signals documented",
                    ],
                    evidence_refs=cell.evidence.evidence_sources + cell.proof.proof_events,
                    context={"cell": cell.model_dump(mode="json")},
                    authority_level=AuthorityLevel.L3_INTERNAL_EXECUTE,
                    max_founder_minutes=60.0,
                    max_duration_hours=20.0,
                    inputs={
                        "pilot_plan": cell.portfolio.next_action,
                        "acceptance_criteria": cell.offer.acceptance_criteria,
                        "proof_method": cell.proof.proof_strength,
                    },
                    expected_output={
                        "delivery_status": "str",
                        "proof_events": "list",
                        "customer_validation": "bool",
                        "expansion_signal": "dict | null",
                    },
                    deliverables=["delivery_log.md", "proof_pack.md", "acceptance_report.json"],
                    acceptance_criteria=[
                        "Pilot milestones met per day-plan",
                        "Proof events captured with evidence refs",
                        "Customer validation recorded (yes/no)",
                    ],
                    stop_conditions=["customer_rejection", "acceptance_criteria_failed", "scope_creep"],
                    stop_loss="stop_pilot_reassess",
                ))

        return packets

    def build_engineer_packets(self, top3: list[Top3Selection], cells: list[EconomicCell]) -> list[WorkPacket]:
        """dealix-engineer: production trust, platform, integrations, security."""
        packets = []

        # Production Trust packet (always)
        packets.append(WorkPacket(
            packet_id=f"eng_prod_trust_{datetime.now(UTC).strftime('%Y%m%d')}",
            agent_role=AgentRole.ENGINEER,
            objective="Verify production trust: runtime health, release identity, DB, TLS, rollback",
            success_criteria=[
                "Release identity verified (git SHA == running SHA)",
                "API health endpoints green",
                "DB migrations current",
                "TLS valid",
                "Rollback tested",
                "No secret leaks",
            ],
            evidence_refs=["release_sha", "health_endpoints", "alembic_head"],
            authority_level=AuthorityLevel.L3_INTERNAL_EXECUTE,
            max_founder_minutes=20.0,
            inputs={"services": ["api", "frontend", "db", "redis"]},
            expected_output={
                "production_trust_report": "dict",
                "release_verified": "bool",
                "issues": "list",
            },
            deliverables=["production_trust_report.json", "release_verification.md"],
            acceptance_criteria=[
                "Git SHA matches running release",
                "All health checks pass",
                "Alembic single head confirmed",
            ],
            stop_conditions=["release_mismatch", "health_check_failed", "secret_leak_detected"],
            stop_loss="halt_deployments_investigate",
        ))

        # Capability enablement for top 3
        cell_map = {c.identity.cell_id: c for c in cells}
        for selection in top3:
            cell = cell_map.get(selection.cell_id)
            if not cell:
                continue

            deps = cell.execution.capability_dependencies + cell.execution.integration_dependencies
            if deps:
                packets.append(WorkPacket(
                    packet_id=f"eng_capability_{selection.cell_id}_{datetime.now(UTC).strftime('%Y%m%d')}",
                    agent_role=AgentRole.ENGINEER,
                    top3_selection=selection,
                    cell_id=selection.cell_id,
                    objective=f"Enable capabilities for {cell.identity.canonical_name}: {', '.join(deps)}",
                    success_criteria=[
                        "Capability dependencies available",
                        "Integration endpoints tested",
                        "Security review passed",
                        "Cost estimates updated",
                    ],
                    evidence_refs=[],
                    context={"cell": cell.model_dump(mode="json"), "dependencies": deps},
                    authority_level=AuthorityLevel.L4_REPO_EXECUTE,
                    max_founder_minutes=45.0,
                    max_duration_hours=8.0,
                    inputs={"dependencies": deps},
                    expected_output={
                        "capability_status": "dict",
                        "integration_tests": "list",
                        "security_review": "str",
                    },
                    deliverables=["capability_readiness.md", "integration_test_results.json"],
                    acceptance_criteria=[
                        "All dependencies resolved or documented",
                        "Integration tests pass",
                        "No HIGH security findings",
                    ],
                    stop_conditions=["dependency_unavailable", "security_blocked", "cost_overrun"],
                    stop_loss="defer_capability_use_fallback",
                ))

        return packets

    def build_content_packets(self, top3: list[Top3Selection], cells: list[EconomicCell]) -> list[WorkPacket]:
        """dealix-content: owned-channel distribution, proof transformation, case studies."""
        packets = []

        # Weekly content packet
        packets.append(WorkPacket(
            packet_id=f"content_weekly_{datetime.now(UTC).strftime('%Y%m%d')}",
            agent_role=AgentRole.CONTENT,
            objective="Produce weekly owned-channel content: LinkedIn drafts, AEO articles, proof packages",
            success_criteria=[
                "3 LinkedIn drafts created (approval-ready)",
                "1 AEO article drafted",
                "Proof pack transformed for distribution",
                "Arabic/English versions prepared",
            ],
            evidence_refs=[],
            authority_level=AuthorityLevel.L2_DRAFT,
            max_founder_minutes=45.0,
            max_duration_hours=6.0,
            inputs={"top3": [s.model_dump() for s in top3]},
            expected_output={
                "linkedin_drafts": "list",
                "aeo_article": "dict",
                "proof_distribution_pack": "dict",
            },
            deliverables=["linkedin_drafts.json", "aeo_article.md", "proof_distribution.json"],
            acceptance_criteria=[
                "All drafts approval-ready (no auto-send)",
                "Arabic + English versions",
                "Proof references customer-validated evidence only",
            ],
            stop_conditions=["no_customer_proof_available", "approval_queue_full"],
            stop_loss="defer_to_next_week",
        ))

        # Case study packets for proven cells
        cell_map = {c.identity.cell_id: c for c in cells}
        for selection in top3:
            cell = cell_map.get(selection.cell_id)
            if not cell or cell.portfolio.lifecycle_state != LifecycleState.PROVEN:
                continue

            if cell.proof.customer_validated and cell.proof.public_use_authorized:
                packets.append(WorkPacket(
                    packet_id=f"content_case_study_{selection.cell_id}_{datetime.now(UTC).strftime('%Y%m%d')}",
                    agent_role=AgentRole.CONTENT,
                    top3_selection=selection,
                    cell_id=selection.cell_id,
                    objective=f"Create case study for {cell.identity.canonical_name}",
                    success_criteria=[
                        "Case study drafted with customer quotes",
                        "Metrics quantified (revenue, time, risk)",
                        "Permission confirmed for public use",
                        "Arabic/English versions",
                    ],
                    evidence_refs=cell.proof.proof_events,
                    context={"cell": cell.model_dump(mode="json")},
                    authority_level=AuthorityLevel.L2_DRAFT,
                    max_founder_minutes=30.0,
                    inputs={"proof_events": cell.proof.proof_events, "metrics": cell.economics},
                    expected_output={
                        "case_study_draft": "dict",
                        "permission_confirmed": "bool",
                    },
                    deliverables=["case_study_draft.md", "permission_record.json"],
                    acceptance_criteria=[
                        "Customer permission documented",
                        "No unverified claims",
                        "Both languages complete",
                    ],
                    stop_conditions=["permission_denied", "insufficient_proof"],
                    stop_loss="keep_internal_only",
                ))

        return packets

    def build_all_packets(
        self,
        top3: list[Top3Selection],
        cells: list[EconomicCell],
        portfolio_snapshot: dict[str, Any],
    ) -> dict[AgentRole, list[WorkPacket]]:
        """Build all packets for all five agents."""
        return {
            AgentRole.PM: self.build_pm_packets(top3, portfolio_snapshot),
            AgentRole.SALES: self.build_sales_packets(top3, cells),
            AgentRole.DELIVERY: self.build_delivery_packets(top3, cells),
            AgentRole.ENGINEER: self.build_engineer_packets(top3, cells),
            AgentRole.CONTENT: self.build_content_packets(top3, cells),
        }


# ─── Packet Execution Tracker ─────────────────────────────────────────


@dataclass
class PacketTracker:
    """Track packet execution status."""

    packets: dict[str, WorkPacket] = field(default_factory=dict)

    def add(self, packet: WorkPacket) -> None:
        self.packets[packet.packet_id] = packet

    def start(self, packet_id: str) -> bool:
        if packet_id in self.packets:
            packet = self.packets[packet_id]
            packet.status = PacketStatus.IN_PROGRESS
            packet.started_at = datetime.now(UTC).isoformat()
            return True
        return False

    def complete(self, packet_id: str, result: dict[str, Any]) -> bool:
        if packet_id in self.packets:
            packet = self.packets[packet_id]
            packet.status = PacketStatus.COMPLETED
            packet.completed_at = datetime.now(UTC).isoformat()
            packet.result = result
            return True
        return False

    def block(self, packet_id: str, reason: str) -> bool:
        if packet_id in self.packets:
            packet = self.packets[packet_id]
            packet.status = PacketStatus.BLOCKED
            packet.result = {"blocked_reason": reason}
            return True
        return False

    def get_by_agent(self, agent: AgentRole) -> list[WorkPacket]:
        return [p for p in self.packets.values() if p.agent_role == agent]

    def get_pending(self) -> list[WorkPacket]:
        return [p for p in self.packets.values() if p.status == PacketStatus.PENDING]

    def summary(self) -> dict[str, Any]:
        by_status: dict[str, int] = {}
        by_agent: dict[str, int] = {}
        for p in self.packets.values():
            by_status[p.status.value] = by_status.get(p.status.value, 0) + 1
            by_agent[p.agent_role.value] = by_agent.get(p.agent_role.value, 0) + 1
        return {
            "total": len(self.packets),
            "by_status": by_status,
            "by_agent": by_agent,
        }


__all__ = [
    "AgentRole",
    "AuthorityLevel",
    "PacketStatus",
    "WorkPacket",
    "AgentPacketBuilder",
    "PacketTracker",
    "Top3Selection",
]
