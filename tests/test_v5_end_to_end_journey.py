"""End-to-end smoke test across the 12 v5 layers.

Walks one fictitious customer (`ACME-PILOT-TEST`) through the full
journey: lead intake → diagnostic → pilot → invoice draft → in
delivery → proof event → proof pack → upsell. Asserts at each step
that the right module accepts the right transition AND that the
hard rules (no live charge, no forbidden tool unlock) hold even
when the loop has progressed all the way to the end.

This is the only test that exercises every v5 layer in one shot.
Each layer also has its own unit tests in test_v5_layers*.py — those
remain authoritative for that layer's surface area; this file only
asserts that the layers compose correctly.
"""
from __future__ import annotations

import os
import tempfile
from pathlib import Path

import pytest

from auto_client_acquisition.agent_governance import (
    AutonomyLevel,
    FORBIDDEN_TOOLS,
    ToolCategory,
    ToolPermission,
    evaluate_action,
)
from auto_client_acquisition.customer_loop import (
    JourneyAdvanceRequest,
    JourneyState,
    advance,
)
from auto_client_acquisition.delivery_factory import build_delivery_plan
from auto_client_acquisition.finance_os import (
    draft_invoice,
    is_live_charge_allowed,
)
from auto_client_acquisition.proof_ledger import (
    FileProofLedger,
    ProofEvent,
    ProofEventType,
    export_redacted,
)
from auto_client_acquisition.role_command_os import (
    RoleName,
    build_role_brief,
)


CUSTOMER_HANDLE = "ACME-PILOT-TEST"


def _advance_or_fail(current: JourneyState, target: JourneyState) -> None:
    """Helper that advances the journey and asserts acceptance."""
    result = advance(JourneyAdvanceRequest(
        current_state=current,
        target_state=target,
        customer_handle=CUSTOMER_HANDLE,
    ))
    assert result.accepted, (
        f"transition {current} → {target} should be allowed; got "
        f"rejection: {result.rejection_reason!r}"
    )
    assert result.from_state == current
    assert result.to_state == target
    # Bilingual checklist must always be present once accepted.
    assert result.next_actions_ar, f"missing AR actions for {target}"
    assert result.next_actions_en, f"missing EN actions for {target}"


