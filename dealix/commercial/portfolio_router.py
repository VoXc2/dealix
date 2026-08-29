"""Deterministic demand-to-package routing over canonical Dealix truth.

Routing is an internal recommendation. It cannot create a relationship, consent,
offer, price, quote, send, payment, deployment, or production authority.
"""

from __future__ import annotations

import hashlib
import json
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

UNKNOWN = "UNKNOWN_NOT_EVIDENCE_BACKED"


class EntryPackage(StrEnum):
    REVENUE_COMMAND = "REVENUE_COMMAND_PILOT"
    COMPANY_BRAIN = "COMPANY_BRAIN_GOVERNED_AI_SPRINT"
    SAUDI_MARKET_ACCESS = "SAUDI_MARKET_ACCESS_SPRINT"
    PARTNER_LAYER = "PARTNER_IMPLEMENTATION_PROOF_LAYER"
    DIAGNOSTIC_DISCOVERY = "FREE_MINI_DIAGNOSTIC_THEN_QUALIFIED_DISCOVERY"
    RESEARCH_NURTURE_SUPPRESS = "RESEARCH_NURTURE_OR_SUPPRESS"


class DemandSignal(BaseModel):
    model_config = ConfigDict(extra="forbid")

    signal_id: str = Field(..., min_length=1)
    company_name: str = Field(..., min_length=1)
    source_ref: str = ""
    observed_at: str = Field(..., min_length=1)
    evidence_refs: list[str] = Field(default_factory=list)
    real_interaction_ref: str = ""
    explicit_inbound_ref: str = ""
    consent_state: str = "UNKNOWN"
    problem_statement: str = ""
    problem_tags: list[str] = Field(default_factory=list)
    requested_capabilities: list[str] = Field(default_factory=list)
    partner_intent: bool = False
    ksa_market_entry_intent: bool = False
    urgency: str = "UNKNOWN"
    economic_relevance: str = "UNKNOWN"
    risk_class: str = "STANDARD"


class PackageRouteDecision(BaseModel):
    model_config = ConfigDict(extra="forbid")

    decision_id: str
    signal_id: str
    recommended_package: EntryPackage
    reason_codes: list[str]
    evidence_refs: list[str]
    relationship_state: str
    consent_state: str
    confidence: str
    missing_evidence: list[str]
    next_action: str
    owner: str
    sla_minutes: int
    authority: dict[str, bool]
    status: str = "INTERNAL_ROUTING_RECOMMENDATION"

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")


