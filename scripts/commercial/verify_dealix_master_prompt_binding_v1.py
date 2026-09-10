#!/usr/bin/env python3
"""Fail-closed source verifier for Dealix server-first master binding V2."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BINDING = ROOT / "config" / "company" / "dealix_master_prompt_binding_v1.json"
CANONICAL_AGENTS = {"dealix-pm", "dealix-sales", "dealix-delivery", "dealix-engineer", "dealix-content"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_verifier(ref: str) -> None:
    path = ROOT / ref
    require(path.is_file(), f"verifier target missing: {ref}")
    result = subprocess.run([sys.executable, str(path)], cwd=ROOT, text=True, capture_output=True, check=False)
    require(result.returncode == 0, f"nested verifier failed: {ref}: {(result.stdout + result.stderr)[-1200:]}")


def main() -> int:
    try:
        require(BINDING.is_file(), "master prompt binding missing")
        binding = json.loads(BINDING.read_text(encoding="utf-8"))
        require(binding.get("schema_version") == 2, "server-first binding schema 2 required")
        require(binding.get("binding_generation") == "SERVER_FIRST_V2", "binding generation drift")
        require(binding.get("runtime_binding_mode") == "INSTALLED_ARTIFACTS_SHA256_FAIL_CLOSED", "runtime binding must fail closed")
        require(binding.get("required_runtime_artifact_hash_match") is True, "runtime hash match must be required")
        require(binding.get("north_star") == "CASH_READY_AUTONOMOUS_DEALIX_COMPANY", "north star drift")
        require(binding.get("mode") == "AGENT_FIRST_FOUNDER_EXCEPTION_ONLY", "agent-first mode required")
        require(set(binding.get("permanent_agents", [])) == CANONICAL_AGENTS, "permanent agent set drift")
        require(len(binding.get("permanent_agents", [])) == 5, "exactly five permanent agents required")
        require(binding.get("deep_wip_max") == 3, "deep WIP drift")
        require(binding.get("expected_arm_count") == 44, "44 governed arms required")
        require(binding.get("l0_l4_autonomous") is True, "L0-L4 autonomy must be enabled")
        require(binding.get("l5_exact_action_bound") is True, "L5 must remain exact-action-bound")
        for key in ("external_send_default", "public_publish_default", "payment_execution_default", "production_mutation_default", "scheduler_created"):
            require(binding.get(key) is False, f"unsafe default drift: {key}")
        require(binding.get("canonical_scheduler_reused") is True, "canonical scheduler must be reused")

        required_flags = {"DEALIX_EXTERNAL_SEND", "EMAIL_LIVE_SEND", "WHATSAPP_ALLOW_LIVE_SEND", "WHATSAPP_OUTBOUND", "PUBLIC_PUBLISH", "PAID_SPEND", "PAYMENT_EXECUTION", "PRODUCTION_MUTATION", "DNS_MUTATION", "DB_MUTATION", "SECRET_MUTATION"}
        require(set(binding.get("required_kill_switches", [])) == required_flags, "material kill-switch contract drift")

        for key in ("binding_env", "binding_sha_env", "prompt_env", "prompt_sha_env", "meta_control_env", "meta_control_sha_env"):
            require(str(binding.get(key, "")).strip(), f"runtime env binding missing: {key}")
        for key in ("runtime_binding_path", "runtime_prompt_path", "runtime_meta_control_path", "runtime_launcher_path"):
            require(str(binding.get(key, "")).startswith("/opt/dealix/control/"), f"runtime path drift: {key}")

        for key in ("prompt_ref", "meta_control_ref", "meta_control_verifier_ref", "meta_control_runtime_ref", "arm_registry_ref", "arm_playbooks_ref", "arm_registry_verifier_ref", "arm_playbooks_verifier_ref"):
            ref = str(binding.get(key, ""))
            require(ref, f"{key} missing")
            require((ROOT / ref).is_file(), f"{key} target missing: {ref}")

        prompt = ROOT / binding["prompt_ref"]
        text = prompt.read_text(encoding="utf-8")
        require(len(text) >= 18000, "master prompt unexpectedly small")
        for marker in binding.get("required_prompt_markers", []):
            require(marker in text, f"master prompt marker missing: {marker}")
        for agent in CANONICAL_AGENTS:
            require(agent in text, f"master prompt missing canonical agent: {agent}")
        for marker in ("ALL_ARMS_ACTIVE != ALL_ARMS_DEEP", "44 governed arms", "cold WhatsApp", "mass LinkedIn", "quote == invoice", "invoice == payment", "merge == deployed", "START-OF-CYCLE LIVE TRUTH SYNC", "RAILWAY STAGED-CHANGE RECONCILIATION"):
            require(marker in text, f"V2 master marker missing: {marker}")

        meta = json.loads((ROOT / binding["meta_control_ref"]).read_text(encoding="utf-8"))
        require(meta.get("schema_version") == 2, "meta-control schema drift")
        require(meta.get("north_star") == binding["north_star"], "meta-control north star drift")
        require(set(meta.get("permanent_agents", [])) == CANONICAL_AGENTS, "meta-control agent drift")
        require(meta.get("deep_wip_max") == 3, "meta-control WIP drift")
        require(meta.get("l5", {}).get("universal_authority") is False, "universal L5 forbidden")
        require(meta.get("l5", {}).get("exact_action_bound") is True, "exact L5 required")

        registry = json.loads((ROOT / binding["arm_registry_ref"]).read_text(encoding="utf-8"))
        playbooks = json.loads((ROOT / binding["arm_playbooks_ref"]).read_text(encoding="utf-8"))
        require(len(registry.get("arms", [])) == 44, "arm registry count drift")
        require(len(playbooks.get("playbooks", [])) == 44, "arm playbook count drift")
        require(registry.get("deep_wip_max") == 3 and playbooks.get("deep_wip_max") == 3, "arm WIP contract drift")

        for key in ("meta_control_verifier_ref", "arm_registry_verifier_ref", "arm_playbooks_verifier_ref"):
            run_verifier(binding[key])

        print("DEALIX_MASTER_PROMPT_BINDING_V2=PASS")
        print("DEALIX_MASTER_PROMPT_BINDING_V1=PASS_COMPAT")
        print(f"MASTER_BINDING_SHA256={sha256(BINDING)}")
        print(f"MASTER_PROMPT_SHA256={sha256(prompt)}")
        print(f"META_CONTROL_SHA256={sha256(ROOT / binding['meta_control_ref'])}")
        print("PERMANENT_AGENTS=5")
        print("ARMS_TOTAL=44")
        print("DEEP_WIP_MAX=3")
        print("L5_EXACT_ACTION_BOUND=true")
        print("SCHEDULER_CREATED=false")
        return 0
    except Exception as exc:  # noqa: BLE001
        print(f"DEALIX_MASTER_PROMPT_BINDING_V2=FAIL reason={exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
