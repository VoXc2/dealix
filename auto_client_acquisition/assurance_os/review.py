"""Layer 6 — Weekly Operating Review + Monthly Board Pack.

The Operating Review answers the 12 weekly questions (data-derivable ones
are answered automatically; the rest are flagged for the founder) and
ends with the 5 mandatory decision slots. The Board Pack assembles the
6 standing board sections, marking any metric the caller did not supply
as ``unknown``.
"""
from __future__ import annotations

from auto_client_acquisition.assurance_os.adapters import ApprovalAdapter
from auto_client_acquisition.assurance_os.funnel import detect_bottleneck
from auto_client_acquisition.assurance_os.models import (
    AcceptanceTestResult,
    AssuranceInputs,
    BoardPack,
    FunnelSnapshot,
    GateResult,
    OperatingReview,
)

_WEEKLY_QUESTIONS: list[tuple[str, str]] = [
    ("q1", "What brought qualified leads this week?"),
    ("q2", "What brought meetings this week?"),
    ("q3", "Where did prospects stop in the funnel?"),
    ("q4", "What was the top objection?"),
    ("q5", "What was the most common support question?"),
    ("q6", "Which channel wasted time?"),
    ("q7", "Which partner brought a good lead?"),
    ("q8", "Which affiliate brought a bad lead?"),
    ("q9", "What action was blocked by governance?"),
    ("q10", "Which workflow repeated?"),
    ("q11", "What should we stop?"),
    ("q12", "What should we double down on?"),
]

# month-section -> list of metric keys looked up in inputs.kpi_values
_BOARD_SECTIONS: dict[str, list[str]] = {
    "revenue": ["booked_revenue", "pipeline", "retainers", "gross_margin"],
    "delivery": ["active_diagnostics", "proof_packs", "delivery_time_days", "qa_score"],
    "growth": ["best_channel_leads", "cac", "conversion_rate", "best_icp_win_rate"],
    "support": ["top_tickets", "auto_resolution_rate", "escalations", "kb_gaps"],
    "governance": ["blocked_actions", "unsupported_claims", "affiliate_violations",
                   "evidence_completeness"],
    "product": ["repeated_workflows", "no_build_decisions", "automation_candidates"],
}


def build_operating_review(
    inputs: AssuranceInputs,
    funnel: FunnelSnapshot,
    gates: list[GateResult],
    tests: list[AcceptanceTestResult],
) -> OperatingReview:
    """Assemble the weekly operating review."""
    bottleneck = detect_bottleneck(funnel)

    stats = ApprovalAdapter().live_stats()
    blocked = (
        f"{stats.value['blocked']} blocked request(s) in the approval store"
        if stats.is_known else "unknown"
    )
    failed_tests = [t.id for t in tests if t.result == "fail"]
    failed_gates = [g.gate_id for g in gates if not g.passed]

    derived: dict[str, str] = {
        "q3": bottleneck if bottleneck != "unknown"
              else "unknown - funnel counts not supplied",
        "q9": blocked,
        "q11": (f"failing acceptance tests: {', '.join(failed_tests)}"
                if failed_tests else "no failing acceptance tests recorded"),
        "q12": (f"gates not yet passed: {', '.join(failed_gates)}"
                if failed_gates else "all gates passed - choose a growth lever"),
    }

    answered: list[dict[str, str]] = []
    for qid, question in _WEEKLY_QUESTIONS:
        answer = derived.get(qid, "unknown - founder to answer in review")
        answered.append({"id": qid, "question": question, "answer": answer})

    decisions = [
        f"Double down: identify the highest-converting source feeding '{bottleneck}'.",
        f"Fix bottleneck: the weakest funnel transition is '{bottleneck}'.",
        "Kill channel: stop any channel with leads but no meetings.",
        "Improve asset: fix the asset behind the worst objection.",
        "No-build / Build: only build where a paid or repeated workflow signal exists.",
    ]

    return OperatingReview(
        week_of=inputs.week_of or "current",
        answered_questions=answered,
        bottleneck=bottleneck,
        decisions=decisions,
    )


def build_board_pack(inputs: AssuranceInputs) -> BoardPack:
    """Assemble the monthly board pack; unsupplied metrics are 'unknown'."""
    sections: dict[str, dict[str, object]] = {}
    for section, metric_keys in _BOARD_SECTIONS.items():
        sections[section] = {
            key: inputs.kpi_values.get(key, "unknown") for key in metric_keys
        }
    return BoardPack(month=inputs.month or "current", sections=sections)
