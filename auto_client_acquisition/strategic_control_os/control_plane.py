"""Control Plane — canonical components index.

See ``docs/strategic_control/CONTROL_PLANE.md``.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ControlPlaneComponent(str, Enum):
    DATA = "data_control"
    AI = "ai_control"
    AGENT = "agent_control"
    WORKFLOW = "workflow_control"
    CLAIM = "claim_control"
    CHANNEL = "channel_control"
    AUDIT = "audit_control"
    PROOF = "proof_control"
    CAPITAL = "capital_control"


CONTROL_PLANE_COMPONENTS: tuple[ControlPlaneComponent, ...] = tuple(ControlPlaneComponent)


@dataclass(frozen=True)
class ControlPlaneIndex:
    """The control plane's published surface for a given offer or BU.

    Each offer declares which components it exercises. A new component
    cannot be silently introduced — adding one requires an explicit
    Decision Log entry referencing the doctrine.
    """

    owner: str  # offer code or BU code
    components: frozenset[ControlPlaneComponent]

    def __post_init__(self) -> None:
        unknown = set(self.components) - set(CONTROL_PLANE_COMPONENTS)
        if unknown:
            raise ValueError(
                "unknown_control_plane_components:"
                + ",".join(sorted(c.value for c in unknown))
            )

    def declares(self, component: ControlPlaneComponent) -> bool:
        return component in self.components
