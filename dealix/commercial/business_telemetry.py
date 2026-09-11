"""Business Telemetry — economic event receipts and observability.

Every meaningful state transition answers:
WHAT happened? WHY? WHO/WHAT authorized it?
WHAT evidence supported it? WHAT economic movement resulted? WHAT did it cost?
"""

from __future__ import annotations

import hashlib
import json
import threading
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class BusinessEventType(StrEnum):
    SIGNAL_CREATED = "signal.created"
    OPPORTUNITY_PROMOTED = "opportunity.promoted"
    OPPORTUNITY_KILLED = "opportunity.killed"
    RELATIONSHIP_PROGRESSED = "relationship.progressed"
    DIAGNOSTIC_CREATED = "diagnostic.created"
    DISCOVERY_COMPLETED = "discovery.completed"
    QUOTE_CREATED = "quote.created"
    INVOICE_CREATED = "invoice.created"
    PAYMENT_VERIFIED = "payment.verified"
    DELIVERY_ACCEPTED = "delivery.accepted"
    PROOF_CUSTOMER_VALIDATED = "proof.customer_validated"
    EXPANSION_CREATED = "expansion.created"
    PORTFOLIO_SLOT_ALLOCATED = "portfolio.slot_allocated"
    PORTFOLIO_SLOT_RELEASED = "portfolio.slot_released"
    MODEL_TASK_ACCEPTED = "model.task.accepted"
    MODEL_TASK_REJECTED = "model.task.rejected"
    APPROVAL_REQUESTED = "approval.requested"
    APPROVAL_EXECUTED = "approval.executed"


class AuthorizationLevel(StrEnum):
    SYSTEM = "system"
    PM_AGENT = "pm_agent"
    SALES_AGENT = "sales_agent"
    DELIVERY_AGENT = "delivery_agent"
    ENGINEER_AGENT = "engineer_agent"
    CONTENT_AGENT = "content_agent"
    FOUNDER = "founder"
    EXTERNAL = "external"


