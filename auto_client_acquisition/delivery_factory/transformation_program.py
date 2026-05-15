"""45-day Enterprise AI Transformation orchestrator.

Where ``delivery_sprint.py`` runs a single 7-day revenue sprint, this
orchestrates a multi-workstream enterprise engagement: the workstreams of
an ``EnterpriseOffering`` are scheduled across a 45-day timeline (parallel
tracks), each gated by founder review.

Runs persist to an append-only JSONL store (env
``DEALIX_TRANSFORMATION_RUNS_PATH``) — same pattern as
``friction_log/store.py`` and ``value_os/value_ledger.py`` — so program
state survives process restarts without requiring a database.

No external sends. Every workstream advance is governance-reviewed.
"""

from __future__ import annotations

import json
import os
import threading
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_DEFAULT_PATH = "var/transformation-runs.jsonl"
_lock = threading.Lock()

# Workstream lifecycle states.
_VALID_STATUSES = frozenset(
    {"pending", "in_progress", "review_required", "done", "blocked"}
)
_DEFAULT_DURATION_DAYS = 45


@dataclass
class Workstream:
    name: str
    track: int  # 1..3 — parallel track lane
    day_start: int
    day_end: int
    status: str = "pending"
    governance_decision: str = "allow_with_review"
    outputs: dict[str, Any] = field(default_factory=dict)
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class TransformationProgram:
    program_run_id: str
    customer_id: str
    offering_id: str
    tier_id: str
    duration_days: int
    started_at: str
    workstreams: list[Workstream] = field(default_factory=list)
    status: str = "in_progress"  # in_progress | completed | blocked
    governance_decision: str = "allow_with_review"

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["workstreams"] = [w.to_dict() for w in self.workstreams]
        return d

    @property
    def progress_pct(self) -> float:
        if not self.workstreams:
            return 0.0
        done = sum(1 for w in self.workstreams if w.status == "done")
        return round(100.0 * done / len(self.workstreams), 1)


def _path() -> Path:
    p = Path(os.environ.get("DEALIX_TRANSFORMATION_RUNS_PATH", _DEFAULT_PATH))
    if not p.is_absolute():
        p = Path(__file__).resolve().parent.parent.parent / p
    return p


def _schedule(workstream_names: tuple[str, ...], duration_days: int) -> list[Workstream]:
    """Lay workstreams across the timeline on 3 parallel tracks with overlap.

    Deterministic: every workstream gets a (day_start, day_end) window so the
    engagement runs as overlapping tracks, not a single serial sprint.
    """
    n = len(workstream_names)
    if n == 0:
        return []
    slice_len = max(1, round(duration_days / n * 1.6))  # >1 slice => overlap
    out: list[Workstream] = []
    for i, name in enumerate(workstream_names):
        start = min(duration_days - 1, round(i * (duration_days - slice_len) / max(1, n - 1)))
        end = min(duration_days, start + slice_len)
        out.append(
            Workstream(
                name=name,
                track=(i % 3) + 1,
                day_start=max(1, start + 1),
                day_end=max(start + 1, end),
            )
        )
    return out


def _append(program: TransformationProgram) -> None:
    """Persist the current program snapshot (append-only — last wins)."""
    path = _path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with _lock:
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(program.to_dict(), ensure_ascii=False) + "\n")


def _read_all() -> dict[str, dict[str, Any]]:
    """Return the latest snapshot per program_run_id."""
    path = _path()
    if not path.exists():
        return {}
    latest: dict[str, dict[str, Any]] = {}
    with _lock:
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except Exception:  # noqa: BLE001
                continue
            rid = rec.get("program_run_id")
            if rid:
                latest[rid] = rec
    return latest


def _hydrate(rec: dict[str, Any]) -> TransformationProgram:
    ws = [Workstream(**w) for w in rec.get("workstreams", [])]
    rec = {**rec, "workstreams": ws}
    return TransformationProgram(**rec)


