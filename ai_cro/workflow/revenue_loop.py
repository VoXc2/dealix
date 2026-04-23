"""
Dealix Revenue Loop — the single heartbeat of the product.

Every opportunity flows through ONE state machine:
   signal → enrich → score → decide_channel → draft → send → wait_reply
         → negotiate → approval_interrupt → book_meeting → summarize → report

Business logic lives HERE, not in prompts. Prompts are thin. Policy layer gates
risky transitions. State is persisted in Postgres (ADR: durable execution).

Design principles:
  - Idempotent transitions (every action carries an idempotency_key).
  - Human-in-the-loop via APPROVAL_REQUIRED → INTERRUPT state.
  - Each transition emits an event the observability layer captures.
  - States serialize to JSON — replay/debug is free.
"""
from __future__ import annotations
import asyncio
import hashlib
import json
import logging
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Optional

logger = logging.getLogger("dealix.revenue_loop")


# ============================================================================
# STATE ENUM — 12 stages, strict ordering, explicit terminal states
# ============================================================================

class Stage(str, Enum):
    SIGNAL         = "signal"            # raw inbound signal ingested
    ENRICH         = "enrich"            # Wathq / Monsha'at / LinkedIn pull
    SCORE          = "score"             # confidence + priority scored
    DECIDE_CHANNEL = "decide_channel"    # email / WhatsApp / call
    DRAFT          = "draft"             # content drafted
    SEND           = "send"              # outbound executed
    WAIT_REPLY     = "wait_reply"        # awaiting response (timer arms)
    NEGOTIATE      = "negotiate"         # reply received, negotiation loop
    APPROVAL       = "approval_interrupt"  # owner decision required
    BOOK           = "book_meeting"      # calendar slot chosen
    SUMMARIZE      = "summarize"         # post-meeting summary
    REPORT         = "report"            # rolled into exec report
    # terminals
    WON            = "won"
    LOST           = "lost"
    BLOCKED        = "blocked"


TERMINAL = {Stage.WON, Stage.LOST, Stage.BLOCKED}

# Allowed transitions — forbid backwards accidents
ALLOWED: dict[Stage, set[Stage]] = {
    Stage.SIGNAL:         {Stage.ENRICH, Stage.BLOCKED},
    Stage.ENRICH:         {Stage.SCORE, Stage.BLOCKED},
    Stage.SCORE:          {Stage.DECIDE_CHANNEL, Stage.LOST, Stage.BLOCKED},
    Stage.DECIDE_CHANNEL: {Stage.DRAFT, Stage.APPROVAL, Stage.BLOCKED},
    Stage.DRAFT:          {Stage.APPROVAL, Stage.SEND, Stage.BLOCKED},
    Stage.SEND:           {Stage.WAIT_REPLY, Stage.BLOCKED},
    Stage.WAIT_REPLY:     {Stage.NEGOTIATE, Stage.LOST, Stage.SEND},  # retry allowed
    Stage.NEGOTIATE:      {Stage.APPROVAL, Stage.BOOK, Stage.LOST, Stage.BLOCKED},
    Stage.APPROVAL:       {Stage.DRAFT, Stage.SEND, Stage.NEGOTIATE, Stage.BOOK,
                           Stage.LOST, Stage.BLOCKED},
    Stage.BOOK:           {Stage.SUMMARIZE, Stage.LOST},
    Stage.SUMMARIZE:      {Stage.REPORT, Stage.WON, Stage.LOST},
    Stage.REPORT:         {Stage.WON, Stage.LOST},
}


# ============================================================================
# STATE — a single opportunity's journey. Serializable. Idempotent.
# ============================================================================

@dataclass
class LoopState:
    opportunity_id: str
    company_id: str
    stage: Stage = Stage.SIGNAL
    tier: str = "starter"                   # starter / pro / enterprise
    sector: str = "unknown"                 # real_estate / construction / retail / fintech
    expected_value_sar: float = 0.0
    win_probability: float = 0.0
    evidence: list[dict[str, Any]] = field(default_factory=list)
    history: list[dict[str, Any]] = field(default_factory=list)  # stage transitions
    pending_action: Optional[dict[str, Any]] = None              # next action draft
    approval_reason: Optional[str] = None
    blocked_reason: Optional[str] = None
    idempotency_keys: set[str] = field(default_factory=set)      # executed actions
    owner_feedback: list[dict[str, Any]] = field(default_factory=list)  # eval signal
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["stage"] = self.stage.value
        d["idempotency_keys"] = sorted(self.idempotency_keys)
        return d

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "LoopState":
        d = {**d}
        d["stage"] = Stage(d["stage"])
        d["idempotency_keys"] = set(d.get("idempotency_keys") or [])
        return cls(**d)


