"""Monthly Board Pack — 8 sections, even if the founder is the only reader.

Turns the founder from "a builder" into "a CEO running a revenue system".
Sections without hard evidence say so — no fabricated numbers.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any

from auto_client_acquisition.revenue_assurance_os.acceptance_tests import (
    run_acceptance_suite,
)
from auto_client_acquisition.revenue_assurance_os.assurance_score import (
    compute_assurance_score,
)
from auto_client_acquisition.revenue_assurance_os.evidence_audit import audit_evidence
from auto_client_acquisition.revenue_assurance_os.funnel_scoreboard import build_scoreboard
from auto_client_acquisition.value_os.value_ledger import list_events

_NO_EVIDENCE = "no evidence yet — founder input required"


@dataclass(frozen=True, slots=True)
class BoardPack:
    month_label: str
    generated_at: str
    sections: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _month_label(now: datetime | None = None) -> str:
    now = now or datetime.now(timezone.utc)
    return f"{now.year}-{now.month:02d}"


def _revenue_section() -> dict[str, Any]:
    events = list_events(limit=10000)
    by_tier: dict[str, float] = {
        "estimated": 0.0,
        "observed": 0.0,
        "verified": 0.0,
        "client_confirmed": 0.0,
    }
    for event in events:
        by_tier.setdefault(event.tier, 0.0)
        by_tier[event.tier] += float(event.amount)
    return {
        "value_events": len(events),
        "by_tier_sar": {k: round(v, 2) for k, v in by_tier.items()},
        "bankable_sar": round(by_tier.get("client_confirmed", 0.0), 2),
        "note": "Only client_confirmed is bankable revenue.",
    }


def build_board_pack(
    *,
    month_label: str | None = None,
    funnel_counts: dict[str, int] | None = None,
    assurance_signals: dict[str, float] | None = None,
) -> BoardPack:
    """Assemble the monthly Board Pack from ledger + assurance evidence."""
    score = compute_assurance_score(assurance_signals)
    acceptance = run_acceptance_suite()
    acceptance_passed = sum(1 for r in acceptance if r.passed)
    evidence = audit_evidence(sample_size=20)

    sections: dict[str, Any] = {
        "1_revenue": _revenue_section(),
        "2_funnel": (build_scoreboard(funnel_counts).to_dict() if funnel_counts else _NO_EVIDENCE),
        "3_delivery": {
            "proof_packs_delivered": _NO_EVIDENCE,
            "cycle_time": _NO_EVIDENCE,
            "missing_inputs": _NO_EVIDENCE,
            "client_value_confirmed": _NO_EVIDENCE,
        },
        "4_support": {
            "tickets": _NO_EVIDENCE,
            "auto_resolved": _NO_EVIDENCE,
            "escalated": _NO_EVIDENCE,
            "kb_gaps": _NO_EVIDENCE,
        },
        "5_partners_affiliates": {
            "leads": _NO_EVIDENCE,
            "qualified_leads": _NO_EVIDENCE,
            "paid_deals": _NO_EVIDENCE,
            "compliance_flags": _NO_EVIDENCE,
            "commission_owed": _NO_EVIDENCE,
        },
        "6_governance": {
            "assurance_score": score["score"],
            "readiness_label": score["readiness_label"],
            "acceptance_cases_passed": f"{acceptance_passed}/{len(acceptance)}",
            "evidence_completeness": evidence.completeness,
            "evidence_audit_passed": evidence.passed,
        },
        "7_product": {
            "repeated_workflows": _NO_EVIDENCE,
            "automation_candidates": _NO_EVIDENCE,
            "no_build_decisions": _NO_EVIDENCE,
        },
        "8_decision_needed": {
            "what_to_double": _NO_EVIDENCE,
            "what_to_kill": _NO_EVIDENCE,
            "what_to_build": _NO_EVIDENCE,
            "what_not_to_build": _NO_EVIDENCE,
        },
    }
    return BoardPack(
        month_label=month_label or _month_label(),
        generated_at=datetime.now(timezone.utc).isoformat(),
        sections=sections,
    )


__all__ = [
    "BoardPack",
    "build_board_pack",
]