def start_program(
    *,
    customer_id: str,
    offering_id: str,
    tier_id: str,
    duration_days: int = _DEFAULT_DURATION_DAYS,
) -> TransformationProgram:
    """Start a 45-day transformation program for an enterprise offering."""
    if not customer_id:
        raise ValueError("customer_id is required")
    from auto_client_acquisition.service_catalog import (
        get_enterprise_offering,
        get_enterprise_tier,
    )

    offering = get_enterprise_offering(offering_id)
    if offering is None:
        raise ValueError(f"unknown_enterprise_offering: {offering_id}")
    if get_enterprise_tier(offering_id, tier_id) is None:
        raise ValueError(f"unknown_tier_for_offering: {tier_id}")

    program = TransformationProgram(
        program_run_id=f"TXP-{uuid.uuid4().hex[:12]}",
        customer_id=customer_id,
        offering_id=offering_id,
        tier_id=tier_id,
        duration_days=duration_days,
        started_at=datetime.now(timezone.utc).isoformat(),
        workstreams=_schedule(offering.workstreams, duration_days),
    )
    _append(program)
    return program


def get_program(program_run_id: str) -> TransformationProgram | None:
    rec = _read_all().get(program_run_id)
    return _hydrate(rec) if rec else None


def list_programs(*, customer_id: str | None = None) -> list[TransformationProgram]:
    progs = [_hydrate(r) for r in _read_all().values()]
    if customer_id:
        progs = [p for p in progs if p.customer_id == customer_id]
    return sorted(progs, key=lambda p: p.started_at)


def advance_workstream(
    *,
    program_run_id: str,
    workstream_name: str,
    new_status: str,
    outputs: dict[str, Any] | None = None,
    notes: str = "",
) -> TransformationProgram:
    """Move one workstream to a new lifecycle state and re-persist the program."""
    if new_status not in _VALID_STATUSES:
        raise ValueError(
            f"invalid status '{new_status}'; expected {sorted(_VALID_STATUSES)}"
        )
    program = get_program(program_run_id)
    if program is None:
        raise ValueError(f"unknown_program_run: {program_run_id}")

    target = next(
        (w for w in program.workstreams if w.name == workstream_name), None
    )
    if target is None:
        raise ValueError(f"unknown_workstream: {workstream_name}")

    target.status = new_status
    if outputs:
        target.outputs = {**target.outputs, **outputs}
    if notes:
        target.notes = notes

    if new_status == "blocked":
        _emit_friction(program.customer_id, workstream_name)

    if all(w.status == "done" for w in program.workstreams):
        program.status = "completed"
    elif any(w.status == "blocked" for w in program.workstreams):
        program.status = "blocked"
    else:
        program.status = "in_progress"

    _append(program)
    return program


def timeline(program_run_id: str) -> dict[str, Any]:
    """Return a day-indexed view of the 45-day timeline (for the UI / API)."""
    program = get_program(program_run_id)
    if program is None:
        raise ValueError(f"unknown_program_run: {program_run_id}")
    return {
        "program_run_id": program.program_run_id,
        "duration_days": program.duration_days,
        "progress_pct": program.progress_pct,
        "status": program.status,
        "tracks": {
            track: [
                {
                    "name": w.name,
                    "day_start": w.day_start,
                    "day_end": w.day_end,
                    "status": w.status,
                }
                for w in program.workstreams
                if w.track == track
            ]
            for track in (1, 2, 3)
        },
    }


def _emit_friction(customer_id: str, workstream_name: str) -> None:
    try:
        from auto_client_acquisition.friction_log.store import emit

        emit(
            customer_id=customer_id,
            kind="schema_failure",
            severity="med",
            workflow_id="transformation_program",
            notes=f"workstream_blocked:{workstream_name}",
        )
    except Exception:  # noqa: BLE001
        pass


def clear_for_test() -> None:
    path = _path()
    if path.exists():
        with _lock:
            path.write_text("", encoding="utf-8")


__all__ = [
    "TransformationProgram",
    "Workstream",
    "advance_workstream",
    "clear_for_test",
    "get_program",
    "list_programs",
    "start_program",
    "timeline",
]
