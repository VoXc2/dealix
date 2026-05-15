"""Failover endpoint selection."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EndpointHealth:
    endpoint: str
    available: bool
    latency_ms: float
    error_rate: float


def needs_failover(primary: EndpointHealth) -> bool:
    return (not primary.available) or primary.error_rate > 0.1


def choose_failover_endpoint(candidates: tuple[EndpointHealth, ...]) -> EndpointHealth | None:
    available = [candidate for candidate in candidates if candidate.available]
    if not available:
        return None
    return min(available, key=lambda item: (item.error_rate, item.latency_ms))


__all__ = ['EndpointHealth', 'choose_failover_endpoint', 'needs_failover']
