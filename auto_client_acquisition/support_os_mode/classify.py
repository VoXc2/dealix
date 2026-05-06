"""Rule-based support triage. No LLM. No external calls."""

from __future__ import annotations

import re
from typing import Any


def classify_support_message(text: str) -> dict[str, Any]:
    """Return category, priority, escalation, and safe draft hint."""
    t = (text or "").strip().lower()
    if not t:
        return {
            "category": "unknown",
            "priority": "P2",
            "escalate": False,
            "action_mode": "suggest_only",
            "reason": "empty_message",
        }

    escalate_patterns = [
        (r"\brefund\b|استرداد|ارجاع المبلغ", "refund", "P0"),
        (r"\bdelete\b.*data|حذف.*بيانات|نسيت حسابي", "privacy_pdpl", "P0"),
        (r"\bexport\b.*data|تصدير.*بيانات", "privacy_pdpl", "P0"),
        (r"\bprivacy\b|pdpl|خصوصية|نظام حماية البيانات", "privacy_pdpl", "P0"),
        (r"\bcharge\b.*wrong|خصم.*غلط|سحب.*بدون|فاتورة.*غلط", "billing", "P0"),
        (r"\bsecurity\b|اختراق|breach|hack", "security", "P0"),
        (r"\bغاضب\b|angry|scam|نصب", "angry_customer", "P0"),
    ]
    for pattern, cat, pri in escalate_patterns:
        if re.search(pattern, t, re.I):
            return {
                "category": cat,
                "priority": pri,
                "escalate": True,
                "action_mode": "approval_required",
                "reason": "matched_escalation_pattern",
            }

    if re.search(r"\bpilot\b|تشخيص|diagnostic|499", t, re.I):
        return {
            "category": "diagnostic_question",
            "priority": "P2",
            "escalate": False,
            "action_mode": "draft_only",
            "reason": "diagnostic_topic",
        }
    if re.search(r"\bproof\b|اثبات|pack", t, re.I):
        return {
            "category": "proof_pack_question",
            "priority": "P2",
            "escalate": False,
            "action_mode": "draft_only",
            "reason": "proof_topic",
        }
    if re.search(r"\bonboarding\b|بدء|setup|تفعيل", t, re.I):
        return {
            "category": "onboarding",
            "priority": "P2",
            "escalate": False,
            "action_mode": "draft_only",
            "reason": "onboarding_topic",
        }

    return {
        "category": "unknown",
        "priority": "P3",
        "escalate": False,
        "action_mode": "draft_only",
        "reason": "no_specific_match_use_kb",
    }
