"""Deterministic execution primitives for the Brand & Growth Portfolio V2.

This module composes the existing Market Radar, canonical workers, channel
registry and proof owners. It is deliberately read-only/draft-only: it cannot
create relationship, consent, send, publish, quote, payment, proof or
production authority.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from typing import Any, Mapping

UNKNOWN = "UNKNOWN_NOT_EVIDENCE_BACKED"

AUTHORITY_KEYS = (
    "relationship",
    "consent",
    "offer",
    "price",
    "quote",
    "contract",
    "external_send",
    "public_publish",
    "payment",
    "customer_proof",
    "execution",
    "production",
)

ZERO_AUTHORITY = {key: False for key in AUTHORITY_KEYS}

GROWTH_ARMS = frozenset(
    {
        "BRAND_AUTHORITY",
        "WEBSITE_CONVERSION",
        "SEARCH_SEO_AEO",
        "FOUNDER_THOUGHT_LEADERSHIP",
        "COMPANY_SOCIAL_VIDEO",
        "EVENT_FIELD_INTELLIGENCE",
        "PARTNER_MARKET_ACCESS",
        "ACCOUNT_ABM_INTELLIGENCE",
        "INBOUND_DIAGNOSTIC_CAPTURE",
        "EMAIL_LIFECYCLE",
        "PR_MEDIA_COMMUNITY_SPEAKING",
        "PROOF_ADVOCACY_REFERRAL",
        "PAID_MEDIA_READINESS",
        "DEEP_TECHNICAL_DEMAND",
        "MARKET_INTELLIGENCE_EXPERIMENTATION",
    }
)

CANONICAL_WORKERS = {
    "BRAND_AUTHORITY": "dealix-content",
    "WEBSITE_CONVERSION": "dealix-content",
    "SEARCH_SEO_AEO": "dealix-content",
    "FOUNDER_THOUGHT_LEADERSHIP": "dealix-content",
    "COMPANY_SOCIAL_VIDEO": "dealix-content",
    "EVENT_FIELD_INTELLIGENCE": "dealix-sales",
    "PARTNER_MARKET_ACCESS": "dealix-sales",
    "ACCOUNT_ABM_INTELLIGENCE": "dealix-sales",
    "INBOUND_DIAGNOSTIC_CAPTURE": "dealix-sales",
    "EMAIL_LIFECYCLE": "dealix-sales",
    "PR_MEDIA_COMMUNITY_SPEAKING": "dealix-content",
    "PROOF_ADVOCACY_REFERRAL": "dealix-delivery",
    "PAID_MEDIA_READINESS": "dealix-pm",
    "DEEP_TECHNICAL_DEMAND": "dealix-engineer",
    "MARKET_INTELLIGENCE_EXPERIMENTATION": "dealix-pm",
}

EXPERIMENT_DECISIONS = frozenset({"SCALE", "ITERATE", "STOP", "INVALID"})
CUSTOMER_PROOF_CLASSES = frozenset({"CUSTOMER_DELIVERY_PROOF", "CUSTOMER_OUTCOME_PROOF"})


def _text(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def _refs(value: Any) -> tuple[str, ...]:
    if not isinstance(value, (list, tuple, set)):
        return ()
    return tuple(sorted({_text(item) for item in value if _text(item)}))


def _parse_datetime(value: Any) -> datetime | None:
    raw = _text(value)
    if not raw:
        return None
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return None


def _fingerprint(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    )
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()[:16]


def _authority() -> dict[str, bool]:
    return dict(ZERO_AUTHORITY)


def validate_source_signal(
    signal: Mapping[str, Any],
    *,
    as_of: str | None = None,
) -> list[str]:
    """Validate the minimum source-bound receipt required by this layer.

    A valid receipt is still research only. The function intentionally does not
    infer a relationship, consent, purchase probability or customer outcome.
    """

    errors: list[str] = []
    for field in ("signal_id", "source_id", "source_ref", "provenance_ref", "fresh_until"):
        if not _text(signal.get(field)):
            errors.append(f"MISSING_{field.upper()}")

    evidence_refs = _refs(signal.get("evidence_refs"))
    if not evidence_refs:
        errors.append("MISSING_EVIDENCE_REFS")

    facts = _refs(signal.get("facts"))
    if not facts:
        errors.append("MISSING_SOURCE_BOUND_FACTS")

    for field in ("inferences", "unknowns"):
        if not isinstance(signal.get(field), list):
            errors.append(f"{field.upper()}_MUST_BE_LIST")

    authority = signal.get("authority")
    if not isinstance(authority, Mapping):
        errors.append("MISSING_AUTHORITY_OBJECT")
    elif any(value is not False for value in authority.values()):
        errors.append("SOURCE_RECEIPT_AUTHORITY_MUST_BE_ZERO")

    expiry = _parse_datetime(signal.get("fresh_until"))
    if expiry is None:
        errors.append("INVALID_FRESH_UNTIL")
    if as_of:
        observed_at = _parse_datetime(as_of)
        if observed_at is None:
            errors.append("INVALID_AS_OF")
        elif expiry is not None and expiry <= observed_at:
            errors.append("STALE_SIGNAL")

    return sorted(set(errors))


def build_content_opportunity(
    signal: Mapping[str, Any],
    *,
    thesis: str,
    buyer_question: str,
    audience: str,
    buying_stage: str,
    asset_type: str,
    channels: list[str] | tuple[str, ...],
    cta: str,
    downstream_event: str,
    as_of: str | None = None,
) -> dict[str, Any]:
    """Create a source-bound, draft-only ContentOpportunity.

    The thesis is explicitly a hypothesis until factual, brand, claim and
    channel QA pass. The function never creates a publish or send action.
    """

    errors = validate_source_signal(signal, as_of=as_of)
    required_text = {
        "thesis": thesis,
        "buyer_question": buyer_question,
        "audience": audience,
        "buying_stage": buying_stage,
        "asset_type": asset_type,
        "cta": cta,
        "downstream_event": downstream_event,
    }
    errors.extend(
        f"MISSING_{field.upper()}"
        for field, value in required_text.items()
        if not _text(value)
    )
    channel_values = _refs(channels)
    if not channel_values:
        errors.append("MISSING_CHANNELS")

    base = {
        "source_signal_id": _text(signal.get("signal_id")),
        "source_evidence_refs": list(_refs(signal.get("evidence_refs"))),
        "provenance_ref": _text(signal.get("provenance_ref")),
        "thesis": _text(thesis),
        "buyer_question": _text(buyer_question),
        "audience": _text(audience),
        "buying_stage": _text(buying_stage),
        "asset_type": _text(asset_type),
        "channels": list(channel_values),
        "cta": _text(cta),
        "downstream_event": _text(downstream_event),
    }
    opportunity_id = f"content-{_fingerprint(base)}"

    if errors:
        return {
            "opportunity_id": opportunity_id,
            "status": "BLOCKED",
            "errors": sorted(set(errors)),
            "authority": _authority(),
        }

    return {
        "opportunity_id": opportunity_id,
        "status": "DRAFT_REVIEW_ONLY",
        "arm": "SEARCH_SEO_AEO",
        "owner": "dealix-content",
        "source_signal_id": base["source_signal_id"],
        "source_evidence_refs": base["source_evidence_refs"],
        "provenance_ref": base["provenance_ref"],
        "thesis": base["thesis"],
        "thesis_semantics": "HYPOTHESIS_UNTIL_FACT_AND_CLAIM_QA",
        "buyer_question": base["buyer_question"],
        "audience": base["audience"],
        "buying_stage": base["buying_stage"],
        "asset_type": base["asset_type"],
        "channels": base["channels"],
        "cta": base["cta"],
        "downstream_event": base["downstream_event"],
        "claim_status": "NEEDS_FACT_BRAND_COMMERCIAL_AND_CHANNEL_QA",
        "attribution_required": True,
        "lifecycle": "DRAFT_REVIEW_ONLY",
        "external_send": False,
        "public_publish": False,
        "authority": _authority(),
    }


def evaluate_proof_reuse(proof: Mapping[str, Any]) -> dict[str, Any]:
    """Gate reuse of a customer proof candidate without publishing it.

    Reuse is ready only when customer validation, limitations, evidence,
    permission and supplied claim units are all present. Claim text is never
    generated or strengthened by this function.
    """

    errors: list[str] = []
    proof_id = _text(proof.get("proof_id"))
    proof_class = _text(proof.get("proof_class")).upper()
    evidence_refs = _refs(proof.get("evidence_refs"))
    limitations = _refs(proof.get("limitations"))
    permission_ref = _text(proof.get("permission_ref"))
    permission_state = _text(proof.get("permission_state")).upper()
    customer_validation_ref = _text(proof.get("customer_validation_ref"))
    claim_units = proof.get("claim_units")

    if not proof_id:
        errors.append("MISSING_PROOF_ID")
    if proof_class not in CUSTOMER_PROOF_CLASSES:
        errors.append("PROOF_CLASS_NOT_CUSTOMER_VALIDATED")
    if not evidence_refs:
        errors.append("MISSING_PROOF_EVIDENCE_REFS")
    if not limitations:
        errors.append("MISSING_LIMITATIONS")
    if not customer_validation_ref:
        errors.append("MISSING_CUSTOMER_VALIDATION_REF")
    if permission_state != "PERMISSIONED" or not permission_ref:
        errors.append("MISSING_RECORDED_PERMISSION")
    if not isinstance(claim_units, list) or not claim_units:
        errors.append("MISSING_CLAIM_UNITS")
    else:
        for index, unit in enumerate(claim_units):
            if not isinstance(unit, Mapping):
                errors.append(f"CLAIM_UNIT_{index}_MUST_BE_OBJECT")
                continue
            if not _text(unit.get("claim_id")) or not _text(unit.get("claim")):
                errors.append(f"CLAIM_UNIT_{index}_MISSING_ID_OR_VERBATIM_CLAIM")

    result = {
        "proof_id": proof_id,
        "proof_class": proof_class,
        "evidence_refs": list(evidence_refs),
        "permission_ref": permission_ref,
        "customer_validation_ref": customer_validation_ref,
        "authority": _authority(),
        "public_customer_proof": False,
        "publication_status": "DRAFT_ONLY",
    }
    if errors:
        result.update(
            {
                "status": "BLOCKED",
                "errors": sorted(set(errors)),
                "reuse_destinations": [],
            }
        )
        return result

    result.update(
        {
            "status": "REUSE_READY_PENDING_CHANNEL_APPROVAL",
            "errors": [],
            "limitations": list(limitations),
            "claim_units": claim_units,
            "reuse_destinations": [
                "sales_enablement_draft",
                "search_asset_draft",
                "content_asset_draft",
                "partner_enablement_draft",
                "referral_draft",
            ],
        }
    )
    return result


def score_portfolio_item(item: Mapping[str, Any]) -> dict[str, Any]:
    """Score one internal allocation candidate.

    This is an attention score only. It is never a purchase probability or a
    commercial qualification decision.
    """

    errors: list[str] = []
    item_id = _text(item.get("item_id"))
    arm = _text(item.get("arm")).upper()
    if not item_id:
        errors.append("MISSING_ITEM_ID")
    if arm not in GROWTH_ARMS:
        errors.append("UNKNOWN_GROWTH_ARM")
    if "purchase_probability" in item:
        errors.append("PURCHASE_PROBABILITY_NOT_ALLOWED")

    numeric_fields = (
        "expected_verified_movement",
        "evidence",
        "urgency",
        "reuse",
        "founder_minutes",
        "agent_tool_cost",
        "risk",
        "capacity",
    )
    values: dict[str, float] = {}
    for field in numeric_fields:
        value = item.get(field)
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            errors.append(f"{field.upper()}_MUST_BE_NUMERIC")
            continue
        values[field] = float(value)

    for field in ("expected_verified_movement", "evidence", "urgency", "reuse"):
        if field in values and not 0.0 <= values[field] <= 1.0:
            errors.append(f"{field.upper()}_OUT_OF_RANGE")
    for field in ("founder_minutes", "agent_tool_cost", "capacity"):
        if field in values and values[field] <= 0:
            errors.append(f"{field.upper()}_MUST_BE_POSITIVE")
    if "risk" in values and not 0.0 <= values["risk"] <= 1.0:
        errors.append("RISK_OUT_OF_RANGE")

    base = {
        "item_id": item_id,
        "arm": arm,
        "worker": CANONICAL_WORKERS.get(arm),
        "authority": _authority(),
    }
    if errors:
        base.update({"status": "BLOCKED", "errors": sorted(set(errors))})
        return base

    denominator_risk = max(values["risk"], 0.1)
    denominator_cost = max(values["agent_tool_cost"], 0.01)
    score = (
        values["expected_verified_movement"]
        * values["evidence"]
        * values["urgency"]
        * values["reuse"]
        / values["founder_minutes"]
        / denominator_cost
        / denominator_risk
        / values["capacity"]
    )
    base.update(
        {
            "status": "INTERNAL_PRIORITY_ONLY",
            "allocation_score": round(score, 12),
            "priority_semantics": (
                "INTERNAL_PRIORITY_ONLY_NOT_PURCHASE_PROBABILITY"
            ),
            "inputs": values,
            "next_action": _text(item.get("next_action"))
            or "PREPARE_NEXT_EVIDENCE_WITHIN_CANONICAL_WORKLOAD",
        }
    )
    return base


def allocate_portfolio(items: list[Mapping[str, Any]], *, limit: int = 5) -> dict[str, Any]:
    """Return the highest-scoring bounded internal work queue."""

    if not isinstance(limit, int) or isinstance(limit, bool) or not 1 <= limit <= 5:
        raise ValueError("limit must be an integer between 1 and 5")

    accepted: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    for item in items:
        scored = score_portfolio_item(item)
        if scored["status"] == "BLOCKED":
            rejected.append(scored)
        else:
            accepted.append(scored)

    accepted.sort(key=lambda row: (-row["allocation_score"], row["item_id"]))
    return {
        "status": "READ_ONLY",
        "limit": limit,
        "items": accepted[:limit],
        "overflow_count": max(0, len(accepted) - limit),
        "rejected": rejected,
        "authority": _authority(),
    }


def validate_experiment(experiment: Mapping[str, Any]) -> list[str]:
    """Validate one SCALE/ITERATE/STOP/INVALID decision without storing it."""

    errors: list[str] = []
    if not _text(experiment.get("experiment_id")):
        errors.append("MISSING_EXPERIMENT_ID")
    if not _text(experiment.get("hypothesis")):
        errors.append("MISSING_HYPOTHESIS")

    decision = _text(experiment.get("decision")).upper()
    if decision not in EXPERIMENT_DECISIONS:
        errors.append("INVALID_OR_MISSING_DECISION")

    evidence_refs = _refs(experiment.get("outcome_evidence_refs"))
    if decision in {"SCALE", "ITERATE", "STOP"} and not evidence_refs:
        errors.append("DECISION_REQUIRES_OUTCOME_EVIDENCE")
    if decision == "SCALE":
        if experiment.get("verified_outcome") is not True:
            errors.append("SCALE_REQUIRES_VERIFIED_OUTCOME")
        if experiment.get("vanity_metrics_only") is True:
            errors.append("VANITY_ONLY_EXPERIMENT_CANNOT_SCALE")

    return sorted(set(errors))


def route_workload(arm: str) -> dict[str, Any]:
    """Map an arm to an existing canonical worker, never a new agent."""

    normalized = _text(arm).upper()
    if normalized not in GROWTH_ARMS:
        return {
            "arm": normalized,
            "status": "BLOCKED",
            "errors": ["UNKNOWN_GROWTH_ARM"],
            "authority": _authority(),
        }
    return {
        "arm": normalized,
        "status": "INTERNAL_WORKLOAD",
        "worker": CANONICAL_WORKERS[normalized],
        "new_permanent_agent": False,
        "new_scheduler": False,
        "authority": _authority(),
    }


__all__ = [
    "AUTHORITY_KEYS",
    "CANONICAL_WORKERS",
    "CUSTOMER_PROOF_CLASSES",
    "EXPERIMENT_DECISIONS",
    "GROWTH_ARMS",
    "UNKNOWN",
    "ZERO_AUTHORITY",
    "allocate_portfolio",
    "build_content_opportunity",
    "evaluate_proof_reuse",
    "route_workload",
    "score_portfolio_item",
    "validate_experiment",
    "validate_source_signal",
]
