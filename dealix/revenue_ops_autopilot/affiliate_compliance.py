"""Affiliate / partner messaging compliance — no misleading claims, disclosure hints."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from dealix.revenue_ops_autopilot.support_pipeline import _financial_guarantee_red_flag

_REPO_ROOT = Path(__file__).resolve().parents[2]
_AFFILIATE_RULES = _REPO_ROOT / "dealix" / "config" / "affiliate_rules.yaml"

_DISCLOSURE_MARKERS_AR = (
    "إفصاح",
    "إعلان",
    "شراكة مدفوعة",
    "عمولة",
    "affiliate",
    "#ad",
    "مدعوم",
)
_DISCLOSURE_MARKERS_EN = ("disclosure", "#ad", "affiliate", "paid partnership", "sponsored")


@dataclass
class AffiliateScanResult:
    allowed: bool
    blocked: bool
    risk_level: str
    reasons: list[str]
    safe_summary_ar: str


def _load_rules() -> dict:
    if not _AFFILIATE_RULES.is_file():
        return {}
    return yaml.safe_load(_AFFILIATE_RULES.read_text(encoding="utf-8")) or {}


def has_affiliate_disclosure(text: str) -> bool:
    raw = (text or "")
    raw_lc = raw.lower()
    if "بدون إفصاح" in raw or "without disclosure" in raw_lc:
        return False
    positive_ar = ("إفصاح شراكة", "إعلان ·", "شراكة مدفوعة", "مدعوم", "عمولة", "#ad")
    if any(p in raw for p in positive_ar):
        return True
    return any(m.lower() in raw_lc for m in _DISCLOSURE_MARKERS_EN)


def scan_affiliate_message(text: str, *, require_disclosure: bool = False) -> AffiliateScanResult:
    """Scan partner/affiliate copy for blocked claims."""

    rules = _load_rules()
    messaging = rules.get("messaging") or {}
    reasons: list[str] = []

    red, code = _financial_guarantee_red_flag(text or "")
    if red:
        reasons.append(code or "misleading_financial_claim")

    banned_phrases = (
        "تضمن لك نمو",
        "مضمون 100",
        "بدون تدخل نهائياً",
        "fully automate your sales",
        "guaranteed revenue",
    )
    tl = (text or "").lower()
    for bp in banned_phrases:
        if bp.lower() in tl or bp in (text or ""):
            reasons.append(f"banned_phrase:{bp[:24]}")
            break

    if messaging.get("no_roi_guarantee") and red:
        reasons.append("affiliate_no_roi_guarantee")

    if require_disclosure and not has_affiliate_disclosure(text or ""):
        reasons.append("disclosure_missing")

    blocked = bool(reasons)
    risk = "critical" if red else ("high" if blocked else "low")

    safe = (
        "المحتوى يحتاج مراجعة: تجنّب وعود إيراد أو أتمتة كاملة بلا حوكمة. "
        "أضف إفصاح شراكة واضحاً (مثال: «إعلان · شراكة مع Dealix») قبل أي نشر."
    )

    return AffiliateScanResult(
        allowed=not blocked,
        blocked=blocked,
        risk_level=risk,
        reasons=reasons,
        safe_summary_ar=safe,
    )
