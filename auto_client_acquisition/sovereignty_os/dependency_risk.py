"""Dependency Risk Map — canonical inventory and uncontrolled-dependency check.

See ``docs/sovereignty/DEPENDENCY_RISK_MAP.md``.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Severity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass(frozen=True)
class DependencyEntry:
    dependency: str
    risk: str
    control: str
    severity: Severity
    fallback: str | None = None

    def is_controlled(self) -> bool:
        """A dependency is controlled if it has either a control or a fallback."""

        return bool(self.control) or bool(self.fallback)


@dataclass(frozen=True)
class DependencyRiskMap:
    entries: tuple[DependencyEntry, ...]

    def by_severity(self, severity: Severity) -> tuple[DependencyEntry, ...]:
        return tuple(e for e in self.entries if e.severity is severity)

    def uncontrolled(self) -> tuple[DependencyEntry, ...]:
        return tuple(e for e in self.entries if not e.is_controlled())


# The doctrine map from the Dependency Risk doc.
DEFAULT_DEPENDENCY_MAP: DependencyRiskMap = DependencyRiskMap(
    entries=(
        DependencyEntry(
            dependency="single_llm_provider",
            risk="price_quality_policy_shock",
            control="llm_gateway_model_router",
            severity=Severity.CRITICAL,
            fallback="balanced_or_local_model",
        ),
        DependencyEntry(
            dependency="founder_delivery",
            risk="bottleneck",
            control="delivery_os_and_checklists",
            severity=Severity.HIGH,
            fallback="bu_delivery_lead",
        ),
        DependencyEntry(
            dependency="custom_projects",
            risk="agency_trap",
            control="productized_offers",
            severity=Severity.HIGH,
            fallback="refuse_custom_scope",
        ),
        DependencyEntry(
            dependency="weak_data_sources",
            risk="bad_outputs",
            control="source_passport",
            severity=Severity.HIGH,
            fallback="deny_access",
        ),
        DependencyEntry(
            dependency="unsafe_automation",
            risk="trust_loss",
            control="governance_runtime",
            severity=Severity.CRITICAL,
            fallback="draft_only_default",
        ),
        DependencyEntry(
            dependency="single_sales_channel",
            risk="growth_fragility",
            control="partners_content_academy",
            severity=Severity.MEDIUM,
            fallback="founder_authority",
        ),
        DependencyEntry(
            dependency="single_client_segment",
            risk="market_fragility",
            control="portfolio_strategy",
            severity=Severity.MEDIUM,
            fallback="cross_sector_pilots",
        ),
        DependencyEntry(
            dependency="no_proof",
            risk="weak_retention",
            control="proof_pack",
            severity=Severity.HIGH,
            fallback="pause_offer",
        ),
        DependencyEntry(
            dependency="no_capital_capture",
            risk="no_compounding",
            control="capital_ledger",
            severity=Severity.HIGH,
            fallback="archive_engagement",
        ),
    ),
)


def has_uncontrolled_dependencies(risk_map: DependencyRiskMap | None = None) -> bool:
    """Return True if any entry lacks both a control and a fallback."""

    risk_map = risk_map or DEFAULT_DEPENDENCY_MAP
    return bool(risk_map.uncontrolled())
