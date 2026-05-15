"""Agent runtime supervision and emergency stop heuristics."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AgentHealthSnapshot:
    agent_id: str
    error_rate: float
    latency_ms_p95: float
    policy_violations_last_hour: int
    last_heartbeat_epoch: int


def supervision_status(snapshot: AgentHealthSnapshot, *, now_epoch: int) -> str:
    heartbeat_age = now_epoch - snapshot.last_heartbeat_epoch
    if snapshot.policy_violations_last_hour > 0 or heartbeat_age > 300:
        return 'critical'
    if snapshot.error_rate > 0.1 or snapshot.latency_ms_p95 > 5000:
        return 'degraded'
    return 'healthy'


def should_emergency_stop(snapshot: AgentHealthSnapshot, *, now_epoch: int) -> bool:
    return supervision_status(snapshot, now_epoch=now_epoch) == 'critical'


__all__ = ['AgentHealthSnapshot', 'should_emergency_stop', 'supervision_status']