# ============================================================================
# TRANSITION ENGINE
# ============================================================================

class InvalidTransition(Exception):
    pass


class RevenueLoop:
    """Engine that transitions LoopState through stages.

    Policy gate is injected — keeps workflow decoupled from policy details.
    """

    def __init__(self, policy_gate: Callable[[LoopState, Stage, dict], Any] | None = None):
        self.policy_gate = policy_gate

    # ------------------------------------------------------------------ core

    def transition(self, state: LoopState, to: Stage,
                   *, payload: dict[str, Any] | None = None,
                   actor: str = "system") -> LoopState:
        """Move state from current → `to`. Records history. Idempotent per payload."""
        payload = payload or {}
        if to not in ALLOWED.get(state.stage, set()):
            raise InvalidTransition(
                f"{state.stage.value} → {to.value} not allowed "
                f"(legal: {[s.value for s in ALLOWED.get(state.stage, [])]})"
            )

        # Idempotency: hash (from_stage, to_stage, payload) per opportunity
        key = self._idempotency_key(state.stage, to, payload)
        if key in state.idempotency_keys:
            logger.info("idempotent skip: %s → %s (key=%s)", state.stage.value, to.value, key[:8])
            return state

        # Policy gate (hooked via Policy Engine v1). Can force APPROVAL or BLOCKED.
        if self.policy_gate:
            verdict = self.policy_gate(state, to, payload)
            if verdict and verdict.get("verdict") == "BLOCK":
                state = self._record(state, Stage.BLOCKED, actor, {
                    "blocked_from": state.stage.value, "target": to.value,
                    "reason": verdict.get("reason"),
                })
                state.blocked_reason = verdict.get("reason")
                state.idempotency_keys.add(key)
                return state
            if verdict and verdict.get("verdict") == "APPROVE" and to not in (Stage.APPROVAL,):
                # force APPROVAL interrupt before the requested transition
                state.pending_action = {"target": to.value, "payload": payload}
                state.approval_reason = verdict.get("reason")
                state = self._record(state, Stage.APPROVAL, actor, {
                    "reason": verdict.get("reason"),
                    "target_after_approval": to.value,
                })
                state.idempotency_keys.add(key)
                return state

        state = self._record(state, to, actor, payload)
        state.idempotency_keys.add(key)
        return state

    # ----------------------------------------------------------- convenience

    def resume_after_approval(self, state: LoopState, decision: str,
                              *, edits: dict | None = None,
                              actor: str = "owner") -> LoopState:
        """Owner acted on the APPROVAL interrupt. Advance or abort."""
        if state.stage is not Stage.APPROVAL:
            raise InvalidTransition(f"not awaiting approval (stage={state.stage.value})")
        state.owner_feedback.append({
            "decision": decision, "edits": edits,
            "at": datetime.now(timezone.utc).isoformat(), "actor": actor,
        })
        if decision == "reject":
            state = self._record(state, Stage.LOST, actor, {"reason": "owner_reject"})
            return state
        pending = state.pending_action or {}
        target = Stage(pending.get("target", Stage.DRAFT.value))
        payload = {**(pending.get("payload") or {}), "edits": edits or {}}
        state.pending_action = None
        state.approval_reason = None
        # Manually record — bypass policy_gate (owner already decided)
        state = self._record(state, target, actor, payload)
        return state

    # ------------------------------------------------------------- internals

    def _record(self, state: LoopState, to: Stage, actor: str,
                payload: dict[str, Any]) -> LoopState:
        state.history.append({
            "from": state.stage.value, "to": to.value, "actor": actor,
            "at": datetime.now(timezone.utc).isoformat(), "payload": payload,
        })
        state.stage = to
        state.updated_at = datetime.now(timezone.utc).isoformat()
        return state

    @staticmethod
    def _idempotency_key(from_: Stage, to: Stage, payload: dict) -> str:
        raw = json.dumps({"f": from_.value, "t": to.value, "p": payload},
                         sort_keys=True, ensure_ascii=False).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()


# ============================================================================
# SELF-TEST — full loop without DB or LLM
# ============================================================================

def _demo_policy_gate(state: LoopState, to: Stage, payload: dict) -> dict | None:
    # demo: force approval if sending to enterprise tier, block hard-coded red lines
    if payload.get("action") == "impersonate_human":
        return {"verdict": "BLOCK", "reason": "impersonation forbidden"}
    if to is Stage.SEND and state.tier == "enterprise":
        return {"verdict": "APPROVE", "reason": "enterprise tier — owner approval required"}
    return None


