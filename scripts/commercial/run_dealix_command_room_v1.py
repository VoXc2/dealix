#!/usr/bin/env python3
"""Canonical Dealix Founder Command Room cycle.

This is the VPS-facing executive entrypoint. It does not replace the Company OS;
it verifies the V2 meta-control kernel and command-room contract, then delegates
work only through the five canonical agent identities and existing Company OS
runners.

No provider side effect is executed here. External conversation effects remain
owned by the existing exact-action-bound external execution gate.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "config" / "company" / "dealix_command_room_v1.json"
VERIFY = ROOT / "scripts" / "commercial" / "verify_dealix_command_room_v1.py"
META_CONFIG = ROOT / "config" / "company" / "dealix_meta_operating_system_v2.json"
META_VERIFY = ROOT / "scripts" / "commercial" / "verify_dealix_meta_operating_system_v2.py"
META_CONTROL = ROOT / "scripts" / "commercial" / "run_dealix_meta_control_v2.py"
META_RECEIPT = ROOT / "reports" / "company_os" / "meta_control" / "latest.json"
OUT = ROOT / "reports" / "company_os" / "command_room"

# Daily work only. Weekly proof assembly is explicitly opt-in below.
RUNNERS: list[tuple[str, str, list[str], str]] = [
    (
        "company_os",
        "dealix-pm",
        ["scripts/commercial/run_company_os_daily.py", "--client", "dealix", "--mode", "draft-only", "--limit", "100"],
        "critical",
    ),
    (
        "autonomous_growth",
        "dealix-sales",
        ["scripts/commercial/run_autonomous_growth_daily.py", "--autonomy-level", "3", "--mode", "draft-only", "--limit", "100"],
        "critical",
    ),
    (
        "self_improvement",
        "dealix-engineer",
        ["scripts/commercial/run_self_improvement_daily.py", "--client", "dealix", "--mode", "draft-only"],
        "critical",
    ),
    (
        "content_factory",
        "dealix-content",
        ["scripts/dealix_content_factory_daily.py"],
        "critical",
    ),
]

WEEKLY_PROOF_RUNNER: tuple[str, str, list[str], str] = (
    "weekly_proof_pack",
    "dealix-delivery",
    ["scripts/commercial/run_weekly_proof_pack.py", "--client", "dealix", "--mode", "draft-only"],
    "critical",
)

FORBIDDEN_LIVE_FLAGS = {
    "DEALIX_EXTERNAL_SEND": {"1", "true", "yes"},
    "EMAIL_LIVE_SEND": {"1", "true", "yes"},
    "WHATSAPP_ALLOW_LIVE_SEND": {"1", "true", "yes"},
    "PUBLIC_PUBLISH": {"1", "true", "yes"},
    "PAYMENT_EXECUTION": {"1", "true", "yes"},
    "PRODUCTION_MUTATION": {"1", "true", "yes"},
}
_BOUND_TRUE = {"1", "true", "yes"}


def stamp() -> str:
    return datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")


def now_iso() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(label: str, argv: list[str], env: dict[str, str] | None = None) -> dict[str, Any]:
    started = now_iso()
    command = [sys.executable, *argv]
    result = subprocess.run(
        command,
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    return {
        "label": label,
        "command": argv,
        "started_at": started,
        "finished_at": now_iso(),
        "rc": result.returncode,
        "stdout_tail": result.stdout[-6000:],
        "stderr_tail": result.stderr[-6000:],
    }


def env_violations() -> list[str]:
    violations: list[str] = []
    for key, bad_values in FORBIDDEN_LIVE_FLAGS.items():
        if os.getenv(key, "").strip().lower() in bad_values:
            violations.append(key)
    return violations


def safe_agent_env(meta_sha: str, owner_agent: str) -> dict[str, str]:
    env = dict(os.environ)
    env["DEALIX_META_CONTROL_BOUND"] = "1"
    env["DEALIX_META_CONTROL_PATH"] = str(META_CONFIG)
    env["DEALIX_META_CONTROL_SHA256"] = meta_sha
    env["DEALIX_PERMANENT_AGENT_ID"] = owner_agent
    env["DEALIX_MAX_DEFAULT_AUTONOMY"] = "L4"
    env["DEALIX_UNIVERSAL_L5"] = "0"
    env["DEALIX_EXTERNAL_SEND"] = "0"
    env["EMAIL_LIVE_SEND"] = "0"
    env["WHATSAPP_ALLOW_LIVE_SEND"] = "0"
    env["PUBLIC_PUBLISH"] = "0"
    env["PAYMENT_EXECUTION"] = "0"
    env["PRODUCTION_MUTATION"] = "0"
    return env


def load_bound_master_prompt(env: dict[str, str]) -> dict[str, Any]:
    """Load and verify the master prompt before an agent lane starts.

    This deliberately reads the artifact rather than trusting inherited env
    markers. The model router independently re-verifies and consumes the same
    prompt at model-inference time.
    """
    if env.get("DEALIX_MASTER_PROMPT_BOUND", "").strip().lower() not in _BOUND_TRUE:
        return {"bound": False, "sha256": "", "bytes": 0}

    path_value = env.get("DEALIX_COMPANY_MASTER_PROMPT", "").strip()
    declared_sha = env.get("DEALIX_COMPANY_MASTER_PROMPT_SHA256", "").strip().lower()
    if not path_value or len(declared_sha) != 64:
        raise RuntimeError("master prompt path/SHA incomplete")
    path = Path(path_value)
    if not path.is_file():
        raise RuntimeError("master prompt artifact missing")
    raw = path.read_bytes()
    actual_sha = hashlib.sha256(raw).hexdigest()
    if actual_sha != declared_sha:
        raise RuntimeError("master prompt SHA mismatch")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise RuntimeError("master prompt is not UTF-8") from exc
    if not text.strip():
        raise RuntimeError("master prompt is empty")
    return {"bound": True, "sha256": actual_sha, "bytes": len(raw)}


def runner_specs(*, include_proof_pack: bool) -> list[tuple[str, str, list[str], str]]:
    specs = list(RUNNERS)
    if include_proof_pack:
        specs.append(WEEKLY_PROOF_RUNNER)
    return specs


def load_config() -> dict[str, Any]:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def load_meta_receipt() -> dict[str, Any]:
    if not META_RECEIPT.is_file():
        return {"status": "MISSING"}
    try:
        return json.loads(META_RECEIPT.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - receipt is non-authoritative if unreadable
        return {"status": "UNREADABLE", "reason": str(exc)}


def write_outputs(payload: dict[str, Any]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    run_stamp = payload["run_id"]
    json_path = OUT / f"{run_stamp}.json"
    md_path = OUT / f"{run_stamp}.md"
    latest_json = OUT / "latest.json"
    latest_md = OUT / "latest.md"

    rendered = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    json_path.write_text(rendered, encoding="utf-8")
    latest_json.write_text(rendered, encoding="utf-8")

    lines = [
        "# Dealix Founder Command Room",
        "",
        f"- Run: `{payload['run_id']}`",
        f"- Generated: `{payload['generated_at']}`",
        f"- Status: **{payload['status']}**",
        f"- North Star: `{payload['north_star']}`",
        f"- Permanent agents: `{len(payload['agents'])}`",
        f"- Channels: `{len(payload['channels'])}`",
        f"- V2 Meta-Control: **{payload['meta_control']['status']}**",
        f"- V2 SHA256: `{payload['meta_control']['sha256']}`",
        f"- Executed lanes bound to Master Prompt: **{payload['master_prompt']['all_executed_lanes_bound']}**",
        "",
        "## CEO Now",
    ]
    for item in payload["ceo_now"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Agent lanes"])
    for lane in payload["lanes"]:
        lines.append(
            f"- **{lane['owner_agent']} / {lane['label']}** — rc={lane['rc']} — {lane['status']} — V2 bound={lane['meta_control_bound']} — master bound={lane['master_prompt_bound']}"
        )
    lines.extend([
        "",
        "## External authority",
        "- Live external effects are not executed by this command-room runner.",
        "- Founder Delegation Sessions are disabled by default and only make exact actions eligible for canonical action-bound approval.",
        "- Existing provider execution gate remains authoritative.",
        "- Universal L5 authority remains false.",
        "",
        "## Command surfaces",
    ])
    for surface in payload["command_surfaces"]:
        lines.append(f"- {surface['type']}: {surface['name']} ({surface['scope']})")
    rendered_md = "\n".join(lines) + "\n"
    md_path.write_text(rendered_md, encoding="utf-8")
    latest_md.write_text(rendered_md, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default="draft-only", choices=["draft-only"])
    parser.add_argument("--include-proof-pack", action="store_true")
    args = parser.parse_args()

    required = (CONFIG, VERIFY, META_CONFIG, META_VERIFY, META_CONTROL)
    if any(not path.is_file() for path in required):
        print("COMMAND_ROOM=BLOCKED_REQUIRED_CONTROL_FILE_MISSING", file=sys.stderr)
        return 2

    live_flags = env_violations()
    if live_flags:
        print(f"COMMAND_ROOM=BLOCKED_LIVE_FLAGS flags={','.join(sorted(live_flags))}", file=sys.stderr)
        return 2

    meta_sha = file_sha256(META_CONFIG)
    meta_preflight = run(
        "meta_control_v2",
        [str(META_CONTROL.relative_to(ROOT))],
        env=safe_agent_env(meta_sha, "dealix-pm"),
    )
    if meta_preflight["rc"] != 0:
        print("COMMAND_ROOM=BLOCKED_META_CONTROL_V2", file=sys.stderr)
        print(meta_preflight["stderr_tail"], file=sys.stderr)
        return int(meta_preflight["rc"] or 1)

    verify = run(
        "command_room_verify",
        [str(VERIFY.relative_to(ROOT))],
        env=safe_agent_env(meta_sha, "dealix-pm"),
    )
    if verify["rc"] != 0:
        print("COMMAND_ROOM=BLOCKED_VERIFIER", file=sys.stderr)
        print(verify["stderr_tail"], file=sys.stderr)
        return int(verify["rc"] or 1)

    config = load_config()
    meta_receipt = load_meta_receipt()
    specs = runner_specs(include_proof_pack=args.include_proof_pack)

    lanes: list[dict[str, Any]] = []
    for label, owner, argv, criticality in specs:
        env = safe_agent_env(meta_sha, owner)
        try:
            prompt_binding = load_bound_master_prompt(env)
        except RuntimeError as exc:
            lanes.append({
                "label": label,
                "owner_agent": owner,
                "criticality": criticality,
                "rc": 78,
                "status": "BLOCKED_MASTER_PROMPT_BINDING_INVALID",
                "stdout_tail": "",
                "stderr_tail": type(exc).__name__,
                "meta_control_bound": True,
                "meta_control_sha256": meta_sha,
                "master_prompt_bound": False,
                "master_prompt_sha256": "",
                "universal_l5": False,
            })
            continue

        if not (ROOT / argv[0]).is_file():
            lanes.append({
                "label": label,
                "owner_agent": owner,
                "criticality": criticality,
                "rc": 127,
                "status": "BLOCKED_MISSING_RUNNER",
                "stdout_tail": "",
                "stderr_tail": argv[0],
                "meta_control_bound": True,
                "meta_control_sha256": meta_sha,
                "master_prompt_bound": prompt_binding["bound"],
                "master_prompt_sha256": prompt_binding["sha256"],
            })
            continue
        receipt = run(label, argv, env=env)
        receipt.update(
            owner_agent=owner,
            criticality=criticality,
            status="PASS" if receipt["rc"] == 0 else "DEGRADED",
            meta_control_bound=True,
            meta_control_sha256=meta_sha,
            master_prompt_bound=prompt_binding["bound"],
            master_prompt_sha256=prompt_binding["sha256"],
            master_prompt_bytes=prompt_binding["bytes"],
            universal_l5=False,
        )
        lanes.append(receipt)

    degraded = [lane for lane in lanes if lane["rc"] != 0]
    all_executed_lanes_bound = bool(lanes) and all(bool(lane.get("master_prompt_bound")) for lane in lanes)
    payload: dict[str, Any] = {
        "schema_version": "dealix.command-room-receipt.v2",
        "run_id": stamp(),
        "generated_at": now_iso(),
        "north_star": config["north_star"],
        "status": "DEGRADED" if degraded else "PASS",
        "meta_control": {
            "status": "PASS",
            "sha256": meta_sha,
            "preflight": meta_preflight,
            "runtime_receipt": meta_receipt,
        },
        "master_prompt": {
            "required_by_launcher": os.getenv("DEALIX_MASTER_PROMPT_BOUND", "").strip().lower() in _BOUND_TRUE,
            "all_executed_lanes_bound": all_executed_lanes_bound,
        },
        "agents": config["canonical_agents"],
        "channels": config["channels"],
        "command_surfaces": config["command_surfaces"],
        "queues": config["queues"],
        "views": config["views"],
        "lanes": lanes,
        "ceo_now": [
            "V2 Meta-Operating Control Kernel is a mandatory preflight for every executed canonical agent lane.",
            "The hash-bound Company Master Prompt is loaded before each executed lane and consumed by model-backed work through the canonical Model Router.",
            "Production Trust remains the first engineering gate until exact-release evidence is green.",
            "Revenue agent continuously ranks evidence-backed opportunities and prepares the next commercial movement.",
            "Delivery proof assembly runs only when explicitly requested by the weekly proof cadence.",
            "Founder attention is reserved for exceptions and exact material authority packets.",
        ],
        "external_execution": {
            "performed_by_command_room": False,
            "delegation_enabled_by_default": config["founder_delegation"]["enabled_by_default"],
            "provider_execution_gate": "dealix.commercial.external_execution_gate",
            "universal_l5": False,
        },
    }
    write_outputs(payload)

    print(f"COMMAND_ROOM={payload['status']}")
    print(f"COMMAND_ROOM_RUN={payload['run_id']}")
    print(f"META_CONTROL_SHA256={meta_sha}")
    print("META_CONTROL_BOUND_TO_ALL_EXECUTED_AGENT_LANES=true")
    print(f"MASTER_PROMPT_BOUND_TO_ALL_EXECUTED_AGENT_LANES={str(all_executed_lanes_bound).lower()}")
    print(f"WEEKLY_PROOF_PACK_INCLUDED={str(args.include_proof_pack).lower()}")
    print(f"COMMAND_ROOM_REPORT={OUT / 'latest.md'}")
    print("EXTERNAL_EFFECTS=NONE_BY_THIS_RUNNER")
    return 1 if degraded else 0


if __name__ == "__main__":
    raise SystemExit(main())
