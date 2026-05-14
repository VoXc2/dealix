"""Execution anti-patterns — detect signals and prescribed remediation."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ExecutionAntiPattern(StrEnum):
    FOUNDER_HERO = "founder_hero_mode"
    FEATURE_FANTASY = "feature_fantasy"
    CUSTOM_CHAOS = "custom_chaos"
    GOVERNANCE_SHORTCUT = "governance_shortcut"
    PROOF_WEAKNESS = "proof_weakness"
    MARKET_CONFUSION = "market_confusion"


@dataclass(frozen=True, slots=True)
class AntiPatternSignal:
    pattern: ExecutionAntiPattern
    remediation: str


def detect_anti_patterns(
    *,
    founder_only_critical_path: bool = False,
    feature_without_usage_signal: bool = False,
    every_client_custom_scope: bool = False,
    output_without_governance_status: bool = False,
    delivery_without_proof_pack: bool = False,
    multiple_primary_ctas: bool = False,
) -> tuple[AntiPatternSignal, ...]:
    hits: list[AntiPatternSignal] = []
    if founder_only_critical_path:
        hits.append(
            AntiPatternSignal(
                pattern=ExecutionAntiPattern.FOUNDER_HERO,
                remediation="templates_checklists_qa_delivery_os",
            ),
        )
    if feature_without_usage_signal:
        hits.append(
            AntiPatternSignal(
                pattern=ExecutionAntiPattern.FEATURE_FANTASY,
                remediation="productization_gate_internal_use_first",
            ),
        )
    if every_client_custom_scope:
        hits.append(
            AntiPatternSignal(
                pattern=ExecutionAntiPattern.CUSTOM_CHAOS,
                remediation="service_catalog_scope_control_capital_review",
            ),
        )
    if output_without_governance_status:
        hits.append(
            AntiPatternSignal(
                pattern=ExecutionAntiPattern.GOVERNANCE_SHORTCUT,
                remediation="no_output_without_governance_status",
            ),
        )
    if delivery_without_proof_pack:
        hits.append(
            AntiPatternSignal(
                pattern=ExecutionAntiPattern.PROOF_WEAKNESS,
                remediation="proof_pack_mandatory",
            ),
        )
    if multiple_primary_ctas:
        hits.append(
            AntiPatternSignal(
                pattern=ExecutionAntiPattern.MARKET_CONFUSION,
                remediation="one_wedge_one_language_one_primary_cta",
            ),
        )
    return tuple(hits)
