"""Daily Founder Command Summary — five-question CEO brief (§39 / Operating Rhythm)."""

from __future__ import annotations

from typing import Any

from auto_client_acquisition.founder_command_summary.engagement_registry import (
    EngagementSnapshot,
)


def _opportunity_score(s: EngagementSnapshot) -> float:
    dq = s.data_quality_score or 0.0
    ps = s.proof_score or 0.0
    stage_bonus = 0.0
    if s.score_done:
        stage_bonus += 15.0
    if s.draft_done:
        stage_bonus += 10.0
    if s.finalize_done:
        stage_bonus += 15.0
    if s.proof_generated:
        stage_bonus += 25.0
    return dq * 0.35 + ps * 0.35 + stage_bonus


def build_daily_founder_summary(
    snapshots: dict[str, EngagementSnapshot],
) -> dict[str, Any]:
    """Aggregate engagement state into the five daily CEO questions (bilingual)."""
    items = list(snapshots.values())
    if not items:
        return {
            "brief_type": "daily_founder_command_summary",
            "engagements_count": 0,
            "questions": {
                "q1_top_revenue": {
                    "ar": "لا توجد مشاركات مسجّلة بعد — شغّل أول Revenue Intelligence sprint.",
                    "en": "No engagements recorded yet — run the first Revenue Intelligence sprint.",
                    "evidence": None,
                },
                "q2_delivery_risk": {
                    "ar": "لا مخاطر تسليم مسجّلة.",
                    "en": "No delivery risks registered.",
                    "evidence": None,
                },
                "q3_governance_risk": {
                    "ar": "لا إشارات حوكمة على مشاركات نشطة.",
                    "en": "No governance signals on active engagements.",
                    "evidence": None,
                },
                "q4_proof_to_improve": {
                    "ar": "لا Proof Packs مكتملة بعد.",
                    "en": "No completed Proof Packs yet.",
                    "evidence": None,
                },
                "q5_stop_or_deprioritize": {
                    "ar": "ركّز على تسجيل أول engagement بعد الـ import.",
                    "en": "Focus on recording the first engagement post-import.",
                    "evidence": None,
                },
            },
        }

    top = max(items, key=_opportunity_score)
    stuck_draft = [s for s in items if s.draft_done and not s.finalize_done]
    gov = [s for s in items if s.pii_flagged or s.governance_notes]
    proof_done = [s for s in items if s.proof_generated and s.proof_score is not None]
    worst_proof = min(proof_done, key=lambda s: s.proof_score or 0.0) if proof_done else None

    return {
        "brief_type": "daily_founder_command_summary",
        "engagements_count": len(items),
        "questions": {
            "q1_top_revenue": {
                "ar": f"أعلى فرصة: {top.client_label or top.engagement_id} — درجة فرصة مركّبة {_opportunity_score(top):.1f}.",
                "en": f"Top opportunity: {top.client_label or top.engagement_id} — composite score {_opportunity_score(top):.1f}.",
                "evidence": {"engagement_id": top.engagement_id, "metric": "opportunity_score"},
            },
            "q2_delivery_risk": {
                "ar": f"{'مخاطر تسليم: مسودات بدون finalize (' + str(len(stuck_draft)) + ')' if stuck_draft else 'لا توقف بين draft و finalize.'}",
                "en": f"{'Delivery risk: drafts without finalize (' + str(len(stuck_draft)) + ')' if stuck_draft else 'No draft→finalize stalls.'}",
                "evidence": [{"engagement_id": s.engagement_id} for s in stuck_draft[:5]] or None,
            },
            "q3_governance_risk": {
                "ar": f"{'تنبيهات حوكمة/PII: ' + str(len(gov)) + ' مشارك(ة)' if gov else 'لا تنبيهات حوكمة مفتوحة.'}",
                "en": f"{'Governance/PII flags: ' + str(len(gov)) + ' engagement(s)' if gov else 'No open governance flags.'}",
                "evidence": [{"engagement_id": s.engagement_id, "notes": list(s.governance_notes)} for s in gov[:5]]
                or None,
            },
            "q4_proof_to_improve": {
                "ar": (
                    f"أضعف Proof حاليًا: {worst_proof.engagement_id} (score {worst_proof.proof_score})"
                    if worst_proof
                    else "أكمل finalize + proof pack لقياس Proof."
                ),
                "en": (
                    f"Weakest proof: {worst_proof.engagement_id} (score {worst_proof.proof_score})"
                    if worst_proof
                    else "Complete finalize + proof pack to measure proof strength."
                ),
                "evidence": {"engagement_id": worst_proof.engagement_id} if worst_proof else None,
            },
            "q5_stop_or_deprioritize": {
                "ar": "راجع engagement بلا تقدم لأكثر من خطوة — أو أوقف عملاء يرفضون الحوكمة.",
                "en": "Review engagements stalled across stages — or pause clients rejecting governance.",
                "evidence": None,
            },
        },
    }
