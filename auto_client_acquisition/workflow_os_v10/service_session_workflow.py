"""Pre-defined ServiceSession workflow — the "growth_starter_7_day" pilot.

One step per Pilot day plus a closing pack-prep step. All steps remain
inert (drafts only, approval-required) — the workflow itself does not
trigger any external send.
"""
from __future__ import annotations

from auto_client_acquisition.workflow_os_v10.schemas import WorkflowDefinition


GROWTH_STARTER_7_DAY = WorkflowDefinition(
    workflow_id="wf_growth_starter_7_day",
    name="growth_starter_7_day",
    description_ar=(
        "حلقة 7 أيام لمسار النمو — كل يوم يولّد مسوّدات تحتاج موافقة "
        "بشرية قبل أيّ إرسال خارجي."
    ),
    description_en=(
        "7-day growth-starter loop — each day produces drafts that require "
        "human approval before any external send."
    ),
    steps=[
        "day_1_kickoff_diagnostic",
        "day_2_top10_opportunity_list",
        "day_3_arabic_outreach_drafts",
        "day_4_followup_plan",
        "day_5_proof_event_log",
        "day_6_qa_gate_review",
        "day_7_proof_pack_assemble",
    ],
)
