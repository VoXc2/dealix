"""Full-Ops Score + Weakness Radar (Phase 4).

Composes:
- Full-Ops Score (10 weighted layers, 0-100 + readiness label)
- Weakness Radar (prioritized list of named gaps with bilingual fixes)
- Health checks (per-subsystem ok/degraded/missing)
- Evidence (the source data that justifies the score)

100% read-only, never raises (uses safe_call).
"""
from auto_client_acquisition.full_ops_radar.evidence import collect_evidence
from auto_client_acquisition.full_ops_radar.health_checks import (
    run_all_health_checks,
)
from auto_client_acquisition.full_ops_radar.score import (
    SCORE_WEIGHTS,
    compute_full_ops_score,
    readiness_label,
)
from auto_client_acquisition.full_ops_radar.weakness_radar import (
    detect_weaknesses,
)

__all__ = [
    "SCORE_WEIGHTS",
    "collect_evidence",
    "compute_full_ops_score",
    "detect_weaknesses",
    "readiness_label",
    "run_all_health_checks",
]
