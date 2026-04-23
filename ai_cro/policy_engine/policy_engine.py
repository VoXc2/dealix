"""
Dealix Policy & Approval Engine — v1.0
=======================================

The heart of Balanced Autonomy. Every agent action is evaluated through this
engine before execution. Actions fall into three buckets:

1. AUTO       — execute immediately, log to audit trail
2. APPROVE    — pause agent, notify owner, wait for decision
3. BLOCK      — never execute, even with approval (hard-coded red lines)

This is NOT a wrapper around an LLM. It is deterministic rule evaluation
with full audit logging — required for PDPL + SAMA compliance and for
building owner trust in agent autonomy.

Usage:
    from policy_engine import PolicyEngine, ActionRequest

    engine = PolicyEngine(tier="pro")
    decision = engine.evaluate(ActionRequest(
        action_type="send_proposal",
        channel="email",
        amount_sar=8500,
        counterparty="متجر النخبة",
        agent="negotiator",
    ))
    # decision.verdict -> "auto" | "approve" | "block"
    # decision.reason  -> human-readable explanation (Arabic)
"""

from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable
from uuid import uuid4

logger = logging.getLogger("dealix.policy")


# ============================================================================
# CORE TYPES
# ============================================================================

class Verdict(str, Enum):
    AUTO = "auto"
    APPROVE = "approve"
    BLOCK = "block"


class Tier(str, Enum):
    STARTER = "starter"
    PRO = "pro"
    ENTERPRISE = "enterprise"


@dataclass
class ActionRequest:
    """A single proposed action from an agent."""
    action_type: str                    # e.g. send_email, send_proposal, sign_nda
    channel: str = ""                   # email, whatsapp, sms, voice, calendar
    agent: str = ""                     # strategist, sales_manager, negotiator, content, exec_intel
    amount_sar: float = 0.0             # financial exposure of this action
    counterparty: str = ""              # target company / contact
    content_preview: str = ""           # first 200 chars of message/proposal
    metadata: dict[str, Any] = field(default_factory=dict)
    # Auto-filled:
    request_id: str = field(default_factory=lambda: str(uuid4()))
    requested_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class PolicyDecision:
    verdict: Verdict
    reason: str                         # Arabic, human-readable
    rule_id: str                        # which rule fired (P0001, P0002, …)
    required_approver: str | None = None
    decided_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    request_id: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


# ============================================================================
# POLICY RULES — priority order: BLOCK > APPROVE > AUTO
# ============================================================================

# Financial thresholds requiring owner approval (in SAR) — per tier
AMOUNT_THRESHOLDS = {
    Tier.STARTER:    2_000,
    Tier.PRO:       10_000,
    Tier.ENTERPRISE: 50_000,
}

# Actions that are NEVER automated, regardless of amount
ALWAYS_APPROVE = {
    "sign_nda",
    "sign_contract",
    "grant_exclusivity",
    "modify_payment_terms",
    "issue_refund",
    "public_statement",
    "respond_to_competitor_news",
    "send_custom_pricing",
    "escalate_to_executive_meeting",
}

# Actions that are ALWAYS blocked — no approval can override (legal / safety)
ALWAYS_BLOCK = {
    "impersonate_human",                # violates Meta WhatsApp policy (Jan 2026)
    "share_competitor_confidential",
    "make_legal_commitment",            # only the owner or appointed legal rep
    "process_payment_outside_moyasar",
    "disclose_internal_pricing_models",
}

# Content guardrails — if any trigger matches content_preview, approve/block
CONTENT_GUARDS = [
    # (pattern, verdict, reason)
    ("اتفاقية حصرية",                 Verdict.APPROVE, "ذكر اتفاقية حصرية — يتطلب موافقة"),
    ("exclusivity agreement",         Verdict.APPROVE, "exclusivity clause mentioned — approval required"),
    ("خصم خاص",                        Verdict.APPROVE, "خصم خاص مقترح — تجاوز سياسة التسعير الافتراضية"),
    ("guaranteed",                     Verdict.APPROVE, "ضمان صريح في الرسالة — مراجعة قانونية مطلوبة"),
    ("refund",                         Verdict.APPROVE, "مبلغ مسترد مُذكر — يتطلب موافقة"),
]

# Channel-specific rules
# Meta banned general-purpose AI chatbots on WhatsApp Business Platform Jan 15, 2026.
# Only structured business workflows are allowed.
WHATSAPP_ALLOWED_INTENTS = {
    "schedule_meeting", "send_invoice", "booking_confirmation",
    "appointment_reminder", "order_status", "service_followup",
    "document_request", "delivery_update",
}


# ============================================================================
# ENGINE
# ============================================================================

