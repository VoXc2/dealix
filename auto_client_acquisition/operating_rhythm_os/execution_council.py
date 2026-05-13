"""Execution Council — 8 canonical roles."""

from __future__ import annotations

from enum import Enum


class ExecutionCouncilRole(str, Enum):
    CEO = "ceo_strategist"
    REVENUE_OWNER = "revenue_owner"
    DELIVERY_OWNER = "delivery_owner"
    PRODUCT_OWNER = "product_owner"
    GOVERNANCE_OWNER = "governance_owner"
    PROOF_OWNER = "proof_owner"
    CLIENT_SUCCESS_OWNER = "client_success_owner"
    FINANCE_OWNER = "finance_owner"


EXECUTION_COUNCIL_ROLES: tuple[ExecutionCouncilRole, ...] = tuple(ExecutionCouncilRole)
