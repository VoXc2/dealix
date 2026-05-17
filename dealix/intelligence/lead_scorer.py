"""
Lead scoring — heuristic now, sklearn-ready when >=200 labeled examples exist.
تسجيل العملاء المحتملين.
"""

from __future__ import annotations

import os
import pickle
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from auto_client_acquisition.policy_config.loader import load_policy

MODEL_PATH = Path(os.getenv("LEAD_SCORER_MODEL", "/opt/dealix/models/lead_scorer.pkl"))


@dataclass
class LeadFeatures:
    company_size: int = 0  # employees
    budget_usd: float = 0.0
    urgency_score: float = 0.0  # 0-1 (from pain extractor)
    message_length: int = 0
    is_arabic: bool = False
    has_company_email: bool = False
    has_phone: bool = False
    pain_points_count: int = 0
    sector_fit: float = 0.0  # 0-1 ICP sector match

    def to_vector(self) -> list[float]:
        return [
            float(self.company_size),
            self.budget_usd,
            self.urgency_score,
            float(self.message_length),
            1.0 if self.is_arabic else 0.0,
            1.0 if self.has_company_email else 0.0,
            1.0 if self.has_phone else 0.0,
            float(self.pain_points_count),
            self.sector_fit,
        ]


@dataclass
class ScoreResult:
    score: float  # 0-1
    tier: str  # cold / warm / hot
    reasons: list[str] = field(default_factory=list)
    model: str = "heuristic"


def _band_points(value: float, bands: list[dict], reasons: list[str]) -> float:
    """First band (in declared order) whose `min` threshold is met."""
    for band in bands:
        if value >= band["min"]:
            reason = band.get("reason")
            if reason:
                reasons.append(reason)
            return float(band["points"])
    return 0.0


def _heuristic_score(f: LeadFeatures) -> ScoreResult:
    policy = load_policy("lead_scoring")
    weights = policy["weights"]
    tiers = policy["tiers"]
    score = 0.0
    reasons: list[str] = []

    score += _band_points(f.company_size, weights["company_size"], reasons)
    score += _band_points(f.budget_usd, weights["budget_usd"], reasons)
    score += _band_points(f.urgency_score, weights["urgency_score"], reasons)

    if f.has_company_email:
        email_w = weights["has_company_email"]
        score += float(email_w["points"])
        if email_w.get("reason"):
            reasons.append(email_w["reason"])
    if f.has_phone:
        score += float(weights["has_phone"]["points"])

    pain_w = weights["pain_points_count"]
    if f.pain_points_count >= pain_w["min"]:
        score += float(pain_w["points"])
        if pain_w.get("reason"):
            reasons.append(pain_w["reason"])

    sector_w = weights["sector_fit"]
    score += float(sector_w["factor"]) * f.sector_fit
    if f.sector_fit >= sector_w["reason_min"]:
        reasons.append(sector_w["reason"])

    score = min(max(score, 0.0), 1.0)
    tier = "hot" if score >= tiers["hot"] else "warm" if score >= tiers["warm"] else "cold"
    return ScoreResult(score=round(score, 3), tier=tier, reasons=reasons, model="heuristic")


class LeadScorer:
    """
    Scores leads. Uses sklearn model when available at MODEL_PATH,
    otherwise falls back to a weighted-heuristic scorer.
    """

    def __init__(self) -> None:
        self._model: Any = None
        if MODEL_PATH.exists():
            try:
                with MODEL_PATH.open("rb") as f:
                    self._model = pickle.load(f)
            except Exception:
                self._model = None

    @property
    def mode(self) -> str:
        return "ml" if self._model is not None else "heuristic"

    def score(self, features: LeadFeatures) -> ScoreResult:
        if self._model is None:
            return _heuristic_score(features)
        try:
            proba = self._model.predict_proba([features.to_vector()])[0][1]
            score = float(proba)
            tier = "hot" if score >= 0.7 else "warm" if score >= 0.45 else "cold"
            return ScoreResult(
                score=round(score, 3), tier=tier, reasons=["ml_model"], model="sklearn"
            )
        except Exception:
            return _heuristic_score(features)
