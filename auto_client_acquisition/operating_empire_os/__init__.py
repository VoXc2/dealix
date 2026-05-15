"""Operating Empire OS — language, trust, proof economy, units, benchmarks."""

from __future__ import annotations

from auto_client_acquisition.operating_empire_os.benchmark_engine import (
    BENCHMARK_SAFE_RULES,
    benchmark_publish_ok,
)
from auto_client_acquisition.operating_empire_os.market_language_score import (
    market_language_coverage_score,
)
from auto_client_acquisition.operating_empire_os.no_commodity_rules import (
    COMMODITY_ESCAPE_FRAME,
    escape_commodity_framing,
)
from auto_client_acquisition.operating_empire_os.partner_gate import partner_empire_gate_readiness
from auto_client_acquisition.operating_empire_os.proof_economy import (
    can_make_public_claim,
    can_publish_case_study,
    can_push_retainer,
)
from auto_client_acquisition.operating_empire_os.trust_infrastructure import (
    TRUST_INFRASTRUCTURE_TENETS,
    TrustInfrastructureAttestation,
    trust_infrastructure_score,
)
from auto_client_acquisition.operating_empire_os.unit_system import (
    UNIT_REGISTRY,
    DealixBusinessUnit,
    UnitSystemProfile,
    get_unit_profile,
)

__all__ = [
    "BENCHMARK_SAFE_RULES",
    "COMMODITY_ESCAPE_FRAME",
    "TRUST_INFRASTRUCTURE_TENETS",
    "UNIT_REGISTRY",
    "DealixBusinessUnit",
    "TrustInfrastructureAttestation",
    "UnitSystemProfile",
    "benchmark_publish_ok",
    "can_make_public_claim",
    "can_publish_case_study",
    "can_push_retainer",
    "escape_commodity_framing",
    "get_unit_profile",
    "market_language_coverage_score",
    "partner_empire_gate_readiness",
    "trust_infrastructure_score",
]
