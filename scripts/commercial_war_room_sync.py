#!/usr/bin/env python3
"""Sync War Room and emit a daily internal commercial activation queue."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from dealix.commercial_ops.api_client import trigger_daily_targeting
from dealix.commercial_ops.autonomous_activation import build_activation_command
from dealix.commercial_ops.outreach_drafts import attach_outreach_drafts
from dealix.commercial_ops.paths import WAR_ROOM_TODAY_JSON
from dealix.commercial_ops.targeting_csv import build_war_room_today, load_targets
from dealix.commercial_ops.targeting_rotation import select_daily_p0_targets


def _atomic_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp.replace(path)


def _source_ref(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(REPO_ROOT.resolve()))
    except ValueError:
        return str(path)


def _activation_dir(explicit: str | None) -> Path:
    if explicit:
        return Path(explicit)
    root = Path(os.environ.get("DEALIX_AUTOPILOT_ROOT", "/opt/dealix/company-autopilot"))
    return root / "reports"


def write_activation_artifacts(payload: dict, *, war_room_path: Path, activation_dir: Path) -> int:
    activation_dir.mkdir(parents=True, exist_ok=True)
    command_path = activation_dir / "commercial-activation-command-latest.json"
    queue_path = activation_dir / "commercial-agent-workload-queue-latest.json"

    command = build_activation_command(payload, source_ref=_source_ref(war_room_path))
    _atomic_json(command_path, command)

    router = REPO_ROOT / "scripts/commercial/route_commercial_agent_workloads_v1.py"
    if not router.is_file():
        print(f"BLOCKED commercial activation router missing: {router}", file=sys.stderr)
        return 2

    proc = subprocess.run(
        [
            sys.executable,
            str(router),
            "--command",
            str(command_path),
            "--output",
            str(queue_path),
        ],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.stdout:
        print(proc.stdout, end="")
    if proc.stderr:
        print(proc.stderr, end="", file=sys.stderr)
    if proc.returncode != 0:
        print(f"DEALIX_COMMERCIAL_ACTIVATION=FAIL router_rc={proc.returncode}", file=sys.stderr)
        return proc.returncode

    print(f"DEALIX_COMMERCIAL_ACTIVATION_COMMAND={command_path}")
    print(f"DEALIX_COMMERCIAL_AGENT_QUEUE={queue_path}")
    print("DEALIX_COMMERCIAL_ACTIVATION=PASS")
    print("EXTERNAL_EFFECTS=NONE")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--top-n", type=int, default=15)
    p.add_argument("--trigger-targeting", action="store_true")
    p.add_argument("--no-rotation", action="store_true", help="Use full CSV ranking only")
    p.add_argument("--out", default=str(WAR_ROOM_TODAY_JSON))
    p.add_argument("--activation-dir", help="Override out-of-repo activation report directory")
    p.add_argument("--skip-activation", action="store_true", help="Only refresh the legacy War Room artifact")
    args = p.parse_args()

    all_rows = load_targets()
    pool = all_rows if args.no_rotation else select_daily_p0_targets(all_rows, top_n=args.top_n)
    payload = attach_outreach_drafts(build_war_room_today(pool, top_n=args.top_n))
    out = Path(args.out)
    _atomic_json(out, payload)
    print(f"WROTE · {out} · targets={len(payload['targets']['items'])}")

    if not args.skip_activation:
        rc = write_activation_artifacts(
            payload,
            war_room_path=out,
            activation_dir=_activation_dir(args.activation_dir),
        )
        if rc != 0:
            return rc

    if args.trigger_targeting:
        result = trigger_daily_targeting()
        if result:
            print(json.dumps({"daily_targeting": result}, ensure_ascii=False, indent=2))
        else:
            print("SKIP daily-targeting (set DEALIX_API_BASE + admin key)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
