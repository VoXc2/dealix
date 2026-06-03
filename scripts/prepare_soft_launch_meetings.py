#!/usr/bin/env python3
"""Prepare Soft Launch meeting lane: top-N client packs + tracker YAML (founder executes calls)."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.client_pack import build_client_pack  # noqa: E402
from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402

TRACKER = ROOT / "docs/commercial/operations/soft_launch_meetings_tracker.yaml"
WAR_ROOM = ROOT / "data/war_room_today.json"
SOP = "docs/commercial/operations/CLIENT_PACK_SOP_AR.md"


def _load_top_targets(n: int) -> list[dict]:
    if WAR_ROOM.is_file():
        data = json.loads(WAR_ROOM.read_text(encoding="utf-8"))
        items = (data.get("targets") or {}).get("items") or []
        if items:
            return items[:n]
    from dealix.commercial_ops.targeting_csv import load_targets
    from dealix.commercial_ops.targeting_rotation import select_daily_p0_targets

    return select_daily_p0_targets(load_targets(), top_n=n)


def main() -> int:
    ensure_stdout_utf8()
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--top-n", type=int, default=10, help="Meeting slots to prepare (default 10, max 15)")
    p.add_argument("--dry-run", action="store_true", help="Build tracker only; skip client pack writes")
    args = p.parse_args()

    targets = _load_top_targets(max(1, min(args.top_n, 12)))
    if not targets:
        print("SOFT_LAUNCH_MEETINGS: FAIL no_targets")
        return 1

    meetings = []
    packs_ok = 0
    for i, row in enumerate(targets, start=1):
        company = (row.get("company") or "").strip()
        pack_dir = ""
        if company and not args.dry_run:
            try:
                pack = build_client_pack(company=company, write_disk=True)
                pack_dir = (pack.get("paths") or {}).get("directory") or ""
                packs_ok += 1
            except ValueError:
                pack_dir = ""

        meetings.append(
            {
                "slot": i,
                "company": company,
                "contact": row.get("contact") or "",
                "motion": row.get("motion") or "A",
                "offer_id": row.get("offer_id") or "ten_lead_audit",
                "status": "scheduled",
                "client_pack_dir": pack_dir,
                "checklist": [
                    "قبل: generate_client_pack + deck_notes",
                    "أثناء: /ar/business-now#strategy + Calendly",
                    "بعد: war-room status + evidence CSV",
                ],
            }
        )

    doc = {
        "updated_at": datetime.now(UTC).isoformat(),
        "goal": "3-5 discovery meetings before paid launch announcement",
        "sop": SOP,
        "ui": {
            "founder": "/ar/ops/founder",
            "war_room": "/ar/ops/war-room",
            "approvals": "/ar/ops/approvals",
        },
        "meetings": meetings,
    }
    TRACKER.parent.mkdir(parents=True, exist_ok=True)
    TRACKER.write_text(
        yaml.safe_dump(doc, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )

    print(f"SOFT_LAUNCH_MEETINGS: OK slots={len(meetings)} packs={packs_ok}")
    try:
        tracker_label = str(TRACKER.relative_to(ROOT))
    except ValueError:
        tracker_label = str(TRACKER)
    print(f"  tracker: {tracker_label}")
    for m in meetings:
        print(f"  [{m['slot']}] {m['company']} -> {m.get('client_pack_dir') or 'no_pack'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
