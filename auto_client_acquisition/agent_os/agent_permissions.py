"""Role & permission matrix — task 2 of the Agent Operating System.

Maps an agent *role* to a decision per *operation type*. This is the
role-level layer; tool-level governance stays with
``auto_client_acquisition.agent_governance.evaluate_action``. The two are
complementary — this module never overrides a forbidden-tool block.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from auto_client_acquisition.agent_os.agent_card import AgentCard
from auto_client_acquisition.agent_os.autonomy_levels import (
    DEFAULT_AUTONOMY,
    AutonomyLevel,
    coerce_autonomy,
)
from auto_client_acquisition.agent_os.tool_permissions import is_tool_allowed


class OperationType(StrEnum):
    READ = "read"
    ANALYZE = "analyze"
    DRAFT = "draft"
    RECOMMEND = "recommend"
    EXECUTE = "execute"
    EXPORT = "export"
    DELETE = "delete"
    APPROVE = "approve"


class PermissionDecision(StrEnum):
    ALLOW = "allow"
    DENY = "deny"
    NEEDS_APPROVAL = "needs_approval"


# Operations that never auto-execute below L4 even when the role allows them.
_APPROVAL_GATED: frozenset[OperationType] = frozenset(
    {OperationType.EXECUTE, OperationType.EXPORT, OperationType.DELETE},
)

_A = PermissionDecision.ALLOW
_D = PermissionDecision.DENY
_N = PermissionDecision.NEEDS_APPROVAL

_ROLE_MATRIX: dict[str, dict[OperationType, PermissionDecision]] = {
    "analyst": {
        OperationType.READ: _A,
        OperationType.ANALYZE: _A,
        OperationType.DRAFT: _D,
        OperationType.RECOMMEND: _D,
        OperationType.EXECUTE: _D,
        OperationType.EXPORT: _D,
        OperationType.DELETE: _D,
        OperationType.APPROVE: _D,
    },
    "recommender": {
        OperationType.READ: _A,
        OperationType.ANALYZE: _A,
        OperationType.DRAFT: _A,
        OperationType.RECOMMEND: _A,
        OperationType.EXECUTE: _N,
        OperationType.EXPORT: _N,
        OperationType.DELETE: _D,
        OperationType.APPROVE: _D,
    },
    "executor": {
        OperationType.READ: _A,
        OperationType.ANALYZE: _A,
        OperationType.DRAFT: _A,
        OperationType.RECOMMEND: _A,
        OperationType.EXECUTE: _A,
        OperationType.EXPORT: _N,
        OperationType.DELETE: _N,
        OperationType.APPROVE: _D,
    },
    "supervisor": {
        OperationType.READ: _A,
        OperationType.ANALYZE: _A,
        OperationType.DRAFT: _A,
        OperationType.RECOMMEND: _A,
        OperationType.EXECUTE: _A,
        OperationType.EXPORT: _A,
        OperationType.DELETE: _N,
        OperationType.APPROVE: _A,
    },
    "admin": dict.fromkeys(OperationType, _A),
}

BUILT_IN_ROLES: frozenset[str] = frozenset(_ROLE_MATRIX)


@dataclass(frozen=True, slots=True)
class PermissionResult:
    role: str
    operation: str
    decision: str
    reason: str

    @property
    def allowed(self) -> bool:
        return self.decision == PermissionDecision.ALLOW.value


def evaluate_permission(
    role: str,
    operation: OperationType | str,
    *,
    autonomy_level: int | AutonomyLevel = DEFAULT_AUTONOMY,
    tool: str | None = None,
    allowed_tools: list[str] | None = None,
) -> PermissionResult:
    """Decide whether ``role`` may perform ``operation``.

    Unknown roles are denied. A forbidden / unpermitted tool forces a DENY.
    Approval-gated operations are downgraded to NEEDS_APPROVAL below L4.
    """
    op = operation if isinstance(operation, OperationType) else OperationType(operation)
    role_norm = role.strip().lower()

    if role_norm not in _ROLE_MATRIX:
        return PermissionResult(role_norm, op.value, _D.value, f"unknown role: {role_norm!r}")

    if tool is not None:
        ok, tool_reason = is_tool_allowed(tool, allowed_tools)
        if not ok:
            return PermissionResult(role_norm, op.value, _D.value, tool_reason)

    base = _ROLE_MATRIX[role_norm].get(op, _D)
    if base is _D:
        return PermissionResult(role_norm, op.value, _D.value, f"role {role_norm!r} may not {op.value}")

    level = coerce_autonomy(autonomy_level)
    if base is _A and op in _APPROVAL_GATED and level < AutonomyLevel.L4_AUTO_WITH_AUDIT:
        return PermissionResult(
            role_norm,
            op.value,
            _N.value,
            f"{op.value} needs approval below autonomy L4",
        )
    return PermissionResult(role_norm, op.value, base.value, "ok")


def card_permission(
    card: AgentCard,
    operation: OperationType | str,
    *,
    tool: str | None = None,
) -> PermissionResult:
    """Evaluate a permission using an agent card's own role + tool boundary."""
    return evaluate_permission(
        card.role,
        operation,
        autonomy_level=card.autonomy_level,
        tool=tool,
        allowed_tools=list(card.allowed_tools),
    )


__all__ = [
    "BUILT_IN_ROLES",
    "OperationType",
    "PermissionDecision",
    "PermissionResult",
    "card_permission",
    "evaluate_permission",
]
