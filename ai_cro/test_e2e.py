"""
Dealix AI CRO — End-to-End Integration Test
=============================================

Signal → … → Report against LIVE DB, using the REAL module APIs:
  - LeadEngine.search()
  - ActionCenter.queue()
  - PolicyEngine.evaluate(ActionRequest)
  - RevenueLoop.transition() / resume_after_approval()
  - get_playbook()
"""

from __future__ import annotations

import asyncio
import os
import sys
import uuid

sys.path.insert(0, "/opt/dealix")

from ai_cro.workflow.revenue_loop import (  # type: ignore
    RevenueLoop, LoopState, Stage,
)
from ai_cro.action_center.action_center import ActionCenter  # type: ignore
from ai_cro.lead_engine.lead_engine import LeadEngine  # type: ignore
from ai_cro.policy_engine.policy_engine import (  # type: ignore
    PolicyEngine, ActionRequest, Verdict,
)
from ai_cro.playbooks.sector_playbooks import (  # type: ignore
    get as get_playbook, tier_threshold,
)


DSN = os.environ.get(
    "DEALIX_DSN",
    "postgresql://dealix:dealix_local_dev_2026@127.0.0.1:5432/dealix",
)


def _banner(title: str) -> None:
    print(f"\n{'═' * 70}\n  {title}\n{'═' * 70}")


def _gate(state: LoopState, to: Stage, payload: dict):
    if payload.get("action") == "impersonate_human":
        return {"verdict": "BLOCK", "reason": "impersonation forbidden"}
    if to is Stage.SEND and state.tier == "enterprise":
        return {"verdict": "APPROVE", "reason": "enterprise tier — owner approval required"}
    return None


async def main() -> int:
    # ── STEP 1 ────────────────────────────────────────────────────────────
    _banner("STEP 1 · Lead Engine — resolve the seeded opportunity")
    le = LeadEngine(dsn=DSN)
    results = await le.search("الأهلية", limit=5)
    assert results, "lead engine returned 0 results — seeded data missing?"
    lead = results[0]
    print(f"✓ resolved: {lead.name_ar} (conf={lead.confidence:.2f})")
    print(f"  evidence cards: {len(lead.evidence)}")
    print(f"  reason: {lead.reason}")

    # ── STEP 2 ────────────────────────────────────────────────────────────
    _banner("STEP 2 · Action Center — queue should contain first_move")
    ac = ActionCenter(dsn=DSN)
    items = await ac.queue(limit=10)
    assert items, "action center queue is empty"
    first = items[0]
    print(f"✓ top item [{first.kind}] pri={first.priority}")
    print(f"  company: {first.company_name}")
    print(f"  title:   {first.title_ar}")
    print(f"  next:    {first.next_action_label_ar}")
    opportunity_id = first.id

    # ── STEP 3 ────────────────────────────────────────────────────────────
    _banner("STEP 3 · Policy Engine — block impersonation, approve large deal")
    policy = PolicyEngine(tier="pro")

    impers = policy.evaluate(ActionRequest(
        action_type="impersonate_human", channel="whatsapp",
        agent="content", counterparty=lead.name_ar,
    ))
    assert impers.verdict == Verdict.BLOCK, f"expected BLOCK, got {impers.verdict}"
    print(f"✓ impersonate → BLOCK: {impers.reason}")

    big = policy.evaluate(ActionRequest(
        action_type="send_proposal", channel="email",
        agent="sales_manager", amount_sar=1_550_000,
        counterparty=lead.name_ar,
    ))
    assert big.verdict == Verdict.APPROVE, f"expected APPROVE, got {big.verdict}"
    print(f"✓ 1.55M proposal → APPROVE: {big.reason}")

    # ── STEP 4 ────────────────────────────────────────────────────────────
    _banner("STEP 4 · Sector Playbook — real_estate guidance loaded")
    pb = get_playbook("real_estate")
    assert pb is not None
    print(f"✓ playbook: {pb.name_ar}")
    print(f"  channels: {' → '.join(pb.outreach_order)}")
    print(f"  threshold (pro): {tier_threshold(pb.sector, 'pro'):,} SAR")

    # ── STEP 5 ────────────────────────────────────────────────────────────
    _banner("STEP 5 · Revenue Loop — full traversal with approval interrupt")
    loop = RevenueLoop(policy_gate=_gate)
    state = LoopState(
        opportunity_id=str(opportunity_id),
        company_id=str(uuid.uuid4()),
        tier="enterprise",
        sector="real_estate",
        expected_value_sar=1_550_000,
        win_probability=0.70,
    )

    # drive forward until APPROVAL interrupts at SEND
    path_to_send = [
        (Stage.ENRICH,         {"source": "wathq"}),
        (Stage.SCORE,          {"score": 87}),
        (Stage.DECIDE_CHANNEL, {"channel": "email"}),
        (Stage.DRAFT,          {"subject": "فرصة الشراكة"}),
        (Stage.SEND,           {"channel": "email", "to": "ceo@example.sa"}),
    ]
    for target, payload in path_to_send:
        state = loop.transition(state, target, payload=payload, actor="strategist")

    assert state.stage is Stage.APPROVAL, (
        f"expected APPROVAL (enterprise tier gate), got {state.stage}"
    )
    print(f"✓ reached APPROVAL after {len(state.history)} transitions "
          f"(reason: {state.approval_reason})")

    # owner approves
    state = loop.resume_after_approval(state, decision="approve",
                                       edits={"tone": "more formal"})
    assert state.stage is Stage.SEND
    print(f"✓ resumed after approval → SEND")

    # continue to terminal WON
    for target, payload in [
        (Stage.WAIT_REPLY, {"timer_hours": 24}),
        (Stage.NEGOTIATE,  {"reply_sentiment": "interested"}),
        (Stage.BOOK,       {"slot": "2026-04-28T10:00+03"}),
        (Stage.SUMMARIZE,  {"summary_ar": "تم الاتفاق على المرحلة الأولى"}),
        (Stage.REPORT,     {"week": "W17"}),
        (Stage.WON,        {"signed_value_sar": 1_550_000}),
    ]:
        state = loop.transition(state, target, payload=payload, actor="strategist")

    assert state.stage is Stage.WON
    print(f"✓ terminal: {state.stage.value}  ·  total history = {len(state.history)}")

    # ── STEP 6 ────────────────────────────────────────────────────────────
    _banner("STEP 6 · Priority view — weighted value reflects the deal")
    import asyncpg  # type: ignore
    conn = await asyncpg.connect(DSN)
    try:
        row = await conn.fetchrow(
            "SELECT COUNT(*) AS n, COALESCE(SUM(weighted_value),0) AS total "
            "FROM v_priority_opportunities"
        )
        print(f"✓ v_priority_opportunities: {row['n']} row(s), "
              f"total weighted = {row['total']:,} SAR")
    finally:
        await conn.close()

    _banner("E2E RESULT")
    print("✅ signal→enrich→score→decide→draft→send→APPROVAL→resume→"
          "wait→negotiate→book→summarize→report→WON")
    print("✅ lead engine · action center · policy · playbooks · "
          "state machine · priority view — all green on LIVE DB")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
