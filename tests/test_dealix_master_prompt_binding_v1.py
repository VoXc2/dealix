from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BINDING = ROOT / "config" / "company" / "dealix_master_prompt_binding_v1.json"
PROMPT = ROOT / "prompts" / "company" / "DEALIX_OMEGA_FOUNDER_COMMAND_ROOM_MASTER_PROMPT.md"
VERIFY = ROOT / "scripts" / "commercial" / "verify_dealix_master_prompt_binding_v1.py"
RUNNER = ROOT / "scripts" / "commercial" / "run_dealix_master_company_cycle_v1.py"
INSTALLER = ROOT / "scripts" / "ops" / "install_dealix_omega_master_company_v1.sh"


def test_binding_points_to_one_canonical_prompt_and_scheduler() -> None:
    data = json.loads(BINDING.read_text(encoding="utf-8"))
    assert data["prompt_ref"] == "prompts/company/DEALIX_OMEGA_FOUNDER_COMMAND_ROOM_MASTER_PROMPT.md"
    assert data["mode"] == "AGENT_FIRST_FOUNDER_EXCEPTION_ONLY"
    assert data["deep_wip_max"] == 3
    assert len(data["permanent_agents"]) == 5
    assert data["scheduler_created"] is False
    assert data["canonical_scheduler_reused"] is True
    assert data["l0_l4_autonomous"] is True
    assert data["l5_exact_action_bound"] is True


def test_master_prompt_contains_company_law_and_truth_firewall() -> None:
    text = PROMPT.read_text(encoding="utf-8")
    for marker in (
        "CASH_READY_AUTONOMOUS_DEALIX_COMPANY",
        "ONE-COMPANY LAW",
        "PERMANENT AGENT ROSTER — EXACTLY FIVE",
        "PRODUCTION TRUST LAW",
        "FOUNDER DELEGATION SESSIONS",
        "OMNICHANNEL OPERATING MODEL",
        "CONTINUOUS COMPANY LOOP",
        "research == relationship",
        "public contact == consent",
        "draft == sent",
        "quote == invoice",
        "invoice == payment",
        "merge == deployed",
    ):
        assert marker in text


def test_runtime_entrypoint_forces_material_effects_off() -> None:
    runner = RUNNER.read_text(encoding="utf-8")
    installer = INSTALLER.read_text(encoding="utf-8")
    verifier = VERIFY.read_text(encoding="utf-8")
    assert 'env["DEALIX_EXTERNAL_SEND"] = "0"' in runner
    assert 'env["PRODUCTION_MUTATION"] = "0"' in runner
    assert "export DEALIX_EXTERNAL_SEND=0" in installer
    assert "export PRODUCTION_MUTATION=0" in installer
    assert "SCHEDULER_CREATED=false" in installer
    assert "systemctl enable" not in installer
    assert "systemctl start" not in installer
    assert "DEALIX_MASTER_PROMPT_BINDING_V1=PASS" in verifier
