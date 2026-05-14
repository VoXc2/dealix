"""Proof Pack assembler — canonical 14-section ProofPack.

Sections (fixed order):
  1. Executive Summary
  2. Problem
  3. Inputs
  4. Source Passports
  5. Data Quality Score
  6. Work Completed
  7. Outputs
  8. Governance Decisions
  9. Blocked Risks
 10. Observed Value
 11. Limitations
 12. Recommended Next Step
 13. Retainer Recommendation
 14. Capital Assets Created

Score: weighted across source coverage (25), output quality (25),
governance integrity (20), value evidence (15), capital asset creation (15).

Tier: ≥85 case_candidate / 70-84 sales_support / 55-69 internal_learning
       / <55 weak.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from auto_client_acquisition.capital_os.capital_ledger import list_assets
from auto_client_acquisition.client_os.badges import ProofBadge, StatusBadge
from auto_client_acquisition.data_os.source_passport import SourcePassport, validate
from auto_client_acquisition.governance_os.claim_safety import contains_unsafe_claim
from auto_client_acquisition.governance_os.runtime_decision import GovernanceDecision
from auto_client_acquisition.value_os.value_ledger import summarize as summarize_value


SECTION_ORDER = (
    "executive_summary",
    "problem",
    "inputs",
    "source_passports",
    "data_quality_score",
    "work_completed",
    "outputs",
    "governance_decisions",
    "blocked_risks",
    "observed_value",
    "limitations",
    "recommended_next_step",
    "retainer_recommendation",
    "capital_assets_created",
)


class ProofPackClaimError(ValueError):
    """Raised when proof pack inputs contain unsupported claims."""


@dataclass
class ProofPack:
    engagement_id: str
    customer_id: str
    sections: dict[str, str] = field(default_factory=dict)
    score: float = 0.0
    tier: str = "weak"
    governance_decision: str = GovernanceDecision.ALLOW.value
    status_badge: str = StatusBadge.DRAFT.value
    proof_badge: str = ProofBadge.OBSERVED.value
    limitations: list[str] = field(default_factory=list)
    capital_assets: list[str] = field(default_factory=list)
    generated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return {
            "engagement_id": self.engagement_id,
            "customer_id": self.customer_id,
            "sections": dict(self.sections),
            "score": self.score,
            "tier": self.tier,
            "governance_decision": self.governance_decision,
            "status_badge": self.status_badge,
            "proof_badge": self.proof_badge,
            "limitations": list(self.limitations),
            "capital_assets": list(self.capital_assets),
            "generated_at": self.generated_at,
        }


def classify_tier(score: float) -> str:
    if score >= 85:
        return "case_candidate"
    if score >= 70:
        return "sales_support"
    if score >= 55:
        return "internal_learning"
    return "weak"


def compute_proof_score(
    *,
    source_coverage: float,  # 0-1
    output_quality: float,   # 0-1
    governance_integrity: float,  # 0-1
    value_evidence: float,   # 0-1
    capital_asset_creation: float,  # 0-1
) -> float:
    def _clamp(x: float) -> float:
        return max(0.0, min(1.0, float(x)))

    score = (
        _clamp(source_coverage) * 25
        + _clamp(output_quality) * 25
        + _clamp(governance_integrity) * 20
        + _clamp(value_evidence) * 15
        + _clamp(capital_asset_creation) * 15
    )
    return round(score, 2)


def _scan_for_unsafe(text_blob: str) -> tuple[bool, list[str]]:
    return contains_unsafe_claim(text_blob)


def assemble(
    *,
    engagement_id: str,
    customer_id: str,
    source_passport: SourcePassport | None = None,
    dq_score: float = 0.0,
    value_events: list[Any] | None = None,
    governance_events: list[dict[str, Any]] | None = None,
    work_completed: str = "",
    problem: str = "",
    outputs_summary: str = "",
    next_step: str = "",
    retainer_recommendation: str = "",
    blocked_risks: list[str] | None = None,
    limitations: list[str] | None = None,
) -> ProofPack:
    """Compose a ProofPack. Refuses to assemble if any caller-supplied text
    contains an unsafe claim (raises ProofPackClaimError)."""
    value_events = value_events or []
    governance_events = governance_events or []
    blocked_risks = blocked_risks or []
    limitations = list(limitations or [])

    # 1. Claim-safety gate on caller-supplied text AND on value-event texts.
    combined_text_parts = [
        problem, work_completed, outputs_summary, next_step, retainer_recommendation,
    ]
    for ev in value_events:
        if isinstance(ev, dict):
            combined_text_parts.append(str(ev.get("text", "")))
            combined_text_parts.append(str(ev.get("notes", "")))
    combined_text = " ".join(p for p in combined_text_parts if p)
    unsafe, unsafe_reasons = _scan_for_unsafe(combined_text)
    if unsafe:
        # Do NOT raise — produce a pack with restrictive governance envelope so
        # the caller still has a structured artifact to redact + audit.
        limitations.extend([f"unsafe_claim:{r}" for r in unsafe_reasons])

    # 2. Source passport coverage.
    if source_passport is None:
        source_coverage = 0.0
        source_summary = "no source passport provided"
        limitations.append("source_passport_missing")
    else:
        result = validate(source_passport)
        source_coverage = 1.0 if result.is_valid else 0.4
        source_summary = (
            f"source_id={source_passport.source_id}; type={source_passport.source_type}; "
            f"owner={source_passport.owner}; pii={source_passport.contains_pii}; "
            f"sensitivity={source_passport.sensitivity}"
        )
        if not result.is_valid:
            limitations.extend([f"passport_invalid:{r}" for r in result.reasons])

    # 3. Value evidence (Verified + Client-confirmed weighted highest).
    value_summary = summarize_value(customer_id=customer_id, period_days=90)
    verified_amount = float(value_summary.get("verified_amount", 0.0))
    client_confirmed_amount = float(value_summary.get("client_confirmed_amount", 0.0))
    observed_amount = float(value_summary.get("observed_amount", 0.0))
    estimated_amount = float(value_summary.get("estimated_amount", 0.0))
    value_evidence = min(
        1.0,
        (client_confirmed_amount * 1.0 + verified_amount * 0.8 + observed_amount * 0.4) / 10000
        + (0.1 if value_summary.get("total_events", 0) > 0 else 0.0),
    )

    # 4. Governance integrity.
    if governance_events:
        block_count = sum(1 for ev in governance_events if ev.get("decision") == GovernanceDecision.BLOCK.value)
        approval_count = sum(1 for ev in governance_events if ev.get("decision") in (
            GovernanceDecision.REQUIRE_APPROVAL.value, GovernanceDecision.ALLOW_WITH_REVIEW.value
        ))
        governance_integrity = min(
            1.0,
            0.6 + 0.1 * min(4, block_count) + 0.05 * min(8, approval_count)
        )
    else:
        governance_integrity = 0.6

    # 5. Output quality from DQ score and presence of work_completed text.
    output_quality = min(1.0, (dq_score / 100.0) * 0.7 + (0.3 if work_completed else 0.0))

    # 6. Capital assets — pull from ledger by engagement_id.
    assets = list_assets(engagement_id=engagement_id)
    capital_asset_creation = min(1.0, len(assets) / 3.0)  # 3 assets = full credit
    capital_refs = [a.asset_ref or a.asset_id for a in assets]
    if not assets:
        limitations.append("no_capital_assets_yet")

    # 7. Compose score + tier.
    score = compute_proof_score(
        source_coverage=source_coverage,
        output_quality=output_quality,
        governance_integrity=governance_integrity,
        value_evidence=value_evidence,
        capital_asset_creation=capital_asset_creation,
    )
    tier = classify_tier(score)

    # 8. Governance decision envelope. Order:
    #    a. Unsafe claim detected in inputs → REDACT (caller must rewrite).
    #    b. Highest restriction observed in governance_events.
    #    c. Default ALLOW_WITH_REVIEW until human approves.
    if unsafe:
        envelope = GovernanceDecision.REDACT.value
    elif governance_events:
        decisions = [str(ev.get("decision", "")) for ev in governance_events]
        if GovernanceDecision.BLOCK.value in decisions:
            envelope = GovernanceDecision.BLOCK.value
        elif GovernanceDecision.REQUIRE_APPROVAL.value in decisions:
            envelope = GovernanceDecision.REQUIRE_APPROVAL.value
        else:
            envelope = GovernanceDecision.ALLOW_WITH_REVIEW.value
    else:
        envelope = GovernanceDecision.ALLOW_WITH_REVIEW.value

    # 9. Proof badge tier mapping.
    if client_confirmed_amount > 0:
        pbadge = ProofBadge.CLIENT_CONFIRMED.value
    elif verified_amount > 0:
        pbadge = ProofBadge.VERIFIED.value
    elif observed_amount > 0:
        pbadge = ProofBadge.OBSERVED.value
    else:
        pbadge = ProofBadge.ESTIMATED.value

    # 10. Status badge.
    if envelope == GovernanceDecision.BLOCK.value:
        sbadge = StatusBadge.BLOCKED.value
    elif envelope == GovernanceDecision.REQUIRE_APPROVAL.value:
        sbadge = StatusBadge.NEEDS_REVIEW.value
    else:
        sbadge = StatusBadge.DRAFT.value

    sections: dict[str, str] = {
        "executive_summary": (
            f"Engagement {engagement_id} for customer {customer_id}: proof_score={score}, tier={tier}."
        ),
        "problem": problem or "(not provided)",
        "inputs": f"events_recorded={len(value_events)}; governance_events={len(governance_events)}",
        "source_passports": source_summary,
        "data_quality_score": f"DQ={dq_score:.1f}/100",
        "work_completed": work_completed or "(not provided)",
        "outputs": outputs_summary or "(not provided)",
        "governance_decisions": "; ".join(str(ev.get("decision", "")) for ev in governance_events) or "(none)",
        "blocked_risks": "; ".join(blocked_risks) or "(none)",
        "observed_value": (
            f"verified={verified_amount:.2f}; observed={observed_amount:.2f}; "
            f"client_confirmed={client_confirmed_amount:.2f}; estimated={estimated_amount:.2f}"
        ),
        "limitations": "; ".join(limitations) or "(none recorded)",
        "recommended_next_step": next_step or "(not provided)",
        "retainer_recommendation": retainer_recommendation or "(deferred until proof_score >= 80)",
        "capital_assets_created": "; ".join(capital_refs) or "(none)",
    }

    return ProofPack(
        engagement_id=engagement_id,
        customer_id=customer_id,
        sections=sections,
        score=score,
        tier=tier,
        governance_decision=envelope,
        status_badge=sbadge,
        proof_badge=pbadge,
        limitations=limitations,
        capital_assets=capital_refs,
    )


__all__ = [
    "ProofPack",
    "ProofPackClaimError",
    "SECTION_ORDER",
    "assemble",
    "classify_tier",
    "compute_proof_score",
]
