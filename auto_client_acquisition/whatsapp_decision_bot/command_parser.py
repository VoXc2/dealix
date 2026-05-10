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

# Map of Arabic command pattern → intent.
# Wave 12 §32.3.5 added 4 new commands + Saudi-dialect alternates.
_PATTERNS: list[tuple[re.Pattern, CommandIntent]] = [
    (re.compile(r"وش\s+الوضع\s+اليوم"), "today_status"),
    # Saudi-dialect alts for today_status (Wave 12 §32.3.5)
    (re.compile(r"ملخص\s+اليوم"), "today_status"),
    (re.compile(r"شو\s+اليوم"), "today_status"),
    (re.compile(r"وش\s+أهم\s+\d?\s*قرارات?"), "top_3_decisions"),
    # Saudi-dialect alt: "أفضل 5 فرص" / "أفضل 3 قرارات"
    (re.compile(r"أفضل\s+\d+\s+(فرص|قرارات)"), "top_3_decisions"),
    (re.compile(r"وش\s+الصفقات?\s+المتأخّرة"), "overdue_deals"),
    (re.compile(r"وش\s+الصفقات\s+المتأخرة"), "overdue_deals"),
    (re.compile(r"وش\s+الدعم\s+المفتوح"), "open_support"),
    (re.compile(r"أعطني\s+التقرير\s+الأسبوعي"), "weekly_report"),
    (re.compile(r"وش\s+المخاطر"), "risks_overview"),
    (re.compile(r"جهز\s+ردّ?\s+للعميل"), "draft_reply"),
    (re.compile(r"اعتمد\s+الردّ?"), "approve_reply"),
    (re.compile(r"صعّد\s+التذكرة|صعد\s+التذكرة"), "escalate_ticket"),
    # ─── Wave 12 §32.3.5 — 4 new founder-vision commands ──────────────
    # show_proof_this_week — اعرض Proof هذا الأسبوع
    (re.compile(r"اعرض\s+Proof|اعرض\s+الإثبات"), "show_proof_this_week"),
    # what_is_overdue — وش المتأخر؟ (Saudi-dialect alt to overdue_deals)
    (re.compile(r"وش\s+المتأخر|شو\s+المتأخر|أيش\s+المتأخر"), "what_is_overdue"),
    # prepare_exec_report — جهز تقرير الإدارة
    (re.compile(r"جهز\s+تقرير\s+(الإدارة|التنفيذ)|جهّز\s+تقرير"), "prepare_exec_report"),
    # show_top_decision_today — اعرض القرار الأهم اليوم / وش أهم قرار الآن
    (re.compile(r"اعرض\s+القرار\s+الأهم|أهم\s+قرار\s+(اليوم|الآن|الان)"), "show_top_decision_today"),
]

SUPPORTED_COMMANDS = [
    "وش الوضع اليوم؟",
    "ملخص اليوم",
    "وش أهم 3 قرارات؟",
    "أفضل 5 فرص",
    "وش الصفقات المتأخرة؟",
    "وش المتأخر؟",
    "وش الدعم المفتوح؟",
    "وش المخاطر؟",
    "جهز رد للعميل",
    "اعتمد الرد",
    "صعّد التذكرة",
    "أعطني التقرير الأسبوعي",
    # Wave 12 §32.3.5 — new founder-vision commands
    "اعرض Proof هذا الأسبوع",
    "جهز تقرير الإدارة",
    "اعرض القرار الأهم اليوم",
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
    # Read-only brief commands (preview_only)
    if intent in (
        "today_status", "top_3_decisions", "overdue_deals",
        "open_support", "risks_overview", "weekly_report",
        # Wave 12 §32.3.5 — 3 of 4 new commands are also read-only briefs
        "show_proof_this_week",
        "what_is_overdue",
        "show_top_decision_today",
    ):
        action_mode = "preview_only"
    elif intent == "draft_reply":
        action_mode = "draft_only"
    # Wave 12 §32.3.5 — generating an exec report is a draft-only action
    # (founder reviews + sends manually; never auto-distributed)
    elif intent == "prepare_exec_report":
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
