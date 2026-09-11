#!/usr/bin/env python3
"""Runtime preflight and truthful control receipt for Dealix Meta-OS V2.

This runner proves source/config invariants and binds a concrete local runtime
instance to the current repository SHA. It deliberately distinguishes enforced
controls from architecture that is only declared or future-triggered.
"""
from __future__ import annotations

import hashlib
import json
import os
import socket
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "config" / "company" / "dealix_meta_operating_system_v2.json"
VERIFY = ROOT / "scripts" / "commercial" / "verify_dealix_meta_operating_system_v2.py"
OUT = ROOT / "reports" / "company_os" / "meta_control"

CANONICAL_AGENTS = [
    "dealix-pm",
    "dealix-sales",
    "dealix-delivery",
    "dealix-engineer",
    "dealix-content",
]
FORBIDDEN_LIVE_FLAGS = {
    "DEALIX_EXTERNAL_SEND": {"1", "true", "yes"},
    "EMAIL_LIVE_SEND": {"1", "true", "yes"},
    "WHATSAPP_ALLOW_LIVE_SEND": {"1", "true", "yes"},
    "PUBLIC_PUBLISH": {"1", "true", "yes"},
    "PAYMENT_EXECUTION": {"1", "true", "yes"},
    "PRODUCTION_MUTATION": {"1", "true", "yes"},
}


def now_iso() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_head() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True,
        capture_output=True, check=False, timeout=15,
    )
    if result.returncode != 0:
        return "unknown"
    value = result.stdout.strip()
    return value if len(value) == 40 else "unknown"


def live_flag_violations() -> list[str]:
    violations: list[str] = []
    for key, forbidden in FORBIDDEN_LIVE_FLAGS.items():
        if os.getenv(key, "").strip().lower() in forbidden:
            violations.append(key)
    return sorted(violations)


def run_verify() -> int:
    result = subprocess.run([sys.executable, str(VERIFY)], cwd=ROOT, check=False)
    return int(result.returncode)


def build_receipt(config: dict[str, Any]) -> dict[str, Any]:
    code_sha = git_head()
    config_sha = sha256(CONFIG)
    instance_material = f"{socket.gethostname()}:{os.getpid()}:{code_sha}:{config_sha}"
    runtime_instance_id = "runtime:" + hashlib.sha256(instance_material.encode("utf-8")).hexdigest()[:24]
    agent_contracts = [
        {
            "agent_id": agent,
            "meta_control_bound": True,
            "max_default_autonomy": "L4",
            "l5_universal_authority": False,
            "material_external_effects_default": False,
            "budget_policy": "BOUND_BY_META_CONTROL_CONTRACT",
        }
        for agent in CANONICAL_AGENTS
    ]
    return {
        "schema_version": "dealix.meta-control-receipt.v2",
        "generated_at": now_iso(),
        "north_star": config["north_star"],
        "objective": config["objective"],
        "repository_head": code_sha,
        "meta_control_sha256": config_sha,
        "runtime_instance_id": runtime_instance_id,
        "workload_identity": {
            "status": "LOCAL_RUNTIME_DERIVED_NOT_CRYPTOGRAPHICALLY_ATTESTED",
            "cryptographic_workload_identity_active": False,
            "spiffe_spire_status": config["identity"]["spiffe_spire"]["status"],
            "spiffe_spire_auto_install": False,
        },
        "enforcement": {
            "kernel_schema_and_invariants": "ENFORCED_BY_PREFLIGHT",
            "five_agent_roster": "ENFORCED_BY_PREFLIGHT_AND_COMMAND_ROOM",
            "deep_wip_max": "ENFORCED_BY_EXISTING_CONSTITUTION_AND_ARM_VERIFIERS",
            "live_effect_default_off": "ENFORCED_BY_ENTRYPOINT_ENV_AND_COMMAND_ROOM",
            "l5_exact_action_bound": "ENFORCED_BY_EXISTING_EXTERNAL_ACTION_AUTHORITY_LAYER",
            "per_tool_runtime_policy_hooks": "PARTIAL_EXISTING_ADAPTERS_NOT_UNIVERSALLY_PROVEN",
            "per_tool_budget_enforcement": "DECLARED_CONTRACT_NOT_UNIVERSALLY_PROVEN",
            "mcp_gateway_universal_routing": "TARGET_ARCHITECTURE_NOT_CLAIMED_ACTIVE",
            "cryptographic_workload_identity": "TRIGGERED_FUTURE_OPTION_NOT_ACTIVE",
        },
        "planes": config["planes"],
        "invariants": {"verified_count": len(config["invariants"]), "status": "PASS"},
        "control_tests": {"declared_count": len(config["control_tests"]), "runtime_all_proven": False},
        "agent_contracts": agent_contracts,
        "l5": {
            "universal_authority": False,
            "exact_action_bound": True,
            "material_effects_default": False,
            "executed_by_meta_control": False,
        },
        "external_effects": "NONE_BY_META_CONTROL",
    }


def write_receipt(receipt: dict[str, Any]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rendered = json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    (OUT / "latest.json").write_text(rendered, encoding="utf-8")
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    (OUT / f"{stamp}.json").write_text(rendered, encoding="utf-8")
    lines = [
        "# Dealix Meta-Operating System V2 — Runtime Control Receipt",
        "",
        f"- Generated: `{receipt['generated_at']}`",
        f"- Repository head: `{receipt['repository_head']}`",
        f"- Meta-control SHA256: `{receipt['meta_control_sha256']}`",
        f"- Runtime instance: `{receipt['runtime_instance_id']}`",
        "- Kernel preflight: **PASS**",
        "- Permanent agents: **5**",
        "- Universal L5: **false**",
        "- External effects by this control: **NONE**",
        "",
        "## Enforcement truth",
    ]
    for key, value in receipt["enforcement"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend([
        "",
        "## Workload identity truth",
        f"- Status: `{receipt['workload_identity']['status']}`",
        "- Cryptographic workload identity is **not** claimed active.",
        "- SPIFFE/SPIRE remains a scale-triggered option and was not installed.",
        "",
    ])
    (OUT / "latest.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    if not CONFIG.is_file() or not VERIFY.is_file():
        print("META_CONTROL_V2=BLOCKED_REQUIRED_FILE_MISSING", file=sys.stderr)
        return 2
    violations = live_flag_violations()
    if violations:
        print(f"META_CONTROL_V2=BLOCKED_LIVE_FLAGS flags={','.join(violations)}", file=sys.stderr)
        return 2
    verify_rc = run_verify()
    if verify_rc != 0:
        print("META_CONTROL_V2=BLOCKED_KERNEL_INVALID", file=sys.stderr)
        return verify_rc or 1
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    receipt = build_receipt(config)
    write_receipt(receipt)
    print("META_CONTROL_V2=PASS")
    print(f"META_CONTROL_SHA256={receipt['meta_control_sha256']}")
    print(f"META_RUNTIME_INSTANCE={receipt['runtime_instance_id']}")
    print("PERMANENT_AGENTS=5")
    print("UNIVERSAL_L5=false")
    print("EXTERNAL_EFFECTS=NONE_BY_META_CONTROL")
    print(f"META_CONTROL_RECEIPT={OUT / 'latest.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
