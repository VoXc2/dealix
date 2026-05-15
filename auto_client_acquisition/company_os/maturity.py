"""Deterministic maturity scoring for the 7 internal systems.

Score is a weighted sum of objective signals (modules wired, doctrine
gates declared, evidence present). No LLM, no I/O.
"""

from __future__ import annotations

from typing import Any

from auto_client_acquisition.company_os.schemas import MaturityBand, SystemEntry
from auto_client_acquisition.company_os.system_registry import list_systems

# Score band thresholds (inclusive lower bound).
_SEED_MAX = 39
_WORKING_MAX = 69
_PROVEN_MAX = 89


def band_from_score(score: int) -> MaturityBand:
    """Map a 0-100 score to a maturity band."""
    if score < 0 or score > 100:
        raise ValueError("score must be between 0 and 100")
    if score <= _SEED_MAX:
        return MaturityBand.SEED
    if score <= _WORKING_MAX:
        return MaturityBand.WORKING
    if score <= _PROVEN_MAX:
        return MaturityBand.PROVEN
    return MaturityBand.SCALED


def score_system(entry: SystemEntry, *, signals: dict[str, Any] | None = None) -> dict[str, Any]:
    """Score one system 0-100 from its registry entry plus optional signals.

    ``signals`` may override observed facts with keys: ``has_api`` (bool),
    ``has_evals`` (bool), ``paid_pilots`` (int). Missing signals default
    to conservative values.
    """
    signals = signals or {}
    modules_pts = min(len(entry.backing_modules), 4) * 10  # up to 40
    gates_pts = min(len(entry.doctrine_gates), 4) * 5  # up to 20
    evidence_pts = 15 if entry.evidence_refs else 0
    api_pts = 15 if signals.get("has_api", False) else 0
    evals_pts = 10 if signals.get("has_evals", False) else 0
    score = modules_pts + gates_pts + evidence_pts + api_pts + evals_pts
    score = max(0, min(100, score))
    return {
        "system_id": entry.system_id,
        "score": score,
        "band": str(band_from_score(score)),
        "breakdown": {
            "modules": modules_pts,
            "doctrine_gates": gates_pts,
            "evidence": evidence_pts,
            "api": api_pts,
            "evals": evals_pts,
        },
    }


def maturity_report(*, signals: dict[str, dict[str, Any]] | None = None) -> dict[str, Any]:
    """Score every one of the 7 systems.

    ``signals`` is keyed by system_id; each value is passed to
    ``score_system`` for that system.
    """
    signals = signals or {}
    rows = [score_system(s, signals=signals.get(s.system_id)) for s in list_systems()]
    avg = round(sum(r["score"] for r in rows) / len(rows), 1) if rows else 0.0
    return {
        "system_count": len(rows),
        "average_score": avg,
        "systems": rows,
    }
