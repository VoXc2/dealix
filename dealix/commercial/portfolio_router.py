"""Deterministic demand-to-package routing over canonical Dealix truth.

Routing is an internal recommendation. It cannot create a relationship,
consent, offer, price, quote, send, payment, proof, execution, deployment, or
production authority.

Public/CRM research is never a relationship. Raw interaction/inbound references
are evidence-presence only and cannot by themselves prove that an interaction
occurred. Commercial package routing requires the canonical interaction state
plus its matching evidence reference. Verified relationship truth remains owned
by the canonical relationship state owner.
"""

from __future__ import annotations

import hashlib
import json
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

UNKNOWN = "UNKNOWN_NOT_EVIDENCE_BACKED"
INTERACTION_EVIDENCE_PRESENT = "INTERACTION_EVIDENCE_PRESENT_NOT_RELATIONSHIP_VERIFIED"


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
    real_interaction_state: str = "UNKNOWN"
    real_interaction_ref: str = ""
    explicit_inbound_ref: str = ""
    relationship_state: str = UNKNOWN
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
    routing_reason: str
    evidence_refs: list[str]
    input_evidence_refs: list[str]
    relationship_state: str
    consent_state: str
    confidence: str
    confidence_semantics: str = "ROUTING_CLARITY_ONLY_NOT_PURCHASE_PROBABILITY"
    missing_evidence: list[str]
    next_evidence_required: list[str]
    next_action: str
    owner: str
    sla_minutes: int
    expiry_hours: int = 24
    authority_class: str = "INTERNAL_ROUTING_RECOMMENDATION_ONLY"
    risk_class: str = "STANDARD"
    authority: dict[str, bool]
    status: str = "INTERNAL_ROUTING_RECOMMENDATION"

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")


