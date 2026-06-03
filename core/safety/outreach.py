"""
Outreach safety primitives: fake reply subjects, unsubscribe presence,
purchased-list detection, and a combined cold-outreach assessment.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .claims import find_prohibited_claims
from .constants import APPROVAL_REQUIRED_DEFAULT, SEND_ENABLED_DEFAULT

# Deceptive subject prefixes that fake a prior conversation.
_FAKE_REPLY_PREFIXES = [
    "re:", "re :", "fwd:", "fwd :", "fw:", "fw :",
    "رد:", "رد :", "إعادة توجيه:", "اعادة توجيه:", "رداً على:",
]

# Markers that indicate unsubscribe / opt-out is present.
_UNSUBSCRIBE_MARKERS = [
    "unsubscribe", "opt out", "opt-out", "stop receiving", "manage preferences",
    "إلغاء الاشتراك", "الغاء الاشتراك", "لإلغاء الاشتراك", "إيقاف الرسائل",
    "ايقاف الرسائل", "لإيقاف", "للإلغاء", "أرسل إيقاف", "ارسل ايقاف",
]

# Markers that a contact came from a purchased / scraped / rented list.
_PURCHASED_LIST_MARKERS = [
    "purchased", "purchased_list", "bought", "bought_list", "rented_list",
    "scraped", "scraper", "data_broker", "list_buy", "cold_list_vendor",
    "قائمة مشتراة", "قائمة جاهزة", "مشتراة",
]


def is_fake_reply_subject(subject: Optional[str]) -> bool:
    """True if the subject fakes a reply/forward (deceptive cold-email tactic)."""
    if not subject:
        return False
    s = subject.strip().lower()
    return any(s.startswith(p) for p in _FAKE_REPLY_PREFIXES)


def has_unsubscribe(body: Optional[str]) -> bool:
    """True if the body contains a recognizable unsubscribe / opt-out path."""
    if not body:
        return False
    low = body.lower()
    return any(m.lower() in low for m in _UNSUBSCRIBE_MARKERS)


def is_purchased_list(source: Optional[object]) -> bool:
    """Detect a purchased/scraped list from a string source or a prospect dict.

    Accepts either a string (the source label) or a dict with ``source`` /
    ``list_source`` / ``acquisition`` keys.
    """
    if source is None:
        return False
    if isinstance(source, dict):
        candidates = [
            str(source.get("source", "")),
            str(source.get("list_source", "")),
            str(source.get("acquisition", "")),
            str(source.get("data_source", "")),
        ]
        if source.get("purchased") is True or source.get("is_purchased") is True:
            return True
        text = " ".join(candidates).lower()
    else:
        text = str(source).lower()
    return any(m.lower() in text for m in _PURCHASED_LIST_MARKERS)


@dataclass
class OutreachAssessment:
    send_ready: bool
    violations: List[str] = field(default_factory=list)
    approval_required: bool = APPROVAL_REQUIRED_DEFAULT
    send_enabled: bool = SEND_ENABLED_DEFAULT
    dry_run: bool = True

    def as_dict(self) -> Dict:
        return {
            "send_ready": self.send_ready,
            "violations": self.violations,
            "approval_required": self.approval_required,
            "send_enabled": self.send_enabled,
            "dry_run": self.dry_run,
        }


def assess_outreach(
    draft: Dict,
    *,
    channel: str = "email",
    prospect: Optional[Dict] = None,
    suppressed: bool = False,
) -> OutreachAssessment:
    """End-to-end cold-outreach safety assessment for one message.

    Hard-stops (send_ready=False) on: prohibited claims, fake reply subject,
    missing unsubscribe (cold email), purchased list, suppressed recipient,
    cold WhatsApp.
    """
    prospect = prospect or {}
    violations: List[str] = []

    subject = draft.get("subject") or ""
    body = draft.get("body") or ""
    is_real_reply = bool(draft.get("is_real_reply", False))

    if find_prohibited_claims(subject + " " + body):
        violations.append("prohibited_claims")

    if is_fake_reply_subject(subject) and not is_real_reply:
        violations.append("fake_reply_subject")

    if channel == "email" and not is_real_reply and not has_unsubscribe(body):
        violations.append("missing_unsubscribe")

    if is_purchased_list(prospect) or is_purchased_list(draft.get("source")):
        violations.append("purchased_list")

    if suppressed or prospect.get("suppressed") is True:
        violations.append("recipient_suppressed")

    if channel == "whatsapp" and not (draft.get("has_consent") or prospect.get("has_consent")):
        violations.append("cold_whatsapp_not_allowed")

    return OutreachAssessment(send_ready=len(violations) == 0, violations=violations)
