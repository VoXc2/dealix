"""90-day Enterprise AI Transformation Program — phase + gate structure.

Pure data module: no I/O, no DB, safe to import in unit tests. The
``enterprise_ai_operating_system`` offering in the service catalog is delivered
through this program. Each phase ends with a gate checkpoint; a phase is not
invoiced until its gate is met (see the offering's KPI commitment).
"""

from __future__ import annotations

from typing import NamedTuple


class ProgramPhase(NamedTuple):
    """One gated phase of the 90-day program."""

    key: str
    name_ar: str
    name_en: str
    week_start: int
    week_end: int
    deliverables: tuple[str, ...]
    gate_checkpoint: str


PROGRAM_PHASES: tuple[ProgramPhase, ...] = (
    ProgramPhase(
        key="ai_audit",
        name_ar="تدقيق الذكاء الاصطناعي",
        name_en="AI Audit",
        week_start=1,
        week_end=2,
        deliverables=(
            "Stakeholder interviews",
            "Operations + data analysis",
            "AI Opportunity Map",
            "Risk map",
            "30/60/90 AI roadmap",
        ),
        gate_checkpoint="AI Opportunity Map approved by founder",
    ),
    ProgramPhase(
        key="foundation",
        name_ar="التأسيس",
        name_en="Foundation",
        week_start=3,
        week_end=4,
        deliverables=(
            "Workspace + auth / users",
            "Knowledge ingestion",
            "Base dashboard",
            "Governance rules",
            "Append-only audit logging",
        ),
        gate_checkpoint="Governance rules + audit logging live",
    ),
    ProgramPhase(
        key="first_agents",
        name_ar="الوكلاء الأوائل",
        name_en="First Agents",
        week_start=5,
        week_end=6,
        deliverables=(
            "Sales or Support AI agent (draft-first)",
            "Company Brain v1",
            "Human handoff path",
            "Approval workflows",
        ),
        gate_checkpoint="First agent passes eval; draft-first verified",
    ),
    ProgramPhase(
        key="integrations",
        name_ar="التكاملات",
        name_en="Integrations",
        week_start=7,
        week_end=8,
        deliverables=(
            "WhatsApp integration contract",
            "CRM integration contract",
            "Email integration contract",
            "Drive / Sheets integration contract",
        ),
        gate_checkpoint="Integration contracts signed off; no live-send enabled",
    ),
    ProgramPhase(
        key="executive_layer",
        name_ar="الطبقة التنفيذية",
        name_en="Executive Layer",
        week_start=9,
        week_end=10,
        deliverables=(
            "ROI dashboard wired to the value ledger",
            "Executive reports",
            "Risk dashboard",
            "Decision memos",
        ),
        gate_checkpoint="ROI dashboard wired to the value ledger",
    ),
    ProgramPhase(
        key="scale_plan",
        name_ar="خطة التوسع",
        name_en="Scale Plan",
        week_start=11,
        week_end=12,
        deliverables=(
            "Team training",
            "Handover package",
            "Adoption plan",
            "Next 6-month roadmap",
            "Retainer proposal",
        ),
        gate_checkpoint="Handover package accepted; Proof Pack assembled",
    ),
)

PROGRAM_DURATION_DAYS = 90


class EnterpriseProgram(NamedTuple):
    """The full 90-day program definition."""

    service_id: str
    name_ar: str
    name_en: str
    duration_days: int
    phases: tuple[ProgramPhase, ...]


def get_program() -> EnterpriseProgram:
    """Return the canonical 90-day Enterprise AI Transformation Program."""
    return EnterpriseProgram(
        service_id="enterprise_ai_operating_system",
        name_ar="برنامج التحول المؤسسي بالذكاء الاصطناعي",
        name_en="Enterprise AI Transformation Program",
        duration_days=PROGRAM_DURATION_DAYS,
        phases=PROGRAM_PHASES,
    )


def list_phases() -> tuple[ProgramPhase, ...]:
    """All program phases in delivery order."""
    return PROGRAM_PHASES


def phase_by_key(key: str) -> ProgramPhase | None:
    """Return one phase by key, or None if unknown."""
    for phase in PROGRAM_PHASES:
        if phase.key == key:
            return phase
    return None
