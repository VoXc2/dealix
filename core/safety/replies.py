"""
Reply classification + routing.

Inbound replies are *untrusted data*. We classify intent and route to a safe
next action. Critically:
  * A positive reply NEVER routes straight to payment — it routes to discovery,
    WhatsApp concierge, or a booking step (human-led).
  * Angry / unsubscribe / bounce replies trigger suppression.
  * Legal / complaint / privacy replies require human handoff.
"""

from __future__ import annotations

import re
from typing import Dict, List

# Classification categories.
POSITIVE = "positive"
NEUTRAL = "neutral"
QUESTION = "question"
ANGRY = "angry"
UNSUBSCRIBE = "unsubscribe"
BOUNCE = "bounce"
COMPLAINT = "complaint"
LEGAL = "legal"
PRIVACY_REQUEST = "privacy_request"

_PATTERNS = [
    # order matters: most safety-critical first
    (BOUNCE, [
        r"(?i)\bmailer-daemon\b", r"(?i)delivery status notification",
        r"(?i)undeliverable", r"(?i)address not found", r"(?i)mailbox full",
        r"(?i)550 ", r"(?i)recipient.{0,10}rejected",
    ]),
    (PRIVACY_REQUEST, [
        r"(?i)delete my data", r"(?i)right to erasure", r"(?i)gdpr", r"(?i)pdpl",
        r"احذف بياناتي", r"حذف بياناتي", r"امسح بياناتي", r"حقي في الحذف",
        r"(?i)data subject request",
    ]),
    (LEGAL, [
        r"(?i)\blawyer\b", r"(?i)\battorney\b", r"(?i)\blegal action\b",
        r"(?i)\bcease and desist\b", r"(?i)\bsue\b", r"(?i)\blawsuit\b",
        r"محامي", r"قانوني", r"إجراء قانوني", r"المحكمة", r"دعوى",
    ]),
    (UNSUBSCRIBE, [
        r"(?i)\bunsubscribe\b", r"(?i)opt[\s-]?out", r"(?i)stop emailing",
        r"(?i)remove me", r"(?i)take me off", r"(?i)\bstop\b",
        r"إلغاء الاشتراك", r"الغاء الاشتراك", r"أوقف", r"ايقاف", r"لا تراسلني",
    ]),
    (ANGRY, [
        r"(?i)\bspam\b", r"(?i)stop spamming", r"(?i)how did you get",
        r"(?i)never contact", r"(?i)harass", r"(?i)reported",
        r"مزعج", r"إزعاج", r"ازعاج", r"بلاغ", r"لا تزعجني", r"سبام",
    ]),
    (COMPLAINT, [
        r"(?i)\bcomplaint\b", r"(?i)disappointed", r"(?i)terrible",
        r"(?i)not happy", r"(?i)refund", r"(?i)escalate",
        r"شكوى", r"غير راضي", r"استرجاع", r"تصعيد", r"سيء",
    ]),
    (POSITIVE, [
        r"(?i)\binterested\b", r"(?i)tell me more", r"(?i)sounds good",
        r"(?i)let'?s talk", r"(?i)book", r"(?i)demo", r"(?i)call me",
        r"(?i)yes\b", r"(?i)keen", r"(?i)how much", r"(?i)pricing",
        r"مهتم", r"يهمني", r"تواصل", r"موعد", r"اجتماع", r"نلتقي", r"ابي اعرف اكثر",
    ]),
    (QUESTION, [r"\?", r"؟"]),
]


def classify_reply(text: str) -> str:
    """Classify an inbound reply into a single safety-prioritized category."""
    if not text or not text.strip():
        return NEUTRAL
    for category, patterns in _PATTERNS:
        for pat in patterns:
            if re.search(pat, text):
                return category
    return NEUTRAL


def route_reply(category: str) -> Dict:
    """Map a reply category to a safe next action.

    Returns a dict with:
        actions          : list of allowed next steps
        suppress         : whether to add the contact to the suppression list
        suppress_reason  : reason if suppress is True
        requires_human   : whether a human must handle it
        allow_payment    : ALWAYS False here (payment is never an auto-route)
    """
    routing = {
        POSITIVE: {
            "actions": ["discovery_call", "whatsapp_concierge", "booking"],
            "suppress": False, "suppress_reason": None,
            "requires_human": False, "allow_payment": False,
        },
        NEUTRAL: {
            "actions": ["nurture", "follow_up"],
            "suppress": False, "suppress_reason": None,
            "requires_human": False, "allow_payment": False,
        },
        QUESTION: {
            "actions": ["answer_draft", "discovery_call"],
            "suppress": False, "suppress_reason": None,
            "requires_human": False, "allow_payment": False,
        },
        ANGRY: {
            "actions": ["suppress", "founder_review"],
            "suppress": True, "suppress_reason": "angry_reply",
            "requires_human": True, "allow_payment": False,
        },
        UNSUBSCRIBE: {
            "actions": ["suppress", "confirm_opt_out"],
            "suppress": True, "suppress_reason": "unsubscribe",
            "requires_human": False, "allow_payment": False,
        },
        BOUNCE: {
            "actions": ["suppress", "mark_invalid"],
            "suppress": True, "suppress_reason": "bounce",
            "requires_human": False, "allow_payment": False,
        },
        COMPLAINT: {
            "actions": ["human_handoff", "founder_review"],
            "suppress": False, "suppress_reason": None,
            "requires_human": True, "allow_payment": False,
        },
        LEGAL: {
            "actions": ["human_handoff", "legal_escalation", "suppress"],
            "suppress": True, "suppress_reason": "legal_request",
            "requires_human": True, "allow_payment": False,
        },
        PRIVACY_REQUEST: {
            "actions": ["human_handoff", "privacy_deletion_runbook", "suppress"],
            "suppress": True, "suppress_reason": "privacy_request",
            "requires_human": True, "allow_payment": False,
        },
    }
    return routing.get(category, routing[NEUTRAL])
