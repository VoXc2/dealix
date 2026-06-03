"""Collect risk lines from reliability_os + RISK_BLOCKED proof events."""
from __future__ import annotations

from typing import Any


def risk_summary(
    health_matrix: dict[str, Any] | None,
    proof_events: list[Any] | None,
) -> list[str]:
    """Build a list of risk lines for the weekly report.

    Sources:
      - any subsystem in ``health_matrix`` whose status is not ``ok``
      - any RISK_BLOCKED proof event in the supplied window

    The list is deduplicated and ordered: subsystem risks first,
    proof-derived risks last. Pure function — no I/O.
    """
    out: list[str] = []
    seen: set[str] = set()

    if isinstance(health_matrix, dict):
        for sub in health_matrix.get("subsystems") or []:
            if not isinstance(sub, dict):
                continue
            status = str(sub.get("status", "")).lower()
            if status and status != "ok":
                name = str(sub.get("name") or "subsystem")
                desc = str(sub.get("description") or "")
                line = f"[{status}] {name}: {desc}".strip()
                if line not in seen:
                    seen.add(line)
                    out.append(line)

    if proof_events:
        for ev in proof_events:
            try:
                ev_type = getattr(ev, "event_type", None)
                if ev_type is None and isinstance(ev, dict):
                    ev_type = ev.get("event_type")
                if str(ev_type) != "risk_blocked":
                    continue
                summary_ar = (
                    getattr(ev, "redacted_summary_ar", None)
                    or getattr(ev, "summary_ar", None)
                    or (ev.get("redacted_summary_ar") if isinstance(ev, dict) else "")
                    or (ev.get("summary_ar") if isinstance(ev, dict) else "")
                    or ""
                )
                line = f"[risk_blocked] {summary_ar}".strip()
                if line and line not in seen:
                    seen.add(line)
                    out.append(line)
            except Exception:
                continue

    return out
