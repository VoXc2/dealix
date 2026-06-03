"""Write founder daily pack index — links today's governed outputs."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from dealix.commercial_ops.doctrine import format_doctrine_markdown
from dealix.commercial_ops.first_paid_tracker import analyze_first_paid_diagnostic
from dealix.commercial_ops.paths import (
    FOUNDER_BRIEFS_DIR,
    REPO_ROOT,
    WAR_ROOM_TODAY_JSON,
)
from dealix.commercial_ops.value_plan import build_value_plan_snapshot


def write_daily_pack_index(
    *,
    date_str: str | None = None,
    digest_path: Path | None = None,
    out_dir: Path | None = None,
) -> Path:
    """Create data/founder_briefs/DAILY_PACK_{date}.md checklist for founder review."""
    day = date_str or datetime.now(UTC).strftime("%Y-%m-%d")
    d = out_dir or FOUNDER_BRIEFS_DIR
    d.mkdir(parents=True, exist_ok=True)
    brief = d / f"brief_{day}.md"
    commercial = digest_path or (d / f"commercial_{day}.md")
    war_room = WAR_ROOM_TODAY_JSON
    first_paid = analyze_first_paid_diagnostic()
    from dealix.commercial_ops.gtm_stack import build_gtm_stack_snapshot

    gtm = build_gtm_stack_snapshot(abm_top_n=5)

    def _rel(p: Path) -> str:
        try:
            return str(p.relative_to(REPO_ROOT)).replace("\\", "/")
        except ValueError:
            return str(p)

    lines = [
        f"# Founder Daily Pack · {day}",
        "",
        format_doctrine_markdown(),
        "",
        "راجع بالترتيب (لا إرسال خارجي بدون موافقة):",
        "",
        f"- [ ] موجز المؤسس: `{_rel(brief)}`"
        + (" _(موجود)_" if brief.is_file() else " _(شغّل run_founder_commercial_day)_"),
        f"- [ ] Commercial digest: `{_rel(commercial)}`"
        + (" _(موجود)_" if commercial.is_file() else " _(مفقود)_"),
        f"- [ ] War Room JSON: `{_rel(war_room)}`"
        + (" _(موجود)_" if war_room.is_file() else " _(مفقود)_"),
        "- [ ] سجّل صفاً في `docs/commercial/operations/evidence_events_tracker.csv`",
        "- [ ] راجع مسودة LinkedIn من digest أو `scripts/social_queue_today.py`",
        "- [ ] مركز الموافقات قبل Gmail/LinkedIn",
        f"- [ ] أول Diagnostic مدفوع: `{first_paid['dod_doc']}`",
        f"- [ ] اجتماعات Soft Launch: `{first_paid['soft_launch_tracker']}`",
        "",
        "## GTM (مسار اليوم + ABM)",
        "",
        f"- المسار الموصى: **{gtm['dual_track']['recommended_track']}** — {gtm['dual_track']['reason_ar']}",
        f"- موجة ABM 1: {gtm['abm_wave1']['active_rows']}/{gtm['abm_wave1']['min_required']} "
        f"صف فعّال · جاهز={gtm['abm_wave1']['wave1_ready']}",
        "- [ ] راجع `py -3 scripts/founder_gtm_status.py`",
        "- [ ] بعد مكالمة: `py -3 scripts/founder_meeting_debrief_init.py --company \"...\"`",
        f"- [ ] دليل: `{gtm['playbook_path']}`",
        "",
        "## سلم الإيراد (لا تخترع أرقاماً)",
        "",
        first_paid["revenue_ladder_ar"],
        "",
        "## CI (GitHub Secrets)",
        "",
        "| Secret | الغرض |",
        "|--------|--------|",
        "| `DEALIX_API_BASE` | revenue-machine يومي |",
        "| `DEALIX_API_KEY` | Bearer للـ API |",
        "| `DEALIX_ADMIN_API_KEY` | War Room + evidence sync (اختياري) |",
        "| `DEALIX_SYNC_EVIDENCE` | `1` لمزامنة CSV → API |",
        "",
        "## تغذية المرشحين",
        "",
        "```bash",
        "python scripts/seed_revenue_machine_candidates.py",
        "# أو: python scripts/import_gtm_revenue_seed.py --dry-run",
        "```",
        "",
        "_Governed autopilot — لا واتساب بارد._",
    ]
    path = d / f"DAILY_PACK_{day}.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    _write_index_json(day, path, commercial, war_room, brief, first_paid, gtm)
    return path


def _write_index_json(
    day: str,
    pack_md: Path,
    commercial: Path,
    war_room: Path,
    brief: Path,
    first_paid: dict[str, Any] | None = None,
    gtm: dict[str, Any] | None = None,
) -> Path:
    """Machine-readable index for founder UI and CI artifacts."""
    d = pack_md.parent

    def _rel(p: Path) -> str:
        try:
            return str(p.relative_to(REPO_ROOT)).replace("\\", "/")
        except ValueError:
            return str(p)

    fp = first_paid or analyze_first_paid_diagnostic()
    gtm_snap = gtm
    if gtm_snap is None:
        from dealix.commercial_ops.gtm_stack import build_gtm_stack_snapshot

        gtm_snap = build_gtm_stack_snapshot(abm_top_n=5)
    from dealix.commercial_ops.full_ops_autopilot import (
        build_full_autonomous_ops_snapshot,
        build_value_plan_hint,
    )

    vp = build_value_plan_hint(top_n=5)
    vp_json = d / f"value_plan_{day}.json"
    vp_json.write_text(json.dumps(vp, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    autonomous_ops = build_full_autonomous_ops_snapshot(
        top_n=5,
        include_nested=False,
        include_value_plan=False,
    )
    from dealix.commercial_ops.value_map_status import write_value_map_artifacts

    vm_paths = write_value_map_artifacts(day=day, motion_top_n=5)
    payload = {
        "date": day,
        "pack_md": _rel(pack_md),
        "brief_md": _rel(brief),
        "commercial_md": _rel(commercial),
        "value_plan_json": _rel(vp_json),
        "commercial_value_map_md": vm_paths.get("md"),
        "commercial_value_map_json": vm_paths.get("json"),
        "war_room_json": _rel(war_room) if war_room.is_file() else None,
        "brief_exists": brief.is_file(),
        "commercial_exists": commercial.is_file(),
        "war_room_exists": war_room.is_file(),
        "ops_ui": {
            "founder": "/ar/ops/founder",
            "war_room": "/ar/ops/war-room",
            "approvals": "/ar/ops/approvals",
            "marketing": "/ar/ops/marketing",
        },
        "first_paid_diagnostic": fp,
        "value_plan": vp,
        "gtm_stack": gtm_snap,
        "soft_launch_meetings": fp["soft_launch_tracker"],
        "full_autonomous_ops": {
            "schema_version": autonomous_ops.get("schema_version"),
            "automation_readiness": autonomous_ops.get("automation_readiness"),
            "founder_only_actions_ar": autonomous_ops.get("founder_only_actions_ar"),
            "commands": autonomous_ops.get("commands"),
        },
    }
    index_path = d / "index.json"
    index_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return index_path


def pack_status(date_str: str | None = None) -> dict[str, Any]:
    day = date_str or datetime.now(UTC).strftime("%Y-%m-%d")
    d = FOUNDER_BRIEFS_DIR
    pack_path = d / f"DAILY_PACK_{day}.md"
    try:
        pack_index = str(pack_path.relative_to(REPO_ROOT)).replace("\\", "/")
    except ValueError:
        pack_index = str(pack_path)
    return {
        "date": day,
        "brief_exists": (d / f"brief_{day}.md").is_file(),
        "commercial_exists": (d / f"commercial_{day}.md").is_file(),
        "war_room_exists": WAR_ROOM_TODAY_JSON.is_file(),
        "pack_index": pack_index,
    }
