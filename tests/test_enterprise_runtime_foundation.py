from __future__ import annotations

from pathlib import Path

import yaml

from auto_client_acquisition.enterprise_infrastructure.runtime import run_governed_workflow

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_WORKFLOW = REPO_ROOT / "workflows" / "sales" / "lead_qualification.workflow.yaml"
DEFAULT_AGENT = REPO_ROOT / "agents" / "sales_agent" / "agent.yaml"


def test_lead_qualification_completes_with_required_approval() -> None:
    result = run_governed_workflow(
        workflow_path=DEFAULT_WORKFLOW,
        agent_path=DEFAULT_AGENT,
        tenant_id="tenant-alpha",
        actor_role="sales_manager",
        approvals={"send_whatsapp_outreach"},
    )

    assert result["run"]["status"] == "completed"
    assert result["run"]["metrics"]["approvals_requested"] == 1
    assert result["run"]["metrics"]["approvals_granted"] == 1
    assert result["executive_report"]["roi_percent"] > 0
    assert result["enterprise_checklist"]["multi_tenancy"] is True
    assert result["enterprise_checklist"]["rbac"] is True


def test_lead_qualification_pauses_when_approval_missing() -> None:
    result = run_governed_workflow(
        workflow_path=DEFAULT_WORKFLOW,
        agent_path=DEFAULT_AGENT,
        tenant_id="tenant-beta",
        actor_role="sales_rep",
    )

    assert result["run"]["status"] == "paused_for_approval"
    assert result["run"]["blocked_step_id"] == "send_whatsapp_outreach"
    assert result["run"]["metrics"]["approvals_requested"] == 1
    assert result["run"]["metrics"]["approvals_granted"] == 0


def test_lead_qualification_rolls_back_when_last_step_fails() -> None:
    result = run_governed_workflow(
        workflow_path=DEFAULT_WORKFLOW,
        agent_path=DEFAULT_AGENT,
        tenant_id="tenant-gamma",
        actor_role="sales_manager",
        approvals={"send_whatsapp_outreach"},
        forced_fail_steps={"update_crm_stage"},
    )

    assert result["run"]["status"] == "rolled_back"
    assert result["run"]["blocked_step_id"] == "update_crm_stage"
    assert result["run"]["metrics"]["rollback_events"] >= 1
    assert result["run"]["metrics"]["value_generated_sar"] == 0


def test_unauthorized_tool_is_blocked_by_governance(tmp_path: Path) -> None:
    workflow_path = tmp_path / "unauthorized.workflow.yaml"
    workflow_path.write_text(
        yaml.safe_dump(
            {
                "workflow_id": "wf::unauthorized",
                "name": "unauthorized_tool_test",
                "trigger": "lead.created",
                "steps": [
                    {
                        "id": "dangerous_step",
                        "name": "Dangerous action",
                        "action": "crm.delete_account",
                        "risk_level": "high",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    result = run_governed_workflow(
        workflow_path=workflow_path,
        agent_path=DEFAULT_AGENT,
        tenant_id="tenant-delta",
        actor_role="sales_manager",
    )

    assert result["run"]["status"] == "failed"
    assert result["run"]["blocked_step_id"] == "dangerous_step"
    assert result["run"]["traces"][0]["decision"] == "block"
