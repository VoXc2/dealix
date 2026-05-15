"""Deterministic 'next week' plan derived from current state.

Hard rule: NEVER invent work. Every line in the plan is grounded in
an existing artifact (service activation matrix, scorecard
recommendations, daily-loop open loops, or non-ok subsystem).
"""
from __future__ import annotations

from typing import Any


def next_week_plan(
    *,
    scorecard: dict[str, Any] | None,
    loop: dict[str, Any] | None,
    health_matrix: dict[str, Any] | None,
    promotion_candidates: list[Any] | None = None,
    limit: int = 7,
) -> list[str]:
    """Compose a grounded plan list. Pure function — no I/O.

    Order of priority:
      1. P0 / P1 recommendations from the scorecard
      2. The single service nearest to Live (from candidates_for_promotion)
      3. Open loops that mention founder decisions (daily-loop)
      4. Any non-ok subsystem appears as a 'stabilize' line
    """
    plan: list[str] = []
    seen: set[str] = set()

    def _add(line: str) -> None:
        line = line.strip()
        if not line or line in seen:
            return
        seen.add(line)
        plan.append(line)

    # 1. Scorecard recommendations (P0 / P1 first)
    if isinstance(scorecard, dict):
        recs = scorecard.get("recommendations") or []
        ranked = sorted(
            (r for r in recs if isinstance(r, dict)),
            key=lambda r: (str(r.get("priority", "P9")), str(r.get("action", ""))),
        )
        for r in ranked:
            prio = str(r.get("priority", "P?"))
            action = str(r.get("action", "")).strip()
            if action:
                _add(f"{prio}: {action}")
            if len(plan) >= limit:
                return plan

    # 2. Top service-promotion candidate from the matrix
    if promotion_candidates:
        try:
            top = promotion_candidates[0]
            sid = getattr(top, "service_id", None) or (
                top.get("service_id") if isinstance(top, dict) else None
            )
            status = getattr(top, "status", None) or (
                top.get("status") if isinstance(top, dict) else None
            )
            if sid:
                _add(
                    f"P1: review promotion candidate '{sid}' "
                    f"(currently {status}); close 8-gate blockers"
                )
        except Exception:
            pass
        if len(plan) >= limit:
            return plan

    # 3. Daily-loop open loops
    if isinstance(loop, dict):
        for ol in (loop.get("open_loops") or [])[:3]:
            if isinstance(ol, str) and ol.strip():
                _add(f"P2: address open loop — {ol}")
            if len(plan) >= limit:
                return plan

    # 4. Non-ok subsystems → stabilize
    if isinstance(health_matrix, dict):
        for sub in health_matrix.get("subsystems") or []:
            if not isinstance(sub, dict):
                continue
            status = str(sub.get("status", "")).lower()
            if status and status != "ok":
                name = str(sub.get("name") or "subsystem")
                _add(f"P2: stabilize {name} (currently {status})")
            if len(plan) >= limit:
                return plan

    return plan
