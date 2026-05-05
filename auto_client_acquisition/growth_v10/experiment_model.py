"""Experiment evaluator — GrowthBook-style outcome recommendation.

Pure deterministic stats — no scipy, no random. Uses Welch's
approximation for a rough p_value_estimate; this is illustrative,
not a published statistical claim.
"""
from __future__ import annotations

import math

from auto_client_acquisition.growth_v10.schemas import Experiment


def _mean(xs: list[float]) -> float:
    return sum(xs) / len(xs) if xs else 0.0


def _variance(xs: list[float]) -> float:
    if len(xs) < 2:
        return 0.0
    mu = _mean(xs)
    return sum((x - mu) ** 2 for x in xs) / (len(xs) - 1)


def _erf(x: float) -> float:
    # Abramowitz & Stegun 7.1.26 — pure-Python erf approximation.
    sign = 1 if x >= 0 else -1
    x = abs(x)
    a1, a2, a3, a4, a5 = (
        0.254829592,
        -0.284496736,
        1.421413741,
        -1.453152027,
        1.061405429,
    )
    p = 0.3275911
    t = 1.0 / (1.0 + p * x)
    y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * math.exp(-x * x)
    return sign * y


def _normal_two_sided_p(z: float) -> float:
    # Two-sided p-value for standard normal z.
    return max(0.0, min(1.0, 1.0 - _erf(abs(z) / math.sqrt(2.0))))


def evaluate_experiment(
    exp: Experiment,
    control_results: list[float],
    variant_results: list[float],
) -> dict:
    """Evaluate experiment results.

    Returns a dict with: winner, p_value_estimate, recommendation.
    Recommendation values: ``adopt``, ``reject``, ``keep_running``,
    ``abort``.
    """
    if exp.status == "blocked":
        return {
            "winner": None,
            "p_value_estimate": 1.0,
            "recommendation": "abort",
            "reason": "experiment_blocked",
        }

    if not control_results or not variant_results:
        return {
            "winner": None,
            "p_value_estimate": 1.0,
            "recommendation": "keep_running",
            "reason": "insufficient_data",
        }

    mu_c = _mean(control_results)
    mu_v = _mean(variant_results)
    var_c = _variance(control_results)
    var_v = _variance(variant_results)
    n_c = len(control_results)
    n_v = len(variant_results)

    se = math.sqrt((var_c / n_c if n_c else 0.0) + (var_v / n_v if n_v else 0.0))
    if se == 0.0:
        # Identical populations or single-sample — fall back to mean delta.
        if mu_v > mu_c:
            winner = "variant"
        elif mu_v < mu_c:
            winner = "control"
        else:
            winner = None
        recommendation = "adopt" if winner == "variant" else (
            "reject" if winner == "control" else "keep_running"
        )
        return {
            "winner": winner,
            "p_value_estimate": 0.0 if winner else 1.0,
            "recommendation": recommendation,
            "reason": "zero_variance",
        }

    z = (mu_v - mu_c) / se
    p = _normal_two_sided_p(z)

    threshold = exp.success_threshold
    delta = mu_v - mu_c

    if p < 0.05 and mu_v > mu_c and delta >= threshold:
        winner = "variant"
        recommendation = "adopt"
    elif p < 0.05 and mu_c > mu_v:
        winner = "control"
        recommendation = "reject"
    elif (n_c + n_v) < 30:
        winner = None
        recommendation = "keep_running"
    else:
        winner = None
        recommendation = "keep_running"

    return {
        "winner": winner,
        "p_value_estimate": round(p, 6),
        "recommendation": recommendation,
        "reason": "computed",
        "mean_control": round(mu_c, 6),
        "mean_variant": round(mu_v, 6),
        "z_score": round(z, 6),
    }
