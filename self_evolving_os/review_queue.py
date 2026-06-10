from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

from .improvement_generator import ImprovementProposal, RiskLevel

logger = logging.getLogger(__name__)


class ReviewStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    IN_REVIEW = "in_review"
    DEFERRED = "deferred"


@dataclass
class ReviewItem:
    review_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    proposal: ImprovementProposal | None = None
    status: ReviewStatus = ReviewStatus.PENDING
    reviewed_by: str | None = None
    reviewed_at: datetime | None = None
    rejection_reason: str | None = None
    comments: list[dict[str, Any]] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class ApprovalResult:
    review_id: str
    proposal_id: str
    approved: bool
    reviewed_by: str | None = None
    reason: str | None = None


class ReviewQueue:
    def __init__(self):
        self._queue: dict[str, ReviewItem] = {}
        self._reviewed: dict[str, ReviewItem] = {}

    async def add(self, proposal: ImprovementProposal) -> ReviewItem:
        item = ReviewItem(
            proposal=proposal,
            status=ReviewStatus.PENDING,
        )
        self._queue[item.review_id] = item
        logger.info(
            "Added proposal '%s' to review queue (risk: %s)",
            proposal.title, proposal.risk_level.value,
        )
        return item

    async def get_pending(
        self,
        risk_level: str | None = None,
    ) -> list[ImprovementProposal]:
        items = [
            item for item in self._queue.values()
            if item.status == ReviewStatus.PENDING
        ]
        if risk_level:
            items = [
                item for item in items
                if item.proposal and item.proposal.risk_level.value == risk_level
            ]
        return [item.proposal for item in items if item.proposal]

    async def approve(
        self,
        proposal_id: str,
        reviewer: str = "founder",
    ) -> ApprovalResult:
        item = self._find_by_proposal_id(proposal_id)
        if not item:
            return ApprovalResult(
                review_id="",
                proposal_id=proposal_id,
                approved=False,
                reason="Proposal not found in review queue",
            )

        item.status = ReviewStatus.APPROVED
        item.reviewed_by = reviewer
        item.reviewed_at = datetime.utcnow()
        self._move_to_reviewed(item)

        logger.info("Proposal '%s' approved by %s", proposal_id, reviewer)
        return ApprovalResult(
            review_id=item.review_id,
            proposal_id=proposal_id,
            approved=True,
            reviewed_by=reviewer,
        )

    async def reject(
        self,
        proposal_id: str,
        reason: str = "",
        reviewer: str = "founder",
    ) -> None:
        item = self._find_by_proposal_id(proposal_id)
        if not item:
            logger.warning("Proposal %s not found for rejection", proposal_id)
            return

        item.status = ReviewStatus.REJECTED
        item.reviewed_by = reviewer
        item.reviewed_at = datetime.utcnow()
        item.rejection_reason = reason
        self._move_to_reviewed(item)

        logger.info("Proposal '%s' rejected by %s: %s", proposal_id, reviewer, reason)

    async def defer(
        self,
        proposal_id: str,
        reason: str = "",
    ) -> None:
        item = self._find_by_proposal_id(proposal_id)
        if item:
            item.status = ReviewStatus.DEFERRED
            if reason:
                item.rejection_reason = reason
            logger.info("Proposal '%s' deferred: %s", proposal_id, reason)

    async def add_comment(
        self,
        proposal_id: str,
        author: str,
        comment: str,
    ) -> None:
        item = self._find_by_proposal_id(proposal_id)
        if item:
            item.comments.append({
                "author": author,
                "comment": comment,
                "timestamp": datetime.utcnow().isoformat(),
            })

    async def get_queue_stats(self) -> dict[str, int]:
        stats: dict[str, int] = {}
        for item in self._queue.values():
            status = item.status.value
            stats[status] = stats.get(status, 0) + 1
        for item in self._reviewed.values():
            status = item.status.value
            stats[status] = stats.get(status, 0) + 1
        return stats

    async def get_reviewed(
        self,
        limit: int = 50,
        status: ReviewStatus | None = None,
    ) -> list[ReviewItem]:
        items = list(self._reviewed.values())
        if status:
            items = [i for i in items if i.status == status]
        return sorted(items, key=lambda i: i.reviewed_at or i.created_at, reverse=True)[:limit]

    async def get_item_by_review_id(self, review_id: str) -> ReviewItem | None:
        return self._queue.get(review_id) or self._reviewed.get(review_id)

    async def queue_length(self) -> int:
        return len([i for i in self._queue.values() if i.status == ReviewStatus.PENDING])

    def _find_by_proposal_id(self, proposal_id: str) -> ReviewItem | None:
        for item in self._queue.values():
            if item.proposal and item.proposal.proposal_id == proposal_id:
                return item
        for item in self._reviewed.values():
            if item.proposal and item.proposal.proposal_id == proposal_id:
                return item
        return None

    def _move_to_reviewed(self, item: ReviewItem) -> None:
        if item.review_id in self._queue:
            del self._queue[item.review_id]
        self._reviewed[item.review_id] = item
