"""Delivery Event Writer — bridges Delivery OS state changes into event_store.

كاتب الأحداث — يربط تغيّرات حالة Delivery OS بـ event_store غير القابل للتعديل.

Every Delivery OS side-effect (stage transition, QA result, proof pack,
handoff, renewal) becomes an immutable event so the project is fully
auditable and replayable.
"""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.delivery_factory.client_handoff import HandoffPacket
from auto_client_acquisition.delivery_factory.qa_review import QAReport
from auto_client_acquisition.delivery_factory.renewal_recommendation import (
    Recommendation,
)
from auto_client_acquisition.delivery_factory.stage_machine import StageTransition
from auto_client_acquisition.revenue_memory.event_store import EventStore, append_event
from auto_client_acquisition.revenue_memory.events import make_event
from core.logging import get_logger

log = get_logger(__name__)


def emit_stage_transition(
    customer_id: str,
    transition: StageTransition,
    *,
    correlation_id: str | None = None,
    store: EventStore | None = None,
) -> str:
    """Emit a `delivery.stage_entered` event."""
    event = make_event(
        event_type="delivery.stage_entered",
        customer_id=customer_id,
        subject_type="account",
        subject_id=transition.project_id,
        payload={
            "from_stage": transition.from_stage,
            "to_stage": transition.to_stage,
            "note_ar": transition.note_ar,
            "note_en": transition.note_en,
            "at": transition.at,
        },
        correlation_id=correlation_id or transition.project_id,
        actor=transition.actor,
    )
    append_event(event, store=store)
    log.info(
        "delivery_event_emitted",
        kind="stage_entered",
        project_id=transition.project_id,
        to_stage=transition.to_stage,
    )
    return event.event_id


def emit_qa_evaluated(
    customer_id: str,
    report: QAReport,
    *,
    correlation_id: str | None = None,
    store: EventStore | None = None,
) -> str:
    """Emit a `delivery.qa_evaluated` event with the full report payload."""
    event = make_event(
        event_type="delivery.qa_evaluated",
        customer_id=customer_id,
        subject_type="account",
        subject_id=report.project_id,
        payload={
            "report_id": report.report_id,
            "ships": report.ships,
            "quality_score": report.score.total,
            "reasons_blocked_en": report.reasons_blocked_en,
            "reviewer": report.reviewer,
        },
        correlation_id=correlation_id or report.project_id,
        actor=report.reviewer,
    )
    append_event(event, store=store)
    log.info(
        "delivery_event_emitted",
        kind="qa_evaluated",
        project_id=report.project_id,
        ships=report.ships,
        score=report.score.total,
    )
    return event.event_id


def emit_proof_pack(
    customer_id: str,
    project_id: str,
    pack_id: str,
    *,
    headline_en: str,
    metric_count: int,
    correlation_id: str | None = None,
    store: EventStore | None = None,
) -> str:
    """Emit a `delivery.proof_pack_created` event."""
    event = make_event(
        event_type="delivery.proof_pack_created",
        customer_id=customer_id,
        subject_type="account",
        subject_id=project_id,
        payload={
            "pack_id": pack_id,
            "headline_en": headline_en,
            "metric_count": metric_count,
        },
        correlation_id=correlation_id or project_id,
    )
    append_event(event, store=store)
    log.info(
        "delivery_event_emitted",
        kind="proof_pack_created",
        project_id=project_id,
        pack_id=pack_id,
    )
    return event.event_id


def emit_handoff(
    customer_id: str,
    packet: HandoffPacket,
    *,
    correlation_id: str | None = None,
    store: EventStore | None = None,
) -> str:
    """Emit a `delivery.handoff_completed` event."""
    event = make_event(
        event_type="delivery.handoff_completed",
        customer_id=customer_id,
        subject_type="account",
        subject_id=packet.project_id,
        payload={
            "handoff_id": packet.handoff_id,
            "title_en": packet.title_en,
            "deliverables_count": len(packet.deliverables_links),
            "signed_off": packet.signed_off,
        },
        correlation_id=correlation_id or packet.project_id,
    )
    append_event(event, store=store)
    log.info(
        "delivery_event_emitted",
        kind="handoff_completed",
        project_id=packet.project_id,
    )
    return event.event_id


def emit_renewal(
    customer_id: str,
    rec: Recommendation,
    *,
    correlation_id: str | None = None,
    store: EventStore | None = None,
) -> str:
    """Emit a `delivery.renewal_proposed` event."""
    event = make_event(
        event_type="delivery.renewal_proposed",
        customer_id=customer_id,
        subject_type="account",
        subject_id=rec.project_id,
        payload={
            "rec_id": rec.rec_id,
            "next_offer": rec.next_offer,
            "name_en": rec.name_en,
            "estimated_price_sar": rec.estimated_price_sar,
            "confidence": rec.confidence,
        },
        correlation_id=correlation_id or rec.project_id,
    )
    append_event(event, store=store)
    log.info(
        "delivery_event_emitted",
        kind="renewal_proposed",
        project_id=rec.project_id,
        next_offer=rec.next_offer,
    )
    return event.event_id


def emit_all_for_project(
    customer_id: str,
    *,
    transitions: list[StageTransition] | None = None,
    qa: QAReport | None = None,
    proof_pack: dict[str, Any] | None = None,
    handoff: HandoffPacket | None = None,
    renewal: Recommendation | None = None,
    store: EventStore | None = None,
) -> list[str]:
    """Convenience: emit every available delivery event for a project. Returns event_ids."""
    ids: list[str] = []
    for t in transitions or []:
        ids.append(emit_stage_transition(customer_id, t, store=store))
    if qa is not None:
        ids.append(emit_qa_evaluated(customer_id, qa, store=store))
    if proof_pack is not None:
        ids.append(
            emit_proof_pack(
                customer_id,
                proof_pack["project_id"],
                proof_pack["pack_id"],
                headline_en=proof_pack.get("headline_en", ""),
                metric_count=int(proof_pack.get("metric_count", 0)),
                store=store,
            )
        )
    if handoff is not None:
        ids.append(emit_handoff(customer_id, handoff, store=store))
    if renewal is not None:
        ids.append(emit_renewal(customer_id, renewal, store=store))
    return ids
