"""Enrichment payload for ops founder-dashboard (Sovereign GTM)."""

from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
from typing import Any

from dealix.commercial_ops.evidence_csv import count_evidence_events, load_evidence_rows
from dealix.commercial_ops.paths import WAR_ROOM_TODAY_JSON
from dealix.commercial_ops.social_queue import get_post_for_date
from dealix.commercial_ops.strategy_refs import load_founder_strategy_refs
from dealix.commercial_ops.targeting_csv import build_war_room_today, load_targets
from dealix.marketing_factory.store import get_marketing_store
from dealix.revenue_ops_autopilot.store import get_autopilot_store
from dealix.revenue_ops_autopilot.war_room import build_daily_summary, normalize_lead


def _bridge_events_7d() -> int:
    store = get_autopilot_store()
    since_7 = datetime.now(UTC) - timedelta(days=7)
    count = 0
    for e in store.list_evidence(limit=900):
        if e.event_type != "external_lead_bridged":
            continue
        created = e.created_at
        if created.tzinfo is None:
            created = created.replace(tzinfo=UTC)
        else:
            created = created.astimezone(UTC)
        if created >= since_7:
            count += 1
    return count


def build_sovereign_gtm_slice() -> dict[str, Any]:
    rows = load_evidence_rows()
    evidence_week = count_evidence_events(rows)
    social = get_post_for_date()

    war_room_json: dict[str, Any] | None = None
    if WAR_ROOM_TODAY_JSON.is_file():
        try:
            war_room_json = json.loads(WAR_ROOM_TODAY_JSON.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            war_room_json = None
    if war_room_json is None:
        war_room_json = build_war_room_today(load_targets())

    store_leads = [normalize_lead(L) for L in get_autopilot_store().list_leads(limit=600)]
    api_summary = build_daily_summary(store_leads)

    top_targets = war_room_json.get("targets", {}).get("items") or api_summary.get("top_targets") or []

    social_tile: dict[str, Any] | None = None
    if social:
        social_tile = {
            "title_ar": social.get("title_ar"),
            "pillar": social.get("pillar"),
            "status": social.get("status"),
            "cta_ar": social.get("cta_ar"),
            "aeo_slug": social.get("aeo_slug"),
            "calendar_date": social.get("calendar_date"),
        }

    mkt = get_marketing_store()
    mkt.ensure_seed_loaded()
    marketing_stats = mkt.stats()

    from dealix.commercial_ops.gtm_stack import build_gtm_stack_snapshot
    from dealix.commercial_ops.outreach_drafts import attach_outreach_drafts
    from dealix.commercial_ops.targeting_rotation import select_daily_p0_targets

    pool = select_daily_p0_targets(load_targets(), top_n=5)
    targeting_pack = attach_outreach_drafts(build_war_room_today(pool, top_n=5))
    targeting_today_top5 = (targeting_pack.get("targets") or {}).get("items") or []

    return {
        "evidence_events_week": evidence_week,
        "social_post_due_today": social_tile,
        "war_room_top_targets": top_targets[:10],
        "war_room_daily_quotas": war_room_json.get("daily_quotas"),
        "war_room_file": str(WAR_ROOM_TODAY_JSON.name),
        "marketing_stats": marketing_stats,
        "targeting_today_top5": targeting_today_top5,
        "bridge_events_7d": _bridge_events_7d(),
        "sample_proof_pack_path": "docs/commercial/operations/sample_proof_pack/SAMPLE_PROOF_PACK_AGENCY_AR.md",
        "master_plan_path": "docs/commercial/MASTER_COMMERCIAL_OPERATING_PLAN_AR.md",
        "sovereign_gtm_path": "docs/commercial/DEALIX_SALES_GTM_SOVEREIGN_MASTER_AR.md",
        "founder_operating_system_path": "docs/ops/FOUNDER_OPERATING_SYSTEM_AR.md",
        "strategy_refs": load_founder_strategy_refs(),
        "gtm_stack": build_gtm_stack_snapshot(abm_top_n=5),
        "gtm_playbook_path": "docs/commercial/GTM_SAUDI_WEB_RESEARCH_PLAYBOOK_AR.md",
    }
