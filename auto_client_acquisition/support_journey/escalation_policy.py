"""Stage-specific escalation policy."""
from __future__ import annotations

from typing import Any


# Stages that ALWAYS escalate to founder (regardless of category)
_MANDATORY_ESCALATE_STAGES = {"billing", "privacy", "renewal"}


def stage_escalation_policy(*, journey_stage: str) -> dict[str, Any]:
    """Returns escalation rules for a stage."""
    must_escalate = journey_stage in _MANDATORY_ESCALATE_STAGES
    sla_hours_priority = {
        "pre_sales": "p2",
        "onboarding": "p2",
        "delivery": "p1",
        "billing": "p0",
        "proof": "p3",
        "renewal": "p1",
        "privacy": "p0",
    }
    return {
        "journey_stage": journey_stage,
        "mandatory_escalate_to_founder": must_escalate,
        "sla_priority": sla_hours_priority.get(journey_stage, "p2"),
        "owner": "founder" if must_escalate else "csm_or_founder",
        "reason_ar": (
            "تصعيد إجباري للمؤسس (مرحلة حسّاسة)."
            if must_escalate else
            "يمكن للـ CSM الردّ بمسوّدة معتمدة."
        ),
        "reason_en": (
            "Mandatory founder escalation (sensitive stage)."
            if must_escalate else
            "CSM can draft an approved reply."
        ),
    }
