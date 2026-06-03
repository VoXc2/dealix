"""Build founder commercial daily digest (markdown + dict)."""

from __future__ import annotations

import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from dealix.commercial_ops.api_client import fetch_founder_dashboard
from dealix.commercial_ops.doctrine import build_soaen_daily, format_doctrine_markdown
from dealix.commercial_ops.evidence_csv import (
    count_evidence_events,
    load_evidence_rows,
    pull_events_from_api,
    scope_requested_within_days,
    sync_rows_to_api,
)
from dealix.commercial_ops.founder_90min import build_founder_90min_sections, render_90min_markdown
from dealix.commercial_ops.kpi_snapshot import load_kpi_commercial_status
from dealix.commercial_ops.market_intelligence_refs import build_market_intel_digest_block
from dealix.commercial_ops.outreach_drafts import attach_outreach_drafts
from dealix.commercial_ops.paths import (
    EVIDENCE_TRACKER_CSV,
    FOUNDER_BRIEFS_DIR,
    REPO_ROOT,
    WAR_ROOM_TODAY_JSON,
)
from dealix.commercial_ops.social_queue import format_linkedin_draft, get_post_for_date
from dealix.commercial_ops.strategy_refs import strategy_links_flat
from dealix.commercial_ops.targeting_csv import build_war_room_today, load_targets
from dealix.commercial_ops.targeting_rotation import preview_next_targets, select_daily_p0_targets
from dealix.commercial_ops.value_plan import build_value_plan_snapshot


def build_commercial_digest(
    *,
    sync_evidence: bool = False,
    pull_evidence: bool = False,
    no_build_days: int = 14,
    skip_no_build: bool = False,
    api_base: str | None = None,
    admin_key: str | None = None,
) -> dict[str, Any]:
    pull_result = None
    if pull_evidence:
        pull_result = pull_events_from_api(api_base=api_base, admin_key=admin_key)
    rows = load_evidence_rows()
    evidence = count_evidence_events(rows, exclude_placeholders=True)
    evidence_all_rows = count_evidence_events(rows)
    war_room_file: dict[str, Any] | None = None
    if WAR_ROOM_TODAY_JSON.is_file():
        try:
            war_room_file = json.loads(WAR_ROOM_TODAY_JSON.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            war_room_file = None
    all_targets = load_targets()
    if war_room_file is None:
        pool = select_daily_p0_targets(all_targets, top_n=15)
        war_room_file = attach_outreach_drafts(build_war_room_today(pool, top_n=15))
    else:
        war_room_file = attach_outreach_drafts(war_room_file)

    rotation_preview = [
        {
            "company": r.get("company"),
            "status": r.get("status"),
            "segment": r.get("segment"),
            "motion": r.get("motion"),
        }
        for r in preview_next_targets(all_targets, top_n=3)
    ]

    social = get_post_for_date()
    linkedin_draft = format_linkedin_draft(social) if social else ""

    api_dash = fetch_founder_dashboard()
    sync_result = None
    if sync_evidence:
        sync_result = sync_rows_to_api(rows, api_base=api_base, admin_key=admin_key, mark_csv=True)

    warnings: list[str] = []
    if not skip_no_build and not scope_requested_within_days(no_build_days, rows):
        warnings.append(
            f"no-build: لا scope_requested خلال {no_build_days} يوماً — ركّز على Diagnostic وليس ميزات."
        )
    if evidence["today_total"] < 1:
        warnings.append("سجّل حدث أدلة واحد على الأقل اليوم في evidence_events_tracker.csv")

    kpi_status = load_kpi_commercial_status()
    if kpi_status.get("pending_count", 0) > 0:
        hint = kpi_status.get("hint_ar") or "أكمل KPI من CRM"
        warnings.append(f"KPI: {hint}")

    founder_90 = build_founder_90min_sections(api_base=api_base, admin_key=admin_key)
    value_plan = build_value_plan_snapshot(motion_top_n=5)
    market_intel = build_market_intel_digest_block()

    today_focus = [
        "Control Tower: أفضل شريحة (وكالة P0) · رسالة · Proof · اعتراض · توقف funnel",
        "War Room: أعلى 10 أهداف + 5 متابعات",
        "10 لمسات موافَق عليها · 1 شريك · 1 حدث أدلة",
        "منشور LinkedIn: مسودة جاهزة — راجع SOAEN ثم انشر يدوياً",
        "مركز الموافقات قبل أي إرسال خارجي",
    ]
    pow = market_intel.get("pillar_of_week")
    if pow and pow.get("topic_ar"):
        today_focus.append(
            f"استخبارات السوق — وثيقة الأسبوع: {pow['topic_ar']} (`{pow.get('doc', '')}`)"
        )
    if market_intel.get("is_friday_review"):
        today_focus.append(
            "جمعة: نفّذ MARKET_INTELLIGENCE_WEEKLY_REVIEW_CHECKLIST_AR (20 دقيقة)"
        )

    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "schema_version": "1.5",
        "market_intelligence": market_intel,
        "value_plan": value_plan,
        "doctrine": build_soaen_daily(),
        "is_estimate": True,
        "rotation_preview_tomorrow": rotation_preview,
        "founder_90min": founder_90,
        "evidence_pull": pull_result,
        "evidence": evidence,
        "evidence_all_rows": evidence_all_rows,
        "kpi_commercial": kpi_status,
        "evidence_tracker_path": str(EVIDENCE_TRACKER_CSV.relative_to(REPO_ROOT)),
        "war_room": war_room_file,
        "social_post_due_today": social,
        "linkedin_draft": linkedin_draft,
        "api_dashboard": api_dash,
        "evidence_sync": sync_result,
        "today_focus_ar": today_focus,
        "no_build_warnings": warnings,
        "links": {
            "master_plan": "docs/commercial/MASTER_COMMERCIAL_OPERATING_PLAN_AR.md",
            "sovereign_gtm": "docs/commercial/DEALIX_SALES_GTM_SOVEREIGN_MASTER_AR.md",
            "founder_operating_system": "docs/ops/FOUNDER_OPERATING_SYSTEM_AR.md",
            "war_room_doc": "docs/ops/DEALIX_REVENUE_WAR_ROOM_AR.md",
            "sample_proof": "docs/commercial/operations/sample_proof_pack/SAMPLE_PROOF_PACK_AGENCY_AR.md",
            **strategy_links_flat(),
        },
    }