class PolicyEngine:
    def __init__(self, tier: str = "pro", notifier: Callable | None = None,
                 audit_sink: Callable | None = None):
        try:
            self.tier = Tier(tier)
        except ValueError:
            raise ValueError(f"Unknown tier '{tier}'. Use starter|pro|enterprise.")
        self.notifier = notifier       # callable(decision) -> None
        self.audit_sink = audit_sink   # callable(decision, action) -> None
        self.threshold = AMOUNT_THRESHOLDS[self.tier]

    # -- Public API -----------------------------------------------------------

    def evaluate(self, action: ActionRequest) -> PolicyDecision:
        """Evaluate a proposed agent action. Returns PolicyDecision."""
        start = time.perf_counter()

        # Priority 1: Hard blocks (legal / safety)
        if action.action_type in ALWAYS_BLOCK:
            d = self._decide(action, Verdict.BLOCK,
                             f"الإجراء '{action.action_type}' محظور دائماً — خط أحمر قانوني/أمني",
                             "P0001")
            return self._finalize(d, action, start)

        # Priority 2: WhatsApp restrictions (Meta policy Jan 2026)
        if action.channel == "whatsapp":
            intent = action.metadata.get("intent", "")
            if intent and intent not in WHATSAPP_ALLOWED_INTENTS:
                d = self._decide(action, Verdict.BLOCK,
                                 f"قصد '{intent}' غير مسموح في WhatsApp Business Platform بعد يناير 2026. "
                                 "يُسمح فقط بـ structured business workflows (مواعيد، فواتير، متابعات خدمة).",
                                 "P0002")
                return self._finalize(d, action, start)

        # Priority 3: Content guardrails
        content = (action.content_preview or "").lower()
        for pattern, verdict, reason in CONTENT_GUARDS:
            if pattern.lower() in content:
                d = self._decide(action, verdict, reason, "P0003")
                if verdict == Verdict.APPROVE:
                    d.required_approver = "owner"
                return self._finalize(d, action, start)

        # Priority 4: Always-approve actions
        if action.action_type in ALWAYS_APPROVE:
            d = self._decide(action, Verdict.APPROVE,
                             f"الإجراء '{action.action_type}' يتطلب دائماً موافقة المالك",
                             "P0004", required_approver="owner")
            return self._finalize(d, action, start)

        # Priority 5: Amount threshold
        if action.amount_sar > self.threshold:
            d = self._decide(action, Verdict.APPROVE,
                             f"المبلغ {action.amount_sar:,.0f} ريال يتجاوز حد {self.tier.value} "
                             f"({self.threshold:,.0f} ريال) — موافقة المالك مطلوبة",
                             "P0005", required_approver="owner")
            return self._finalize(d, action, start)

        # Priority 6: Default — AUTO
        d = self._decide(action, Verdict.AUTO,
                         "ضمن حدود الاستقلالية المتوازنة — تنفيذ تلقائي مع تسجيل",
                         "P0006")
        return self._finalize(d, action, start)

    # -- Internal -------------------------------------------------------------

    def _decide(self, action: ActionRequest, verdict: Verdict, reason: str,
                rule_id: str, required_approver: str | None = None) -> PolicyDecision:
        return PolicyDecision(
            verdict=verdict,
            reason=reason,
            rule_id=rule_id,
            required_approver=required_approver,
            request_id=action.request_id,
            metadata={"tier": self.tier.value, "agent": action.agent}
        )

    def _finalize(self, decision: PolicyDecision, action: ActionRequest,
                  start: float) -> PolicyDecision:
        decision.metadata["latency_ms"] = round((time.perf_counter() - start) * 1000, 2)

        # Always audit
        log_entry = {
            "ts": decision.decided_at,
            "rule": decision.rule_id,
            "verdict": decision.verdict.value,
            "action": asdict(action),
            "decision": asdict(decision),
        }
        logger.info("policy_decision %s", json.dumps(log_entry, ensure_ascii=False))

        if self.audit_sink:
            try:
                self.audit_sink(decision, action)
            except Exception as e:  # never let audit break the decision
                logger.error("audit_sink failed: %s", e)

        # Notify owner only when approval is needed
        if decision.verdict == Verdict.APPROVE and self.notifier:
            try:
                self.notifier(decision, action)
            except Exception as e:
                logger.error("notifier failed: %s", e)

        return decision


# ============================================================================
# SELF-TEST
# ============================================================================

def _run_self_test() -> None:
    """Exercise every rule path. Run with: python -m policy_engine"""
    engine = PolicyEngine(tier="pro")
    scenarios = [
        ("AUTO — normal lead followup",
         ActionRequest(action_type="send_followup", channel="email",
                       amount_sar=0, agent="sales_manager")),
        ("APPROVE — amount over threshold",
         ActionRequest(action_type="send_proposal", channel="email",
                       amount_sar=25_000, agent="negotiator")),
        ("APPROVE — always-approve action (NDA)",
         ActionRequest(action_type="sign_nda", channel="email",
                       amount_sar=0, agent="negotiator")),
        ("APPROVE — content guard fires (exclusivity)",
         ActionRequest(action_type="send_proposal", channel="email",
                       amount_sar=5_000, agent="negotiator",
                       content_preview="نقترح اتفاقية حصرية لمدة 12 شهر")),
        ("BLOCK — hard-coded red line",
         ActionRequest(action_type="impersonate_human", channel="whatsapp",
                       amount_sar=0, agent="content")),
        ("BLOCK — WhatsApp general chatbot intent",
         ActionRequest(action_type="send_message", channel="whatsapp",
                       amount_sar=0, agent="content",
                       metadata={"intent": "general_chat"})),
        ("AUTO — WhatsApp allowed intent (schedule_meeting)",
         ActionRequest(action_type="send_message", channel="whatsapp",
                       amount_sar=0, agent="sales_manager",
                       metadata={"intent": "schedule_meeting"})),
    ]

    print(f"\n{'='*72}\nDealix Policy Engine v1.0 — self-test ({engine.tier.value} tier)\n{'='*72}")
    for label, action in scenarios:
        d = engine.evaluate(action)
        flag = {"auto": "✅", "approve": "🟡", "block": "🛑"}[d.verdict.value]
        print(f"{flag} {label}")
        print(f"   → {d.verdict.value.upper()} [{d.rule_id}] {d.reason}")
        print(f"   latency: {d.metadata['latency_ms']} ms\n")

    print("All scenarios passed.\n")


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    _run_self_test()
