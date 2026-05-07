"""Saudi Arabic command parser.

Maps Arabic phrases to CommandIntent. Unrecognized → "unknown".
Unsafe → "blocked_unsafe" via policy.is_unsafe_command.
"""
from __future__ import annotations

import re
from typing import Any

from auto_client_acquisition.integration_upgrade import hide_internal_terms
from auto_client_acquisition.whatsapp_decision_bot.policy import is_unsafe_command
from auto_client_acquisition.whatsapp_decision_bot.schemas import (
    ActionMode,
    CommandIntent,
    CommandResult,
)

# Map of Arabic command pattern → intent
_PATTERNS: list[tuple[re.Pattern, CommandIntent]] = [
    (re.compile(r"وش\s+الوضع\s+اليوم"), "today_status"),
    (re.compile(r"وش\s+أهم\s+\d?\s*قرارات?"), "top_3_decisions"),
    (re.compile(r"وش\s+الصفقات?\s+المتأخّرة"), "overdue_deals"),
    (re.compile(r"وش\s+الصفقات\s+المتأخرة"), "overdue_deals"),
    (re.compile(r"وش\s+الدعم\s+المفتوح"), "open_support"),
    (re.compile(r"أعطني\s+التقرير\s+الأسبوعي"), "weekly_report"),
    (re.compile(r"وش\s+المخاطر"), "risks_overview"),
    (re.compile(r"جهز\s+ردّ?\s+للعميل"), "draft_reply"),
    (re.compile(r"اعتمد\s+الردّ?"), "approve_reply"),
    (re.compile(r"صعّد\s+التذكرة|صعد\s+التذكرة"), "escalate_ticket"),
]

SUPPORTED_COMMANDS = [
    "وش الوضع اليوم؟",
    "وش أهم 3 قرارات؟",
    "وش الصفقات المتأخرة؟",
    "وش الدعم المفتوح؟",
    "وش المخاطر؟",
    "جهز رد للعميل",
    "اعتمد الرد",
    "صعّد التذكرة",
    "أعطني التقرير الأسبوعي",
]


def _classify(text: str) -> CommandIntent:
    for pat, intent in _PATTERNS:
        if pat.search(text):
            return intent
    return "unknown"


def parse_command(*, text: str, customer_handle: str | None = None) -> CommandResult:
    """Classify the Arabic command and return a CommandResult."""
    is_unsafe, matched = is_unsafe_command(text)
    if is_unsafe:
        return CommandResult(
            intent="blocked_unsafe",
            action_mode="blocked",
            text_input=text[:500],
            output_ar=(
                "هذا الأمر مرفوض — Dealix لا يدعم الإرسال الجماعي ولا "
                "القوائم المشتراة ولا التواصل البارد. كل رسالة تحتاج "
                "موافقتك اليدويّة وعلاقة قائمة مع العميل."
            ),
            output_en=(
                "Command refused — Dealix does not support broadcast sends, "
                "purchased lists, or cold outreach. Every message requires "
                "manual approval and a pre-existing relationship."
            ),
            requires_approval=False,  # blocked is terminal
            payload={"matched_unsafe_patterns": matched},
        )

    intent = _classify(text)
    action_mode: ActionMode
    if intent in ("today_status", "top_3_decisions", "overdue_deals",
                  "open_support", "risks_overview", "weekly_report"):
        action_mode = "preview_only"  # read-only briefs
    elif intent == "draft_reply":
        action_mode = "draft_only"
    elif intent in ("approve_reply", "escalate_ticket"):
        action_mode = "approval_required"
    else:
        action_mode = "preview_only"

    return CommandResult(
        intent=intent,
        action_mode=action_mode,
        text_input=hide_internal_terms(text)[:500],
        payload={"customer_handle": customer_handle} if customer_handle else {},
    )
