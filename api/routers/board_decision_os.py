"""Board Decision OS router — strategic overview for the founder/board.

Endpoint (prefix /api/v1/board-decision-os):
  GET /overview — commercial gate status (G1-G7), the North Star count
                  (Governed Value Decisions Created), and a CEL summary.

Wraps `auto_client_acquisition/board_decision_os/` and reads the commercial
event stream via `commercial_os`.
"""

from __future__ import annotations

from collections import Counter
from typing import Any

from fastapi import APIRouter, Query

from auto_client_acquisition.board_decision_os import (
    BOARD_DECISION_INPUT_SIGNALS,
    BOARD_MEMO_SECTIONS,
    CEO_COMMAND_CENTER_SURFACES,
)
from auto_client_acquisition.commercial_os.gates import evaluate_gates
from auto_client_acquisition.commercial_os.projections import (
    current_commercial_state,
)
from auto_client_acquisition.revenue_memory.event_store import get_default_store

router = APIRouter(prefix="/api/v1/board-decision-os", tags=["board-decision-os"])

_GOVERNANCE_DECISION = "approval_required"


@router.get("/overview")
async def board_overview(
    customer_id: str = Query(..., min_length=1),
    has_active_retainer: bool = Query(default=False),
) -> dict[str, Any]:
    """Strategic overview: gate status + North Star count + CEL summary.

    The North Star metric is **Governed Value Decisions Created**: the count
    of engagements that reached `CEL7_confirmed` (revenue recognized only on
    a paid invoice — hard rule 5).
    """
    events = list(get_default_store().read_for_customer(customer_id))

    gates = evaluate_gates(events, has_active_retainer=has_active_retainer)
    states = current_commercial_state(events)

    cel_counts: Counter[str] = Counter(s["cel"] for s in states.values())
    state_counts: Counter[str] = Counter(s["state"] for s in states.values())

    # North Star — Governed Value Decisions Created (CEL7_confirmed only).
    north_star = cel_counts.get("CEL7_confirmed", 0)

    return {
        "customer_id": customer_id,
        "north_star": {
            "metric": "Governed Value Decisions Created",
            "count": north_star,
            "definition": "Engagements that reached CEL7_confirmed (paid invoice).",
        },
        "gates": {gid: g.to_dict() for gid, g in gates.items()},
        "gates_passed": sorted(gid for gid, g in gates.items() if g.passed),
        "cel_summary": {
            "engagements": len(states),
            "by_cel": dict(cel_counts),
            "by_state": dict(state_counts),
        },
        "board_inputs": {
            "input_signals": list(BOARD_DECISION_INPUT_SIGNALS),
            "memo_sections": list(BOARD_MEMO_SECTIONS),
            "ceo_command_center_surfaces": list(CEO_COMMAND_CENTER_SURFACES),
        },
        "governance_decision": _GOVERNANCE_DECISION,
    }
