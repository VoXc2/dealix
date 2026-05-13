"""Weighted board scorecards — Offer, Client, Productization."""

from __future__ import annotations

from auto_client_acquisition.board_decision_os.schemas import (
    ClientScorecardInput,
    OfferScorecardInput,
    ProductizationScorecardInput,
    ScorecardResult,
)

OFFER_WEIGHTS: dict[str, float] = {
    "win_rate": 15,
    "gross_margin": 15,
    "proof_strength": 20,
    "retainer_conversion": 20,
    "repeatability": 15,
    "governance_safety": 10,
    "productization_signal": 5,
}

CLIENT_WEIGHTS: dict[str, float] = {
    "clear_pain": 15,
    "executive_sponsor": 15,
    "data_readiness": 15,
    "governance_alignment": 15,
    "adoption_score": 15,
    "proof_score": 15,
    "expansion_potential": 10,
}

PRODUCT_WEIGHTS: dict[str, float] = {
    "repeated_pain": 20,
    "delivery_hours_saved": 20,
    "revenue_linkage": 20,
    "risk_reduction": 15,
    "client_pull": 15,
    "build_simplicity": 10,
}


def _weighted_total(values: dict[str, float], weights: dict[str, float]) -> float:
    num = sum(values[k] * weights[k] for k in weights)
    den = sum(weights.values())
    return round(num / den, 2)


def _offer_band(total: float) -> ScorecardResult:
    if total >= 85:
        return ScorecardResult(
            total=total,
            band="top",
            board_read_ar="توسيع (Scale)",
            board_read_en="Scale",
        )
    if total >= 70:
        return ScorecardResult(
            total=total,
            band="strong",
            board_read_ar="تحسين ثم البيع بقوة أكبر",
            board_read_en="Improve and sell",
        )
    if total >= 55:
        return ScorecardResult(
            total=total,
            band="mid",
            board_read_ar="بايلوت فقط",
            board_read_en="Pilot only",
        )
    return ScorecardResult(
        total=total,
        band="low",
        board_read_ar="تعليق / إيقاف",
        board_read_en="Hold / Kill",
    )


def _client_band(total: float) -> ScorecardResult:
    if total >= 85:
        return ScorecardResult(
            total=total,
            band="top",
            board_read_ar="حساب استراتيجي",
            board_read_en="Strategic account",
        )
    if total >= 70:
        return ScorecardResult(
            total=total,
            band="strong",
            board_read_ar="جاهز للريتينر",
            board_read_en="Retainer-ready",
        )
    if total >= 55:
        return ScorecardResult(
            total=total,
            band="mid",
            board_read_ar="يحتاج تمكين",
            board_read_en="Enablement needed",
        )
    return ScorecardResult(
        total=total,
        band="low",
        board_read_ar="تجنب / تشخيص فقط",
        board_read_en="Avoid / diagnostic only",
    )


def _product_band(total: float) -> ScorecardResult:
    if total >= 85:
        return ScorecardResult(
            total=total,
            band="top",
            board_read_ar="ابنِ الآن",
            board_read_en="Build now",
        )
    if total >= 70:
        return ScorecardResult(
            total=total,
            band="strong",
            board_read_ar="MVP",
            board_read_en="MVP",
        )
    if total >= 55:
        return ScorecardResult(
            total=total,
            band="mid",
            board_read_ar="قالب / يدوي",
            board_read_en="Template / manual",
        )
    return ScorecardResult(
        total=total,
        band="low",
        board_read_ar="تعليق",
        board_read_en="Hold",
    )


def score_offer(inp: OfferScorecardInput) -> ScorecardResult:
    vals = inp.model_dump()
    total = _weighted_total(vals, OFFER_WEIGHTS)
    return _offer_band(total)


def score_client(inp: ClientScorecardInput) -> ScorecardResult:
    vals = inp.model_dump()
    total = _weighted_total(vals, CLIENT_WEIGHTS)
    return _client_band(total)


def score_productization(inp: ProductizationScorecardInput) -> ScorecardResult:
    vals = inp.model_dump()
    total = _weighted_total(vals, PRODUCT_WEIGHTS)
    return _product_band(total)
