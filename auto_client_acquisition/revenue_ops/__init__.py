"""Revenue Ops — the Governed Revenue Ops Diagnostic delivery surface.

Pure-function core for the Diagnostic entry service: create + score a
diagnostic, intake a CRM/data file, assemble a decision passport, and generate
governed follow-up drafts. Every external action is approval-gated; nothing
auto-sends.
"""

from __future__ import annotations

from auto_client_acquisition.revenue_ops.decision_passport import (
    DecisionPassportSummary,
    build_decision_passport,
)
from auto_client_acquisition.revenue_ops.diagnostic import (
    Diagnostic,
    create_diagnostic,
)
from auto_client_acquisition.revenue_ops.follow_up_drafts import (
    FollowUpDraft,
    generate_follow_up_drafts,
)
from auto_client_acquisition.revenue_ops.scoring import (
    ReadinessScore,
    score_readiness,
)
from auto_client_acquisition.revenue_ops.upload import (
    UploadResult,
    intake_csv,
)

__all__ = [
    "DecisionPassportSummary",
    "Diagnostic",
    "FollowUpDraft",
    "ReadinessScore",
    "UploadResult",
    "build_decision_passport",
    "create_diagnostic",
    "generate_follow_up_drafts",
    "intake_csv",
    "score_readiness",
]
