#!/usr/bin/env python3
"""Expand commercial ops across targeting, social, War Room, meetings, value plan (idempotent)."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402
from scripts.expand_agency_targets_seed import (  # noqa: E402
    DEFAULT_MIN_ROWS,
    WAVE2_TARGET_ROWS,
    WAVE3_TARGET_ROWS,
    WAVE4_TARGET_ROWS,
    expand_targets,
)


def _run(cmd: list[str], *, label: str) -> int:
    print(f"\n== {label} ==")
    proc = subprocess.run(cmd, cwd=ROOT)
    if proc.returncode != 0:
        print(f"  WARN: {label} exit={proc.returncode}")
    return proc.returncode


def main() -> int:
    ensure_stdout_utf8()
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--min-rows", type=int, default=DEFAULT_MIN_ROWS)
    p.add_argument("--wave2", action="store_true", help=f"Target {WAVE2_TARGET_ROWS} accounts")
    p.add_argument(
        "--wave3",
        action="store_true",
        help=f"Target {WAVE3_TARGET_ROWS} accounts (inbound prep, warm-only)",
    )
    p.add_argument(
        "--wave4",
        action="store_true",
        help=f"Target {WAVE4_TARGET_ROWS} accounts (AEO/inbound prep after proof gate)",
    )
    p.add_argument("--enrich-warm", action="store_true", help="Tag high-priority rows with warm_list notes")
    p.add_argument("--meetings", type=int, default=10, help="Soft launch meeting packs")
    p.add_argument("--touch-drafts", type=int, default=15, help="War Room touch drafts")
    p.add_argument(
        "--cycle-weeks",
        type=int,
        default=28,
        help="Social content queue cycle weeks (default 28)",
    )
    p.add_argument("--skip-import", action="store_true")
    p.add_argument("--skip-war-room", action="store_true")
    args = p.parse_args()

    py = sys.executable
    if args.wave4:
        min_rows = WAVE4_TARGET_ROWS
    elif args.wave3:
        min_rows = WAVE3_TARGET_ROWS
    elif args.wave2:
        min_rows = WAVE2_TARGET_ROWS
    else:
        min_rows = max(80, args.min_rows)
    fail = 0

    print("== expand_commercial_ops_all ==")
    print(f"  target_rows={min_rows} meetings={args.meetings} touch_drafts={args.touch_drafts}")

    try:
        before, after = expand_targets(min_rows=min_rows)
        print(f"  targeting: {before} -> {after} rows")
    except FileNotFoundError as exc:
        print(f"  FAIL targeting: {exc}")
        fail = 1

    cycle = str(max(12, min(args.cycle_weeks, 28)))
    _run(
        [py, str(ROOT / "scripts/expand_social_queue_12w.py"), "--cycle-weeks", cycle],
        label=f"social queue ({cycle}w)",
    )
    if args.enrich_warm or args.wave2 or args.wave3 or args.wave4:
        warm_limit = "150" if args.wave4 else "100"
        _run(
            [py, str(ROOT / "scripts/enrich_targeting_warm.py"), "--limit", warm_limit],
            label="ABM warm enrich",
        )

    if not args.skip_war_room:
        _run([py, str(ROOT / "scripts/commercial_war_room_sync.py")], label="war room sync")
        if not args.skip_import:
            import_cmd = [py, str(ROOT / "scripts/import_war_room_targets.py"), "--apply"]
            if os.environ.get("DEALIX_ADMIN_API_KEY"):
                import_cmd.append("--via-api")
            _run(import_cmd, label="war room import")
        _run(
            [
                py,
                str(ROOT / "scripts/generate_war_room_touch_drafts.py"),
                f"--top-n={args.touch_drafts}",
            ],
            label="touch drafts",
        )

    _run(
        [
            py,
            str(ROOT / "scripts/prepare_soft_launch_meetings.py"),
            f"--top-n={args.meetings}",
        ],
        label="soft launch meetings",
    )
    _run([py, str(ROOT / "scripts/generate_weekly_content_drafts.py")], label="weekly content drafts")
    _run([py, str(ROOT / "scripts/founder_motion_a_pipeline.py"), "--top-n", "15"], label="Motion A")
    _run([py, str(ROOT / "scripts/founder_all_motions_pipeline.py"), "--top-n", "5"], label="Motions A-D")
    _run([py, str(ROOT / "scripts/founder_weekly_scorecard.py")], label="weekly scorecard")
    _run([py, str(ROOT / "scripts/rotate_agency_targets.py"), "--dry-run"], label="P0 rotation preview")

    import importlib

    vp_mod = importlib.import_module("dealix.commercial_ops.value_plan")
    snapshot = vp_mod.build_value_plan_snapshot(motion_top_n=10)
    briefs = ROOT / "data/founder_briefs"
    briefs.mkdir(parents=True, exist_ok=True)
    day = datetime.now(UTC).strftime("%Y-%m-%d")
    md_path = briefs / f"value_plan_{day}.md"
    json_path = briefs / f"value_plan_{day}.json"
    md_path.write_text(vp_mod.render_value_plan_markdown(snapshot), encoding="utf-8")
    json_path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")
    print("\n== value plan snapshot ==")
    print(f"  WROTE {md_path.relative_to(ROOT)}")
    print(f"  WROTE {json_path.relative_to(ROOT)}")
    print(f"  targeting_pool={snapshot['targeting']['agency_pool_rows']}")

    vp_rc = _run([py, str(ROOT / "scripts/verify_value_plan_stack.py")], label="value plan stack verify")
    if vp_rc != 0:
        fail = 1

    print(f"\nCOMMERCIAL_OPS_EXPAND={'FAIL' if fail else 'OK'}")
    return fail


if __name__ == "__main__":
    raise SystemExit(main())
