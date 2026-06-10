from __future__ import annotations

import logging
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from .improvement_generator import ImprovementProposal, RiskLevel

logger = logging.getLogger(__name__)


@dataclass
class ApplicationResult:
    proposal_id: str
    success: bool
    applied_changes: dict[str, Any] = field(default_factory=dict)
    error: str | None = None
    duration_ms: float = 0.0
    applied_at: datetime = field(default_factory=datetime.utcnow)


class AutoApplier:
    AUTO_APPLY_RISK_LEVELS = ["low"]

    def __init__(self, approval_required: bool = False):
        self._approval_required = approval_required
        self._application_log: list[ApplicationResult] = []
        self._applied_proposals: set[str] = set()

    async def try_apply(self, proposal: ImprovementProposal) -> ApplicationResult:
        start = time.time()

        if not await self.can_auto_apply(proposal):
            return ApplicationResult(
                proposal_id=proposal.proposal_id,
                success=False,
                error=f"Proposal risk level '{proposal.risk_level.value}' not in auto-apply range: {self.AUTO_APPLY_RISK_LEVELS}",
            )

        if proposal.proposal_id in self._applied_proposals:
            return ApplicationResult(
                proposal_id=proposal.proposal_id,
                success=False,
                error="Proposal already applied",
            )

        try:
            applied = await self._apply_changes(proposal)
            self._applied_proposals.add(proposal.proposal_id)

            duration = (time.time() - start) * 1000
            result = ApplicationResult(
                proposal_id=proposal.proposal_id,
                success=True,
                applied_changes=applied,
                duration_ms=round(duration, 2),
            )

            self._application_log.append(result)
            logger.info(
                "Auto-applied proposal %s: %s (%.0fms)",
                proposal.proposal_id, proposal.title, duration,
            )
            return result

        except Exception as e:
            logger.exception("Failed to auto-apply proposal %s", proposal.proposal_id)
            result = ApplicationResult(
                proposal_id=proposal.proposal_id,
                success=False,
                error=str(e),
                duration_ms=(time.time() - start) * 1000,
            )
            self._application_log.append(result)
            return result

    async def can_auto_apply(self, proposal: ImprovementProposal) -> bool:
        if proposal.risk_level.value not in self.AUTO_APPLY_RISK_LEVELS:
            return False
        if self._approval_required:
            return False
        return True

    async def apply_with_approval(self, proposal: ImprovementProposal) -> ApplicationResult:
        return await self.try_apply(proposal)

    async def rollback_application(self, proposal_id: str) -> bool:
        for result in reversed(self._application_log):
            if result.proposal_id == proposal_id and result.success:
                try:
                    await self._rollback_changes(result.applied_changes)
                    self._applied_proposals.discard(proposal_id)
                    logger.info("Rolled back application of proposal %s", proposal_id)
                    return True
                except Exception as e:
                    logger.error("Rollback failed for proposal %s: %s", proposal_id, e)
                    return False
        return False

    async def get_application_history(
        self,
        limit: int = 50,
    ) -> list[ApplicationResult]:
        return self._application_log[-limit:]

    async def get_applied_count(self) -> int:
        return len(self._applied_proposals)

    async def _apply_changes(self, proposal: ImprovementProposal) -> dict[str, Any]:
        logger.debug("Applying changes for proposal %s: %s", proposal.proposal_id, proposal.config_changes)
        return {
            "applied": True,
            "config_changes": proposal.config_changes,
            "proposal_id": proposal.proposal_id,
            "category": proposal.category.value,
        }

    async def _rollback_changes(self, applied_changes: dict[str, Any]) -> None:
        logger.debug("Rolling back changes: %s", applied_changes)
