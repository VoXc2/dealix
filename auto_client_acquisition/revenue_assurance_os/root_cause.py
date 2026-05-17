"""Root Cause Matrix — when results are weak, diagnose before building.

Maps the worst funnel bottleneck to likely causes and the corrective
action. Crucially: most bottlenecks are fixed by selling/messaging
changes, not by building features.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from auto_client_acquisition.revenue_assurance_os.funnel_scoreboard import (
    FunnelStage,
    worst_bottleneck,
)


@dataclass(frozen=True, slots=True)
class RootCauseDiagnosis:
    bottleneck_stage: str
    likely_causes: tuple[str, ...]
    recommended_action: str
    build_recommended: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# Bottleneck stage -> (likely causes, recommended action, build is allowed).
_MATRIX: dict[str, tuple[tuple[str, ...], str, bool]] = {
    FunnelStage.CONVERSATIONS.value: (
        ("icp", "message", "channel", "content", "cta"),
        "Fix the ICP or the message. Do not build a feature.",
        False,
    ),
    FunnelStage.PROOF_PACK_REQUESTS.value: (
        ("weak_proof", "unclear_cta", "offer_not_understood", "low_trust"),
        "Improve the Sample Proof Pack and the Diagnostic page.",
        False,
    ),
    FunnelStage.MEETINGS.value: (
        ("weak_proof", "unclear_cta", "offer_not_understood", "low_trust"),
        "Improve the Sample Proof Pack and the Diagnostic page.",
        False,
    ),
    FunnelStage.SCOPES.value: (
        ("weak_discovery", "pain_not_qualified", "demo_too_long", "value_not_priced"),
        "Use a 12-minute demo and close with a clear scope.",
        False,
    ),
    FunnelStage.INVOICES.value: (
        ("price", "timing", "no_decision_maker", "low_urgency"),
        "Add a Starter Diagnostic or a mini pilot to lower the entry cost.",
        False,
    ),
    FunnelStage.PAID.value: (
        ("price", "timing", "no_decision_maker", "low_urgency"),
        "Add a Starter Diagnostic or a mini pilot to lower the entry cost.",
        False,
    ),
    FunnelStage.PROOF_PACKS_DELIVERED.value: (
        ("missing_checklists", "missing_templates", "manual_proof_assembly"),
        "Delivery is the paid bottleneck — build checklists, templates, proof generator.",
        True,
    ),
    FunnelStage.UPSELLS.value: (
        ("proof_pack_has_no_next_decision",),
        "End every Proof Pack with 3 paid next decisions.",
        False,
    ),
}

_DEFAULT = (
    ("icp", "message", "channel"),
    "Diagnose the message and ICP before building anything.",
    False,
)


def diagnose(funnel_counts: dict[str, int]) -> RootCauseDiagnosis:
    """Diagnose the weakest funnel transition and recommend an action."""
    bottleneck = worst_bottleneck(funnel_counts)
    causes, action, build_ok = _MATRIX.get(bottleneck, _DEFAULT)
    return RootCauseDiagnosis(
        bottleneck_stage=bottleneck,
        likely_causes=causes,
        recommended_action=action,
        build_recommended=build_ok,
    )


__all__ = [
    "RootCauseDiagnosis",
    "diagnose",
]
