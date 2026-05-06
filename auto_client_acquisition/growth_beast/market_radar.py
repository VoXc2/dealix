"""Market Radar — public-source signal evaluator.

V12.5 hard rule: NO HTTP fetching from this module. Signals are
caller-supplied (the founder or a manual research process feeds them).
This keeps Dealix scrape-free by construction.
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

SignalSource = Literal[
    "job_post",         # company hiring (sales/CS/growth role)
    "press",            # public press release
    "tender",           # public tender / Etimad
    "directory",        # public business directory entry
    "founder_observation",  # founder noticed in conversation/event
    "partner_referral", # partner suggested
    "inbound",          # company contacted Dealix
]

SignalType = Literal[
    "hiring_sales_team",
    "expanding_support",
    "launching_product",
    "raised_funding",
    "support_complaints",
    "weak_followup",
    "no_proof_visible",
    "needs_growth_clarity",
    "asking_about_dealix",
    "other",
]


class MarketSignal(BaseModel):
    """A single market signal. Source MUST be public or the founder's
    own observation. NEVER scraped from a closed source."""

    model_config = ConfigDict(extra="forbid")

    source_type: SignalSource
    sector_hint: str = "tbd"
    company_placeholder: str = Field(
        default="Slot-X",
        description="Placeholder only — never real company name in repo",
        max_length=80,
    )
    signal_type: SignalType
    signal_text_redacted: str = Field(max_length=300)
    confidence: float = Field(ge=0.0, le=1.0)
    why_now: str = ""
    public_only: bool = True
    contains_personal_data: bool = False
    risk_flags: list[str] = Field(default_factory=list)


def evaluate_signals(signals: list[MarketSignal]) -> dict:
    """Aggregate + flag signals.

    Returns counts by type/source + risk_flags rolled up. Pure
    function. No I/O.
    """
    if not signals:
        return {
            "total": 0,
            "by_type": {},
            "by_source": {},
            "high_confidence_count": 0,
            "personal_data_signals": 0,
            "risk_flags": [],
            "action_mode": "suggest_only",
        }
    by_type: dict[str, int] = {}
    by_source: dict[str, int] = {}
    high_conf = 0
    personal = 0
    flags: list[str] = []
    for s in signals:
        by_type[s.signal_type] = by_type.get(s.signal_type, 0) + 1
        by_source[s.source_type] = by_source.get(s.source_type, 0) + 1
        if s.confidence >= 0.7:
            high_conf += 1
        if s.contains_personal_data:
            personal += 1
            flags.append(f"PII_in_{s.source_type}")
        flags.extend(s.risk_flags)
    return {
        "total": len(signals),
        "by_type": by_type,
        "by_source": by_source,
        "high_confidence_count": high_conf,
        "personal_data_signals": personal,
        "risk_flags": list(set(flags)),
        "action_mode": "suggest_only",
    }
