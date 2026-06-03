"""
Draft personalization grading + GTM quality gate.

A cold draft must reach at least grade **P1** on personalization before it can
ever become "send-ready". Grades (worst -> best): P0 < P1 < P2 < P3.

The quality gate combines personalization with the other outbound guards
(prohibited claims, unsubscribe presence, fake reply subjects, suppression,
secret leakage). It never returns ``send_ready=True`` unless every guard
passes AND a human approval is still recorded downstream.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .claims import find_prohibited_claims
from .constants import APPROVAL_REQUIRED_DEFAULT, SEND_ENABLED_DEFAULT

GRADES = ["P0", "P1", "P2", "P3"]

# Unresolved merge placeholders that mean the draft was never personalized.
_PLACEHOLDER = re.compile(r"(\[[^\]]+\]|\{[^}]+\}|<<[^>]+>>|XXX+)")


def _grade_index(grade: str) -> int:
    try:
        return GRADES.index(grade)
    except ValueError:
        return 0


def grade_at_least(grade: str, minimum: str) -> bool:
    """True if ``grade`` is at least ``minimum`` on the P0..P3 scale."""
    return _grade_index(grade) >= _grade_index(minimum)


def personalization_grade(draft: Dict) -> str:
    """Grade how personalized an outbound draft is.

    ``draft`` keys used (all optional):
        body, subject, company, decision_maker, pain, sector, metric, cta

    Returns one of P0/P1/P2/P3.
    """
    body = (draft.get("body") or "") + " " + (draft.get("subject") or "")
    score = 0

    company = (draft.get("company") or "").strip()
    if company and company in body:
        score += 1

    pain = (draft.get("pain") or "").strip()
    if pain and (pain in body or any(w in body for w in pain.split() if len(w) > 3)):
        score += 1

    dm = (draft.get("decision_maker") or "").strip()
    if dm and (dm.split("/")[0].strip() in body):
        score += 1

    if draft.get("sector") and str(draft["sector"]).strip() in body:
        score += 1

    if draft.get("metric") and str(draft["metric"]).strip() in body:
        score += 1

    # Clear single call to action (question form, common Arabic CTA verbs).
    if any(tok in body for tok in ["?", "؟", "نقدر", "هل", "تحب", "يناسبك"]):
        score += 1

    # Penalty: unresolved placeholders mean it was never actually personalized.
    if _PLACEHOLDER.search(body):
        score = min(score, 1)

    # Penalty: too short to be a real message.
    if len((draft.get("body") or "").strip()) < 40:
        score = min(score, 1)

    if score <= 1:
        return "P0"
    if score <= 3:
        return "P1"
    if score <= 5:
        return "P2"
    return "P3"


@dataclass
class DraftEvaluation:
    send_ready: bool
    grade: str
    violations: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    approval_required: bool = APPROVAL_REQUIRED_DEFAULT
    send_enabled: bool = SEND_ENABLED_DEFAULT
    risk_level: str = "medium"

    def as_dict(self) -> Dict:
        return {
            "send_ready": self.send_ready,
            "grade": self.grade,
            "violations": self.violations,
            "warnings": self.warnings,
            "approval_required": self.approval_required,
            "send_enabled": self.send_enabled,
            "risk_level": self.risk_level,
        }


def evaluate_draft(
    draft: Dict,
    *,
    channel: str = "email",
    min_grade: str = "P1",
    suppressed: bool = False,
) -> DraftEvaluation:
    """Run the full GTM quality gate on a single draft.

    A draft is ``send_ready`` only when it passes EVERY guard. Even then,
    approval_required stays True and send_enabled stays False — actual sending
    is a separate, human-gated step that lives outside this engine.
    """
    from .outreach import is_fake_reply_subject, has_unsubscribe  # local import avoids cycle

    violations: List[str] = []
    warnings: List[str] = []

    body = draft.get("body") or ""
    subject = draft.get("subject") or ""

    # 1) Prohibited / guaranteed claims.
    claims = find_prohibited_claims(body + " " + subject)
    if claims:
        violations.append("prohibited_claims:" + ",".join(claims))

    # 2) Personalization threshold.
    grade = personalization_grade(draft)
    if not grade_at_least(grade, min_grade):
        violations.append(f"below_min_personalization:{grade}<{min_grade}")

    # 3) Fake Re:/Fwd: subject on a cold draft.
    if is_fake_reply_subject(subject) and not draft.get("is_real_reply", False):
        violations.append("fake_reply_subject")

    # 4) Unsubscribe required for cold email.
    if channel == "email" and not draft.get("is_real_reply", False):
        if not has_unsubscribe(body):
            violations.append("missing_unsubscribe")

    # 5) Suppressed recipient can never be send-ready.
    if suppressed:
        violations.append("recipient_suppressed")

    # 6) Cold WhatsApp is not allowed at all.
    if channel == "whatsapp" and not draft.get("has_consent", False):
        violations.append("cold_whatsapp_not_allowed")

    # 7) Secret / API-key leakage in the body.
    from .whatsapp import contains_secret_or_api_key
    if contains_secret_or_api_key(body) or contains_secret_or_api_key(subject):
        violations.append("secret_in_draft")

    send_ready = len(violations) == 0
    risk = "low" if send_ready else "high"
    return DraftEvaluation(
        send_ready=send_ready,
        grade=grade,
        violations=violations,
        warnings=warnings,
        risk_level=risk,
    )
