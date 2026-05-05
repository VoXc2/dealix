"""V12 Compliance OS — action × consent matrix evaluator.

Pure function. No DB, no external call, no PII storage. Returns a
deterministic verdict for every (action_type, channel, consent_state)
triple with bilingual reasons.

Hardcoded outcomes (NEVER configurable):
- cold_whatsapp / cold_email / scrape / linkedin_automation /
  purchased_list → always ``blocked``
- delete_request / export_request / withdraw_consent → always
  ``escalate`` (needs_review with action_mode=approval_required)

For warm + consent-aware actions, the verdict combines the channel
sensitivity + the consent_state.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

ActionVerdict = Literal["allowed", "blocked", "needs_review"]

Channel = Literal[
    "whatsapp",
    "email",
    "linkedin",
    "phone",
    "in_person",
    "warm_intro",
    "internal",
]

ConsentState = Literal[
    "granted",
    "withdrawn",
    "not_yet_asked",
    "expired",
    "unknown",
]


@dataclass
class ActionDecision:
    verdict: ActionVerdict
    reason_ar: str
    reason_en: str
    action_mode: str  # one of suggest_only/draft_only/approval_required/approved_manual/blocked
    escalate_to_human: bool


# Always-blocked actions (regardless of consent)
_HARD_BLOCKED_ACTIONS: dict[str, tuple[str, str]] = {
    "cold_whatsapp": (
        "واتساب بارد ممنوع نهائيّاً وفق سياسة Dealix و PDPL",
        "Cold WhatsApp is hard-blocked per Dealix policy and PDPL.",
    ),
    "cold_email": (
        "إيميل بارد ممنوع نهائيّاً",
        "Cold email is hard-blocked.",
    ),
    "linkedin_automation": (
        "أتمتة LinkedIn ممنوعة (انتهاك ToS)",
        "LinkedIn automation is hard-blocked (ToS violation).",
    ),
    "scrape": (
        "السحب الآلي للبيانات ممنوع",
        "Scraping is hard-blocked.",
    ),
    "purchased_list": (
        "استخدام قوائم مشتراة ممنوع وفق PDPL",
        "Use of purchased lists is hard-blocked per PDPL.",
    ),
    "live_charge": (
        "الخصم الحيّ مغلق افتراضيّاً",
        "Live charge is blocked by default.",
    ),
}


# Always-escalate actions (data-rights requests must reach a human)
_ESCALATE_ACTIONS: dict[str, tuple[str, str]] = {
    "delete_request": (
        "طلب الحذف يحتاج تصعيد للمؤسس وفق PDPL — مهلة 30 يوم",
        "Delete request must escalate to founder per PDPL — 30-day SLA.",
    ),
    "export_request": (
        "طلب التصدير يحتاج تصعيد للمؤسس وفق PDPL",
        "Export request must escalate to founder per PDPL.",
    ),
    "withdraw_consent": (
        "سحب الموافقة يحتاج تنفيذ فوري وتصعيد للمؤسس",
        "Withdraw-consent must execute immediately and escalate.",
    ),
    "correct_data": (
        "طلب تصحيح البيانات يحتاج تصعيد للمؤسس",
        "Data correction request must escalate to founder.",
    ),
}


# Always-allowed (low-risk, internal) actions
_INTERNAL_ALLOWED: set[str] = {
    "internal_note",
    "draft_to_review",
    "compose_diagnostic",
    "compose_proof_pack",
    "compose_executive_brief",
}


# Channels that require active consent
_CONSENT_REQUIRED_CHANNELS: set[Channel] = {
    "whatsapp",
    "email",
    "phone",
}


def _channel_safe_for_outbound(channel: Channel) -> bool:
    return channel in {"warm_intro", "in_person", "internal"}


def evaluate_action(
    *,
    action_type: str,
    channel: Channel = "internal",
    consent_state: ConsentState = "unknown",
    customer_id: str | None = None,  # noqa: ARG001 — kept for symmetry
) -> ActionDecision:
    """Return a deterministic decision for the (action, channel, consent) triple."""

    # 1. Always-blocked actions
    if action_type in _HARD_BLOCKED_ACTIONS:
        ar, en = _HARD_BLOCKED_ACTIONS[action_type]
        return ActionDecision(
            verdict="blocked",
            reason_ar=ar,
            reason_en=en,
            action_mode="blocked",
            escalate_to_human=False,
        )

    # 2. Always-escalate actions (data rights)
    if action_type in _ESCALATE_ACTIONS:
        ar, en = _ESCALATE_ACTIONS[action_type]
        return ActionDecision(
            verdict="needs_review",
            reason_ar=ar,
            reason_en=en,
            action_mode="approval_required",
            escalate_to_human=True,
        )

    # 3. Always-allowed internal/draft actions
    if action_type in _INTERNAL_ALLOWED:
        return ActionDecision(
            verdict="allowed",
            reason_ar="إجراء داخليّ آمن — لا اتّصال خارجيّ",
            reason_en="Safe internal action — no external contact.",
            action_mode="draft_only",
            escalate_to_human=False,
        )

    # 4. Outbound-to-customer actions: require consent OR safe channel
    if action_type in {"send_message", "send_outreach", "send_followup"}:
        if _channel_safe_for_outbound(channel):
            # warm intro / in-person / internal — allowed as draft
            return ActionDecision(
                verdict="allowed",
                reason_ar="قناة آمنة (warm intro / مباشر) — مسوّدة بانتظار اعتماد المؤسس",
                reason_en="Safe channel (warm intro / in person) — draft awaits founder approval.",
                action_mode="draft_only",
                escalate_to_human=False,
            )
        if channel in _CONSENT_REQUIRED_CHANNELS:
            if consent_state == "granted":
                return ActionDecision(
                    verdict="allowed",
                    reason_ar=(
                        f"موافقة سارية على قناة {channel} — مسوّدة بانتظار اعتماد المؤسس"
                    ),
                    reason_en=(
                        f"Active consent on channel {channel} — draft awaits founder approval."
                    ),
                    action_mode="draft_only",
                    escalate_to_human=False,
                )
            if consent_state == "withdrawn":
                return ActionDecision(
                    verdict="blocked",
                    reason_ar="الموافقة مسحوبة — ممنوع الاتصال على هذه القناة",
                    reason_en="Consent withdrawn — outbound on this channel is blocked.",
                    action_mode="blocked",
                    escalate_to_human=True,
                )
            return ActionDecision(
                verdict="needs_review",
                reason_ar=(
                    f"لا توجد موافقة سارية على {channel} — يحتاج مراجعة المؤسس"
                ),
                reason_en=(
                    f"No active consent on {channel} — requires founder review."
                ),
                action_mode="approval_required",
                escalate_to_human=True,
            )

    # 5. Unknown action — fail-safe to needs_review
    return ActionDecision(
        verdict="needs_review",
        reason_ar=f"إجراء غير مُصنَّف '{action_type}' — يحتاج مراجعة",
        reason_en=f"Unclassified action '{action_type}' — review required.",
        action_mode="approval_required",
        escalate_to_human=True,
    )
