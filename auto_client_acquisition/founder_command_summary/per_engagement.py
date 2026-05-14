"""Per-engagement blocker classification + next action for Founder Summary."""

from __future__ import annotations

from typing import Any, Literal

from auto_client_acquisition.founder_command_summary.engagement_registry import (
    EngagementSnapshot,
)

BlockerCategory = Literal[
    "none",
    "data_readiness",
    "source_passport",
    "pipeline_stall",
    "governance_pii",
    "proof_weak",
    "retainer_not_ready",
]


def classify_engagement_blocker(s: EngagementSnapshot) -> tuple[BlockerCategory, str, str, dict[str, Any]]:
    """Return (category, next_action_ar, next_action_en, detail)."""
    if not s.import_done:
        return (
            "data_readiness",
            "أكمل import + Source Passport validation.",
            "Complete import + Source Passport validation.",
            {"stage": "import"},
        )
    if s.pii_flagged and s.draft_done:
        return (
            "governance_pii",
            "راجع مسودات تحتوي PII — موافقة بشرية قبل أي إجراء خارجي.",
            "Review drafts with PII — human approval before any external action.",
            {"notes": list(s.governance_notes)},
        )
    if s.import_done and not s.score_done:
        return (
            "pipeline_stall",
            "شغّل scoring لترتيب الحسابات وتحديد Top 10.",
            "Run scoring to rank accounts and surface Top 10.",
            {"stage": "score"},
        )
    if s.score_done and not s.draft_done:
        return (
            "pipeline_stall",
            "ولّد Draft Pack (DRAFT_ONLY) ثم راجعه بشريًا.",
            "Generate Draft Pack (DRAFT_ONLY) then human review.",
            {"stage": "draft_pack"},
        )
    if s.draft_done and not s.finalize_done:
        return (
            "pipeline_stall",
            "أكمل finalize لبناء سرد Proof Pack v2.",
            "Run finalize to assemble Proof Pack v2 narrative.",
            {"stage": "finalize"},
        )
    if s.finalize_done and not s.proof_generated:
        return (
            "proof_weak",
            "ولّد Proof Pack الرسمي واحسب proof_score.",
            "Generate formal Proof Pack and compute proof_score.",
            {"stage": "proof_pack"},
        )
    if s.proof_generated:
        ps = s.proof_score or 0.0
        ch = s.client_health or 0.0
        if ps < 80.0 or ch < 70.0:
            return (
                "retainer_not_ready",
                "حسّن الجودة أو التبني قبل دفع Retainer — راجع retainer-gate.",
                "Improve quality or adoption before retainer push — check retainer-gate.",
                {"proof_score": ps, "client_health": ch},
            )
    if s.retainer_evaluated and s.retainer_decision:
        return (
            "none",
            f"التسليم متقدم — قرار retainer: {s.retainer_decision}",
            f"Pipeline advanced — retainer decision: {s.retainer_decision}",
            {"retainer_decision": s.retainer_decision},
        )
    return (
        "none",
        "المسار ضمن التوقعات — تابع الخطوة التالية في الـ pipeline.",
        "On track — proceed with the next pipeline step.",
        {"stages": s.to_public_dict()["stages"]},
    )
