"""Structured log line for a single policy evaluation (in-memory / persistence-agnostic)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PolicyCheckLogEntry:
    policy_id: str
    matched_rules: tuple[str, ...]
    decision: str
    notes: str


__all__ = ["PolicyCheckLogEntry"]
