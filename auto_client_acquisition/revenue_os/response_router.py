"""V17 Response Router — classify inbound replies and route to safe actions.

Thin deterministic adapter over the canonical email reply classifier
(``auto_client_acquisition.email.reply_classifier``). Maps its fine-grained
categories to the V17 response taxonomy:

    POSITIVE, QUESTION, OBJECTION, REFERRAL, WRONG_PERSON, NOT_NOW, NO,
    UNSUBSCRIBE, BOUNCE, AUTO_REPLY, UNKNOWN

Every route returns the immediate safe action:

- UNSUBSCRIBE / NO  -> suppress immediately (no further marketing candidates)
- BOUNCE           -> invalidate endpoint
- AUTO_REPLY       -> do not count as engagement
- POSITIVE         -> discovery prep
- QUESTION         -> evidence-backed reply draft (human review)
- OBJECTION        -> objection handling draft
- REFERRAL         -> new evidence-backed relationship record
- WRONG_PERSON     -> role correction research
- NOT_NOW          -> future action with reason/date
- UNKNOWN          -> human review

Never auto-sends. ``auto_send_allowed`` is always False except the mandatory
unsubscribe acknowledgement, mirroring the canonical reply classifier.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from auto_client_acquisition.email.reply_classifier import (
    ReplyClassification,
    classify_rule_based,
)


class ResponseCategory(StrEnum):
    POSITIVE = "POSITIVE"
    QUESTION = "QUESTION"
    OBJECTION = "OBJECTION"
    REFERRAL = "REFERRAL"
    WRONG_PERSON = "WRONG_PERSON"
    NOT_NOW = "NOT_NOW"
    NO = "NO"
    UNSUBSCRIBE = "UNSUBSCRIBE"
    BOUNCE = "BOUNCE"
    AUTO_REPLY = "AUTO_REPLY"
    UNKNOWN = "UNKNOWN"


# Canonical reply-classifier categories -> V17 taxonomy.
_CANONICAL_TO_V17: dict[str, ResponseCategory] = {
    "interested": ResponseCategory.POSITIVE,
    "ask_price": ResponseCategory.QUESTION,
    "ask_details": ResponseCategory.QUESTION,
    "ask_demo": ResponseCategory.POSITIVE,
    "not_now": ResponseCategory.NOT_NOW,
    "objection_budget": ResponseCategory.OBJECTION,
    "objection_ai": ResponseCategory.OBJECTION,
    "objection_privacy": ResponseCategory.OBJECTION,
    "already_has_crm": ResponseCategory.OBJECTION,
    "partnership": ResponseCategory.POSITIVE,
    "unsubscribe": ResponseCategory.UNSUBSCRIBE,
    "angry": ResponseCategory.UNKNOWN,
    "unclear": ResponseCategory.UNKNOWN,
}

# Explicit negative/positive markers not reliably caught by the regex
# classifier (e.g. hard no, wrong person, bounce, auto-reply headers).
_HARD_NO_PATTERNS = ("no thanks", "not interested", "لا شكرا", "لست مهتما", "لا أريد")
_WRONG_PERSON_PATTERNS = (
    "wrong person",
    "not the right person",
    "ليس الشخص المناسب",
    "لست الشخص المناسب",
    "أرسل هذا إلى",
    "لست المعني",
    "هذا ليس تخصصي",
)
_BOUNCE_PATTERNS = ("mailer-daemon", "delivery status notification", "550", "mailbox unavailable", "recipient rejected")
_AUTO_REPLY_PATTERNS = ("auto-reply", "automatic reply", "out of office", "vacation", "إجازة", "خارج المكتب", "auto reply")
_REFERRAL_PATTERNS = ("شوف", "تواصل مع", "contact this person", "talk to", "try ", "recommend you contact")
_NOT_NOW_PATTERNS = (
    "بعد شهر",
    "بعد شهرين",
    "شهر",
    "لاحقاً",
    "لاحقا",
    "بعد رمضان",
    "بعد العيد",
    "next quarter",
    "next month",
    "in a month",
    "later",
    "maybe later",
    "not now",
    "ليس الآن",
)


def _contains_any(text: str, patterns: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(p.lower() in lowered for p in patterns)


def route_response(
    text: str,
    *,
    canonical: ReplyClassification | None = None,
) -> dict[str, Any]:
    """Classify an inbound reply and return the V17 route + safe action.

    Deterministic. Uses the canonical classifier when provided; otherwise
    runs the rule-based fast path. Never auto-sends.
    """
    raw = (text or "").strip()
    if not raw:
        return {
            "category": ResponseCategory.UNKNOWN.value,
            "route": "human_review",
            "action": "UNKNOWN: empty reply requires human review",
            "suppress": False,
            "auto_send_allowed": False,
        }

    # Hard-signal overrides first (bounce / auto-reply / unsubscribe must win).
    if _contains_any(raw, _BOUNCE_PATTERNS):
        return {
            "category": ResponseCategory.BOUNCE.value,
            "route": "invalidate_endpoint",
            "action": "BOUNCE: mark endpoint invalid; do not retry",
            "suppress": True,
            "auto_send_allowed": False,
        }
    if _contains_any(raw, _AUTO_REPLY_PATTERNS):
        return {
            "category": ResponseCategory.AUTO_REPLY.value,
            "route": "do_not_count",
            "action": "AUTO_REPLY: do not count as engagement",
            "suppress": False,
            "auto_send_allowed": False,
        }
    if _contains_any(raw, _HARD_NO_PATTERNS):
        return {
            "category": ResponseCategory.NO.value,
            "route": "close_respectfully",
            "action": "NO: close respectfully; suppress further marketing candidates",
            "suppress": True,
            "auto_send_allowed": False,
        }
    if _contains_any(raw, _WRONG_PERSON_PATTERNS):
        return {
            "category": ResponseCategory.WRONG_PERSON.value,
            "route": "role_correction",
            "action": "WRONG_PERSON: role correction research before any new touch",
            "suppress": False,
            "auto_send_allowed": False,
        }
    if _contains_any(raw, _NOT_NOW_PATTERNS):
        return {
            "category": ResponseCategory.NOT_NOW.value,
            "route": "future_action",
            "action": "NOT_NOW: schedule bounded future action with reason/date",
            "suppress": False,
            "auto_send_allowed": False,
        }
    if _contains_any(raw, _REFERRAL_PATTERNS):
        return {
            "category": ResponseCategory.REFERRAL.value,
            "route": "new_relationship",
            "action": "REFERRAL: record new evidence-backed relationship with provenance",
            "suppress": False,
            "auto_send_allowed": False,
        }

    # Use the canonical classifier output if supplied; else rule-based path.
    if canonical is not None:
        cat = canonical.category
    else:
        cat, _confidence = classify_rule_based(raw)

    v17 = _CANONICAL_TO_V17.get(cat, ResponseCategory.UNKNOWN)

    routes: dict[ResponseCategory, tuple[str, str, bool]] = {
        ResponseCategory.POSITIVE: (
            "discovery_prep",
            "POSITIVE: prepare discovery conversation",
            False,
        ),
        ResponseCategory.QUESTION: (
            "evidence_reply_draft",
            "QUESTION: draft evidence-backed reply for human review",
            False,
        ),
        ResponseCategory.OBJECTION: (
            "objection_handling",
            "OBJECTION: draft objection response; do not auto-send",
            False,
        ),
        ResponseCategory.REFERRAL: (
            "new_relationship",
            "REFERRAL: record evidence-backed relationship with provenance",
            False,
        ),
        ResponseCategory.WRONG_PERSON: (
            "role_correction",
            "WRONG_PERSON: role correction research",
            False,
        ),
        ResponseCategory.NOT_NOW: (
            "future_action",
            "NOT_NOW: schedule bounded future action with reason/date",
            False,
        ),
        ResponseCategory.NO: (
            "close_respectfully",
            "NO: close respectfully; suppress further marketing candidates",
            True,
        ),
        ResponseCategory.UNSUBSCRIBE: (
            "suppress_immediately",
            "UNSUBSCRIBE: suppress immediately; mandatory ack only",
            True,
        ),
        ResponseCategory.BOUNCE: (
            "invalidate_endpoint",
            "BOUNCE: invalidate endpoint",
            True,
        ),
        ResponseCategory.AUTO_REPLY: (
            "do_not_count",
            "AUTO_REPLY: do not count as engagement",
            False,
        ),
        ResponseCategory.UNKNOWN: (
            "human_review",
            "UNKNOWN: human review required",
            False,
        ),
    }
    route, action, suppress = routes[v17]
    # Mirror canonical classifier: only mandatory unsubscribe ack may send.
    auto_send = v17 == ResponseCategory.UNSUBSCRIBE
    return {
        "category": v17.value,
        "route": route,
        "action": action,
        "suppress": suppress,
        "auto_send_allowed": auto_send,
    }


def route_classification(canonical: ReplyClassification) -> dict[str, Any]:
    """Route an already-built canonical classification (no reclassification)."""
    v17 = _CANONICAL_TO_V17.get(canonical.category, ResponseCategory.UNKNOWN)
    routes: dict[ResponseCategory, tuple[str, str, bool]] = {
        ResponseCategory.POSITIVE: (
            "discovery_prep",
            "POSITIVE: prepare discovery conversation",
            False,
        ),
        ResponseCategory.QUESTION: (
            "evidence_reply_draft",
            "QUESTION: draft evidence-backed reply for human review",
            False,
        ),
        ResponseCategory.OBJECTION: (
            "objection_handling",
            "OBJECTION: draft objection response; do not auto-send",
            False,
        ),
        ResponseCategory.REFERRAL: (
            "new_relationship",
            "REFERRAL: record evidence-backed relationship with provenance",
            False,
        ),
        ResponseCategory.WRONG_PERSON: (
            "role_correction",
            "WRONG_PERSON: role correction research",
            False,
        ),
        ResponseCategory.NOT_NOW: (
            "future_action",
            "NOT_NOW: schedule bounded future action with reason/date",
            False,
        ),
        ResponseCategory.NO: (
            "close_respectfully",
            "NO: close respectfully; suppress further marketing candidates",
            True,
        ),
        ResponseCategory.UNSUBSCRIBE: (
            "suppress_immediately",
            "UNSUBSCRIBE: suppress immediately; mandatory ack only",
            True,
        ),
        ResponseCategory.BOUNCE: (
            "invalidate_endpoint",
            "BOUNCE: invalidate endpoint",
            True,
        ),
        ResponseCategory.AUTO_REPLY: (
            "do_not_count",
            "AUTO_REPLY: do not count as engagement",
            False,
        ),
        ResponseCategory.UNKNOWN: (
            "human_review",
            "UNKNOWN: human review required",
            False,
        ),
    }
    route, action, suppress = routes[v17]
    auto_send = v17 == ResponseCategory.UNSUBSCRIBE
    return {
        "category": v17.value,
        "route": route,
        "action": action,
        "suppress": suppress,
        "auto_send_allowed": auto_send,
    }


__all__ = [
    "ResponseCategory",
    "route_classification",
    "route_response",
]
