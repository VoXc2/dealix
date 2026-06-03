"""Draft builder — emits an outreach draft and routes it to
approval_center as draft_only / approval_required.

Hard rules:
- NEVER returns approved_execute (founder approves manually)
- Forbidden tokens scrub before returning
- All drafts are bilingual (AR primary, EN secondary)
- Runs forbidden-token regex before returning
"""
from __future__ import annotations

import re
import uuid
from typing import Any

# Forbidden tokens (must match tests/test_landing_forbidden_claims.py)
_FORBIDDEN = [
    re.compile(r"\bguaranteed?\b", re.IGNORECASE),
    re.compile(r"\bblast\b", re.IGNORECASE),
    re.compile(r"\bscraping\b", re.IGNORECASE),
    re.compile(r"\bcold\s+(whatsapp|outreach|email|messaging)\b", re.IGNORECASE),
    re.compile(r"نضمن"),
]


def _scrub(text: str) -> tuple[str, list[str]]:
    """Replace forbidden tokens with [REDACTED]; return (clean_text, findings)."""
    findings: list[str] = []
    cleaned = text
    for pat in _FORBIDDEN:
        if pat.search(cleaned):
            findings.append(pat.pattern)
            cleaned = pat.sub("[REDACTED]", cleaned)
    return cleaned, findings


def _template(channel: str, sector: str | None) -> tuple[str, str]:
    """Default bilingual templates per channel."""
    if channel == "whatsapp":
        ar = (
            "السلام عليكم،\n"
            "ملاحظتنا حركة ايجابية في {sector_ar}. "
            "نحب نعرض كيف Dealix يقدر يساعد فريقكم في تأهيل الـ leads بسرعة. "
            "تناسبكم مكالمة قصيرة ٣٠ دقيقة هذا الأسبوع؟"
        )
        en = (
            "Hi,\n"
            "We noticed positive movement in {sector_en}. "
            "Happy to share how Dealix helps teams qualify leads faster. "
            "Open to a 30-min call this week?"
        )
    elif channel == "email":
        ar = (
            "السلام عليكم،\n\n"
            "أكتب لكم بخصوص فرصة محتملة لمساعدة فريقكم في تأهيل الـ leads "
            "خلال ٣٠ ثانية بدلاً من ٣٠ دقيقة. هذا الأسلوب يجعلكم أوّل من يردّ "
            "على العميل في {sector_ar}.\n\n"
            "إذا كان الموضوع مهم، نقدر نرتب مكالمة قصيرة هذا الأسبوع."
        )
        en = (
            "Hello,\n\n"
            "Writing about a potential opportunity to help your team qualify "
            "leads in 30 seconds instead of 30 minutes — making you the first "
            "to respond in {sector_en}.\n\n"
            "If interested, happy to schedule a short call this week."
        )
    else:
        ar = "نقترح إضافة الفرصة إلى لوحة المتابعة لمراجعتها لاحقًا."
        en = "We suggest queueing this opportunity in the dashboard for later review."

    sector_ar = sector or "قطاعكم"
    sector_en = sector or "your sector"
    return ar.format(sector_ar=sector_ar), en.format(sector_en=sector_en)


def build_draft(
    *,
    leadops_id: str,
    customer_handle: str | None,
    sector: str | None,
    offer_route: dict[str, Any],
    next_action: dict[str, Any],
) -> dict[str, Any]:
    """Build a draft envelope ready for approval_center.create_approval.

    Returns {
      'draft_id', 'action_mode', 'channel',
      'text_ar', 'text_en', 'safety_findings',
      'approval_payload': { ... ready for approval_center }
    }
    """
    channel = offer_route.get("channel", "dashboard")
    text_ar_raw, text_en_raw = _template(channel, sector)

    text_ar, findings_ar = _scrub(text_ar_raw)
    text_en, findings_en = _scrub(text_en_raw)
    findings = list(set(findings_ar + findings_en))

    draft_id = f"draft_{uuid.uuid4().hex[:10]}"

    # action_mode = blocked if anything was flagged; else approval_required
    action_mode = "blocked" if findings else "approval_required"

    approval_payload = {
        "object_type": "outreach_draft",
        "object_id": draft_id,
        "action_type": f"send_{channel}",
        "action_mode": action_mode,
        "channel": channel,
        "summary_ar": text_ar[:200],
        "summary_en": text_en[:200],
        "risk_level": "high" if channel == "whatsapp" else "medium",
        "proof_impact": f"leadops:{leadops_id}",
    }

    return {
        "draft_id": draft_id,
        "action_mode": action_mode,
        "channel": channel,
        "text_ar": text_ar,
        "text_en": text_en,
        "safety_findings": findings,
        "approval_payload": approval_payload,
        "customer_handle": customer_handle,
        "leadops_id": leadops_id,
        "next_action_owner": next_action.get("owner", "founder"),
        "next_action_deadline": next_action.get("deadline_iso"),
    }