class PortfolioPackageRouter:
    """Route evidenced demand without becoming a truth or authority owner."""

    _TECH = {
        "ai",
        "agent",
        "agents",
        "automation",
        "company_brain",
        "company_knowledge",
        "knowledge",
        "knowledge_management",
        "enterprise_search",
        "rag",
        "workflow",
        "workflow_intelligence",
        "integration",
        "technical_capability",
        "copilot",
        "decision_intelligence",
        "document_intelligence",
        "tender_intelligence",
        "proposal_intelligence",
        "customer_operations",
        "support_automation",
    }
    _REVENUE = {
        "revenue",
        "sales",
        "crm",
        "follow_up",
        "pipeline",
        "quote",
        "handoff",
        "lead",
        "conversion",
        "renewal",
        "proposal",
    }
    _TECH_TERMS = (
        "company brain",
        "company knowledge",
        "knowledge management",
        "enterprise search",
        "agent",
        "automation",
        "decision intelligence",
        "document intelligence",
        "tender intelligence",
        "proposal intelligence",
        "customer operations",
        "support automation",
        "ذكاء اصطناعي",
        "أتمتة",
        "إدارة المعرفة",
        "ذكاء القرار",
        "ذكاء القرارات",
        "ذكاء العطاءات",
        "عمليات العملاء",
        "أتمتة الدعم",
    )
    _REVENUE_TERMS = (
        "revenue",
        "sales",
        "pipeline",
        "follow-up",
        "مبيعات",
        "إيراد",
        "متابعة",
    )
    _CONSENT_STATES = {
        "CONSENTED",
        "OPTED_OUT",
        "SUPPRESSED",
        "EXPIRED",
        "UNKNOWN",
    }
    _RISK_CLASSES = {"LOW", "STANDARD", "HIGH", "PROHIBITED", "UNKNOWN"}
    _INTERACTION_STATES = {"REAL_INTERACTION", "EXPLICIT_INBOUND"}

    @staticmethod
    def _normalized(values: list[str]) -> set[str]:
        return {
            value.strip().lower().replace(" ", "_")
            for value in values
            if value.strip()
        }

    @staticmethod
    def _authority() -> dict[str, bool]:
        return {
            "relationship": False,
            "consent": False,
            "offer": False,
            "price": False,
            "quote": False,
            "contract": False,
            "external_send": False,
            "payment": False,
            "customer_proof": False,
            "execution": False,
            "production": False,
        }

    def _families(
        self,
        signal: DemandSignal,
        tags: set[str],
        statement: str,
    ) -> set[EntryPackage]:
        families: set[EntryPackage] = set()
        if signal.partner_intent:
            families.add(EntryPackage.PARTNER_LAYER)
        if signal.ksa_market_entry_intent:
            families.add(EntryPackage.SAUDI_MARKET_ACCESS)
        if tags & self._TECH or any(term in statement for term in self._TECH_TERMS):
            families.add(EntryPackage.COMPANY_BRAIN)
        if tags & self._REVENUE or any(term in statement for term in self._REVENUE_TERMS):
            families.add(EntryPackage.REVENUE_COMMAND)
        return families

    def route(self, signal: DemandSignal) -> PackageRouteDecision:
        source_refs = {
            *[ref.strip() for ref in signal.evidence_refs if ref.strip()],
            *([signal.source_ref.strip()] if signal.source_ref.strip() else []),
        }
        real_interaction_ref = signal.real_interaction_ref.strip()
        explicit_inbound_ref = signal.explicit_inbound_ref.strip()
        interaction_refs = {
            *([real_interaction_ref] if real_interaction_ref else []),
            *([explicit_inbound_ref] if explicit_inbound_ref else []),
        }
        refs = sorted(source_refs | interaction_refs)

        interaction_state = signal.real_interaction_state.strip().upper() or UNKNOWN
        interaction_evidenced = (
            interaction_state == "REAL_INTERACTION" and bool(real_interaction_ref)
        ) or (
            interaction_state == "EXPLICIT_INBOUND" and bool(explicit_inbound_ref)
        )

        declared_relationship = signal.relationship_state.strip().upper() or UNKNOWN
        relationship_verified = (
            declared_relationship == "VERIFIED_RELATIONSHIP" and interaction_evidenced
        )
        if relationship_verified:
            relationship_state = "VERIFIED_RELATIONSHIP"
        elif interaction_evidenced:
            relationship_state = INTERACTION_EVIDENCE_PRESENT
        else:
            relationship_state = UNKNOWN

        consent = signal.consent_state.strip().upper() or "UNKNOWN"
        if consent not in self._CONSENT_STATES:
            consent = UNKNOWN

        risk = signal.risk_class.strip().upper() or "UNKNOWN"
        if risk not in self._RISK_CLASSES:
            risk = UNKNOWN

        tags = self._normalized(signal.problem_tags + signal.requested_capabilities)
        statement = signal.problem_statement.strip().lower()
        families = self._families(signal, tags, statement)
        reasons: list[str] = []
        missing: list[str] = []

        if not source_refs:
            missing.append("source-linked evidence")
        if interaction_state not in self._INTERACTION_STATES:
            missing.append("canonical real interaction or explicit inbound state")
        elif not interaction_evidenced:
            missing.append("matching interaction evidence reference")
        if declared_relationship == "VERIFIED_RELATIONSHIP" and not interaction_evidenced:
            missing.append("supporting canonical interaction state and evidence")
        elif interaction_evidenced and not relationship_verified:
            missing.append("canonical verified relationship state")
        if consent in {"UNKNOWN", "EXPIRED"}:
            missing.append("current channel consent or eligibility state")
        if (
            not statement
            and not tags
            and not signal.partner_intent
            and not signal.ksa_market_entry_intent
        ):
            missing.append("problem statement or capability request")
        if signal.economic_relevance == "UNKNOWN":
            missing.append("economic relevance")
        if signal.urgency == "UNKNOWN":
            missing.append("urgency")
        if risk == "UNKNOWN":
            missing.append("risk or regulatory class")

        if consent in {"OPTED_OUT", "SUPPRESSED"}:
            package = EntryPackage.RESEARCH_NURTURE_SUPPRESS
            reasons.append("CHANNEL_SUPPRESSED")
            next_action = "HONOR_SUPPRESSION_AND_KEEP_INTERNAL_RESEARCH_ONLY"
            owner = "governance"
            confidence = "HIGH"
            status = "SUPPRESSED"
            authority_class = "NO_EXTERNAL_ACTION_AUTHORITY"
            expiry_hours = 0
        elif risk == "PROHIBITED":
            package = EntryPackage.RESEARCH_NURTURE_SUPPRESS
            reasons.append("PROHIBITED_RISK_CLASS")
            next_action = "STOP_COMMERCIAL_PROGRESSION_AND_RECORD_GOVERNANCE_REASON"
            owner = "governance"
            confidence = "HIGH"
            status = "GOVERNANCE_BLOCKED"
            authority_class = "NO_COMMERCIAL_PROGRESSION_AUTHORITY"
            expiry_hours = 0
        elif not interaction_evidenced:
            package = EntryPackage.RESEARCH_NURTURE_SUPPRESS
            reasons.append("RESEARCH_IS_NOT_RELATIONSHIP_OR_LEGITIMATE_DEMAND")
            if interaction_refs:
                reasons.append("RAW_INTERACTION_REFERENCE_NOT_CANONICAL_STATE")
            next_action = "CAPTURE_CANONICAL_REAL_INTERACTION_OR_EXPLICIT_INBOUND_STATE"
            owner = "lead_acquisition"
            confidence = "HIGH"
            status = "RESEARCH_ONLY"
            authority_class = "INTERNAL_RESEARCH_ONLY"
            expiry_hours = 24
        elif len(families) > 1:
            package = EntryPackage.DIAGNOSTIC_DISCOVERY
            reasons.append("MULTIPLE_PACKAGE_FAMILIES_REQUIRE_DISCOVERY")
            missing.append("primary problem and scope priority")
            next_action = "COMPLETE_FREE_MINI_DIAGNOSTIC_AND_RESOLVE_PRIMARY_PROBLEM"
            owner = "diagnostic"
            confidence = "LOW"
            status = "DISCOVERY_REQUIRED"
            authority_class = "INTERNAL_DISCOVERY_PREPARATION_ONLY"
            expiry_hours = 24
        elif len(families) == 1:
            package = next(iter(families))
            if package == EntryPackage.PARTNER_LAYER:
                reasons.append("PARTNER_OR_IMPLEMENTATION_INTENT")
                next_action = "PREPARE_PARTNER_QUALIFICATION_PACKET"
                owner = "partner"
                confidence = "HIGH"
            elif package == EntryPackage.SAUDI_MARKET_ACCESS:
                reasons.append("KSA_MARKET_ENTRY_INTENT")
                next_action = "PREPARE_SOURCED_MARKET_ACCESS_DIAGNOSTIC"
                owner = "market_intelligence"
                confidence = "HIGH"
            elif package == EntryPackage.COMPANY_BRAIN:
                reasons.append("TECHNICAL_AI_OR_CONTEXT_DEMAND")
                next_action = "RUN_COMPANY_BRAIN_SPRINT_ASSESSMENT"
                owner = "diagnostic"
                confidence = "MEDIUM"
            else:
                reasons.append("REVENUE_EXECUTION_PROBLEM")
                next_action = "RUN_REVENUE_MINI_DIAGNOSTIC"
                owner = "revenue_intelligence"
                confidence = "MEDIUM"
            status = "INTERNAL_ROUTING_RECOMMENDATION"
            authority_class = "PACKAGE_HYPOTHESIS_ONLY"
            expiry_hours = 24
        else:
            package = EntryPackage.DIAGNOSTIC_DISCOVERY
            reasons.append("LEGITIMATE_DEMAND_REQUIRES_PROBLEM_CLARIFICATION")
            next_action = "COMPLETE_FREE_MINI_DIAGNOSTIC"
            owner = "diagnostic"
            confidence = "LOW"
            status = "DISCOVERY_REQUIRED"
            authority_class = "INTERNAL_DISCOVERY_PREPARATION_ONLY"
            expiry_hours = 24

        if risk == "HIGH" and status not in {
            "SUPPRESSED",
            "GOVERNANCE_BLOCKED",
            "RESEARCH_ONLY",
        }:
            reasons.append("HIGH_RISK_REQUIRES_GOVERNANCE_REVIEW")
            next_action = "PREPARE_EVIDENCE_PACKET_FOR_GOVERNANCE_REVIEW"
            owner = "governance"
            status = "GOVERNANCE_REVIEW_REQUIRED"
            authority_class = "GOVERNANCE_REVIEW_REQUIRED"
            confidence = "LOW" if confidence == "LOW" else "MEDIUM"

        if interaction_evidenced and not relationship_verified:
            reasons.append("INTERACTION_EVIDENCE_IS_NOT_VERIFIED_RELATIONSHIP")
        if consent in {"UNKNOWN", "EXPIRED"}:
            reasons.append("DIRECT_MARKETING_PERMISSION_NOT_ESTABLISHED")
        if not source_refs:
            reasons.append("NO_SOURCE_LINKED_EVIDENCE")

        reasons = sorted(set(reasons))
        missing = sorted(set(missing))
        routing_reason = reasons[0] if reasons else "NO_ROUTING_REASON"

        fingerprint = json.dumps(
            {
                "signal": signal.model_dump(mode="json"),
                "package": package.value,
                "reasons": reasons,
                "status": status,
                "risk": risk,
                "authority_class": authority_class,
                "relationship_state": relationship_state,
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
            reason_codes=reasons,
            routing_reason=routing_reason,
            evidence_refs=refs,
            input_evidence_refs=refs,
            relationship_state=relationship_state,
            consent_state=consent,
            confidence=confidence,
            missing_evidence=missing,
            next_evidence_required=missing,
            next_action=next_action,
            owner=owner,
            sla_minutes=15 if interaction_evidenced else 240,
            expiry_hours=expiry_hours,
            authority_class=authority_class,
            risk_class=risk,
            authority=self._authority(),
            status=status,
        )


__all__ = [
    "DemandSignal",
    "EntryPackage",
    "INTERACTION_EVIDENCE_PRESENT",
    "PackageRouteDecision",
    "PortfolioPackageRouter",
    "UNKNOWN",
]
