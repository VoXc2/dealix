"""Business unit charter schema for Dealix Group."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class BusinessUnitCharter:
    name: str
    problem_statement: str
    buyer_persona: str
    primary_offer: str
    recurring_offer: str
    product_modules: list[str] = field(default_factory=list)
    proof_type: str = ""

    kpis: list[str] = field(default_factory=list)
    playbook_ref: str = ""
    risk_profile: str = ""
    owner: str = ""
    venture_readiness_score: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)
