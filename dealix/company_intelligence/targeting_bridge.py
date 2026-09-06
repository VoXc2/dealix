"""Bridge canonical Company Intelligence signals into Targeting V1 dossiers.

This module deliberately reuses the existing Company Intelligence signal spine.
It does not create a second signal store, Opportunity Graph, CRM, scheduler, or
external-action authority.

Operational detectors should first pass through ``normalize_signal`` into a
``CanonicalSignal``. Targeting then binds each canonical signal to an explicit
evidence tier and combines it with commercial hypotheses supplied by the
canonical commercial owner.

Important fail-closed properties:
- evidence tier is explicit; it is never inferred from a URL or provider name;
- withdrawn-consent signals are not usable as targeting evidence;
- mixed signal families require an explicit family choice from the caller;
- high target value still does not grant channel execution authority.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from dealix.company_intelligence.signal_contracts import (
    CanonicalSignal,
    ConsentStatus as SignalConsentStatus,
    SignalType,
)
from dealix.company_intelligence.targeting import (
    Actionability,
    EvidenceItem,
    EvidenceTier,
    SignalFamily,
    TargetDossier,
    TargetValueFeatures,
    evidence_expiry,
)


@dataclass(frozen=True)
class TargetingSignalBinding:
    """One canonical signal plus its explicitly classified evidence tier."""

    signal: CanonicalSignal
    evidence_tier: EvidenceTier


@dataclass(frozen=True)
class TargetingDossierContext:
    """Commercial context that signals alone cannot truthfully infer."""

    company_name: str
    canonical_domain: str
    why_them: str
    why_now: str
    problem_hypothesis: str
    business_cost_hypothesis: str
    offer_route: str
    proof_baseline: str
    features: TargetValueFeatures
    actionability: Actionability
    active_thread_or_opportunity: bool = False


_SIGNAL_FAMILY_BY_CANONICAL_TYPE: dict[SignalType, SignalFamily] = {
    SignalType.CUSTOMER: SignalFamily.CUSTOMER_EXPERIENCE_PRESSURE,
    SignalType.PARTNER: SignalFamily.PARTNER_FIT,
    SignalType.PRODUCT: SignalFamily.GROWTH_TRANSITION,
    SignalType.MARKET: SignalFamily.GROWTH_TRANSITION,
    SignalType.RISK: SignalFamily.GOVERNANCE_PROOF_PRESSURE,
    SignalType.MONEY: SignalFamily.REVENUE_LEAKAGE,
    SignalType.TRAINING: SignalFamily.GROWTH_TRANSITION,
    SignalType.VENTURE: SignalFamily.GROWTH_TRANSITION,
    SignalType.API: SignalFamily.TECHNOLOGY_TRANSITION,
    SignalType.TRUST: SignalFamily.GOVERNANCE_PROOF_PRESSURE,
    SignalType.REGULATORY: SignalFamily.GOVERNANCE_PROOF_PRESSURE,
    SignalType.COMPETITIVE: SignalFamily.GROWTH_TRANSITION,
    SignalType.ECONOMIC: SignalFamily.GROWTH_TRANSITION,
    SignalType.TECH_ADOPTION: SignalFamily.TECHNOLOGY_TRANSITION,
}


def suggested_signal_family(signal_type: SignalType) -> SignalFamily:
    """Return the bounded Targeting V1 family for a canonical signal type.

    ``PERSONAL`` is intentionally unsupported because personal-context signals
    must not silently enter B2B targeting. Callers must use a business signal.
    """

    try:
        return _SIGNAL_FAMILY_BY_CANONICAL_TYPE[signal_type]
    except KeyError as exc:
        raise ValueError(
            f"canonical signal type {signal_type.value!r} is not eligible for B2B targeting"
        ) from exc


def evidence_from_canonical_signal(
    binding: TargetingSignalBinding,
) -> EvidenceItem:
    """Convert canonical signal truth into Targeting V1 evidence."""

    signal = binding.signal
    if signal.consent_status == SignalConsentStatus.WITHDRAWN:
        raise ValueError("withdrawn-consent signal cannot be used as targeting evidence")
    if not signal.claim.strip():
        raise ValueError("canonical signal must contain a non-empty claim")

    expires_at = signal.expires_at or evidence_expiry(
        observed_at=signal.observed_at,
        tier=binding.evidence_tier,
    )
    return EvidenceItem(
        source_id=signal.source_id,
        source_url=signal.evidence_ref,
        tier=binding.evidence_tier,
        observed_at=signal.observed_at,
        expires_at=expires_at,
        claim=signal.claim,
        confidence=signal.confidence,
    )


def build_target_dossier_from_canonical_signals(
    bindings: Iterable[TargetingSignalBinding],
    *,
    context: TargetingDossierContext,
    signal_family: SignalFamily | None = None,
) -> TargetDossier:
    """Build one evidence-first targeting dossier from canonical graph signals.

    Signal evidence can establish *what changed*. The caller must still provide
    the commercial hypothesis, proof baseline, relationship/consent state, and
    target-value features. This prevents research from fabricating commercial
    truth or action authority.
    """

    material = tuple(bindings)
    if not material:
        raise ValueError("at least one canonical signal binding is required")

    company_ids = {binding.signal.company_id for binding in material}
    if len(company_ids) != 1:
        raise ValueError("all targeting signals must belong to one canonical company")
    company_id = next(iter(company_ids))

    evidence = tuple(evidence_from_canonical_signal(binding) for binding in material)

    if signal_family is None:
        families = {
            suggested_signal_family(binding.signal.signal_type)
            for binding in material
        }
        if len(families) != 1:
            raise ValueError(
                "mixed canonical signal families require an explicit targeting signal_family"
            )
        signal_family = next(iter(families))

    return TargetDossier(
        company_id=company_id,
        company_name=context.company_name,
        canonical_domain=context.canonical_domain,
        signal_family=signal_family,
        why_them=context.why_them,
        why_now=context.why_now,
        problem_hypothesis=context.problem_hypothesis,
        business_cost_hypothesis=context.business_cost_hypothesis,
        offer_route=context.offer_route,
        proof_baseline=context.proof_baseline,
        evidence=evidence,
        features=context.features,
        actionability=context.actionability,
        active_thread_or_opportunity=context.active_thread_or_opportunity,
    )
