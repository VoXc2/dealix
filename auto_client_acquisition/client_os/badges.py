"""Canonical badge enums for Dealix.

Status, Risk, and Proof badges with bilingual labels. Imported by:
- proof_os.proof_pack (tier badge)
- value_os.monthly_report (tier badge per value line)
- adoption_os.adoption_score (status badge)
- approval_center.approval_renderer (risk badges) — replaces local _RISK_BADGE_AR/EN dicts
- api routers that render workspace panels
"""
from __future__ import annotations

from enum import StrEnum


class StatusBadge(StrEnum):
    DRAFT = "draft"
    NEEDS_REVIEW = "needs_review"
    APPROVED = "approved"
    BLOCKED = "blocked"
    REDACTED = "redacted"
    PROOF_LINKED = "proof_linked"
    CLIENT_READY = "client_ready"


class RiskBadge(StrEnum):
    CONTAINS_PII = "contains_pii"
    DRAFT_ONLY = "draft_only"
    APPROVAL_REQUIRED = "approval_required"
    SOURCE_MISSING = "source_missing"
    PROOF_MISSING = "proof_missing"
    CLAIM_RISK = "claim_risk"
    CHANNEL_RISK = "channel_risk"


class ProofBadge(StrEnum):
    ESTIMATED = "estimated"
    OBSERVED = "observed"
    VERIFIED = "verified"
    CLIENT_CONFIRMED = "client_confirmed"
    CASE_SAFE = "case_safe"


BADGE_LABELS_AR: dict[str, str] = {
    StatusBadge.DRAFT.value: "مسودّة",
    StatusBadge.NEEDS_REVIEW.value: "بحاجة مراجعة",
    StatusBadge.APPROVED.value: "معتمد",
    StatusBadge.BLOCKED.value: "محجوب",
    StatusBadge.REDACTED.value: "تم تنقيحه",
    StatusBadge.PROOF_LINKED.value: "مرتبط بـProof",
    StatusBadge.CLIENT_READY.value: "جاهز للعميل",
    RiskBadge.CONTAINS_PII.value: "يحتوي بيانات شخصية",
    RiskBadge.DRAFT_ONLY.value: "مسودّة فقط",
    RiskBadge.APPROVAL_REQUIRED.value: "موافقة مطلوبة",
    RiskBadge.SOURCE_MISSING.value: "مصدر مفقود",
    RiskBadge.PROOF_MISSING.value: "Proof مفقود",
    RiskBadge.CLAIM_RISK.value: "مخاطر ادعاء",
    RiskBadge.CHANNEL_RISK.value: "مخاطر قناة",
    ProofBadge.ESTIMATED.value: "تقديري",
    ProofBadge.OBSERVED.value: "ملاحظ",
    ProofBadge.VERIFIED.value: "مُتحقَّق",
    ProofBadge.CLIENT_CONFIRMED.value: "مؤكَّد من العميل",
    ProofBadge.CASE_SAFE.value: "آمن للنشر كحالة",
}


BADGE_LABELS_EN: dict[str, str] = {
    StatusBadge.DRAFT.value: "Draft",
    StatusBadge.NEEDS_REVIEW.value: "Needs Review",
    StatusBadge.APPROVED.value: "Approved",
    StatusBadge.BLOCKED.value: "Blocked",
    StatusBadge.REDACTED.value: "Redacted",
    StatusBadge.PROOF_LINKED.value: "Proof-linked",
    StatusBadge.CLIENT_READY.value: "Client-ready",
    RiskBadge.CONTAINS_PII.value: "Contains PII",
    RiskBadge.DRAFT_ONLY.value: "Draft-only",
    RiskBadge.APPROVAL_REQUIRED.value: "Approval required",
    RiskBadge.SOURCE_MISSING.value: "Source missing",
    RiskBadge.PROOF_MISSING.value: "Proof missing",
    RiskBadge.CLAIM_RISK.value: "Claim risk",
    RiskBadge.CHANNEL_RISK.value: "Channel risk",
    ProofBadge.ESTIMATED.value: "Estimated",
    ProofBadge.OBSERVED.value: "Observed",
    ProofBadge.VERIFIED.value: "Verified",
    ProofBadge.CLIENT_CONFIRMED.value: "Client-confirmed",
    ProofBadge.CASE_SAFE.value: "Case-safe",
}


def label(badge: StatusBadge | RiskBadge | ProofBadge | str, lang: str = "en") -> str:
    key = badge.value if isinstance(badge, StrEnum) else str(badge)
    table = BADGE_LABELS_AR if lang == "ar" else BADGE_LABELS_EN
    return table.get(key, key)


__all__ = [
    "BADGE_LABELS_AR",
    "BADGE_LABELS_EN",
    "ProofBadge",
    "RiskBadge",
    "StatusBadge",
    "label",
]
