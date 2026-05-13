"""Client-side roles inside an adopting client."""

from __future__ import annotations

from enum import Enum


class ClientRole(str, Enum):
    EXECUTIVE_SPONSOR = "executive_sponsor"
    WORKFLOW_OWNER = "workflow_owner"
    OPERATOR = "operator"
    GOVERNANCE_REVIEWER = "governance_reviewer"
    DEALIX_SUCCESS_OWNER = "dealix_success_owner"


CLIENT_ROLES: tuple[ClientRole, ...] = tuple(ClientRole)
