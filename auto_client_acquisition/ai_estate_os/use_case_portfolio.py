"""Use case portfolio entry."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class UseCaseEntry:
    slug: str
    status: str
    owner: str


__all__ = ["UseCaseEntry"]
