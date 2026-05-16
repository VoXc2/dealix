"""Approval checkpoint engine."""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import StrEnum


class ApprovalState(StrEnum):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'


@dataclass(frozen=True, slots=True)
class ApprovalRequest:
    request_id: str
    action_name: str
    requester: str
    state: ApprovalState
    created_at_epoch: int
    approver: str = ''


_REQUESTS: dict[str, ApprovalRequest] = {}


def create_approval_request(*, request_id: str, action_name: str, requester: str, now_epoch: int) -> ApprovalRequest:
    req = ApprovalRequest(
        request_id=request_id,
        action_name=action_name,
        requester=requester,
        state=ApprovalState.PENDING,
        created_at_epoch=now_epoch,
    )
    _REQUESTS[request_id] = req
    return req


def decide_approval(*, request_id: str, approve: bool, approver: str) -> ApprovalRequest:
    current = _REQUESTS.get(request_id)
    if current is None:
        raise KeyError('approval_request_not_found')
    state = ApprovalState.APPROVED if approve else ApprovalState.REJECTED
    updated = replace(current, state=state, approver=approver)
    _REQUESTS[request_id] = updated
    return updated


def get_approval_request(request_id: str) -> ApprovalRequest | None:
    return _REQUESTS.get(request_id)


def list_pending_approvals() -> tuple[ApprovalRequest, ...]:
    return tuple(req for req in _REQUESTS.values() if req.state == ApprovalState.PENDING)


def clear_approval_requests_for_tests() -> None:
    _REQUESTS.clear()


__all__ = [
    'ApprovalRequest',
    'ApprovalState',
    'clear_approval_requests_for_tests',
    'create_approval_request',
    'decide_approval',
    'get_approval_request',
    'list_pending_approvals',
]