def _test_loop():
    loop = RevenueLoop(policy_gate=_demo_policy_gate)
    s = LoopState(
        opportunity_id=str(uuid.uuid4()),
        company_id=str(uuid.uuid4()),
        tier="pro", sector="real_estate",
        expected_value_sar=2_500_000, win_probability=0.62,
    )

    for target, payload in [
        (Stage.ENRICH,         {"source": "wathq", "cr": "7000123"}),
        (Stage.SCORE,          {"score": 87}),
        (Stage.DECIDE_CHANNEL, {"channel": "email"}),
        (Stage.DRAFT,          {"subject": "فرصة شراكة مجمع الملك فهد"}),
        (Stage.SEND,           {"channel": "email", "to": "ceo@example.sa"}),
        (Stage.WAIT_REPLY,     {"timer_hours": 24}),
        (Stage.NEGOTIATE,      {"reply_sentiment": "interested"}),
        (Stage.BOOK,           {"slot": "2026-04-24T10:00+03"}),
        (Stage.SUMMARIZE,      {"summary_ar": "ناقشنا..."}),
        (Stage.REPORT,         {"week": "W17"}),
        (Stage.WON,            {"signed_value_sar": 2_500_000}),
    ]:
        s = loop.transition(s, target, payload=payload, actor="strategist_agent")
        print(f"  → {s.stage.value:25s}  hist={len(s.history):2d}  idemp={len(s.idempotency_keys)}")

    assert s.stage is Stage.WON
    assert len(s.history) == 11
    print("✅ Happy-path loop: 11 transitions, terminal WON")

    # Test 2 — policy gate forces approval
    s2 = LoopState(opportunity_id="op2", company_id="c2", tier="enterprise")
    s2 = loop.transition(s2, Stage.ENRICH, payload={})
    s2 = loop.transition(s2, Stage.SCORE, payload={})
    s2 = loop.transition(s2, Stage.DECIDE_CHANNEL, payload={})
    s2 = loop.transition(s2, Stage.DRAFT, payload={})
    s2 = loop.transition(s2, Stage.SEND, payload={"channel": "email"})
    assert s2.stage is Stage.APPROVAL, f"enterprise tier should hit approval, got {s2.stage}"
    assert s2.approval_reason is not None
    print(f"✅ Policy interrupt: enterprise → APPROVAL (reason: {s2.approval_reason})")

    s2 = loop.resume_after_approval(s2, decision="approve",
                                    edits={"tone": "more formal"})
    assert s2.stage is Stage.SEND
    print(f"✅ Resume after approval: owner approved → SEND (edits applied)")

    # Test 3 — hard block
    s3 = LoopState(opportunity_id="op3", company_id="c3", tier="pro")
    s3 = loop.transition(s3, Stage.ENRICH, payload={})
    s3 = loop.transition(s3, Stage.SCORE, payload={})
    s3 = loop.transition(s3, Stage.DECIDE_CHANNEL, payload={})
    s3 = loop.transition(s3, Stage.DRAFT,
                         payload={"action": "impersonate_human", "body": "..."})
    assert s3.stage is Stage.BLOCKED
    print(f"✅ Policy block: impersonate_human → BLOCKED (reason: {s3.blocked_reason})")

    # Test 4 — idempotency (replaying the SAME transition is a no-op)
    s4 = LoopState(opportunity_id="op4", company_id="c4", tier="pro")
    s4 = loop.transition(s4, Stage.ENRICH, payload={})
    s4 = loop.transition(s4, Stage.SCORE, payload={})
    s4 = loop.transition(s4, Stage.DECIDE_CHANNEL, payload={})
    s4 = loop.transition(s4, Stage.DRAFT, payload={})
    s4 = loop.transition(s4, Stage.SEND, payload={"msg_id": "m-42"})
    before = len(s4.history)
    # Simulate a webhook replay of the DRAFT→SEND transition already executed.
    # The engine is called with the previous stage restored (as a replay would).
    s4_replay = loop.transition(
        LoopState.from_dict({**s4.to_dict(), "stage": "draft"}),
        Stage.SEND, payload={"msg_id": "m-42"},
    )
    # idempotency_keys was already populated, so SEND should short-circuit.
    assert s4_replay.stage is Stage.DRAFT, "replay should not re-execute"
    print(f"✅ Idempotency: replayed DRAFT→SEND short-circuited (still DRAFT)")

    # Test 5 — serialize/deserialize round trip
    blob = json.dumps(s.to_dict(), ensure_ascii=False)
    s_restored = LoopState.from_dict(json.loads(blob))
    assert s_restored.stage == s.stage
    assert len(s_restored.history) == len(s.history)
    print(f"✅ Serialization: {len(blob)} bytes round-tripped")

    print("\nAll revenue-loop tests passed.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    _test_loop()
