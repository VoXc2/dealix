"""Agent Risk Board — per-agent row with risk band."""

from __future__ import annotations

from dataclasses import dataclass

from auto_client_acquisition.endgame_os.agent_control import AutonomyLevel


@dataclass(frozen=True)
class AgentRiskBoardRow:
    agent_id: str
    owner: str
    purpose: str
    autonomy_level: AutonomyLevel
    allowed_inputs: tuple[str, ...]
    allowed_tools: tuple[str, ...]
    forbidden_actions: tuple[str, ...]
    last_audit: str | None
    risk_level: str          # low | medium | high | critical
    incident_count: int
    decommission_status: str  # active | paused | retired


def agent_risk_band(row: AgentRiskBoardRow) -> str:
    """Compose a band string from autonomy + risk + incidents."""

    if row.decommission_status == "retired":
        return "retired"
    if row.autonomy_level >= AutonomyLevel.EXTERNAL_RESTRICTED:
        return "enterprise_only"
    if row.incident_count > 0 and row.risk_level in {"high", "critical"}:
        return "containment_required"
    if row.autonomy_level >= AutonomyLevel.EXECUTE_INTERNAL_AFTER_APPROVAL:
        return "contract_required"
    return "mvp_allowed"
