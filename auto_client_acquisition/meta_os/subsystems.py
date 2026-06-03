"""Nine subsystems of the Dealix Meta-Operating System (ordered pipeline)."""

from __future__ import annotations

from typing import Final

META_SUBSYSTEMS: Final[tuple[str, ...]] = (
    "signal",
    "diagnosis",
    "offer",
    "delivery",
    "governance",
    "proof",
    "capital",
    "productization",
    "venture",
)
