"""AI Inventory row completeness — governance visibility contract."""

from __future__ import annotations

from dataclasses import dataclass

REQUIRED_INVENTORY_FIELDS: tuple[str, ...] = (
    "use_case_id",
    "department",
    "owner",
    "data_sources",
    "agent_or_model",
    "risk_level",
    "approval_path",
    "audit_status",
    "proof_metric",
    "status",
)


@dataclass(frozen=True, slots=True)
class AIInventoryRow:
    use_case_id: str
    department: str
    owner: str
    data_source_ids: tuple[str, ...]
    agent_or_model: str
    risk_level: str
    approval_path: str
    audit_status: str
    proof_metric: str
    status: str


def ai_inventory_row_complete(row: AIInventoryRow) -> tuple[bool, tuple[str, ...]]:
    missing: list[str] = []
    if not row.use_case_id.strip():
        missing.append("use_case_id")
    if not row.department.strip():
        missing.append("department")
    if not row.owner.strip():
        missing.append("owner")
    if not row.data_source_ids:
        missing.append("data_sources")
    if not row.agent_or_model.strip():
        missing.append("agent_or_model")
    if not row.risk_level.strip():
        missing.append("risk_level")
    if not row.approval_path.strip():
        missing.append("approval_path")
    if not row.audit_status.strip():
        missing.append("audit_status")
    if not row.proof_metric.strip():
        missing.append("proof_metric")
    if not row.status.strip():
        missing.append("status")
    return not missing, tuple(missing)
