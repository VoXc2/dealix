"""Commercial Sovereignty — multi-stream revenue with concentration check.

See ``docs/sovereignty/COMMERCIAL_SOVEREIGNTY.md``.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class RevenueRole(str, Enum):
    PROVE = "prove"
    STABILIZE = "stabilize"
    SCALE = "scale"
    DISTRIBUTE = "distribute"
    COMPOUND = "compound"
    QUALIFY = "qualify"
    VALIDATE = "validate"
    LARGE_CONTRACTS = "large_contracts"


@dataclass(frozen=True)
class RevenueLine:
    name: str
    role: RevenueRole
    amount: float

    def __post_init__(self) -> None:
        if self.amount < 0:
            raise ValueError("amount_must_be_non_negative")


@dataclass(frozen=True)
class RevenueMix:
    period: str
    lines: tuple[RevenueLine, ...]

    def total(self) -> float:
        return sum(line.amount for line in self.lines)

    def share(self, name: str) -> float:
        total = self.total()
        if total == 0:
            return 0.0
        return sum(line.amount for line in self.lines if line.name == name) / total

    def lines_by_role(self, role: RevenueRole) -> tuple[RevenueLine, ...]:
        return tuple(line for line in self.lines if line.role is role)


# Doctrine ceiling: no single line may exceed this share of the mix
# without triggering an Intelligence OS review.
DEFAULT_CONCENTRATION_CEILING: float = 0.6


def excessive_concentration(
    mix: RevenueMix,
    *,
    ceiling: float = DEFAULT_CONCENTRATION_CEILING,
) -> tuple[bool, tuple[str, ...]]:
    """Return ``(triggered, lines_over_ceiling)``."""

    if not 0.0 < ceiling <= 1.0:
        raise ValueError("ceiling_out_of_range")
    over: list[str] = []
    for line in mix.lines:
        if mix.share(line.name) > ceiling:
            over.append(line.name)
    # de-duplicate while preserving order
    seen: set[str] = set()
    unique_over = tuple(x for x in over if not (x in seen or seen.add(x)))
    return (bool(unique_over), unique_over)
