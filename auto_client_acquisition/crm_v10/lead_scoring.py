"""Deterministic lead scoring — fit + urgency from Account + Lead.

No randomness. No LLM. Inputs in → identical scores out.
"""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.crm_v10.schemas import Account, Lead

CANONICAL_SAUDI_B2B_SECTORS: frozenset[str] = frozenset({
    "b2b_services",
    "b2b_saas",
    "agency",
    "logistics",
    "construction",
    "professional_services",
    "manufacturing",
    "financial_services",
    "real_estate_b2b",
    "enterprise",
})

PRIORITY_REGIONS: frozenset[str] = frozenset({
    "riyadh",
    "jeddah",
    "dammam",
})

URGENCY_TOKENS: tuple[str, ...] = ("urgent", "عاجل")


def _redact_notes(notes: str) -> str:
    """Drop anything that looks like an email/phone — surface only the
    coarse class. Notes feed into the score, never into reasons.
    """
    if not notes:
        return ""
    redacted = []
    for token in notes.split():
        if "@" in token or token.replace("+", "").replace("-", "").isdigit():
            redacted.append("[redacted]")
        else:
            redacted.append(token)
    return " ".join(redacted)


def score_lead(lead: Lead, account: Account) -> dict[str, Any]:
    """Return ``{fit_score, urgency_score, reasons}`` clamped to 0..1."""
    fit = 0.0
    urgency = 0.0
    reasons: list[str] = []

    sector = (account.sector or "").lower()
    if sector in CANONICAL_SAUDI_B2B_SECTORS:
        fit += 0.3
        reasons.append(f"sector:{sector}:+0.30")

    region = (account.region or "").lower()
    if region in PRIORITY_REGIONS:
        fit += 0.2
        reasons.append(f"region:{region}:+0.20")

    if lead.source == "warm_intro":
        fit += 0.3
        reasons.append("source:warm_intro:+0.30")

    notes_lc = (lead.notes or "").lower()
    if any(tok in notes_lc for tok in URGENCY_TOKENS):
        urgency += 0.5
        reasons.append("notes:urgency_token:+0.50")

    fit = max(0.0, min(1.0, fit))
    urgency = max(0.0, min(1.0, urgency))

    return {
        "fit_score": fit,
        "urgency_score": urgency,
        "reasons": reasons,
        "notes_redacted": _redact_notes(lead.notes),
    }


__all__ = [
    "CANONICAL_SAUDI_B2B_SECTORS",
    "PRIORITY_REGIONS",
    "URGENCY_TOKENS",
    "score_lead",
]
