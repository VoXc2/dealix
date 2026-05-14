"""Support Desk Sprint — classify, draft reply (draft_only), SLA targets (no send)."""

from __future__ import annotations

from collections import Counter
from typing import Any

from auto_client_acquisition.commercial_engagements.schemas import (
    SupportDeskMessageIn,
    SupportDeskSprintInput,
    SupportDeskSprintReport,
)
from auto_client_acquisition.support_os.classifier import classify_message
from auto_client_acquisition.support_os.responder import draft_response
from auto_client_acquisition.support_os.sla import category_to_priority, compute_sla


def _coerce_message(raw: str | SupportDeskMessageIn | dict[str, Any]) -> tuple[str, str | None]:
    if isinstance(raw, str):
        return raw, None
    if isinstance(raw, SupportDeskMessageIn):
        text = (raw.text or raw.body or "").strip()
        return text, raw.id
    if isinstance(raw, dict):
        text = (raw.get("text") or raw.get("body") or "")
        if isinstance(text, str):
            return text.strip(), raw.get("id") if isinstance(raw.get("id"), str) else None
    raise TypeError("Each message must be a str, SupportDeskMessageIn, or dict with text/body")


def run_support_desk_sprint(
    inp: SupportDeskSprintInput | dict[str, Any],
) -> SupportDeskSprintReport:
    if isinstance(inp, dict):
        inp = SupportDeskSprintInput.model_validate(inp)

    items: list[dict[str, Any]] = []
    categories: list[str] = []

    for i, raw in enumerate(inp.messages):
        msg, mid = _coerce_message(raw)
        clf = classify_message(msg)
        draft = draft_response(message=msg, classification=clf)
        pri = category_to_priority(clf.category)
        sla = compute_sla(pri)

        items.append(
            {
                "index": i,
                "message_id": mid,
                "category": clf.category,
                "confidence": clf.confidence,
                "needs_human_immediately": clf.needs_human_immediately,
                "draft_action_mode": draft.action_mode,
                "draft_text_ar": draft.text_ar,
                "draft_text_en": draft.text_en,
                "insufficient_evidence": draft.insufficient_evidence,
                "sla_priority": sla.priority,
                "sla_minutes": sla.minutes,
                "sla_label_ar": sla.label_ar,
            }
        )
        categories.append(clf.category)

    summary = dict(Counter(categories))
    return SupportDeskSprintReport(items=items, summary=summary)
