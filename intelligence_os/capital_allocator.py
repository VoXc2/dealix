from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class AllocationCategory(str, Enum):
    ENGINEERING = "engineering"
    SALES = "sales"
    MARKETING = "marketing"
    INFRASTRUCTURE = "infrastructure"
    AI_MODELS = "ai_models"
    COMPLIANCE = "compliance"
    CUSTOMER_SUCCESS = "customer_success"
    RESEARCH = "research"


@dataclass
class AllocationBucket:
    category: AllocationCategory = AllocationCategory.ENGINEERING
    current_allocation: float = 0.0
    recommended_allocation: float = 0.0
    min_allocation: float = 0.0
    max_allocation: float = 0.0
    roi_score: float = 0.0
    urgency: int = 0
    notes: str = ""


@dataclass
class AllocationShift:
    from_category: AllocationCategory
    to_category: AllocationCategory
    amount: float
    reason: str
    expected_roi: float
    confidence: float
    risk_level: str = "medium"


@dataclass
class AllocationReport:
    total_capital: float = 0.0
    allocations: list[AllocationBucket] = field(default_factory=list)
    shifts: list[AllocationShift] = field(default_factory=list)
    overall_efficiency_score: float = 0.0
    total_recommended_shift: float = 0.0
    generated_at: datetime = field(default_factory=datetime.utcnow)
    summary: str = ""


