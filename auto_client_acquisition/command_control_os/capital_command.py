"""Capital Command — typed capital asset records and engagement check.

See ``docs/command_control/CAPITAL_COMMAND.md``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class CapitalType(str, Enum):
    SERVICE = "service_capital"
    PRODUCT = "product_capital"
    KNOWLEDGE = "knowledge_capital"
    TRUST = "trust_capital"
    MARKET = "market_capital"
    STANDARD = "standard_capital"
    PARTNER = "partner_capital"
    VENTURE = "venture_capital"


@dataclass(frozen=True)
class CapitalAssetRecord:
    capital_id: str
    type: CapitalType
    title: str
    description: str
    source_engagement_id: str
    business_unit: str
    owner: str
    reuse_count: int = 0
    public_ok: bool = False
    linked_proof_ids: tuple[str, ...] = ()
    maturity: str = "draft"  # draft | reviewed | productized
    status: str = "active"   # active | archived

    def __post_init__(self) -> None:
        if not self.capital_id:
            raise ValueError("capital_id_required")
        if self.reuse_count < 0:
            raise ValueError("reuse_count_must_be_non_negative")
        if self.maturity not in {"draft", "reviewed", "productized"}:
            raise ValueError("invalid_maturity")
        if self.status not in {"active", "archived"}:
            raise ValueError("invalid_status")


@dataclass(frozen=True)
class EngagementCapitalSummary:
    engagement_id: str
    assets: tuple[CapitalAssetRecord, ...] = field(default_factory=tuple)
    expansion_path_documented: bool = False

    def has_trust_asset(self) -> bool:
        return any(a.type is CapitalType.TRUST for a in self.assets)

    def has_product_or_knowledge_asset(self) -> bool:
        return any(
            a.type in {CapitalType.PRODUCT, CapitalType.KNOWLEDGE}
            for a in self.assets
        )


def engagement_strategically_complete(summary: EngagementCapitalSummary) -> bool:
    """Enforce the per-engagement minimum from the doctrine."""

    return (
        summary.has_trust_asset()
        and summary.has_product_or_knowledge_asset()
        and summary.expansion_path_documented
    )
