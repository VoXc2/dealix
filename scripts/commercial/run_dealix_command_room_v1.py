#!/usr/bin/env python3
"""Canonical Dealix Founder Command Room cycle.

This is the VPS-facing executive entrypoint. It does not replace the Company OS;
it verifies the command-room contract and delegates work to the existing Company
OS, autonomous growth, self-improvement, and optional proof-pack runners.

No provider side effect is executed here. External conversation effects remain
owned by the existing action-bound external execution gate.
"""
from __future__ import annotations

import argparse
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
OUT = ROOT / "reports" / "company_os" / "command_room"

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
        "weekly_proof_pack",
        "dealix-delivery",
        ["scripts/commercial/run_weekly_proof_pack.py", "--client", "dealix", "--mode", "draft-only"],
        "critical",
    ),
    (
        "content_factory",
        "dealix-content",
        ["scripts/dealix_content_factory_daily.py"],
        "critical",
    ),
]

FORBIDDEN_LIVE_FLAGS = {
    "DEALIX_EXTERNAL_SEND": {"1", "true", "yes"},
    "EMAIL_LIVE_SEND": {"1", "true", "yes"},
    "WHATSAPP_ALLOW_LIVE_SEND": {"1", "true", "yes"},
    "PUBLIC_PUBLISH": {"1", "true", "yes"},
    "PAYMENT_EXECUTION": {"1", "true", "yes"},
    "PRODUCTION_MUTATION": {"1", "true", "yes"},
}


def stamp() -> str:
    return datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")


def now_iso() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def run(label: str, argv: list[str]) -> dict[str, Any]:
    started = now_iso()
    command = [sys.executable, *argv]
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
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


def load_config() -> dict[str, Any]:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


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
        "",
        "## CEO Now",
    ]
    for item in payload["ceo_now"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Agent lanes"])
    for lane in payload["lanes"]:
        lines.append(
            f"- **{lane['owner_agent']} / {lane['label']}** — rc={lane['rc']} — {lane['status']}"
        )
    lines.extend([
        "",
        "## External authority",
        "- Live external effects are not executed by this command-room runner.",
        "- Founder Delegation Sessions are disabled by default and only make exact actions eligible for canonical action-bound approval.",
        "- Existing provider execution gate remains authoritative.",
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

    if not CONFIG.is_file() or not VERIFY.is_file():
        print("COMMAND_ROOM=BLOCKED_CONFIG_OR_VERIFIER_MISSING", file=sys.stderr)
        return 2

    live_flags = env_violations()
    if live_flags:
        print(f"COMMAND_ROOM=BLOCKED_LIVE_FLAGS flags={','.join(sorted(live_flags))}", file=sys.stderr)
        return 2

    verify = run("command_room_verify", [str(VERIFY.relative_to(ROOT))])
    if verify["rc"] != 0:
        print("COMMAND_ROOM=BLOCKED_VERIFIER", file=sys.stderr)
        print(verify["stderr_tail"], file=sys.stderr)
        return int(verify["rc"] or 1)

    config = load_config()
    # Delivery proof is a canonical default lane now. Keep the legacy flag
    # accepted for CLI compatibility, but never duplicate the lane.
    runner_specs = list(RUNNERS)
    _ = args.include_proof_pack

    lanes: list[dict[str, Any]] = []
    for label, owner, argv, criticality in runner_specs:
        if not (ROOT / argv[0]).is_file():
            lanes.append({
                "label": label,
                "owner_agent": owner,
                "criticality": criticality,
                "rc": 127,
                "status": "BLOCKED_MISSING_RUNNER",
                "stdout_tail": "",
                "stderr_tail": argv[0],
            })
            continue
        receipt = run(label, argv)
        receipt.update(
            owner_agent=owner,
            criticality=criticality,
            status="PASS" if receipt["rc"] == 0 else "DEGRADED",
        )
        lanes.append(receipt)

    degraded = [lane for lane in lanes if lane["rc"] != 0]
    payload: dict[str, Any] = {
        "schema_version": "dealix.command-room-receipt.v1",
        "run_id": stamp(),
        "generated_at": now_iso(),
        "north_star": config["north_star"],
        "status": "DEGRADED" if degraded else "PASS",
        "agents": config["canonical_agents"],
        "channels": config["channels"],
        "command_surfaces": config["command_surfaces"],
        "queues": config["queues"],
        "views": config["views"],
        "lanes": lanes,
        "ceo_now": [
            "Production Trust remains the first engineering gate until exact-release evidence is green.",
            "Revenue agent continuously ranks evidence-backed opportunities and prepares the next commercial movement.",
            "Conversation channels route inbound/requested follow-up to dealix-sales; marketing remains authority-aware.",
            "Delivery and Proof lanes capture customer evidence without promoting synthetic evidence.",
            "Founder attention is reserved for exceptions and exact material authority packets.",
        ],
        "external_execution": {
            "performed_by_command_room": False,
            "delegation_enabled_by_default": config["founder_delegation"]["enabled_by_default"],
            "provider_execution_gate": "dealix.commercial.external_execution_gate",
        },
    }
    write_outputs(payload)

    print(f"COMMAND_ROOM={payload['status']}")
    print(f"COMMAND_ROOM_RUN={payload['run_id']}")
    print(f"COMMAND_ROOM_REPORT={OUT / 'latest.md'}")
    print("EXTERNAL_EFFECTS=NONE_BY_THIS_RUNNER")
    return 1 if degraded else 0


if __name__ == "__main__":
    raise SystemExit(main())
