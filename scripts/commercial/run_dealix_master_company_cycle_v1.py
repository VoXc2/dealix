#!/usr/bin/env python3
"""Server-first, hash-bound master entrypoint for the Dealix Company OS."""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
BINDING = ROOT / "config" / "company" / "dealix_master_prompt_binding_v1.json"
VERIFY = ROOT / "scripts" / "commercial" / "verify_dealix_master_prompt_binding_v1.py"
COMMAND_ROOM = ROOT / "scripts" / "commercial" / "run_dealix_command_room_v1.py"
COMMAND_ROOM_OUT = ROOT / "reports" / "company_os" / "command_room"
OUT = ROOT / "reports" / "company_os" / "master_company_cycle"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def now_iso() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def fail(reason: str, rc: int = 2) -> int:
    print(f"MASTER_COMPANY_CYCLE=BLOCKED_{reason}", file=sys.stderr)
    return rc


def git_head() -> str:
    result = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True, check=False)
    value = result.stdout.strip().lower()
    return value if result.returncode == 0 and len(value) == 40 else "unknown"


def resolve_artifact(*, canonical: Path, path_env: str, sha_env: str) -> tuple[Path, str, str]:
    canonical_hash = sha256(canonical)
    runtime_value = os.getenv(path_env, "").strip()
    declared_hash = os.getenv(sha_env, "").strip().lower()
    if bool(runtime_value) != bool(declared_hash):
        raise RuntimeError(f"partial runtime binding for {path_env}/{sha_env}")
    if not runtime_value:
        return canonical, canonical_hash, "REPO_SHADOW"
    runtime = Path(runtime_value)
    if not runtime.is_file():
        raise RuntimeError(f"runtime artifact missing: {runtime}")
    runtime_hash = sha256(runtime)
    if declared_hash != runtime_hash:
        raise RuntimeError(f"declared SHA mismatch: {path_env}")
    if runtime_hash != canonical_hash:
        raise RuntimeError(f"installed artifact drift: {path_env}")
    return runtime, runtime_hash, "INSTALLED_HASH_BOUND"


