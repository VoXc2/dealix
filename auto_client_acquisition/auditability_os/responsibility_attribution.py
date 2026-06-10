"""Responsibility attribution — who is accountable for an artifact."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ResponsibilityAttribution:
    artifact_id: str
    actor_id: str
    role: str
    accountable_party: str


def attribution_valid(a: ResponsibilityAttribution) -> bool:
    return all((a.artifact_id.strip(), a.actor_id.strip(), a.role.strip(), a.accountable_party.strip()))


__all__ = ["ResponsibilityAttribution", "attribution_valid"]
