"""Board scorecards — weighted 0–100 signals for offers, clients, productization."""

from __future__ import annotations

from dataclasses import dataclass

from auto_client_acquisition.board_decision_os.schemas import (
    ClientScorecardInput,
    OfferScorecardInput,
    ProductizationScorecardInput,
    ScorecardResult,
)

# Win rate, gross margin, proof strength, retainer conversion, repeatability,
# governance safety, productization signal
_OFFER_WEIGHTS: tuple[int, ...] = (15, 15, 20, 20, 15, 10, 5)

# Clear pain, executive sponsor, data readiness, governance alignment,
# adoption, proof, expansion potential
_CLIENT_WEIGHTS: tuple[int, ...] = (15, 15, 15, 15, 15, 15, 10)

# Repeated pain, delivery hours saved, revenue linkage, risk reduction,
# client pull, build simplicity
_PRODUCTIZATION_WEIGHTS: tuple[int, ...] = (20, 20, 20, 15, 15, 10)


def _clamp_pct(value: int) -> int:
    if value < 0:
        return 0
    if value > 100:
        return 100
    return value


def _weighted_score(values: tuple[int, ...], weights: tuple[int, ...]) -> int:
    total = sum(_clamp_pct(v) * w for v, w in zip(values, weights, strict=True))
    return min(100, total // 100)


@dataclass(frozen=True, slots=True)
class OfferScorecardDimensions:
    win_rate: int
    gross_margin: int
    proof_strength: int
    retainer_conversion: int
    repeatability: int
    governance_safety: int
    productization_signal: int


@dataclass(frozen=True, slots=True)
class ClientScorecardDimensions:
    clear_pain: int
    executive_sponsor: int
    data_readiness: int
    governance_alignment: int
    adoption_score: int
    proof_score: int
    expansion_potential: int


@dataclass(frozen=True, slots=True)
class ProductizationScorecardDimensions:
    repeated_pain: int
    delivery_hours_saved: int
    revenue_linkage: int
    risk_reduction: int
    client_pull: int
    build_simplicity: int


def offer_scorecard_score(dimensions: OfferScorecardDimensions) -> int:
    d = dimensions
    return _weighted_score(
        (
            d.win_rate,
            d.gross_margin,
            d.proof_strength,
            d.retainer_conversion,
            d.repeatability,
            d.governance_safety,
            d.productization_signal,
        ),
        _OFFER_WEIGHTS,
    )


def client_scorecard_score(dimensions: ClientScorecardDimensions) -> int:
    d = dimensions
    return _weighted_score(
        (
            d.clear_pain,
            d.executive_sponsor,
            d.data_readiness,
            d.governance_alignment,
            d.adoption_score,
            d.proof_score,
            d.expansion_potential,
        ),
        _CLIENT_WEIGHTS,
    )


def productization_scorecard_score(dimensions: ProductizationScorecardDimensions) -> int:
    d = dimensions
    return _weighted_score(
        (
            d.repeated_pain,
            d.delivery_hours_saved,
            d.revenue_linkage,
            d.risk_reduction,
            d.client_pull,
            d.build_simplicity,
        ),
        _PRODUCTIZATION_WEIGHTS,
    )


def offer_scorecard_band(score: int) -> str:
    if score >= 85:
        return "scale"
    if score >= 70:
        return "improve_and_sell"
    if score >= 55:
        return "pilot_only"
    return "hold_kill"


def client_scorecard_band(score: int) -> str:
    if score >= 85:
        return "strategic_account"
    if score >= 70:
        return "retainer_ready"
    if score >= 55:
        return "enablement_needed"
    return "avoid_or_diagnostic"


def productization_scorecard_band(score: int) -> str:
    if score >= 85:
        return "build_now"
    if score >= 70:
        return "mvp"
    if score >= 55:
        return "template_manual"
    return "hold"


def _pct(v: float) -> int:
    return max(0, min(100, int(round(v))))


def score_offer(inp: OfferScorecardInput) -> ScorecardResult:
    """HTTP helper: Pydantic input → weighted score + board-facing bands."""
    d = OfferScorecardDimensions(
        win_rate=_pct(inp.win_rate),
        gross_margin=_pct(inp.gross_margin),
        proof_strength=_pct(inp.proof_strength),
        retainer_conversion=_pct(inp.retainer_conversion),
        repeatability=_pct(inp.repeatability),
        governance_safety=_pct(inp.governance_safety),
        productization_signal=_pct(inp.productization_signal),
    )
    total_i = offer_scorecard_score(d)
    key = offer_scorecard_band(total_i)
    if key == "scale":
        return ScorecardResult(
            total=float(total_i),
            band="top",
            board_read_ar="توسيع (Scale)",
            board_read_en="Scale",
        )
    if key == "improve_and_sell":
        return ScorecardResult(
            total=float(total_i),
            band="strong",
            board_read_ar="تحسين ثم البيع بقوة أكبر",
            board_read_en="Improve and sell",
        )
    if key == "pilot_only":
        return ScorecardResult(
            total=float(total_i),
            band="mid",
            board_read_ar="بايلوت فقط",
            board_read_en="Pilot only",
        )
    return ScorecardResult(
        total=float(total_i),
        band="low",
        board_read_ar="تعليق / إيقاف",
        board_read_en="Hold / Kill",
    )


def score_client(inp: ClientScorecardInput) -> ScorecardResult:
    d = ClientScorecardDimensions(
        clear_pain=_pct(inp.clear_pain),
        executive_sponsor=_pct(inp.executive_sponsor),
        data_readiness=_pct(inp.data_readiness),
        governance_alignment=_pct(inp.governance_alignment),
        adoption_score=_pct(inp.adoption_score),
        proof_score=_pct(inp.proof_score),
        expansion_potential=_pct(inp.expansion_potential),
    )
    total_i = client_scorecard_score(d)
    key = client_scorecard_band(total_i)
    if key == "strategic_account":
        return ScorecardResult(
            total=float(total_i),
            band="top",
            board_read_ar="حساب استراتيجي",
            board_read_en="Strategic account",
        )
    if key == "retainer_ready":
        return ScorecardResult(
            total=float(total_i),
            band="strong",
            board_read_ar="جاهز للريتينر",
            board_read_en="Retainer-ready",
        )
    if key == "enablement_needed":
        return ScorecardResult(
            total=float(total_i),
            band="mid",
            board_read_ar="يحتاج تمكين",
            board_read_en="Enablement needed",
        )
    return ScorecardResult(
        total=float(total_i),
        band="low",
        board_read_ar="تجنب / تشخيص فقط",
        board_read_en="Avoid / diagnostic only",
    )


def score_productization(inp: ProductizationScorecardInput) -> ScorecardResult:
    d = ProductizationScorecardDimensions(
        repeated_pain=_pct(inp.repeated_pain),
        delivery_hours_saved=_pct(inp.delivery_hours_saved),
        revenue_linkage=_pct(inp.revenue_linkage),
        risk_reduction=_pct(inp.risk_reduction),
        client_pull=_pct(inp.client_pull),
        build_simplicity=_pct(inp.build_simplicity),
    )
    total_i = productization_scorecard_score(d)
    key = productization_scorecard_band(total_i)
    if key == "build_now":
        return ScorecardResult(
            total=float(total_i),
            band="top",
            board_read_ar="ابنِ الآن",
            board_read_en="Build now",
        )
    if key == "mvp":
        return ScorecardResult(
            total=float(total_i),
            band="strong",
            board_read_ar="MVP",
            board_read_en="MVP",
        )
    if key == "template_manual":
        return ScorecardResult(
            total=float(total_i),
            band="mid",
            board_read_ar="قالب / يدوي",
            board_read_en="Template / manual",
        )
    return ScorecardResult(
        total=float(total_i),
        band="low",
        board_read_ar="تعليق",
        board_read_en="Hold",
    )
