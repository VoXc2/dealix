#!/usr/bin/env python3
"""Deterministic fair allocator for the shared Dealix OpenCode worker pool.

This is policy, not a second scheduler. The canonical session_factory owns
leases, worktrees, execution, recovery and acceptance. This module only chooses
which READY modifying jobs receive the currently available deep-work slots.
"""
from __future__ import annotations

from collections import Counter
from typing import Any, Iterable

PERMANENT_AGENTS = (
    "dealix-pm",
    "dealix-sales",
    "dealix-delivery",
    "dealix-engineer",
    "dealix-content",
)

LANE_ORDER = ("REVENUE", "BUILD", "CUSTOMER_MARKET")
LANE_BY_CLASS = {
    "COMMERCIAL_REASONING": "REVENUE",
    "ENGINEERING": "BUILD",
    "REVIEW": "BUILD",
    "DELIVERY": "CUSTOMER_MARKET",
    "RESEARCH": "CUSTOMER_MARKET",
    "CONTENT": "CUSTOMER_MARKET",
}

# Maximum concurrent deep workers owned by one permanent agent. The engineer
# may borrow one extra slot, but can never consume the global pool alone.
AGENT_DEEP_CAP = {
    "dealix-pm": 1,
    "dealix-sales": 1,
    "dealix-delivery": 1,
    "dealix-engineer": 2,
    "dealix-content": 1,
}

AGENT_ALLOWED_CLASSES = {
    "dealix-pm": frozenset({"RESEARCH", "REVIEW", "COMMERCIAL_REASONING"}),
    "dealix-sales": frozenset({"RESEARCH", "COMMERCIAL_REASONING"}),
    "dealix-delivery": frozenset({"RESEARCH", "REVIEW", "DELIVERY"}),
    "dealix-engineer": frozenset({"RESEARCH", "REVIEW", "ENGINEERING"}),
    "dealix-content": frozenset({"RESEARCH", "REVIEW", "CONTENT"}),
}

URGENCY_WEIGHT = {
    "critical": 30.0,
    "high": 15.0,
    "normal": 0.0,
    "low": -10.0,
}


def lane_for(job: dict[str, Any]) -> str:
    return LANE_BY_CLASS.get(str(job.get("JOB_CLASS")), "CUSTOMER_MARKET")


def agent_fit_errors(job: dict[str, Any]) -> list[str]:
    owner = str(job.get("OWNER_AGENT") or "")
    job_class = str(job.get("JOB_CLASS") or "")
    if owner not in PERMANENT_AGENTS:
        return [f"invalid owner: {owner}"]
    if not job.get("MODIFYING"):
        return []
    allowed = AGENT_ALLOWED_CLASSES[owner]
    if job_class not in allowed:
        return [f"owner/job-class mismatch: {owner} cannot own {job_class}"]
    return []


def active_owner_counts(leases: Iterable[dict[str, Any]]) -> Counter[str]:
    counts: Counter[str] = Counter()
    for lease in leases:
        owner = str(lease.get("OWNER") or "")
        if owner in PERMANENT_AGENTS:
            counts[owner] += 1
    return counts


def priority_score(job: dict[str, Any]) -> float:
    priority = float(job.get("PRIORITY") or 0.0)
    urgency = URGENCY_WEIGHT.get(str(job.get("URGENCY") or "normal").lower(), 0.0)
    return priority + urgency


def _eligible(job: dict[str, Any], owner_counts: Counter[str]) -> bool:
    owner = str(job.get("OWNER_AGENT") or "")
    return (
        bool(job.get("MODIFYING"))
        and job.get("AUTHORITY_LEVEL") != "L5"
        and not agent_fit_errors(job)
        and owner_counts[owner] < AGENT_DEEP_CAP[owner]
    )


def select_deep_jobs(
    candidates: Iterable[dict[str, Any]],
    *,
    slots: int,
    leases: Iterable[dict[str, Any]] = (),
) -> list[dict[str, Any]]:
    """Select at most ``slots`` jobs with lane fairness and per-agent caps."""
    slots = max(0, int(slots))
    if slots == 0:
        return []
    owner_counts = active_owner_counts(leases)
    remaining = sorted(
        [job for job in candidates if _eligible(job, owner_counts)],
        key=lambda item: (-priority_score(item), str(item.get("CREATED_AT") or "")),
    )
    selected: list[dict[str, Any]] = []

    # Seed one slot from each economic lane before allowing borrowing.
    for lane in LANE_ORDER:
        if len(selected) >= slots:
            break
        for job in list(remaining):
            owner = str(job.get("OWNER_AGENT"))
            if lane_for(job) == lane and owner_counts[owner] < AGENT_DEEP_CAP[owner]:
                selected.append(job)
                owner_counts[owner] += 1
                remaining.remove(job)
                break

    # Any unused slot is borrowable by the strongest remaining bounded job.
    for job in remaining:
        if len(selected) >= slots:
            break
        owner = str(job.get("OWNER_AGENT"))
        if owner_counts[owner] >= AGENT_DEEP_CAP[owner]:
            continue
        selected.append(job)
        owner_counts[owner] += 1
    return selected


def allocation_receipt(selected: Iterable[dict[str, Any]]) -> dict[str, Any]:
    jobs = list(selected)
    return {
        "selected": len(jobs),
        "lanes": dict(Counter(lane_for(job) for job in jobs)),
        "owners": dict(Counter(str(job.get("OWNER_AGENT")) for job in jobs)),
        "global_policy": "DEEP_WIP_MAX remains owned by session_factory",
        "per_agent_caps": dict(AGENT_DEEP_CAP),
    }