class CapitalAllocator:
    def __init__(self):
        self._current_budgets: dict[AllocationCategory, float] = {
            AllocationCategory.ENGINEERING: 10000.0,
            AllocationCategory.SALES: 5000.0,
            AllocationCategory.MARKETING: 3000.0,
            AllocationCategory.INFRASTRUCTURE: 2000.0,
            AllocationCategory.AI_MODELS: 4000.0,
            AllocationCategory.COMPLIANCE: 1000.0,
            AllocationCategory.CUSTOMER_SUCCESS: 2000.0,
            AllocationCategory.RESEARCH: 3000.0,
        }
        self._total_capital = sum(self._current_budgets.values())
        self._performance_history: dict[str, list[float]] = {}

    async def analyze_allocation(self) -> AllocationReport:
        buckets = await self._build_buckets()
        shifts = await self._calculate_shifts(buckets)
        efficiency = self._calculate_efficiency(buckets)
        total_shift = sum(s.amount for s in shifts)

        bucket_lines = "\n".join(
            f"  {b.category.value}: ${b.current_allocation:.0f} -> ${b.recommended_allocation:.0f} "
            f"(ROI: {b.roi_score:.2f})"
            for b in sorted(buckets, key=lambda b: b.roi_score, reverse=True)
        )
        shift_lines = "\n".join(
            f"  ${s.amount:.0f} from {s.from_category.value} to {s.to_category.value}: {s.reason}"
            for s in shifts
        )

        summary = (
            f"Capital Allocation Analysis\n"
            f"Total Capital: ${self._total_capital:,.0f}\n"
            f"Efficiency Score: {efficiency:.2f}\n"
            f"Recommended Reallocation: ${total_shift:,.0f}\n\n"
            f"Buckets:\n{bucket_lines}\n\n"
            f"Recommended Shifts:\n{shift_lines if shift_lines else '  None recommended'}"
        )

        return AllocationReport(
            total_capital=self._total_capital,
            allocations=buckets,
            shifts=shifts,
            overall_efficiency_score=efficiency,
            total_recommended_shift=total_shift,
            summary=summary,
        )

    async def recommend_shifts(self) -> list[AllocationShift]:
        report = await self.analyze_allocation()
        return report.shifts

    async def apply_shift(self, shift: AllocationShift) -> bool:
        if shift.from_category not in self._current_budgets:
            logger.error("Unknown from_category: %s", shift.from_category)
            return False
        if shift.to_category not in self._current_budgets:
            logger.error("Unknown to_category: %s", shift.to_category)
            return False
        if self._current_budgets[shift.from_category] < shift.amount:
            logger.warning(
                "Insufficient funds in %s: need %.0f, have %.0f",
                shift.from_category.value, shift.amount,
                self._current_budgets[shift.from_category],
            )
            return False

        self._current_budgets[shift.from_category] -= shift.amount
        self._current_budgets[shift.to_category] += shift.amount

        logger.info(
            "Applied shift: $%.0f from %s to %s",
            shift.amount, shift.from_category.value, shift.to_category.value,
        )
        return True

    async def get_budget(self, category: AllocationCategory) -> float:
        return self._current_budgets.get(category, 0.0)

    async def set_budget(self, category: AllocationCategory, amount: float) -> None:
        self._current_budgets[category] = amount
        self._total_capital = sum(self._current_budgets.values())

    async def record_performance(
        self,
        category: AllocationCategory,
        roi: float,
    ) -> None:
        key = category.value
        if key not in self._performance_history:
            self._performance_history[key] = []
        self._performance_history[key].append(roi)
        if len(self._performance_history[key]) > 100:
            self._performance_history[key] = self._performance_history[key][-100:]

    async def _build_buckets(self) -> list[AllocationBucket]:
        buckets = []
        for category, allocation in self._current_budgets.items():
            roi = await self._estimate_roi(category)
            urgency = await self._get_urgency(category)
            min_alloc = allocation * 0.5
            max_alloc = allocation * 2.0
            rec_alloc = self._calculate_recommended(category, allocation, roi, urgency)

            buckets.append(AllocationBucket(
                category=category,
                current_allocation=allocation,
                recommended_allocation=round(rec_alloc, 0),
                min_allocation=min_alloc,
                max_allocation=max_alloc,
                roi_score=roi,
                urgency=urgency,
                notes=self._get_category_notes(category, roi, urgency),
            ))
        return buckets

    async def _calculate_shifts(
        self,
        buckets: list[AllocationBucket],
    ) -> list[AllocationShift]:
        shifts = []
        underperformers = [b for b in buckets if b.current_allocation > b.recommended_allocation and b.roi_score < 0.5]
        outperformers = [b for b in buckets if b.current_allocation < b.recommended_allocation and b.roi_score > 0.7]

        for under in underperformers:
            for over in outperformers:
                gap = min(
                    under.current_allocation - under.recommended_allocation,
                    over.recommended_allocation - over.current_allocation,
                )
                if gap > 100:
                    shifts.append(AllocationShift(
                        from_category=under.category,
                        to_category=over.category,
                        amount=round(gap * 0.3, 0),
                        reason=f"Reallocating from low-ROI {under.category.value} (ROI: {under.roi_score:.2f}) "
                               f"to high-ROI {over.category.value} (ROI: {over.roi_score:.2f})",
                        expected_roi=over.roi_score,
                        confidence=min(0.9, over.roi_score + 0.1),
                        risk_level="medium" if under.urgency < 7 else "high",
                    ))
        return shifts[:5]

    async def _estimate_roi(self, category: AllocationCategory) -> float:
        roi_map = {
            AllocationCategory.SALES: 0.85,
            AllocationCategory.MARKETING: 0.75,
            AllocationCategory.CUSTOMER_SUCCESS: 0.70,
            AllocationCategory.AI_MODELS: 0.65,
            AllocationCategory.ENGINEERING: 0.60,
            AllocationCategory.RESEARCH: 0.50,
            AllocationCategory.INFRASTRUCTURE: 0.45,
            AllocationCategory.COMPLIANCE: 0.30,
        }
        base = roi_map.get(category, 0.5)
        historical = self._performance_history.get(category.value, [])
        if historical:
            avg_recent = sum(historical[-10:]) / min(len(historical[-10:]), 10)
            base = (base + avg_recent) / 2
        return round(base, 2)

    async def _get_urgency(self, category: AllocationCategory) -> int:
        urgency_map = {
            AllocationCategory.COMPLIANCE: 9,
            AllocationCategory.SALES: 8,
            AllocationCategory.INFRASTRUCTURE: 7,
            AllocationCategory.CUSTOMER_SUCCESS: 6,
            AllocationCategory.MARKETING: 5,
            AllocationCategory.AI_MODELS: 4,
            AllocationCategory.ENGINEERING: 3,
            AllocationCategory.RESEARCH: 2,
        }
        return urgency_map.get(category, 5)

    def _calculate_recommended(
        self,
        category: AllocationCategory,
        current: float,
        roi: float,
        urgency: int,
    ) -> float:
        base = current * (0.5 + roi * 0.5)
        urgency_bonus = current * (urgency / 20)
        return base + urgency_bonus

    def _calculate_efficiency(self, buckets: list[AllocationBucket]) -> float:
        if not buckets:
            return 0.0
        weighted = sum(b.roi_score * b.current_allocation for b in buckets)
        total = sum(b.current_allocation for b in buckets)
        return round(weighted / total, 2) if total > 0 else 0.0

    def _get_category_notes(
        self,
        category: AllocationCategory,
        roi: float,
        urgency: int,
    ) -> str:
        if roi >= 0.8:
            return f"High performer, consider increasing budget"
        elif roi >= 0.5:
            return f"Moderate ROI (${roi:.2f}), maintain current allocation"
        elif urgency >= 7:
            return f"Low ROI but high urgency, maintain minimum"
        return f"Consider reducing allocation, explore optimization"
