"""Deterministic buyer outputs assembled from one canonical evidence snapshot.

This module is intentionally pure and stateless. It creates the three governed
buyer-facing/internal outputs defined by the deterministic buyer outputs contract:
Revenue Leak Map, Customer Proof Decision Pack, and Executive Command.

It does not write a database, create a scheduler, call an LLM, send messages,
create payment state, or promote research into a relationship.
"""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from datetime import UTC, datetime
from typing import Any, ClassVar

from pydantic import BaseModel, ConfigDict, Field

UNKNOWN = "UNKNOWN_NOT_EVIDENCE_BACKED"
SCHEMA_VERSION = "1.0.0"
AUTHORITY_REF = "Dealix #1317 deterministic buyer outputs"


class EvidenceItem(BaseModel):
    """A source-linked observation available to all three outputs."""

    model_config = ConfigDict(extra="forbid")

    evidence_id: str = Field(..., min_length=1)
    source_ref: str = Field(..., min_length=1)
    observed_at: str = Field(..., min_length=1)
    summary: str = ""
    kind: str = "source"
    synthetic: bool = False
    customer_validated: bool = False


class ProcessObservation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    observation_id: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    evidence_refs: list[str] = Field(default_factory=list, min_length=1)


class ObservedLeak(BaseModel):
    model_config = ConfigDict(extra="forbid")

    leak_id: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    evidence_refs: list[str] = Field(..., min_length=1)
    owner: str = UNKNOWN
    severity: str = "UNKNOWN"


class HypothesizedLeak(BaseModel):
    model_config = ConfigDict(extra="forbid")

    hypothesis_id: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    supporting_refs: list[str] = Field(default_factory=list)


class OwnerGap(BaseModel):
    model_config = ConfigDict(extra="forbid")

    gap_id: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    owner: str = UNKNOWN
    next_action: str = UNKNOWN
    evidence_refs: list[str] = Field(default_factory=list)


class Intervention(BaseModel):
    model_config = ConfigDict(extra="forbid")

    intervention_id: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)
    rationale: str = Field(..., min_length=1)
    evidence_refs: list[str] = Field(default_factory=list)
    status: str = "HYPOTHESIS_ONLY"


class BaselineMetric(BaseModel):
    model_config = ConfigDict(extra="forbid")

    metric_id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    value: str = Field(..., min_length=1)
    unit: str = ""
    observed_at: str = Field(..., min_length=1)
    evidence_refs: list[str] = Field(..., min_length=1)
    customer_approved: bool = False


class ApprovedAction(BaseModel):
    model_config = ConfigDict(extra="forbid")

    action_id: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    approved: bool = False
    approval_ref: str = ""
    evidence_refs: list[str] = Field(default_factory=list)


class OutcomeEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    outcome_id: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    recorded_at: str = Field(..., min_length=1)
    evidence_refs: list[str] = Field(..., min_length=1)
    metric_before: str = ""
    metric_after: str = ""
    customer_validated: bool = False
    synthetic: bool = False