class PortfolioPackageRouter:
    """Route legitimate demand without granting commercial or external authority."""

    _TECH = {
        "ai", "agent", "agents", "automation", "company_brain", "knowledge",
        "rag", "workflow", "integration", "technical_capability", "copilot",
    }
    _REVENUE = {
        "revenue", "sales", "crm", "follow_up", "pipeline", "quote",
        "handoff", "lead", "conversion", "renewal", "proposal",
    }

    @staticmethod
    def _normalized(values: list[str]) -> set[str]:
        return {value.strip().lower().replace(" ", "_") for value in values if value.strip()}

    def route(self, signal: DemandSignal) -> PackageRouteDecision:
        refs = sorted({
            *[ref.strip() for ref in signal.evidence_refs if ref.strip()],
            *([signal.source_ref.strip()] if signal.source_ref.strip() else []),
            *([signal.real_interaction_ref.strip()] if signal.real_interaction_ref.strip() else []),
            *([signal.explicit_inbound_ref.strip()] if signal.explicit_inbound_ref.strip() else []),
        })
        relationship_verified = bool(signal.real_interaction_ref.strip() or signal.explicit_inbound_ref.strip())
        relationship_state = "VERIFIED_RELATIONSHIP" if relationship_verified else UNKNOWN
        consent = signal.consent_state.strip().upper()
        if consent not in {"CONSENTED", "OPTED_OUT", "SUPPRESSED", "EXPIRED", "UNKNOWN"}:
            consent = UNKNOWN

        tags = self._normalized(signal.problem_tags + signal.requested_capabilities)
        statement = signal.problem_statement.lower()
        reasons: list[str] = []
        missing: list[str] = []

        if not refs and not relationship_verified:
            package = EntryPackage.RESEARCH_NURTURE_SUPPRESS
            reasons.append("NO_SOURCE_LINKED_EVIDENCE_OR_RELATIONSHIP")
            next_action = "CAPTURE_SOURCE_AND_REAL_INTERACTION_OR_EXPLICIT_INBOUND"
            owner = "market_intelligence"
            confidence = "HIGH"
        elif consent in {"OPTED_OUT", "SUPPRESSED"}:
            package = EntryPackage.RESEARCH_NURTURE_SUPPRESS
            reasons.append("CHANNEL_SUPPRESSED")
            next_action = "HONOR_SUPPRESSION_AND_KEEP_INTERNAL_RESEARCH_ONLY"
            owner = "governance"
            confidence = "HIGH"
        elif signal.partner_intent:
            package = EntryPackage.PARTNER_LAYER
            reasons.append("PARTNER_OR_IMPLEMENTATION_INTENT")
            next_action = "PREPARE_PARTNER_QUALIFICATION_PACKET"
            owner = "partner"
            confidence = "HIGH"
        elif signal.ksa_market_entry_intent:
            package = EntryPackage.SAUDI_MARKET_ACCESS
            reasons.append("KSA_MARKET_ENTRY_INTENT")
            next_action = "PREPARE_SOURCED_MARKET_ACCESS_DIAGNOSTIC"
            owner = "market_intelligence"
            confidence = "HIGH"
        elif tags & self._TECH or any(word in statement for word in ("company brain", "agent", "automation", "ذكاء اصطناعي", "أتمتة")):
            package = EntryPackage.COMPANY_BRAIN
            reasons.append("TECHNICAL_AI_OR_CONTEXT_DEMAND")
            next_action = "RUN_COMPANY_BRAIN_SPRINT_ASSESSMENT"
            owner = "diagnostic"
            confidence = "MEDIUM"
        elif tags & self._REVENUE or any(word in statement for word in ("revenue", "sales", "pipeline", "follow-up", "مبيعات", "إيراد", "متابعة")):
            package = EntryPackage.REVENUE_COMMAND
            reasons.append("REVENUE_EXECUTION_PROBLEM")
            next_action = "RUN_REVENUE_MINI_DIAGNOSTIC"
            owner = "revenue_intelligence"
            confidence = "MEDIUM"
        elif relationship_verified:
            package = EntryPackage.DIAGNOSTIC_DISCOVERY
            reasons.append("LEGITIMATE_DEMAND_REQUIRES_PROBLEM_CLARIFICATION")
            next_action = "COMPLETE_FREE_MINI_DIAGNOSTIC"
            owner = "diagnostic"
            confidence = "LOW"
        else:
            package = EntryPackage.RESEARCH_NURTURE_SUPPRESS
            reasons.append("INSUFFICIENT_EVIDENCE")
            next_action = "CAPTURE_NEXT_EVIDENCE"
            owner = "lead_acquisition"
            confidence = "LOW"

        if not refs:
            missing.append("source-linked evidence")
        if not relationship_verified:
            missing.append("real interaction or explicit inbound reference")
        if consent == "UNKNOWN":
            missing.append("channel consent state")
        if not signal.problem_statement.strip() and not tags:
            missing.append("problem statement or capability request")
        if signal.economic_relevance == "UNKNOWN":
            missing.append("economic relevance")
        if signal.urgency == "UNKNOWN":
            missing.append("urgency")

        fingerprint = json.dumps(
            {
                "signal": signal.model_dump(mode="json"),
                "package": package.value,
                "reasons": sorted(reasons),
            },
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        decision_id = hashlib.sha256(fingerprint.encode("utf-8")).hexdigest()[:16]
        return PackageRouteDecision(
            decision_id=decision_id,
            signal_id=signal.signal_id,
            recommended_package=package,
            reason_codes=sorted(reasons),
            evidence_refs=refs,
            relationship_state=relationship_state,
            consent_state=consent,
            confidence=confidence,
            missing_evidence=sorted(missing),
            next_action=next_action,
            owner=owner,
            sla_minutes=15 if relationship_verified else 240,
            authority={
                "offer": False,
                "price": False,
                "quote": False,
                "external_send": False,
                "payment": False,
                "execution": False,
                "production": False,
            },
        )


__all__ = [
    "DemandSignal",
    "EntryPackage",
    "PackageRouteDecision",
    "PortfolioPackageRouter",
    "UNKNOWN",
]
