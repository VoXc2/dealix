#!/usr/bin/env python3
"""Server-first, hash-bound master entrypoint for the Dealix Company OS."""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
BINDING = ROOT / "config" / "company" / "dealix_master_prompt_binding_v1.json"
VERIFY = ROOT / "scripts" / "commercial" / "verify_dealix_master_prompt_binding_v1.py"
COMMAND_ROOM = ROOT / "scripts" / "commercial" / "run_dealix_command_room_v1.py"
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
    value = result.stdout.strip()
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
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    (OUT / f"{stamp}.json").write_text(rendered, encoding="utf-8")


def main() -> int:
    if not BINDING.is_file() or not VERIFY.is_file() or not COMMAND_ROOM.is_file():
        return fail("REQUIRED_FILE_MISSING")

    verify = subprocess.run([sys.executable, str(VERIFY)], cwd=ROOT, check=False)
    if verify.returncode != 0:
        return fail("MASTER_BINDING_INVALID", int(verify.returncode or 1))

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
    except Exception as exc:  # noqa: BLE001 - fail-closed binding boundary
        print(f"MASTER_BINDING_ERROR={type(exc).__name__}:{exc}", file=sys.stderr)
        return fail("RUNTIME_ARTIFACT_HASH_MISMATCH")

    env = dict(os.environ)
    env[str(binding["binding_env"])] = str(runtime_binding)
    env[str(binding["binding_sha_env"])] = binding_hash
    env[str(binding["prompt_env"])] = str(runtime_prompt)
    env[str(binding["prompt_sha_env"])] = prompt_hash
    env[str(binding["meta_control_env"])] = str(runtime_meta)
    env[str(binding["meta_control_sha_env"])] = meta_hash
    env["DEALIX_MASTER_PROMPT_BOUND"] = "1"
    env["DEALIX_META_CONTROL_BOUND"] = "1"
    env["DEALIX_UNIVERSAL_L5"] = "0"
    env["DEALIX_EXTERNAL_SEND"] = "0"
    env["PUBLIC_PUBLISH"] = "0"
    env["PAYMENT_EXECUTION"] = "0"
    env["PRODUCTION_MUTATION"] = "0"
    for key in binding["required_kill_switches"]:
        env[str(key)] = "0"

    started = now_iso()
    result = subprocess.run([sys.executable, str(COMMAND_ROOM), *sys.argv[1:]], cwd=ROOT, env=env, check=False)
    receipt = {
        "schema_version": "dealix.master-company-cycle.v2",
        "started_at": started,
        "finished_at": now_iso(),
        "repository_head": git_head(),
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
        "governed_arm_count": binding["expected_arm_count"],
        "deep_wip_max": binding["deep_wip_max"],
        "command_room_rc": result.returncode,
        "status": "PASS" if result.returncode == 0 else "DEGRADED",
        "universal_l5": False,
        "material_external_effects_executed": False,
        "kill_switches_forced_off": binding["required_kill_switches"],
    }
    write_receipt(receipt)
    print(f"MASTER_COMPANY_CYCLE_RC={result.returncode}")
    print(f"MASTER_BINDING_SHA256={binding_hash}")
    print(f"MASTER_PROMPT_SHA256={prompt_hash}")
    print(f"META_CONTROL_SHA256={meta_hash}")
    print("MASTER_PROMPT_BOUND=true")
    print("META_CONTROL_BOUND=true")
    print("PERMANENT_AGENTS=5")
    print("ARMS_TOTAL=44")
    print("UNIVERSAL_L5=false")
    print("MATERIAL_EXTERNAL_EFFECTS=DISABLED_BY_ENTRYPOINT")
    print(f"MASTER_RECEIPT={OUT / 'latest.json'}")
    return int(result.returncode)


if __name__ == "__main__":
    raise SystemExit(main())