def write_receipt(payload: dict[str, Any]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rendered = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    (OUT / "latest.json").write_text(rendered, encoding="utf-8")
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S%fZ")
    (OUT / f"{stamp}-{payload['invocation_id'][:12]}.json").write_text(rendered, encoding="utf-8")


def _command_room_run_id(stdout: str) -> str:
    for line in stdout.splitlines():
        if line.startswith("COMMAND_ROOM_RUN="):
            value = line.split("=", 1)[1].strip()
            if value:
                return value
    return ""


def _load_exact_command_room_receipt(run_id: str) -> dict[str, Any]:
    if not run_id:
        raise RuntimeError("command-room run id missing")
    path = COMMAND_ROOM_OUT / f"{run_id}.json"
    if not path.is_file():
        raise RuntimeError("exact command-room receipt missing")
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("run_id") != run_id:
        raise RuntimeError("command-room receipt run id mismatch")
    return data


def main() -> int:
    if not BINDING.is_file() or not VERIFY.is_file() or not COMMAND_ROOM.is_file():
        return fail("REQUIRED_FILE_MISSING")

    verify = subprocess.run([sys.executable, str(VERIFY)], cwd=ROOT, check=False)
    if verify.returncode != 0:
        return fail("MASTER_BINDING_INVALID", int(verify.returncode or 1))

    launch_head = git_head()
    if launch_head == "unknown":
        return fail("REPOSITORY_HEAD_UNRESOLVED")

    binding = json.loads(BINDING.read_text(encoding="utf-8"))
    try:
        runtime_binding, binding_hash, binding_mode = resolve_artifact(
            canonical=BINDING,
            path_env=str(binding["binding_env"]),
            sha_env=str(binding["binding_sha_env"]),
        )
        canonical_prompt = ROOT / str(binding["prompt_ref"])
        runtime_prompt, prompt_hash, prompt_mode = resolve_artifact(
            canonical=canonical_prompt,
            path_env=str(binding["prompt_env"]),
            sha_env=str(binding["prompt_sha_env"]),
        )
        canonical_meta = ROOT / str(binding["meta_control_ref"])
        runtime_meta, meta_hash, meta_mode = resolve_artifact(
            canonical=canonical_meta,
            path_env=str(binding["meta_control_env"]),
            sha_env=str(binding["meta_control_sha_env"]),
        )
    except Exception as exc:  # noqa: BLE001
        print(f"MASTER_BINDING_ERROR={type(exc).__name__}:{exc}", file=sys.stderr)
        return fail("RUNTIME_ARTIFACT_HASH_MISMATCH")

    invocation_id = uuid.uuid4().hex
    env = dict(os.environ)
    env[str(binding["binding_env"])] = str(runtime_binding)
    env[str(binding["binding_sha_env"])] = binding_hash
    env[str(binding["prompt_env"])] = str(runtime_prompt)
    env[str(binding["prompt_sha_env"])] = prompt_hash
    env[str(binding["meta_control_env"])] = str(runtime_meta)
    env[str(binding["meta_control_sha_env"])] = meta_hash
    env["DEALIX_MASTER_PROMPT_BOUND"] = "1"
    env["DEALIX_META_CONTROL_BOUND"] = "1"
    env["DEALIX_COMMAND_ROOM_INVOCATION_ID"] = invocation_id
    env["DEALIX_EXPECTED_REPOSITORY_HEAD"] = launch_head
    env["DEALIX_UNIVERSAL_L5"] = "0"
    env["DEALIX_EXTERNAL_SEND"] = "0"
    env["PUBLIC_PUBLISH"] = "0"
    env["PAYMENT_EXECUTION"] = "0"
    env["PRODUCTION_MUTATION"] = "0"
    for key in binding["required_kill_switches"]:
        env[str(key)] = "0"

    started = now_iso()
    result = subprocess.run(
        [sys.executable, str(COMMAND_ROOM), *sys.argv[1:]],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.stdout:
        print(result.stdout, end="" if result.stdout.endswith("\n") else "\n")
    if result.stderr:
        print(result.stderr, file=sys.stderr, end="" if result.stderr.endswith("\n") else "\n")

    command_room_run_id = _command_room_run_id(result.stdout)
    prompt_binding_verified = False
    receipt_error = ""
    try:
        command_room_receipt = _load_exact_command_room_receipt(command_room_run_id)
        master_state = command_room_receipt.get("master_prompt") or {}
        prompt_binding_verified = bool(
            command_room_receipt.get("invocation_id") == invocation_id
            and command_room_receipt.get("repository_head") == launch_head
            and master_state.get("active_sha256") == prompt_hash
            and master_state.get("all_executed_lanes_bound") is True
        )
        if not prompt_binding_verified:
            raise RuntimeError("command-room receipt binding mismatch")
    except Exception as exc:  # noqa: BLE001
        receipt_error = type(exc).__name__

    finish_head = git_head()
    head_stable = finish_head == launch_head
    effective_rc = int(result.returncode)
    if effective_rc == 0 and (not prompt_binding_verified or not head_stable):
        effective_rc = 78

    receipt = {
        "schema_version": "dealix.master-company-cycle.v3",
        "invocation_id": invocation_id,
        "started_at": started,
        "finished_at": now_iso(),
        "repository_head_start": launch_head,
        "repository_head_finish": finish_head,
        "repository_head_stable": head_stable,
        "north_star": binding["north_star"],
        "binding_generation": binding["binding_generation"],
        "runtime_binding_mode": binding["runtime_binding_mode"],
        "artifacts": {
            "binding": {"path": str(runtime_binding), "sha256": binding_hash, "mode": binding_mode},
            "master_prompt": {"path": str(runtime_prompt), "sha256": prompt_hash, "mode": prompt_mode},
            "meta_control": {"path": str(runtime_meta), "sha256": meta_hash, "mode": meta_mode},
        },
        "permanent_agents": binding["permanent_agents"],
        "permanent_agent_count": len(binding["permanent_agents"]),
        "permanent_agents_note": "Logical business roles / compatibility aliases only. Agentic Holding registry + ResourceGovernor remain runtime fleet-size authority.",
        "governed_arm_count": binding["expected_arm_count"],
        "deep_wip_max": binding["deep_wip_max"],
        "command_room_run_id": command_room_run_id,
        "command_room_rc": result.returncode,
        "command_room_receipt_error": receipt_error,
        "master_prompt_bound_to_all_executed_agent_lanes": prompt_binding_verified,
        "effective_rc": effective_rc,
        "status": "PASS" if effective_rc == 0 else "DEGRADED",
        "universal_l5": False,
        "material_external_effects_executed": False,
        "kill_switches_forced_off": binding["required_kill_switches"],
    }
    write_receipt(receipt)
    print(f"MASTER_COMPANY_CYCLE_RC={effective_rc}")
    print(f"MASTER_INVOCATION_ID={invocation_id}")
    print(f"MASTER_BINDING_SHA256={binding_hash}")
    print(f"MASTER_PROMPT_SHA256={prompt_hash}")
    print(f"META_CONTROL_SHA256={meta_hash}")
    print(f"MASTER_PROMPT_BOUND={str(prompt_binding_verified).lower()}")
    print(f"REPOSITORY_HEAD_STABLE={str(head_stable).lower()}")
    print("META_CONTROL_BOUND=true")
    print("PERMANENT_AGENTS=5 (logical business roles / compatibility aliases)")
    print("ARMS_TOTAL=44")
    print("UNIVERSAL_L5=false")
    print("MATERIAL_EXTERNAL_EFFECTS=DISABLED_BY_ENTRYPOINT")
    print(f"MASTER_RECEIPT={OUT / 'latest.json'}")
    return effective_rc


if __name__ == "__main__":
    raise SystemExit(main())