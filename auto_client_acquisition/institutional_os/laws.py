"""Institutional laws — reference ids (documentation mirror)."""

from __future__ import annotations

from typing import Final, NamedTuple


class LawRef(NamedTuple):
    law_id: str
    title_en: str


DEALIX_LAWS: Final[tuple[LawRef, ...]] = (
    LawRef("L1", "The Proof Law"),
    LawRef("L2", "The Capital Law"),
    LawRef("L3", "The Governance Law"),
    LawRef("L4", "The Productization Law"),
    LawRef("L5", "The Retainer Law"),
    LawRef("L6", "The Focus Law"),
    LawRef("L7", "The Kill Law"),
)