def render_digest_markdown(digest: dict[str, Any]) -> str:
    ev = digest["evidence"]
    wr = digest.get("war_room") or {}
    social = digest.get("social_post_due_today") or {}
    f90 = digest.get("founder_90min") or {}
    doctrine_md = format_doctrine_markdown(digest.get("doctrine"))
    lines = [
        f"# Dealix — Commercial Digest · {ev.get('date', '')}",
        "",
        doctrine_md,
        "",
        render_90min_markdown(f90),
        "",
        "## تركيز اليوم",
        "",
    ]
    for item in digest.get("today_focus_ar") or []:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## أحداث الأدلة",
            "",
            f"- اليوم: **{ev.get('today_total', 0)}** · الأسبوع: **{ev.get('week_total', 0)}**",
            "",
            "### اليوم حسب النوع",
            "",
        ]
    )
    for k, v in sorted((ev.get("today_by_type") or {}).items()):
        lines.append(f"- `{k}`: {v}")
    if not (ev.get("today_by_type")):
        lines.append("- _(لا أحداث مسجّلة اليوم)_")

    lines.extend(["", "## War Room — أعلى الأهداف", ""])
    for row in (wr.get("targets") or {}).get("items") or []:
        co = row.get("company") or row.get("target") or "?"
        st = row.get("status") or "?"
        seg = row.get("segment") or "?"
        mot = row.get("motion") or "?"
        na = row.get("next_action") or "?"
        lines.append(f"- **{co}** · `{st}` · motion={mot} · segment={seg} · التالي: {na}")
        draft = (row.get("outreach_draft_ar") or "").strip()
        if draft:
            lines.append(f"  - مسودة لمسة: {draft[:120]}…")

    preview = digest.get("rotation_preview_tomorrow") or []
    if preview:
        lines.extend(["", "## غداً (معاينة تدوير P0)", ""])
        for row in preview:
            lines.append(
                f"- **{row.get('company', '?')}** · `{row.get('status', '')}` · {row.get('segment', '')}"
            )

    if social:
        lines.extend(
            [
                "",
                "## منشور LinkedIn (مسودة)",
                "",
                f"**{social.get('title_ar', '')}** · pillar={social.get('pillar')} · status={social.get('status')}",
                "",
                "```",
                digest.get("linkedin_draft") or "",
                "```",
                "",
                "### SOAEN قبل النشر",
                "",
            ]
        )
        for chk in social.get("soaen_checklist_ar") or []:
            lines.append(f"- [ ] {chk}")

    api = digest.get("api_dashboard")
    if api:
        tiles = api.get("tiles") or {}
        lines.extend(["", "## API Dashboard", ""])
        for k, v in tiles.items():
            lines.append(f"- `{k}`: {v}")

    vp = digest.get("value_plan") or {}
    if vp:
        fp = vp.get("first_paid_diagnostic") or {}
        lines.extend(
            [
                "",
                "## Value Plan (بوابة القيمة)",
                "",
                f"- First paid: `{fp.get('verdict')}` · payment (real): {fp.get('payment_received_real', 0)} · proof: {fp.get('proof_pack_delivered_real', 0)}",
                f"- Motion A أهداف: {len((vp.get('motion_a') or {}).get('targets') or [])}",
            ]
        )
        for t in (vp.get("motion_a") or {}).get("targets") or []:
            lines.append(
                f"  - **{t.get('company')}** · `{t.get('status')}` — {t.get('next_action_ar')}"
            )
        for w in vp.get("warnings_ar") or []:
            lines.append(f"> ⚠️ {w}")

    kpi = digest.get("kpi_commercial") or {}
    if kpi.get("registry_exists"):
        lines.extend(
            [
                "",
                "## KPI تجاري (من السجل — لا أرقام مخترعة)",
                "",
                f"- جاهز: **{kpi.get('ready_count', 0)}** · معلّق: **{kpi.get('pending_count', 0)}**",
                f"- ملف الاستيراد: {'موجود' if kpi.get('import_file_exists') else 'غير موجود'}",
            ]
        )
        if kpi.get("hint_ar"):
            lines.append(f"- {kpi['hint_ar']}")
        tracker = digest.get("evidence_tracker_path")
        if tracker:
            lines.append(f"- أحداث الأدلة: `{tracker}`")

    for w in digest.get("no_build_warnings") or []:
        lines.append("")
        lines.append(f"> ⚠️ {w}")

    mi = digest.get("market_intelligence") or {}
    if mi:
        lines.extend(["", "## استخبارات السوق (توجيه اليوم)", ""])
        pow_doc = mi.get("pillar_of_week") or {}
        if pow_doc.get("topic_ar"):
            lines.append(
                f"- **وثيقة الأسبوع:** {pow_doc['topic_ar']} — `{pow_doc.get('doc', '')}`"
            )
        if mi.get("master_index"):
            lines.append(f"- **الفهرس:** `{mi['master_index']}`")
        if mi.get("is_friday_review") and mi.get("friday_checklist"):
            lines.append(f"- **جمعة:** راجع `{mi['friday_checklist']}`")
        if not mi.get("status_ok"):
            lines.append("- ⚠️ بعض مسارات استخبارات السوق ناقصة — راجع `market_intelligence_status`")

    lines.extend(
        [
            "",
            "---",
            "_Governed autopilot: مسودات + موافقة — لا إرسال بارد._",
            f"_Generated: {digest.get('generated_at')}_",
        ]
    )
    return "\n".join(lines)


def write_digest_file(digest: dict[str, Any], out_dir: Path | None = None) -> Path:
    d = out_dir or FOUNDER_BRIEFS_DIR
    d.mkdir(parents=True, exist_ok=True)
    day = (digest.get("evidence") or {}).get("date") or datetime.now(UTC).strftime("%Y-%m-%d")
    path = d / f"commercial_{day}.md"
    path.write_text(render_digest_markdown(digest) + "\n", encoding="utf-8")
    return path