class PaymentEvidence(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: str = "UNKNOWN"
    payment_proof_refs: list[str] = Field(default_factory=list)
    verified_revenue_sar: float | None = Field(default=None, ge=0)
    invoice_refs: list[str] = Field(default_factory=list)


class DeliveryEvidence(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: str = "UNKNOWN"
    delivery_proof_refs: list[str] = Field(default_factory=list)


class DecisionCandidate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    decision_id: str = Field(..., min_length=1)
    decision: str = Field(..., min_length=1)
    owner: str = UNKNOWN
    evidence_refs: list[str] = Field(default_factory=list)
    confidence: str = "LOW"
    deadline: str = UNKNOWN


class RiskInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    risk_id: str = Field(..., min_length=1)
    risk_class: str = Field(..., min_length=1)
    severity: str = "MEDIUM"
    evidence_refs: list[str] = Field(default_factory=list)
    mitigation: str = Field(..., min_length=1)
    owner: str = UNKNOWN


class BuyerEvidenceSnapshot(BaseModel):
    """The single read-only input shared by every buyer output."""

    model_config = ConfigDict(extra="forbid")

    tenant_or_account_id: str = Field(..., min_length=1)
    company_name: str = Field(..., min_length=1)
    sector: str = "b2b_services"
    source_sha: str = Field(..., min_length=1)
    as_of: str = Field(..., min_length=1)
    stale_after: str = ""
    authority_ref: str = AUTHORITY_REF
    evidence: list[EvidenceItem] = Field(default_factory=list)
    process_observations: list[ProcessObservation] = Field(default_factory=list)
    observed_leaks: list[ObservedLeak] = Field(default_factory=list)
    hypothesized_leaks: list[HypothesizedLeak] = Field(default_factory=list)
    owner_gaps: list[OwnerGap] = Field(default_factory=list)
    proposed_interventions: list[Intervention] = Field(default_factory=list)
    baseline: list[BaselineMetric] = Field(default_factory=list)
    agreed_objective: str = ""
    agreed_objective_evidence_refs: list[str] = Field(default_factory=list)
    approved_actions: list[ApprovedAction] = Field(default_factory=list)
    outcome_events: list[OutcomeEvent] = Field(default_factory=list)
    customer_validation_state: str = "UNKNOWN"
    customer_validation_refs: list[str] = Field(default_factory=list)
    payment_evidence: PaymentEvidence = Field(default_factory=PaymentEvidence)
    delivery_evidence: DeliveryEvidence = Field(default_factory=DeliveryEvidence)
    decision_candidates: list[DecisionCandidate] = Field(default_factory=list)
    risks: list[RiskInput] = Field(default_factory=list)
    requested_next_evidence: list[str] = Field(default_factory=list)
    requested_next_action: str = ""


class BuyerOutputsBundle(BaseModel):
    model_config = ConfigDict(extra="forbid")

    revenue_leak_map: dict[str, Any]
    customer_proof_decision_pack: dict[str, Any]
    executive_command: dict[str, Any]

    _metadata_keys: ClassVar[tuple[str, ...]] = ("revenue_leak_map", "customer_proof_decision_pack", "executive_command")

    def to_dict(self) -> dict[str, Any]:
        return deepcopy(self.model_dump(mode="json"))

    def semantic_dict(self) -> dict[str, Any]:
        """Return equality material with generated metadata excluded."""

        data = self.to_dict()
        for output_name in self._metadata_keys:
            metadata = data[output_name].get("metadata", {})
            metadata.pop("generated_at", None)
        return data


class BuyerOutputsEngine:
    """Build all governed buyer outputs from one normalized evidence snapshot."""

    def build(self, snapshot: BuyerEvidenceSnapshot) -> BuyerOutputsBundle:
        index = {item.evidence_id: item for item in snapshot.evidence}
        self._validate_refs(snapshot, index)
        metadata = self._metadata(snapshot, index)
        revenue_leak_map = self._build_revenue_leak_map(snapshot, index, metadata)
        proof_pack = self._build_proof_pack(snapshot, index, metadata)
        executive_command = self._build_executive_command(
            snapshot,
            index,
            metadata,
            revenue_leak_map,
            proof_pack,
        )
        return BuyerOutputsBundle(
            revenue_leak_map=revenue_leak_map,
            customer_proof_decision_pack=proof_pack,
            executive_command=executive_command,
        )

    @staticmethod
    def _parse_timestamp(value: str) -> datetime:
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ValueError(f"timestamp must be ISO-8601: {value}") from exc
        if parsed.tzinfo is None:
            raise ValueError(f"timestamp must include timezone: {value}")
        return parsed.astimezone(UTC)

    @classmethod
    def _validate_refs(
        cls,
        snapshot: BuyerEvidenceSnapshot,
        index: dict[str, EvidenceItem],
    ) -> None:
        refs: list[str] = []
        for item in snapshot.evidence:
            cls._parse_timestamp(item.observed_at)
            refs.append(item.evidence_id)
        cls._parse_timestamp(snapshot.as_of)
        if snapshot.stale_after:
            cls._parse_timestamp(snapshot.stale_after)

        def require_known(values: list[str], label: str) -> None:
            missing = sorted(set(values) - set(index))
            if missing:
                raise ValueError(f"{label} references unknown evidence: {missing}")

        for item in snapshot.process_observations:
            require_known(item.evidence_refs, item.observation_id)
        for item in snapshot.observed_leaks:
            require_known(item.evidence_refs, item.leak_id)
            if any(index[ref].synthetic for ref in item.evidence_refs):
                raise ValueError(f"{item.leak_id} cannot promote synthetic evidence to an observed leak")
        for item in snapshot.hypothesized_leaks:
            require_known(item.supporting_refs, item.hypothesis_id)
        for item in snapshot.owner_gaps:
            require_known(item.evidence_refs, item.gap_id)
        for item in snapshot.proposed_interventions:
            require_known(item.evidence_refs, item.intervention_id)
        for item in snapshot.baseline:
            cls._parse_timestamp(item.observed_at)
            require_known(item.evidence_refs, item.metric_id)
        require_known(snapshot.agreed_objective_evidence_refs, "agreed_objective")
        for item in snapshot.approved_actions:
            require_known(item.evidence_refs, item.action_id)
        for item in snapshot.outcome_events:
            cls._parse_timestamp(item.recorded_at)
            require_known(item.evidence_refs, item.outcome_id)
        require_known(snapshot.payment_evidence.payment_proof_refs, "payment_proof")
        require_known(snapshot.payment_evidence.invoice_refs, "invoice")
        require_known(snapshot.delivery_evidence.delivery_proof_refs, "delivery_proof")
        require_known(snapshot.customer_validation_refs, "customer_validation")

        invalid_payment_refs = [
            ref for ref in snapshot.payment_evidence.payment_proof_refs
            if index[ref].synthetic or index[ref].kind.lower() not in {"payment", "payment_proof", "payment_provider_event"}
        ]
        if invalid_payment_refs:
            raise ValueError(f"payment proof refs must be non-synthetic payment evidence: {sorted(invalid_payment_refs)}")

        invalid_delivery_refs = [
            ref for ref in snapshot.delivery_evidence.delivery_proof_refs
            if index[ref].synthetic or index[ref].kind.lower() not in {"delivery", "delivery_proof", "accepted_delivery"}
        ]
        if invalid_delivery_refs:
            raise ValueError(f"delivery proof refs must be non-synthetic delivery evidence: {sorted(invalid_delivery_refs)}")

        invalid_validation_refs = [
            ref for ref in snapshot.customer_validation_refs
            if index[ref].synthetic or not index[ref].customer_validated
        ]
        if invalid_validation_refs:
            raise ValueError(f"customer validation refs must be non-synthetic customer-validated evidence: {sorted(invalid_validation_refs)}")
        for item in snapshot.decision_candidates:
            require_known(item.evidence_refs, item.decision_id)
        for item in snapshot.risks:
            require_known(item.evidence_refs, item.risk_id)

        if (
            snapshot.payment_evidence.verified_revenue_sar is not None
            and not snapshot.payment_evidence.payment_proof_refs
        ):
            raise ValueError("verified revenue requires payment proof refs")
        if snapshot.payment_evidence.status.upper() in {"PAID", "VERIFIED"} and not snapshot.payment_evidence.payment_proof_refs:
            raise ValueError("paid status requires external payment proof refs")

    @staticmethod
    def _canonical(value: Any) -> Any:
        if isinstance(value, dict):
            return {key: BuyerOutputsEngine._canonical(value[key]) for key in sorted(value)}
        if isinstance(value, list):
            items = [BuyerOutputsEngine._canonical(item) for item in value]
            return sorted(
                items,
                key=lambda item: json.dumps(item, ensure_ascii=False, sort_keys=True, separators=(",", ":")),
            )
        return value

    @classmethod
    def _input_fingerprint(cls, snapshot: BuyerEvidenceSnapshot) -> str:
        normalized = cls._canonical(snapshot.model_dump(mode="json"))
        payload = json.dumps(normalized, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]

    @classmethod
    def _metadata(
        cls,
        snapshot: BuyerEvidenceSnapshot,
        index: dict[str, EvidenceItem],
    ) -> dict[str, Any]:
        as_of = cls._parse_timestamp(snapshot.as_of)
        observed = sorted(
            ((cls._parse_timestamp(item.observed_at), item.observed_at) for item in index.values()),
            key=lambda pair: pair[0],
        )
        oldest = observed[0][1] if observed else UNKNOWN
        newest = observed[-1][1] if observed else UNKNOWN
        stale = True
        if snapshot.stale_after and observed:
            stale = as_of > cls._parse_timestamp(snapshot.stale_after)
        freshness = {
            "as_of": snapshot.as_of,
            "oldest_evidence_at": oldest,
            "newest_evidence_at": newest,
            "stale_after": snapshot.stale_after or UNKNOWN,
            "stale": stale,
        }
        return {
            "schema_version": SCHEMA_VERSION,
            "generated_at": datetime.now(UTC).isoformat(),
            "source_sha": snapshot.source_sha,
            "tenant_or_account_id": snapshot.tenant_or_account_id,
            "input_evidence_refs": sorted(index),
            "freshness": freshness,
            "generator": "BuyerOutputsEngine",
            "authority_ref": snapshot.authority_ref or AUTHORITY_REF,
            "unknown_semantics": UNKNOWN,
        }

    @staticmethod
    def _evidence_dict(item: EvidenceItem) -> dict[str, Any]:
        return item.model_dump(mode="json")

    @staticmethod
    def _refs(values: list[str]) -> list[str]:
        return sorted({value.strip() for value in values if value.strip()})

    @classmethod
    def _model_dict_with_refs(cls, item: BaseModel, *ref_fields: str) -> dict[str, Any]:
        data = item.model_dump(mode="json")
        for field in ref_fields:
            data[field] = cls._refs(data.get(field, []))
        return data

    @staticmethod
    def _customer_validation_state(value: str, validation_refs: list[str]) -> str:
        normalized = value.strip().upper()
        if not validation_refs:
            return UNKNOWN
        return normalized if normalized in {"VALIDATED", "CONFIRMED"} else UNKNOWN

    @classmethod
    def _unknowns(cls, snapshot: BuyerEvidenceSnapshot, index: dict[str, EvidenceItem]) -> list[str]:
        unknowns: list[str] = []
        if not index:
            unknowns.append("No source-linked evidence was supplied.")
        if not snapshot.baseline:
            unknowns.append("No customer-approved baseline was supplied.")
        if not snapshot.agreed_objective:
            unknowns.append("No agreed customer objective was supplied.")
        if not snapshot.payment_evidence.payment_proof_refs:
            unknowns.append("Payment is not verified; invoice or proposal artifacts are not payment proof.")
        if not snapshot.delivery_evidence.delivery_proof_refs:
            unknowns.append("Delivery evidence is not verified.")
        if cls._customer_validation_state(snapshot.customer_validation_state, snapshot.customer_validation_refs) == UNKNOWN:
            unknowns.append("Customer validation remains unknown.")
        return unknowns

    @classmethod
    def _next_evidence(cls, snapshot: BuyerEvidenceSnapshot, index: dict[str, EvidenceItem]) -> list[str]:
        needs = list(snapshot.requested_next_evidence)
        if not index:
            needs.append("Capture a real interaction with source, timestamp, and lawful context.")
        if not snapshot.baseline:
            needs.append("Record a customer-approved baseline with owner, source, and timestamp.")
        if not snapshot.agreed_objective:
            needs.append("Record the customer-approved objective before proposing a pilot.")
        if not snapshot.payment_evidence.payment_proof_refs:
            needs.append("If a pilot is accepted, record external payment proof before delivery.")
        if not snapshot.delivery_evidence.delivery_proof_refs:
            needs.append("Record delivery evidence before interpreting customer value.")
        return sorted(dict.fromkeys(needs))

    @classmethod
    def _next_action(cls, snapshot: BuyerEvidenceSnapshot, index: dict[str, EvidenceItem]) -> dict[str, Any]:
        if snapshot.requested_next_action:
            action = snapshot.requested_next_action
        elif not index:
            action = "CAPTURE_REAL_INTERACTION"
        elif not snapshot.agreed_objective:
            action = "RUN_QUALIFIED_DISCOVERY"
        elif not snapshot.baseline:
            action = "AGREE_BASELINE"
        elif not snapshot.payment_evidence.payment_proof_refs:
            action = "PREPARE_CUSTOMER_SPECIFIC_QUOTE_FOR_REVIEW"
        elif not snapshot.delivery_evidence.delivery_proof_refs:
            action = "VERIFY_PILOT_DELIVERY"
        else:
            action = "REVIEW_STOP_EXPAND_REDESIGN"
        return {
            "action": action,
            "owner": "founder_or_assigned_owner",
            "approval_required": True,
            "external_send_allowed": False,
        }

    @classmethod
    def _build_revenue_leak_map(
        cls,
        snapshot: BuyerEvidenceSnapshot,
        index: dict[str, EvidenceItem],
        metadata: dict[str, Any],
    ) -> dict[str, Any]:
        unknowns = cls._unknowns(snapshot, index)
        interventions = sorted(
            (cls._model_dict_with_refs(item, "evidence_refs") for item in snapshot.proposed_interventions),
            key=lambda item: (item["intervention_id"], item["title"]),
        )[:3]
        observed_leaks = [
            cls._model_dict_with_refs(item, "evidence_refs")
            for item in sorted(snapshot.observed_leaks, key=lambda item: item.leak_id)
        ]
        hypotheses = []
        for item in sorted(snapshot.hypothesized_leaks, key=lambda item: item.hypothesis_id):
            data = cls._model_dict_with_refs(item, "supporting_refs")
            data["classification"] = "HYPOTHESIS"
            hypotheses.append(data)
        return {
            "metadata": deepcopy(metadata),
            "account_context": {
                "tenant_or_account_id": snapshot.tenant_or_account_id,
                "company_name": snapshot.company_name,
                "sector": snapshot.sector,
                "relationship_state": UNKNOWN,
            },
            "evidence_inventory": [
                cls._evidence_dict(item) for item in sorted(index.values(), key=lambda item: item.evidence_id)
            ],
            "observed_process": [
                cls._model_dict_with_refs(item, "evidence_refs")
                for item in sorted(snapshot.process_observations, key=lambda item: item.observation_id)
            ],
            "observed_leaks": observed_leaks,
            "hypothesized_leaks": hypotheses,
            "owner_and_next_action_gaps": [
                cls._model_dict_with_refs(item, "evidence_refs")
                for item in sorted(snapshot.owner_gaps, key=lambda item: item.gap_id)
            ],
            "data_and_proof_gaps": unknowns,
            "top_interventions": interventions,
            "pilot_hypothesis": {
                "status": "HYPOTHESIS_ONLY",
                "statement": "A bounded pilot may test selected interventions after qualification, approved scope, and baseline agreement.",
                "evidence_refs": cls._refs(
                    [ref for item in snapshot.proposed_interventions for ref in item.evidence_refs]
                ),
            },
            "unknowns": unknowns,
            "next_evidence": cls._next_evidence(snapshot, index),
            "next_action": cls._next_action(snapshot, index),
        }

    @classmethod
    def _verified_payment_refs(
        cls,
        snapshot: BuyerEvidenceSnapshot,
        index: dict[str, EvidenceItem],
    ) -> list[str]:
        refs = snapshot.payment_evidence.payment_proof_refs
        if snapshot.payment_evidence.status.upper() not in {"PAID", "VERIFIED"}:
            return []
        return sorted(ref for ref in refs if not index[ref].synthetic)

    @classmethod
    def _verified_delivery_refs(
        cls,
        snapshot: BuyerEvidenceSnapshot,
        index: dict[str, EvidenceItem],
    ) -> list[str]:
        if snapshot.delivery_evidence.status.upper() not in {"DELIVERED", "VERIFIED"}:
            return []
        return sorted(ref for ref in snapshot.delivery_evidence.delivery_proof_refs if not index[ref].synthetic)

    @classmethod
    def _build_proof_pack(
        cls,
        snapshot: BuyerEvidenceSnapshot,
        index: dict[str, EvidenceItem],
        metadata: dict[str, Any],
    ) -> dict[str, Any]:
        payment_refs = cls._verified_payment_refs(snapshot, index)
        delivery_refs = cls._verified_delivery_refs(snapshot, index)
        outcome_events = [
            cls._model_dict_with_refs(item, "evidence_refs")
            for item in sorted(snapshot.outcome_events, key=lambda item: (item.outcome_id, item.recorded_at))
        ]
        customer_validated = cls._customer_validation_state(snapshot.customer_validation_state, snapshot.customer_validation_refs) != UNKNOWN
        interpretation_refs = sorted(set(delivery_refs if customer_validated else []))
        business_interpretation: dict[str, Any]
        if interpretation_refs:
            business_interpretation = {
                "status": "EVIDENCE_BACKED",
                "statement": "Recorded delivery evidence is available for customer review; no unverified outcome is inferred.",
                "evidence_refs": interpretation_refs,
            }
        else:
            business_interpretation = {
                "status": UNKNOWN,
                "statement": "No customer-value interpretation is published without customer validation and delivery evidence.",
                "evidence_refs": [],
            }
        unknowns = cls._unknowns(snapshot, index)
        if customer_validated and not delivery_refs:
            unknowns.append("Customer validation exists, but delivery evidence is not verified.")
        return {
            "metadata": deepcopy(metadata),
            "baseline": [
                cls._model_dict_with_refs(item, "evidence_refs")
                for item in sorted(snapshot.baseline, key=lambda item: item.metric_id)
            ] or UNKNOWN,
            "agreed_objective": {
                "value": snapshot.agreed_objective or UNKNOWN,
                "evidence_refs": cls._refs(snapshot.agreed_objective_evidence_refs),
            },
            "approved_actions": [
                cls._model_dict_with_refs(item, "evidence_refs")
                for item in sorted(snapshot.approved_actions, key=lambda item: item.action_id)
                if item.approved and item.approval_ref
            ] or UNKNOWN,
            "outcome_events": outcome_events or UNKNOWN,
            "evidence_refs": sorted(index),
            "business_interpretation": business_interpretation,
            "limitations": [
                "Proposal is not revenue.",
                "Invoice is not payment.",
                "Synthetic evidence is never customer proof.",
                "Public proof requires explicit customer permission.",
                "No result, ROI, or customer-value claim is inferred from missing evidence.",
            ],
            "customer_validation_state": cls._customer_validation_state(snapshot.customer_validation_state, snapshot.customer_validation_refs),
            "payment_evidence_state": {
                "status": "VERIFIED" if payment_refs else UNKNOWN,
                "payment_proof_refs": payment_refs,
                "invoice_refs": sorted(snapshot.payment_evidence.invoice_refs),
                "verified_revenue_sar": (
                    snapshot.payment_evidence.verified_revenue_sar
                    if payment_refs
                    else UNKNOWN
                ),
            },
            "delivery_evidence_state": {
                "status": "VERIFIED" if delivery_refs else UNKNOWN,
                "delivery_proof_refs": delivery_refs,
            },
            "decision_options": ["STOP", "EXPAND", "REDESIGN", UNKNOWN],
            "unknowns": list(dict.fromkeys(unknowns)),
            "next_evidence": cls._next_evidence(snapshot, index),
            "next_action": cls._next_action(snapshot, index),
        }

    @classmethod
    def _build_executive_command(
        cls,
        snapshot: BuyerEvidenceSnapshot,
        index: dict[str, EvidenceItem],
        metadata: dict[str, Any],
        revenue_leak_map: dict[str, Any],
        proof_pack: dict[str, Any],
    ) -> dict[str, Any]:
        payment_refs = proof_pack["payment_evidence_state"]["payment_proof_refs"]
        verified_revenue = proof_pack["payment_evidence_state"]["verified_revenue_sar"]
        if payment_refs:
            closest_money_path = "PILOT_DELIVERY" if proof_pack["delivery_evidence_state"]["status"] == "UNKNOWN_NOT_EVIDENCE_BACKED" else "REVIEW_STOP_EXPAND_REDESIGN"
        elif snapshot.agreed_objective and snapshot.baseline:
            closest_money_path = "CUSTOMER_SPECIFIC_QUOTE"
        elif index:
            closest_money_path = "QUALIFIED_DISCOVERY"
        else:
            closest_money_path = "REAL_INTERACTION"

        decisions = [
            cls._model_dict_with_refs(item, "evidence_refs")
            for item in sorted(snapshot.decision_candidates, key=lambda item: item.decision_id)
        ][:3]
        if not decisions:
            decisions = [{
                "decision_id": "DECISION-BUYER-OUTPUTS-REVIEW",
                "decision": "GATHER_EVIDENCE_BEFORE_COMMERCIAL_COMMITMENT",
                "owner": "founder_or_assigned_owner",
                "evidence_refs": sorted(index),
                "confidence": "LOW",
                "deadline": UNKNOWN,
            }]
        risks = [
            cls._model_dict_with_refs(item, "evidence_refs")
            for item in sorted(snapshot.risks, key=lambda item: item.risk_id)
        ][:3]
        if not risks:
            risks = [{
                "risk_id": "RISK-EVIDENCE-COMPLETENESS",
                "risk_class": "evidence_completeness",
                "severity": "HIGH" if not index else "MEDIUM",
                "evidence_refs": sorted(index),
                "mitigation": "Collect source-linked evidence and keep unknown values unknown.",
                "owner": "founder_or_assigned_owner",
            }]
        action_fingerprint = hashlib.sha256(
            json.dumps(
                {
                    "action": "REVIEW_BUYER_OUTPUTS",
                    "source_sha": snapshot.source_sha,
                    "account": snapshot.tenant_or_account_id,
                },
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()[:24]
        approvals = [{
            "approval_id": f"APPROVAL-{action_fingerprint}",
            "action_fingerprint": action_fingerprint,
            "authority_class": "INTERNAL_FOUNDER_REVIEW",
            "evidence_refs": sorted(index),
            "expiry": UNKNOWN,
            "decision_options": ["STOP", "EXPAND", "REDESIGN", UNKNOWN],
        }]
        return {
            "metadata": deepcopy(metadata),
            "money": {
                "verified_revenue": verified_revenue,
                "verified_payment_state": "VERIFIED" if payment_refs else UNKNOWN,
                "closest_money_path": closest_money_path,
                "economic_evidence_refs": sorted(payment_refs),
            },
            "decisions": decisions,
            "risks": risks,
            "approvals": approvals,
            "next_action": cls._next_action(snapshot, index),
        }


__all__ = [
    "UNKNOWN",
    "ApprovedAction",
    "BaselineMetric",
    "BuyerEvidenceSnapshot",
    "BuyerOutputsBundle",
    "BuyerOutputsEngine",
    "DecisionCandidate",
    "DeliveryEvidence",
    "EvidenceItem",
    "HypothesizedLeak",
    "Intervention",
    "ObservedLeak",
    "OutcomeEvent",
    "OwnerGap",
    "PaymentEvidence",
    "ProcessObservation",
    "RiskInput",
]