class EconomicReceipt(BaseModel):
    """Immutable receipt for a business event."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    receipt_id: str
    event_type: BusinessEventType
    entity_type: str  # "cell", "relationship", "proof", "approval", etc.
    entity_id: str
    occurred_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    authorized_by: AuthorizationLevel
    authorized_by_id: str = ""

    # What & Why
    what_happened: str
    why: str

    # Evidence
    evidence_refs: list[str] = Field(default_factory=list)
    evidence_summary: str = ""

    # Economic Impact
    economic_movement: str = "none"  # "validated", "revenue", "cost", "proof", "learning"
    value_sar: float | None = None
    cost_sar: float | None = None

    # Context
    cell_id: str | None = None
    top3_rank: int | None = None
    wip_slot: bool = False

    # Verification
    verified: bool = False
    verification_ref: str = ""

    def __post_init__(self) -> None:
        if not self.receipt_id:
            payload = self.model_dump(mode="json", exclude={"receipt_id", "occurred_at"})
            object.__setattr__(self, "receipt_id", hashlib.sha256(
                json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
            ).hexdigest()[:16])


class BusinessTelemetry:
    """Append-only business event store with receipts."""

    def __init__(self, storage_path: Path | None = None) -> None:
        self._lock = threading.Lock()
        self._storage_path = storage_path or Path("data/business_telemetry.jsonl")
        self._receipts: list[EconomicReceipt] = []
        self._load()

    def emit(
        self,
        event_type: BusinessEventType,
        entity_type: str,
        entity_id: str,
        what_happened: str,
        why: str,
        authorized_by: AuthorizationLevel,
        authorized_by_id: str = "",
        evidence_refs: list[str] | None = None,
        evidence_summary: str = "",
        economic_movement: str = "none",
        value_sar: float | None = None,
        cost_sar: float | None = None,
        cell_id: str | None = None,
        top3_rank: int | None = None,
        wip_slot: bool = False,
        verified: bool = False,
        verification_ref: str = "",
    ) -> EconomicReceipt:
        """Emit a business event and create receipt."""
        receipt = EconomicReceipt(
            receipt_id="",
            event_type=event_type,
            entity_type=entity_type,
            entity_id=entity_id,
            authorized_by=authorized_by,
            authorized_by_id=authorized_by_id,
            what_happened=what_happened,
            why=why,
            evidence_refs=evidence_refs or [],
            evidence_summary=evidence_summary,
            economic_movement=economic_movement,
            value_sar=value_sar,
            cost_sar=cost_sar,
            cell_id=cell_id,
            top3_rank=top3_rank,
            wip_slot=wip_slot,
            verified=verified,
            verification_ref=verification_ref,
        )

        with self._lock:
            self._receipts.append(receipt)
            self._persist(receipt)

        return receipt

    def _persist(self, receipt: EconomicReceipt) -> None:
        try:
            self._storage_path.parent.mkdir(parents=True, exist_ok=True)
            line = receipt.model_dump_json() + "\n"
            with self._storage_path.open("a", encoding="utf-8") as f:
                f.write(line)
        except Exception:
            pass

    def _load(self) -> None:
        if not self._storage_path.exists():
            return
        try:
            with self._storage_path.open("r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        receipt = EconomicReceipt.model_validate_json(line)
                        self._receipts.append(receipt)
                    except Exception:
                        continue
        except Exception:
            pass

    def query(
        self,
        event_type: BusinessEventType | None = None,
        entity_type: str | None = None,
        entity_id: str | None = None,
        cell_id: str | None = None,
        since: str | None = None,
        limit: int = 100,
    ) -> list[EconomicReceipt]:
        with self._lock:
            results = self._receipts
            if event_type:
                results = [r for r in results if r.event_type == event_type]
            if entity_type:
                results = [r for r in results if r.entity_type == entity_type]
            if entity_id:
                results = [r for r in results if r.entity_id == entity_id]
            if cell_id:
                results = [r for r in results if r.cell_id == cell_id]
            if since:
                results = [r for r in results if r.occurred_at >= since]
            return results[-limit:]

    def get_receipt(self, receipt_id: str) -> EconomicReceipt | None:
        with self._lock:
            for r in self._receipts:
                if r.receipt_id == receipt_id:
                    return r
            return None

    def summary(self, since: str | None = None) -> dict[str, Any]:
        with self._lock:
            results = self._receipts
            if since:
                results = [r for r in results if r.occurred_at >= since]

            by_type: dict[str, int] = {}
            by_auth: dict[str, int] = {}
            total_value = 0.0
            total_cost = 0.0
            verified_count = 0

            for r in results:
                by_type[r.event_type.value] = by_type.get(r.event_type.value, 0) + 1
                by_auth[r.authorized_by.value] = by_auth.get(r.authorized_by.value, 0) + 1
                if r.value_sar:
                    total_value += r.value_sar
                if r.cost_sar:
                    total_cost += r.cost_sar
                if r.verified:
                    verified_count += 1

            return {
                "total_events": len(results),
                "by_type": by_type,
                "by_authorization": by_auth,
                "total_value_sar": total_value,
                "total_cost_sar": total_cost,
                "verified_events": verified_count,
                "verification_rate": verified_count / len(results) if results else 0.0,
            }


# ─── Convenience Emitters for Common Events ────────────────────────────


class TelemetryEmitter:
    """Helper to emit common business events with proper context."""

    def __init__(self, telemetry: BusinessTelemetry) -> None:
        self.t = telemetry

    def signal_created(self, cell_id: str, signal_ref: str, source: str) -> EconomicReceipt:
        return self.t.emit(
            event_type=BusinessEventType.SIGNAL_CREATED,
            entity_type="signal",
            entity_id=signal_ref,
            what_happened=f"Market signal captured for {cell_id}",
            why=f"Source: {source}",
            authorized_by=AuthorizationLevel.SYSTEM,
            evidence_refs=[signal_ref],
            cell_id=cell_id,
        )

    def opportunity_promoted(
        self,
        cell_id: str,
        from_state: str,
        to_state: str,
        gate: str,
        evidence_refs: list[str],
        authorized_by: AuthorizationLevel = AuthorizationLevel.PM_AGENT,
    ) -> EconomicReceipt:
        return self.t.emit(
            event_type=BusinessEventType.OPPORTUNITY_PROMOTED,
            entity_type="cell",
            entity_id=cell_id,
            what_happened=f"Cell promoted: {from_state} → {to_state} via {gate}",
            why=f"Promotion gate {gate} satisfied",
            authorized_by=authorized_by,
            evidence_refs=evidence_refs,
            economic_movement="validated",
            cell_id=cell_id,
        )

    def opportunity_killed(self, cell_id: str, trigger: str, reason: str) -> EconomicReceipt:
        return self.t.emit(
            event_type=BusinessEventType.OPPORTUNITY_KILLED,
            entity_type="cell",
            entity_id=cell_id,
            what_happened=f"Cell killed: {trigger}",
            why=reason,
            authorized_by=AuthorizationLevel.PM_AGENT,
            economic_movement="cost_avoided",
            cell_id=cell_id,
        )

    def diagnostic_created(self, cell_id: str, diagnostic_ref: str, qualified: bool) -> EconomicReceipt:
        return self.t.emit(
            event_type=BusinessEventType.DIAGNOSTIC_CREATED,
            entity_type="diagnostic",
            entity_id=diagnostic_ref,
            what_happened=f"Diagnostic generated for {cell_id}: {'qualified' if qualified else 'not qualified'}",
            why="Problem quantification and buyer validation",
            authorized_by=AuthorizationLevel.SALES_AGENT,
            evidence_refs=[diagnostic_ref],
            economic_movement="learning",
            cell_id=cell_id,
        )

    def payment_verified(self, cell_id: str, payment_ref: str, amount_sar: float) -> EconomicReceipt:
        return self.t.emit(
            event_type=BusinessEventType.PAYMENT_VERIFIED,
            entity_type="payment",
            entity_id=payment_ref,
            what_happened=f"Payment verified: {amount_sar} SAR",
            why="Independent payment verification completed",
            authorized_by=AuthorizationLevel.FOUNDER,
            evidence_refs=[payment_ref],
            economic_movement="revenue",
            value_sar=amount_sar,
            cell_id=cell_id,
            verified=True,
            verification_ref=payment_ref,
        )

    def proof_customer_validated(self, cell_id: str, proof_ref: str, proof_level: str) -> EconomicReceipt:
        return self.t.emit(
            event_type=BusinessEventType.PROOF_CUSTOMER_VALIDATED,
            entity_type="proof",
            entity_id=proof_ref,
            what_happened=f"Customer-validated proof captured: {proof_level}",
            why="Delivery acceptance criteria met, customer confirmed",
            authorized_by=AuthorizationLevel.DELIVERY_AGENT,
            evidence_refs=[proof_ref],
            economic_movement="proof",
            cell_id=cell_id,
            verified=True,
            verification_ref=proof_ref,
        )

    def portfolio_slot_allocated(self, cell_id: str, slot_number: int, approved_by: str) -> EconomicReceipt:
        return self.t.emit(
            event_type=BusinessEventType.PORTFOLIO_SLOT_ALLOCATED,
            entity_type="wip_slot",
            entity_id=f"slot_{slot_number}",
            what_happened=f"Deep WIP slot {slot_number} allocated to {cell_id}",
            why="President Command allocation",
            authorized_by=AuthorizationLevel.FOUNDER,
            authorized_by_id=approved_by,
            economic_movement="capacity_committed",
            cell_id=cell_id,
            top3_rank=slot_number,
            wip_slot=True,
        )

    def approval_requested(self, approval_id: str, action: str, cell_id: str) -> EconomicReceipt:
        return self.t.emit(
            event_type=BusinessEventType.APPROVAL_REQUESTED,
            entity_type="approval",
            entity_id=approval_id,
            what_happened=f"Approval requested for {action} on {cell_id}",
            why="Policy requires explicit approval for material external effect",
            authorized_by=AuthorizationLevel.SYSTEM,
            evidence_refs=[approval_id],
            cell_id=cell_id,
        )

    def approval_executed(self, approval_id: str, action: str, cell_id: str, executed_by: str) -> EconomicReceipt:
        return self.t.emit(
            event_type=BusinessEventType.APPROVAL_EXECUTED,
            entity_type="approval",
            entity_id=approval_id,
            what_happened=f"Approval executed: {action} on {cell_id}",
            why="Founder approved material external action",
            authorized_by=AuthorizationLevel.FOUNDER,
            authorized_by_id=executed_by,
            evidence_refs=[approval_id],
            economic_movement="external_effect",
            cell_id=cell_id,
            verified=True,
            verification_ref=approval_id,
        )


# ─── Singleton ────────────────────────────────────────────────────────

_DEFAULT_TELEMETRY: BusinessTelemetry | None = None


def get_telemetry() -> BusinessTelemetry:
    global _DEFAULT_TELEMETRY
    if _DEFAULT_TELEMETRY is None:
        _DEFAULT_TELEMETRY = BusinessTelemetry()
    return _DEFAULT_TELEMETRY


def get_emitter() -> TelemetryEmitter:
    return TelemetryEmitter(get_telemetry())


def reset_telemetry_for_tests(telemetry: BusinessTelemetry | None = None) -> BusinessTelemetry | None:
    global _DEFAULT_TELEMETRY
    _DEFAULT_TELEMETRY = telemetry
    return _DEFAULT_TELEMETRY


__all__ = [
    "BusinessEventType",
    "AuthorizationLevel",
    "EconomicReceipt",
    "BusinessTelemetry",
    "TelemetryEmitter",
    "get_telemetry",
    "get_emitter",
    "reset_telemetry_for_tests",
]