def test_full_v5_customer_journey_end_to_end():
    """Walk the happy path from lead intake to upsell across all
    12 v5 layers. No external sends, no live charges."""

    # ── 1. lead_intake → diagnostic_requested ───────────────────
    _advance_or_fail(JourneyState.LEAD_INTAKE, JourneyState.DIAGNOSTIC_REQUESTED)

    # ── 2. diagnostic_requested → diagnostic_sent ───────────────
    _advance_or_fail(
        JourneyState.DIAGNOSTIC_REQUESTED,
        JourneyState.DIAGNOSTIC_SENT,
    )

    # ── 3. diagnostic_sent → pilot_offered ──────────────────────
    _advance_or_fail(JourneyState.DIAGNOSTIC_SENT, JourneyState.PILOT_OFFERED)

    # ── 4. finance_os: draft a 499 SAR pilot invoice ────────────
    invoice = draft_invoice(
        tier_id="growth_starter_pilot",
        customer_email="ops@acme-pilot-test.example.sa",
        customer_handle=CUSTOMER_HANDLE,
    )
    assert invoice.amount_sar == 499.0
    assert invoice.tier_id == "growth_starter_pilot"
    assert invoice.approval_status == "approval_required"
    # Hard rule: even with a draft invoice in hand, live charge stays off.
    live = is_live_charge_allowed()
    assert live["allowed"] is False, (
        f"is_live_charge_allowed must remain False; got {live!r}"
    )

    # ── 5. pilot_offered → payment_pending → paid_or_committed ──
    _advance_or_fail(JourneyState.PILOT_OFFERED, JourneyState.PAYMENT_PENDING)
    _advance_or_fail(
        JourneyState.PAYMENT_PENDING,
        JourneyState.PAID_OR_COMMITTED,
    )

    # ── 6. delivery_factory: build a real delivery plan ─────────
    plan = build_delivery_plan("lead_intake_whatsapp")
    plan_dict = plan.to_dict()
    assert plan_dict["service_id"] == "lead_intake_whatsapp"
    assert plan_dict["workflow_plan_ar"], "Arabic workflow must be non-empty"
    assert plan_dict["workflow_plan_en"], "English workflow must be non-empty"
    assert plan_dict["intake_checklist"], "intake checklist must be non-empty"
    assert plan_dict["approval_required"] is True

    # ── 7. paid_or_committed → in_delivery ──────────────────────
    _advance_or_fail(JourneyState.PAID_OR_COMMITTED, JourneyState.IN_DELIVERY)

    # ── 8. proof_ledger: record one event in an isolated temp dir
    with tempfile.TemporaryDirectory() as tmp:
        ledger = FileProofLedger(base_dir=Path(tmp))
        recorded = ledger.record(ProofEvent(
            event_type=ProofEventType.DELIVERY_TASK_COMPLETED,
            customer_handle=CUSTOMER_HANDLE,
            service_id="lead_intake_whatsapp",
            summary_ar="تم تسليم 10 فرص + مسوّدات عربيّة.",
            summary_en="Delivered 10 opportunities + Arabic drafts.",
            evidence_source="manual_pilot_session_1",
            confidence=1.0,
            consent_for_publication=False,
        ))
        assert recorded.id.startswith("evt_")
        assert recorded.customer_handle == CUSTOMER_HANDLE
        # Without consent, redacted_export must anonymize the handle.
        bundle = export_redacted(
            customer_handle=CUSTOMER_HANDLE,
            ledger=ledger,
        )
        assert bundle["total_returned"] == 1
        ev = bundle["events"][0]
        assert ev["customer_handle"] == "<anonymized>", (
            "customer_handle must be anonymized in export when "
            "consent_for_publication=False"
        )
        assert ev["summary_ar"] == ""
        assert ev["summary_en"] == ""

    # ── 9. in_delivery → proof_pack_ready → proof_pack_sent → upsell
    _advance_or_fail(JourneyState.IN_DELIVERY, JourneyState.PROOF_PACK_READY)
    _advance_or_fail(JourneyState.PROOF_PACK_READY, JourneyState.PROOF_PACK_SENT)
    _advance_or_fail(
        JourneyState.PROOF_PACK_SENT,
        JourneyState.UPSELL_RECOMMENDED,
    )

    # ── 10. role_command_os: CEO brief reflects the same data plane
    ceo = build_role_brief(RoleName.CEO)
    assert ceo.role == RoleName.CEO.value
    assert ceo.summary_ar, "CEO brief must have an Arabic summary"
    assert ceo.summary_en, "CEO brief must have an English summary"
    assert ceo.top_decisions, "CEO brief must have at least one decision"
    # Guardrails must always be present and on.
    assert ceo.guardrails["no_live_send"] is True
    assert ceo.guardrails["no_scraping"] is True
    assert ceo.guardrails["no_cold_outreach"] is True

    # ── 11. invariant: live charge STILL not allowed after the
    # full happy path. Progression in the loop never unlocks money.
    live_after = is_live_charge_allowed()
    assert live_after["allowed"] is False, (
        "is_live_charge_allowed must remain False even after the "
        f"full journey; got {live_after!r}"
    )


def test_journey_does_not_unlock_forbidden_agent_tools():
    """Independent of journey state, the agent_governance plane
    refuses every FORBIDDEN tool for every autonomy level. The
    customer-loop progress never grants new permissions."""
    forbidden = [
        ToolCategory.SEND_WHATSAPP_LIVE,
        ToolCategory.LINKEDIN_AUTOMATION,
        ToolCategory.SCRAPE_WEB,
        ToolCategory.CHARGE_PAYMENT_LIVE,
        ToolCategory.SEND_EMAIL_LIVE,
    ]
    for tool in forbidden:
        assert tool in FORBIDDEN_TOOLS, (
            f"{tool} must be on FORBIDDEN_TOOLS"
        )
        for level in AutonomyLevel:
            verdict = evaluate_action(
                agent_id="acme_pilot_journey_agent",
                tool=tool,
                autonomy_level=level,
                # Even if the agent's allowed_tools mistakenly
                # contains a forbidden tool, FORBIDDEN_TOOLS wins.
                allowed_tools=[tool],
            )
            assert verdict.permitted is False, (
                f"tool {tool} at level {level} must NOT be permitted "
                f"even if listed in allowed_tools; got {verdict.to_dict()!r}"
            )
            assert verdict.permission == ToolPermission.FORBIDDEN.value


def test_invalid_transition_is_rejected_with_honest_reason():
    """Skipping stages (e.g. lead_intake → in_delivery) must fail
    with a clear rejection reason — never silently accepted."""
    result = advance(JourneyAdvanceRequest(
        current_state=JourneyState.LEAD_INTAKE,
        target_state=JourneyState.IN_DELIVERY,
        customer_handle=CUSTOMER_HANDLE,
    ))
    assert result.accepted is False
    assert result.to_state is None
    assert result.rejection_reason
    assert "not allowed" in result.rejection_reason
