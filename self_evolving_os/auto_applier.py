from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from .improvement_generator import ImprovementProposal

logger = logging.getLogger(__name__)

LEGACY_COMPATIBILITY_ONLY = True
LEGACY_DEACTIVATION_REASON = (
    "LEGACY_SELF_EVOLVING_APPLIER_DEACTIVATED: route evidence-backed changes through "
    "the canonical Dealix Development Factory (issue -> fresh-main branch/worktree -> "
    "tests -> Draft PR -> sovereign exact-head verification -> decision)"
)


@dataclass
class ApplicationResult:
    proposal_id: str
    success: bool
    applied_changes: dict[str, Any] = field(default_factory=dict)
    error: str | None = None
    duration_ms: float = 0.0
    applied_at: datetime = field(default_factory=datetime.utcnow)


class AutoApplier:
    """Legacy compatibility surface; automatic application is permanently disabled.

    The root ``self_evolving_os`` package is not an execution authority. Keeping
    this class import-compatible avoids breaking historical callers while making
    every mutation path fail closed. Approved engineering work must be routed to
    the canonical Development Factory and repository governance instead.
    """

    AUTO_APPLY_RISK_LEVELS: list[str] = []

    def __init__(self, approval_required: bool = True):
        self._approval_required = True
        self._application_log: list[ApplicationResult] = []
        self._applied_proposals: set[str] = set()
        if approval_required is False:
            logger.warning("Legacy AutoApplier ignores approval_required=False and remains fail-closed")

    async def try_apply(self, proposal: ImprovementProposal) -> ApplicationResult:
        return self._blocked_result(proposal)

    async def can_auto_apply(self, proposal: ImprovementProposal) -> bool:
        _ = proposal
        return False

    async def apply_with_approval(
        self,
        proposal: ImprovementProposal,
        *,
        approved: bool = False,
        reviewer: str | None = None,
    ) -> ApplicationResult:
        _ = (approved, reviewer)
        return self._blocked_result(proposal)

    async def rollback_application(self, proposal_id: str) -> bool:
        _ = proposal_id
        return False

    async def get_application_history(
        self,
        limit: int = 50,
    ) -> list[ApplicationResult]:
        return self._application_log[-limit:]

    async def get_applied_count(self) -> int:
        return 0

    async def _apply_changes(self, proposal: ImprovementProposal) -> dict[str, Any]:
        raise RuntimeError(LEGACY_DEACTIVATION_REASON)

    async def _rollback_changes(self, applied_changes: dict[str, Any]) -> None:
        _ = applied_changes
        raise RuntimeError(LEGACY_DEACTIVATION_REASON)

    def _blocked_result(self, proposal: ImprovementProposal) -> ApplicationResult:
        start = time.time()
        result = ApplicationResult(
            proposal_id=proposal.proposal_id,
            success=False,
            error=LEGACY_DEACTIVATION_REASON,
            duration_ms=round((time.time() - start) * 1000, 2),
        )
        self._application_log.append(result)
        logger.info("Blocked legacy self-evolving application for proposal %s", proposal.proposal_id)
        return result
