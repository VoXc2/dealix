"""Fair allocation contracts for the shared Dealix OpenCode pool."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "scripts" / "ops" / "opencode_agent_allocator.py"
spec = importlib.util.spec_from_file_location("opencode_agent_allocator", PATH)
allocator = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(allocator)


def _job(owner: str, job_class: str, priority: float = 50, urgency: str = "normal") -> dict:
    return {
        "JOB_ID": f"{owner}-{job_class}-{priority}-{urgency}",
        "OWNER_AGENT": owner,
        "JOB_CLASS": job_class,
        "PRIORITY": priority,
        "URGENCY": urgency,
        "AUTHORITY_LEVEL": "L3",
        "MODIFYING": True,
        "CREATED_AT": "2026-09-12T00:00:00+00:00",
    }


def test_three_slots_seed_three_economic_lanes() -> None:
    jobs = [
        _job("dealix-sales", "COMMERCIAL_REASONING", 70),
        _job("dealix-engineer", "ENGINEERING", 90),
        _job("dealix-delivery", "DELIVERY", 60),
        _job("dealix-engineer", "REVIEW", 95),
    ]
    selected = allocator.select_deep_jobs(jobs, slots=3)
    assert {allocator.lane_for(job) for job in selected} == {
        "REVENUE", "BUILD", "CUSTOMER_MARKET"
    }


def test_engineer_can_borrow_second_slot_but_not_third() -> None:
    jobs = [
        _job("dealix-engineer", "ENGINEERING", 99),
        _job("dealix-engineer", "REVIEW", 98),
        _job("dealix-engineer", "RESEARCH", 97),
    ]
    selected = allocator.select_deep_jobs(jobs, slots=3)
    assert len(selected) == 2
    assert all(job["OWNER_AGENT"] == "dealix-engineer" for job in selected)


def test_owner_class_mismatch_fails_closed() -> None:
    errors = allocator.agent_fit_errors(_job("dealix-sales", "ENGINEERING"))
    assert errors


def test_live_owner_lease_consumes_agent_capacity() -> None:
    jobs = [
        _job("dealix-engineer", "ENGINEERING", 90),
        _job("dealix-engineer", "REVIEW", 80),
        _job("dealix-sales", "COMMERCIAL_REASONING", 70),
    ]
    leases = [{"OWNER": "dealix-engineer"}]
    selected = allocator.select_deep_jobs(jobs, slots=3, leases=leases)
    assert sum(job["OWNER_AGENT"] == "dealix-engineer" for job in selected) == 1


def test_critical_urgency_can_raise_a_job_within_lane() -> None:
    normal = _job("dealix-sales", "COMMERCIAL_REASONING", 70, "normal")
    critical = _job("dealix-pm", "COMMERCIAL_REASONING", 50, "critical")
    selected = allocator.select_deep_jobs([normal, critical], slots=1)
    assert selected[0]["OWNER_AGENT"] == "dealix-pm"
