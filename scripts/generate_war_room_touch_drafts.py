#!/usr/bin/env python3
"""Generate governed outreach drafts for top War Room P0 targets (no external send)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.targeting_csv import load_targets
from dealix.commercial_ops.targeting_rotation import select_daily_p0_targets
from dealix.revenue_ops_autopilot.orchestrator import RevenueAutopilotOrchestrator
from dealix.revenue_ops_autopilot.outreach_templates import build_outreach_draft
from dealix.revenue_ops_autopilot.war_room import (
    normalize_lead,
    outreach_transition_allowed,
    sync_stage_from_war_room,
)


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--top-n", type=int, default=10)
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    orch = RevenueAutopilotOrchestrator()
    store = orch.store
    pool = select_daily_p0_targets(load_targets(), top_n=args.top_n)
    companies = {(r.get("company") or "").strip().lower() for r in pool if r.get("company")}

    drafted: list[str] = []
    skipped: list[str] = []

    for lead in store.list_leads(limit=2000):
        co = (lead.company or "").strip().lower()
        if co not in companies:
            continue
        nl = normalize_lead(lead)
        if nl.war_room_status not in {"not_contacted", "message_drafted"}:
            skipped.append(nl.id)
            continue
        draft = build_outreach_draft(
            company=nl.company,
            contact=nl.name,
            segment=nl.segment,
            pain=nl.pain_hypothesis or nl.pain,
        )
        tgt = "message_drafted"
        ok, _ = outreach_transition_allowed(nl.war_room_status, tgt)  # type: ignore[arg-type]
        if not ok and nl.war_room_status != tgt:
            skipped.append(nl.id)
            continue
        if args.dry_run:
            drafted.append(nl.company or nl.id)
            continue
        from datetime import UTC, datetime

        updated = nl.model_copy(
            update={
                "outreach_draft_snippet_ar": draft,
                "war_room_status": tgt,  # type: ignore[assignment]
                "stage": sync_stage_from_war_room(tgt),  # type: ignore[arg-type]
                "updated_at": datetime.now(UTC),
            },
        )
        store.upsert_lead(updated)
        drafted.append(nl.company or nl.id)

    result = {"drafted": len(drafted), "skipped": len(skipped), "companies": drafted}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"WAR_ROOM_TOUCH_DRAFTS: OK drafted={len(drafted)} dry_run={args.dry_run}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
