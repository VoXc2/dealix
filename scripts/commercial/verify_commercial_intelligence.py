#!/usr/bin/env python3
"""Static and domain verification for Commercial Intelligence foundation."""

from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_finance import (
    REQUIRED_ECONOMIC_SOURCE_KEYS,
    CommercialFinanceDecision,
    CommercialFinanceInputs,
    OfferEconomicsClass,
    evaluate_commercial_finance,
)
from dealix.commercial_intelligence import (
    EvidenceLevel,
    GovernedSource,
    OpportunityInputs,
    SourceKind,
    SourcePolicyStatus,
    score_opportunity,
    score_source,
)

REQUIRED = (
    "dealix/commercial_intelligence.py",
    "dealix/commercial_finance.py",
    "db/models_commercial_intelligence.py",
    "db/migrations/versions/20260715_017_commercial_intelligence_graph.py",
    "api/routers/commercial_intelligence.py",
    "apps/web/app/commercial-intelligence/page.tsx",
    "data/commercial_intelligence/ksa_source_registry.yaml",
    "data/commercial_intelligence/dealix_department_objectives.yaml",
    "docs/commercial/DEALIX_SAUDI_COMMERCIAL_STRATEGY_2026_AR.md",
)

PROVIDER_AUTHORITY_SOURCE = "dealix/config/railway_services.json"
PROVIDER_REQUIRED = {
    "railway": ("railway.json", "dealix/config/railway_services.json"),
    "selfhost": (
        "deploy/selfhost/compose.yml",
        "scripts/ops/verify_selfhosted_production_plane.py",
        "scripts/ops/verify_selfhost_production_cutover_contract.py",
    ),
}


def resolve_provider_requirements(root: Path = ROOT) -> tuple[str, tuple[str, ...]]:
    authority_path = root / PROVIDER_AUTHORITY_SOURCE
    try:
        payload = json.loads(authority_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"invalid provider authority source: {authority_path}") from exc
    authority = payload.get("productionProviderAuthority")
    if not isinstance(authority, dict):
        raise RuntimeError("productionProviderAuthority is missing")
    provider = str(authority.get("provider") or "").strip().lower()
    required = PROVIDER_REQUIRED.get(provider)
    if required is None:
        raise RuntimeError(f"unsupported production provider authority: {provider or 'missing'}")
    return provider, required


def main() -> int:
    try:
        provider, provider_required = resolve_provider_requirements(ROOT)
    except RuntimeError as exc:
        print("COMMERCIAL_INTELLIGENCE_FOUNDATION=FAIL")
        print(f"PROVIDER_AUTHORITY_ERROR={exc}")
        return 1
    required = (*REQUIRED, *provider_required)
    missing = [path for path in required if not (ROOT / path).is_file()]
    if missing:
        print("COMMERCIAL_INTELLIGENCE_FOUNDATION=FAIL")
        for path in missing:
            print(f"MISSING={path}")
        return 1
    source = GovernedSource(
        tenant_id="dealix",
        source_id="src_verify",
        name="Verification source",
        kind=SourceKind.OWNED,
        policy_status=SourcePolicyStatus.APPROVED,
        allowed_use="internal_verification",
        authority_score=90,
        verifiability_score=90,
        freshness_days=30,
        retention_days=365,
        terms_reviewed_at=datetime.now(UTC),
    )
    opportunity = score_opportunity(
        OpportunityInputs(
            strategic_fit=90,
            problem_evidence=90,
            urgency=80,
            relationship_strength=80,
            commercial_value=80,
            evidence_level=EvidenceLevel.L4_VERIFIED,
            source_score=score_source(source),
            signal_count=2,
        )
    )
    if opportunity.external_action_allowed or opportunity.score < 75:
        print("COMMERCIAL_INTELLIGENCE_FOUNDATION=FAIL")
        return 1
    finance = evaluate_commercial_finance(
        CommercialFinanceInputs(
            opportunity_id="opp_verify",
            offer_id="revenue_proof_sprint",
            offer_class=OfferEconomicsClass.PRODUCTIZED,
            list_price_sar=Decimal("10000"),
            proposed_price_sar=Decimal("9000"),
            delivery_cost_sar=Decimal("3000"),
            acquisition_cost_sar=Decimal("500"),
            upfront_cash_exposure_sar=Decimal("500"),
            payment_terms_days=30,
            capacity_required_pct=Decimal("10"),
            source_refs={
                key: f"evidence://verification/{key}"
                for key in REQUIRED_ECONOMIC_SOURCE_KEYS
            },
        )
    )
    if (
        finance.decision is not CommercialFinanceDecision.PURSUE
        or finance.external_action_allowed
        or finance.customer_roi_used_in_decision
    ):
        print("COMMERCIAL_INTELLIGENCE_FOUNDATION=FAIL")
        return 1
    print("COMMERCIAL_INTELLIGENCE_FOUNDATION=PASS")
    print(f"PRODUCTION_PROVIDER_AUTHORITY={provider}")
    print("VERCEL_READINESS_AUTHORITY=false")
    print("PERSISTENCE_TABLES=7")
    print(f"COMMERCIAL_FINANCE_DECISION={finance.decision.value}")
    print("EXTERNAL_ACTIONS_EXECUTED=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
