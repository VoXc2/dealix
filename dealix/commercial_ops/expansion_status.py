"""Commercial expansion snapshot — targeting, social, ABM, gates (no invented revenue)."""

from __future__ import annotations

from typing import Any

from dealix.commercial_ops.gtm_stack import build_gtm_stack_snapshot
from dealix.commercial_ops.social_queue import load_social_queue
from dealix.commercial_ops.targeting_csv import load_targets


def build_expansion_status(*, abm_top_n: int = 10) -> dict[str, Any]:
    targets = load_targets()
    n = len(targets)
    queue = load_social_queue()
    posts = list(queue.get("posts") or [])
    cycle = int(queue.get("cycle_weeks") or 12)
    gtm = build_gtm_stack_snapshot(abm_top_n=abm_top_n)

    motion_counts = {"A": 0, "B": 0, "C": 0, "D": 0}
    for row in targets:
        m = (row.get("motion") or "A").strip().upper()
        if m in motion_counts:
            motion_counts[m] += 1

    targeting = {
        "pool_rows": n,
        "soft_strict_min": 120,
        "wave2_min": 150,
        "wave3_prep_min": 200,
        "wave4_prep_min": 250,
        "wave2_ready": n >= 150,
        "wave3_prep_ready": n >= 200,
        "wave4_prep_ready": n >= 250,
        "motion_counts": motion_counts,
    }
    social = {
        "posts": len(posts),
        "cycle_weeks": cycle,
        "target_posts_20w": 100,
        "target_posts_24w": 120,
        "target_posts_28w": 140,
        "queue_ready_20w": len(posts) >= 100 and cycle >= 20,
        "queue_ready_24w": len(posts) >= 120 and cycle >= 24,
        "queue_ready_28w": len(posts) >= 140 and cycle >= 28,
    }
    scripts = {
        "expand_full": "powershell -File scripts/founder_commercial_expand.ps1 -Full",
        "expand_all": "py -3 scripts/expand_commercial_ops_all.py --wave4 --cycle-weeks 28 --enrich-warm",
        "expand_wave3": "py -3 scripts/expand_commercial_ops_all.py --wave3",
        "expand_wave4": "py -3 scripts/expand_commercial_ops_all.py --wave4",
        "enrich_warm": "py -3 scripts/enrich_targeting_warm.py",
        "all_motions": "py -3 scripts/founder_all_motions_pipeline.py",
        "value_plan_day": "powershell -File scripts/run_value_plan_day.ps1",
        "api_status": "/api/v1/ops-autopilot/founder/expansion-status",
    }
    return {
        "targeting": targeting,
        "social": social,
        "gtm_stack": gtm,
        "scripts": scripts,
        "next_actions_ar": _next_actions_ar(targeting, social, gtm),
    }


def _next_actions_ar(
    targeting: dict[str, Any],
    social: dict[str, Any],
    gtm: dict[str, Any],
) -> list[str]:
    out: list[str] = []
    if not targeting["wave2_ready"]:
        out.append("شغّل: expand_agency_targets_seed.py --wave2 (هدف 150 صف).")
    if not social.get("queue_ready_28w"):
        out.append("شغّل: expand_social_queue_12w.py --cycle-weeks 28.")
    elif not targeting.get("wave4_prep_ready"):
        out.append("للموجة 4: expand_commercial_ops_all.py --wave4 (250 صف).")
    abm = gtm.get("abm_wave1") or {}
    if abm and not abm.get("wave1_ready"):
        out.append(
            f"موجة ABM 1: {abm.get('active_rows', 0)}/{abm.get('min_required', 30)} — enrich_targeting_warm.py"
        )
    if not out:
        out.append("التوسعة التقنية جاهزة — ركّز على لمسات warm + أول Diagnostic مدفوع.")
    return out
