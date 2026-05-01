"""Saudi Market Radar for Dealix v3."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from math import exp
from typing import Any


@dataclass(frozen=True)
class MarketSignal:
    company: str
    sector: str
    city: str
    signal_type: str
    strength: float
    days_old: int = 0
    evidence: str = ""

    def score(self) -> float:
        freshness = exp(-self.days_old / 21)
        sector_boost = {
            "clinics": 1.20,
            "real_estate": 1.15,
            "logistics": 1.10,
            "training": 1.08,
            "hospitality": 1.05,
        }.get(self.sector, 1.0)
        return round(max(0.0, min(100.0, self.strength * freshness * sector_boost)), 2)

    def why_now_ar(self) -> str:
        labels = {
            "hiring_sales": "الشركة توظف في المبيعات، وهذا غالباً يعني توسع أو ضغط على توليد الطلب.",
            "new_branch": "يوجد مؤشر توسع/فرع جديد، وهذا وقت ممتاز لعرض نظام نمو أسرع.",
            "booking_link": "لديهم مسار حجز واضح، ويمكن تحسين الردود والتحويل عبر واتساب.",
            "website_change": "تغير في الموقع يدل على تحديث عرض أو حملة جديدة.",
            "event_participation": "مشاركتهم في فعالية تعني استعداد أعلى لعلاقات وشراكات جديدة.",
        }
        return labels.get(self.signal_type, "يوجد مؤشر سوق يستحق المتابعة الآن.")

    def to_dict(self) -> dict[str, Any]:
        return {
            "company": self.company,
            "sector": self.sector,
            "city": self.city,
            "signal_type": self.signal_type,
            "strength": self.strength,
            "days_old": self.days_old,
            "score": self.score(),
            "evidence": self.evidence,
            "why_now_ar": self.why_now_ar(),
        }


def rank_opportunities(signals: list[MarketSignal], limit: int = 20) -> list[dict[str, Any]]:
    ranked = sorted(signals, key=lambda item: item.score(), reverse=True)
    return [item.to_dict() for item in ranked[:limit]]


def demo_signals() -> list[MarketSignal]:
    return [
        MarketSignal("عيادة نمو الرياض", "clinics", "Riyadh", "hiring_sales", 92, 2, "3 sales roles posted"),
        MarketSignal("وسيط عقار جدة", "real_estate", "Jeddah", "new_branch", 85, 5, "new branch page"),
        MarketSignal("أكاديمية تدريب الشرقية", "training", "Dammam", "booking_link", 80, 1, "public booking link"),
    ]


def sector_heatmap(signals: list[MarketSignal]) -> list[dict[str, Any]]:
    buckets: dict[str, list[float]] = {}
    for signal in signals:
        buckets.setdefault(signal.sector, []).append(signal.score())
    return [
        {"sector": sector, "avg_intent": round(sum(scores) / len(scores), 2), "signals": len(scores)}
        for sector, scores in sorted(buckets.items(), key=lambda item: sum(item[1]) / len(item[1]), reverse=True)
    ]
