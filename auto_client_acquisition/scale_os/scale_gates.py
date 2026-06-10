"""Scale gates, leverage tiers, and ladder steps for sovereign scaling."""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum, StrEnum

GateResult = tuple[bool, list[str]]


class LeverageTier(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    EXTREME = "extreme"


class ScaleLadderStep(IntEnum):
    FOUNDER_LED = 1
    PRODUCTIZED = 2
    TOOL_ASSISTED = 3
    TEAM_ASSISTED = 4
    PARTNER_ASSISTED = 5
    PLATFORM_ASSISTED = 6
    ACADEMY_ENABLED = 7
    VENTURE_LED = 8
    STANDARD_LED = 9


@dataclass(frozen=True, slots=True)
class Gate1FounderToProductized:
    same_service_sold_count: int = 0
    same_pain_repeated: bool = False
    same_deliverables_repeated: bool = False


@dataclass(frozen=True, slots=True)
class Gate2ProductizedToTool:
    manual_step_repeats: int = 0
    hours_per_manual_step: float = 0.0
    affects_quality_or_margin: bool = False


@dataclass(frozen=True, slots=True)
class Gate3ToolToTeam:
    checklists_clear: bool = False
    qa_clear: bool = False
    margin_allows_team: bool = False
    delivery_without_full_founder_context: bool = False


@dataclass(frozen=True, slots=True)
class Gate4TeamToPartner:
    delivery_standard_fixed: bool = False
    trust_pack_ready: bool = False
    partner_certification_exists: bool = False
    audit_rights_clear: bool = False


@dataclass(frozen=True, slots=True)
class Gate5PartnerToPlatform:
    client_needs_workspace: bool = False
    deliverables_repeatable: bool = False
    approval_reporting_repeatable: bool = False


@dataclass(frozen=True, slots=True)
class Gate6PlatformToAcademy:
    project_count: int = 0
    proof_backed_cases: int = 0
    method_stable: bool = False
    templates_stable: bool = False


@dataclass(frozen=True, slots=True)
class Gate7AcademyToVenture:
    has_paying_clients: bool = False
    has_retainer_clients: bool = False
    has_product_module: bool = False
    has_owner: bool = False
    has_playbook: bool = False


def evaluate_gate1(s: Gate1FounderToProductized) -> GateResult:
    failed: list[str] = []
    if s.same_service_sold_count < 2:
        failed.append("same_service_sold_count_lt_2")
    if not s.same_pain_repeated:
        failed.append("pain_not_repeated")
    if not s.same_deliverables_repeated:
        failed.append("deliverables_not_repeated")
    return len(failed) == 0, failed


def evaluate_gate2(s: Gate2ProductizedToTool) -> GateResult:
    failed: list[str] = []
    if s.manual_step_repeats < 3:
        failed.append("manual_step_repeats_lt_3")
    if s.hours_per_manual_step <= 2:
        failed.append("manual_step_hours_not_gt_2")
    if not s.affects_quality_or_margin:
        failed.append("no_quality_or_margin_impact")
    return len(failed) == 0, failed


def evaluate_gate3(s: Gate3ToolToTeam) -> GateResult:
    failed: list[str] = []
    if not s.checklists_clear:
        failed.append("checklists_not_clear")
    if not s.qa_clear:
        failed.append("qa_not_clear")
    if not s.margin_allows_team:
        failed.append("margin_not_sufficient")
    if not s.delivery_without_full_founder_context:
        failed.append("founder_context_still_required")
    return len(failed) == 0, failed


def evaluate_gate4(s: Gate4TeamToPartner) -> GateResult:
    failed: list[str] = []
    if not s.delivery_standard_fixed:
        failed.append("delivery_standard_not_fixed")
    if not s.trust_pack_ready:
        failed.append("trust_pack_not_ready")
    if not s.partner_certification_exists:
        failed.append("partner_certification_missing")
    if not s.audit_rights_clear:
        failed.append("audit_rights_not_clear")
    return len(failed) == 0, failed


def evaluate_gate5(s: Gate5PartnerToPlatform) -> GateResult:
    failed: list[str] = []
    if not s.client_needs_workspace:
        failed.append("workspace_need_not_confirmed")
    if not s.deliverables_repeatable:
        failed.append("deliverables_not_repeatable")
    if not s.approval_reporting_repeatable:
        failed.append("approval_reporting_not_repeatable")
    return len(failed) == 0, failed


def evaluate_gate6(s: Gate6PlatformToAcademy) -> GateResult:
    failed: list[str] = []
    if s.project_count < 10:
        failed.append("project_count_lt_10")
    if s.proof_backed_cases < 3:
        failed.append("proof_cases_lt_3")
    if not s.method_stable:
        failed.append("method_not_stable")
    if not s.templates_stable:
        failed.append("templates_not_stable")
    return len(failed) == 0, failed


def evaluate_gate7(s: Gate7AcademyToVenture) -> GateResult:
    failed: list[str] = []
    if not s.has_paying_clients:
        failed.append("no_paying_clients")
    if not s.has_retainer_clients:
        failed.append("no_retainer_clients")
    if not s.has_product_module:
        failed.append("no_product_module")
    if not s.has_owner:
        failed.append("no_owner")
    if not s.has_playbook:
        failed.append("no_playbook")
    return len(failed) == 0, failed
