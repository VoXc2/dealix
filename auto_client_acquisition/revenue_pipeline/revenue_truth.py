"""Revenue Pipeline — single-source-of-truth snapshot + V12.1 gate."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class RevenueTruthSnapshot:
    total_leads: int
    commitments: int
    paid: int
    total_revenue_sar: int
    revenue_live: bool
    paid_pilot_ready: bool
    v12_1_unlocked: bool
    proof_event_files_count: int
    blockers: list[str]
    next_action_ar: str
    next_action_en: str


def snapshot_revenue_truth(
    *,
    pipeline_summary: dict[str, int],
    proof_event_files_count: int = 0,
) -> RevenueTruthSnapshot:
    """Compose the canonical revenue-truth snapshot.

    ``pipeline_summary`` comes from ``RevenuePipeline.summary()``.
    ``proof_event_files_count`` counts non-template entries under
    ``docs/proof-events/``.

    Decision rules (canonical, do NOT silently change):
    - ``revenue_live`` is True ONLY if pipeline_summary['paid'] >= 1
      (real cash landed) AND total_revenue_sar > 0.
    - ``paid_pilot_ready`` is the V11/V12 truth label — always True
      because manual payment fallback is documented.
    - ``v12_1_unlocked`` per ``docs/V12_1_TRIGGER_RULES.md`` —
      requires AT LEAST ONE of: paid >= 1, commitments >= 1,
      proof_event_files_count >= 1.
    """
    paid = pipeline_summary.get("paid", 0)
    commitments = pipeline_summary.get("commitments", 0)
    total_revenue_sar = pipeline_summary.get("total_revenue_sar", 0)
    revenue_live = paid >= 1 and total_revenue_sar > 0

    v12_1_unlocked = (
        paid >= 1
        or commitments >= 1
        or proof_event_files_count >= 1
    )

    blockers: list[str] = []
    if paid == 0:
        blockers.append("no_paid_pilot_yet")
    if commitments == 0:
        blockers.append("no_written_commitment_yet")
    if proof_event_files_count == 0:
        blockers.append("no_real_proof_event_logged_yet")

    if revenue_live:
        next_ar = "اعتمد flip لـ REVENUE_LIVE=yes في PR منفصل + ابدأ V12.1 patch"
        next_en = "Flip REVENUE_LIVE=yes in a dedicated PR + begin V12.1 patches."
    elif v12_1_unlocked:
        next_ar = "V12.1 مسموح — ابنِ الـ patch المستند للأدلّة الموجودة فقط"
        next_en = "V12.1 unlocked — build patches grounded in existing evidence only."
    else:
        next_ar = "نفّذ 14_DAY_FIRST_REVENUE_PLAYBOOK — لا كود جديد"
        next_en = "Run 14_DAY_FIRST_REVENUE_PLAYBOOK — no new code."

    return RevenueTruthSnapshot(
        total_leads=pipeline_summary.get("total_leads", 0),
        commitments=commitments,
        paid=paid,
        total_revenue_sar=total_revenue_sar,
        revenue_live=revenue_live,
        paid_pilot_ready=True,
        v12_1_unlocked=v12_1_unlocked,
        proof_event_files_count=proof_event_files_count,
        blockers=blockers,
        next_action_ar=next_ar,
        next_action_en=next_en,
    )


def is_v12_1_unlocked(snapshot: RevenueTruthSnapshot) -> bool:
    return snapshot.v12_1_unlocked


def to_dict(snapshot: RevenueTruthSnapshot) -> dict[str, Any]:
    return {
        "total_leads": snapshot.total_leads,
        "commitments": snapshot.commitments,
        "paid": snapshot.paid,
        "total_revenue_sar": snapshot.total_revenue_sar,
        "revenue_live": snapshot.revenue_live,
        "paid_pilot_ready": snapshot.paid_pilot_ready,
        "v12_1_unlocked": snapshot.v12_1_unlocked,
        "proof_event_files_count": snapshot.proof_event_files_count,
        "blockers": snapshot.blockers,
        "next_action_ar": snapshot.next_action_ar,
        "next_action_en": snapshot.next_action_en,
    }
