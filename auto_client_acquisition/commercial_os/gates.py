"""Commercial Gates G1-G7.

Canonical spec: docs/commercial/COMMERCIAL_GATES.md

A gate is passed / not passed — never a percentage, never a date. Each gate
reads recorded facts from the commercial event stream. Pure: no I/O.

G7 (Platform Signal) reads the `friction_log` repeated-workflow signal where a
customer scope is supplied; otherwise it computes a repeated-workflow signature
from the event stream itself. The fallback is a documented simplification — see
`_g7_from_event_stream`.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable
from dataclasses import dataclass, field

from auto_client_acquisition.revenue_memory.events import RevenueEvent

# Number of repetitions that trip the platform-signal gate.
_PLATFORM_SIGNAL_THRESHOLD = 3
# Number of `sent` messages required for the first market-proof gate.
_FIRST_MARKET_PROOF_SENT = 5


@dataclass(frozen=True)
class GateStatus:
    """Pass / not-pass status for one gate, with the facts behind it."""

    gate: str
    name: str
    passed: bool
    detail: str
    evidence: dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> dict[str, object]:
        return {
            "gate": self.gate,
            "name": self.name,
            "passed": self.passed,
            "detail": self.detail,
            "evidence": dict(self.evidence),
        }


def _g7_from_event_stream(events: list[RevenueEvent]) -> tuple[bool, str, int]:
    """Compute the platform signal from a repeated-workflow signature.

    Simplification: with no `friction_log` scope available, a repeated
    workflow is approximated by counting commercial events that share a
    `workflow_signature` payload key. Three or more repetitions of the same
    signature trips G7.
    """
    signatures = Counter(
        sig
        for e in events
        if isinstance((sig := e.payload.get("workflow_signature")), str) and sig
    )
    if not signatures:
        return False, "no_repeated_workflow_signature_in_event_stream", 0
    top_sig, top_count = signatures.most_common(1)[0]
    passed = top_count >= _PLATFORM_SIGNAL_THRESHOLD
    detail = (
        f"workflow '{top_sig}' repeated {top_count}x"
        if passed
        else f"top workflow repeated {top_count}x (need {_PLATFORM_SIGNAL_THRESHOLD})"
    )
    return passed, detail, top_count


def evaluate_gates(
    events: Iterable[RevenueEvent],
    *,
    has_active_retainer: bool = False,
    friction_repeated_workflow_count: int | None = None,
) -> dict[str, GateStatus]:
    """Evaluate the seven commercial gates over a commercial event stream.

    Args:
        events: commercial RevenueEvents (non-commercial events ignored).
        has_active_retainer: a recurring monthly engagement is active (G6).
        friction_repeated_workflow_count: if supplied, the `friction_log`
            repeated-workflow signal count used for G7 instead of the
            event-stream fallback.

    Returns:
        `{gate_id: GateStatus}` for G1-G7. A gate, once passed, stays passed:
        callers persist the historical fact themselves.
    """
    ev = list(events)

    sent = [e for e in ev if e.event_type == "commercial.sent"]
    classified = [e for e in ev if e.event_type == "commercial.reply_classified"]
    cel5 = [
        e
        for e in ev
        if e.event_type == "commercial.meeting_used"
        and e.payload.get("commercial_state") == "used_in_meeting"
    ]
    cel6 = [
        e
        for e in ev
        if e.event_type
        in ("commercial.scope_requested", "commercial.pilot_intro_requested")
    ]
    paid = [e for e in ev if e.event_type == "commercial.invoice_paid"]

    # G5 — the same offer reaches invoice_paid twice.
    paid_by_offer = Counter(
        offer_id
        for e in paid
        if isinstance((offer_id := e.payload.get("offer_id")), str) and offer_id
    )
    repeat_offer = max(paid_by_offer.values(), default=0)

    # G1 — 5 messages reach `sent` and at least one reply is classified.
    g1_passed = len(sent) >= _FIRST_MARKET_PROOF_SENT and len(classified) >= 1

    # G7 — platform signal.
    if friction_repeated_workflow_count is not None:
        g7_count = friction_repeated_workflow_count
        g7_passed = g7_count >= _PLATFORM_SIGNAL_THRESHOLD
        g7_detail = (
            f"friction_log repeated-workflow count {g7_count}"
            if g7_passed
            else f"friction_log repeated-workflow count {g7_count} "
            f"(need {_PLATFORM_SIGNAL_THRESHOLD})"
        )
    else:
        g7_passed, g7_detail, g7_count = _g7_from_event_stream(ev)

    return {
        "G1": GateStatus(
            gate="G1",
            name="First Market Proof",
            passed=g1_passed,
            detail=(
                f"{len(sent)} sent, {len(classified)} classified"
                if g1_passed
                else f"{len(sent)}/{_FIRST_MARKET_PROOF_SENT} sent, "
                f"{len(classified)} classified"
            ),
            evidence={"sent": len(sent), "reply_classified": len(classified)},
        ),
        "G2": GateStatus(
            gate="G2",
            name="Meeting Proof",
            passed=len(cel5) >= 1,
            detail=f"{len(cel5)} engagement(s) reached used_in_meeting",
            evidence={"used_in_meeting": len(cel5)},
        ),
        "G3": GateStatus(
            gate="G3",
            name="Pull Proof",
            passed=len(cel6) >= 1,
            detail=f"{len(cel6)} scope/intro request(s)",
            evidence={"cel6_requests": len(cel6)},
        ),
        "G4": GateStatus(
            gate="G4",
            name="Revenue Proof",
            passed=len(paid) >= 1,
            detail=f"{len(paid)} invoice(s) paid",
            evidence={"invoice_paid": len(paid)},
        ),
        "G5": GateStatus(
            gate="G5",
            name="Repeatability",
            passed=repeat_offer >= 2,
            detail=(
                f"an offer reached invoice_paid {repeat_offer}x"
                if repeat_offer
                else "no offer paid twice"
            ),
            evidence={"max_paid_per_offer": repeat_offer},
        ),
        "G6": GateStatus(
            gate="G6",
            name="Retainer",
            passed=bool(has_active_retainer),
            detail=(
                "an active retainer engagement exists"
                if has_active_retainer
                else "no active retainer engagement"
            ),
            evidence={"active_retainer": int(bool(has_active_retainer))},
        ),
        "G7": GateStatus(
            gate="G7",
            name="Platform Signal",
            passed=g7_passed,
            detail=g7_detail,
            evidence={"repeated_workflow_count": g7_count},
        ),
    }
