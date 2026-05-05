"""Pure composition: BuildRequest -> CompanyBrainV6."""
from __future__ import annotations

from auto_client_acquisition.company_brain_v6.next_best_action import next_best_action
from auto_client_acquisition.company_brain_v6.risk_profile import compute_risk_profile
from auto_client_acquisition.company_brain_v6.schemas import (
    FORBIDDEN_CHANNELS,
    BuildRequest,
    CompanyBrainV6,
)
from auto_client_acquisition.company_brain_v6.service_matcher import recommend_service


_OFFER_TEMPLATES: dict[str, str] = {
    "b2b_services": "B2B services tailored for KSA mid-market.",
    "b2b_saas": "B2B SaaS platform for Saudi operators.",
    "agency": "Agency services with measurable proof of delivery.",
    "training_consulting": "Training and consulting engagements.",
    "local_services": "Local services for KSA customers.",
    "ecommerce_b2c": "Direct-to-consumer ecommerce in KSA.",
    "real_estate": "Real-estate offerings tuned for KSA buyers.",
    "healthcare_clinic": "Clinic services with PDPL-compliant intake.",
    "enterprise": "Enterprise solutions with executive review cadence.",
}


def _normalize_channels(values: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for v in values or []:
        s = str(v).strip()
        if not s or s in seen:
            continue
        seen.add(s)
        out.append(s)
    return out


def _enforce_blocked(allowed: list[str], blocked: list[str]) -> tuple[list[str], list[str]]:
    blocked_set = set(blocked)
    for ch in FORBIDDEN_CHANNELS:
        blocked_set.add(ch)
    # User cannot remove a forbidden channel from blocked by listing it allowed.
    allowed_clean = [a for a in allowed if a not in blocked_set]
    blocked_out: list[str] = []
    seen: set[str] = set()
    for v in [*blocked, *FORBIDDEN_CHANNELS]:
        if v in seen:
            continue
        seen.add(v)
        blocked_out.append(v)
    return allowed_clean, blocked_out


def build_company_brain_v6(req: BuildRequest) -> CompanyBrainV6:
    """Compose a per-customer brain from the request.

    Pure composition; no LLM, no network. Always enforces the three
    forbidden channels in ``blocked_channels`` regardless of input.
    """
    current = _normalize_channels(req.current_channels)
    allowed_in = _normalize_channels(req.allowed_channels)
    blocked_in = _normalize_channels(req.blocked_channels)
    allowed, blocked = _enforce_blocked(allowed_in, blocked_in)

    offer = _OFFER_TEMPLATES.get(
        req.sector,
        f"Offer for {req.sector} in {req.region} — to be detailed.",
    )
    icp = (
        f"Decision-makers in {req.sector} based in {req.region} "
        "with budget authority and a clear pain to solve."
    )

    brain = CompanyBrainV6(
        company_handle=req.company_handle,
        sector=req.sector,
        region=req.region,
        offer=offer,
        icp=icp,
        current_channels=current,
        allowed_channels=allowed,
        blocked_channels=blocked,
        tone_preference=req.tone_preference,
        language_preference=req.language_preference,
        pain_points=list(req.pain_points or []),
        growth_goal=req.growth_goal,
        evidence_ids=[f"req:{req.company_handle}"],
    )
    brain.service_recommendation = recommend_service(brain)
    brain.risk_profile = compute_risk_profile(brain)
    brain.next_best_action = next_best_action(brain)
    return brain
