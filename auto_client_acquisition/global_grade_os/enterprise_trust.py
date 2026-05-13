"""Enterprise Trust Architecture — Source Passport + trust posture.

See ``docs/global_grade/ENTERPRISE_TRUST_ARCHITECTURE.md``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class SensitivityLevel(str, Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"


class AllowedUse(str, Enum):
    INTERNAL_ANALYSIS = "internal_analysis"
    DRAFT_ONLY = "draft_only"
    APPROVED_EXTERNAL = "approved_external"
    AGGREGATED_BENCHMARK = "aggregated_benchmark"
    PUBLIC_PUBLICATION = "public_publication"


@dataclass(frozen=True)
class SourcePassport:
    source_id: str
    source_type: str
    owner: str
    allowed_use: frozenset[AllowedUse]
    contains_pii: bool
    sensitivity: SensitivityLevel
    ai_access_allowed: bool
    external_use_allowed: bool
    residency: str
    license: str | None = None
    refresh_cadence: str | None = None
    last_reviewed_at: str | None = None

    def __post_init__(self) -> None:
        if not self.source_id:
            raise ValueError("source_id_required")
        if not self.owner:
            raise ValueError("owner_required")
        if not self.allowed_use:
            raise ValueError("allowed_use_required")
        if self.external_use_allowed and AllowedUse.APPROVED_EXTERNAL not in self.allowed_use:
            raise ValueError("external_use_inconsistent_with_allowed_use")

    def permits(self, use: AllowedUse) -> bool:
        return use in self.allowed_use


@dataclass(frozen=True)
class TrustPosture:
    """The default trust posture applied across all engagements."""

    data_residency_in_region: bool
    redact_personal_data_before_transit: bool
    draft_only_until_approved: bool
    cold_outreach_forbidden: bool
    public_claims_require_proof_pack_id: bool
    cross_tenant_data_forbidden: bool
    model_output_as_contract_forbidden: bool

    notes: tuple[str, ...] = field(default_factory=tuple)


def default_trust_posture() -> TrustPosture:
    """Return the enforced default posture for new engagements."""

    return TrustPosture(
        data_residency_in_region=True,
        redact_personal_data_before_transit=True,
        draft_only_until_approved=True,
        cold_outreach_forbidden=True,
        public_claims_require_proof_pack_id=True,
        cross_tenant_data_forbidden=True,
        model_output_as_contract_forbidden=True,
    )
