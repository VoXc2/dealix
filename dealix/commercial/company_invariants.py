"""Company Invariant Registry — canonical invariants INV-001..007."""

from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

class InvariantSeverity(StrEnum):
    CRITICAL = "critical"
    HIGH = "high"

class CompanyInvariant(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    invariant_id: str
    description: str
    severity: InvariantSeverity
    enforcement: str
    test: str
    owner: str = "dealix-pm"

INVARIANTS: list[CompanyInvariant] = [
    CompanyInvariant(invariant_id="INV-001", description="dynamic hierarchical agent registry (3856 logical via Agentic Holding) with 5 legacy executor aliases", severity=InvariantSeverity.CRITICAL, enforcement="AgentHierarchyRegistry + audit_agent_team.py --strict + legacy_executor_owner compatibility", test="tests/test_agent_team_audit.py"),
    CompanyInvariant(invariant_id="INV-002", description="resource-governed concurrency (ResourceGovernor host-aware) with economic deep WIP <= 3 focus limit", severity=InvariantSeverity.CRITICAL, enforcement="ResourceGovernor.budget + EconomicCellRegistry.claim_deep_wip_slot + DeepWipEnforcer + tests", test="tests/test_deep_wip_enforcer.py"),
    CompanyInvariant(invariant_id="INV-003", description="no verified payment without PAYMENT_VERIFIED evidence", severity=InvariantSeverity.CRITICAL, enforcement="FinancialOS.add_record state check", test="tests/test_financial_truth.py"),
    CompanyInvariant(invariant_id="INV-004", description="no cold WhatsApp mass automation", severity=InvariantSeverity.CRITICAL, enforcement="channel_registry BLOCKED + consent_registry", test="tests/test_no_cold_whatsapp.py"),
    CompanyInvariant(invariant_id="INV-005", description="no external publish at L0-L4", severity=InvariantSeverity.HIGH, enforcement="opencode permission deny + approval_center", test="tests/test_no_external_without_approval.py"),
    CompanyInvariant(invariant_id="INV-006", description="no public local LLM", severity=InvariantSeverity.HIGH, enforcement="ollama 127.0.0.1:11434 loopback + firewall", test="tests/test_no_public_llm.py"),
    CompanyInvariant(invariant_id="INV-007", description="production green requires exact release parity", severity=InvariantSeverity.CRITICAL, enforcement="dealix-server-sentinel API_RELEASE_PARITY", test="tests/test_production_trust.py"),
]

def get_invariants() -> list[CompanyInvariant]:
    return INVARIANTS

__all__ = ["CompanyInvariant", "InvariantSeverity", "INVARIANTS", "get_invariants"]
