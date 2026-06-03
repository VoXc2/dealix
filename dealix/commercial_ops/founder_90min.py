"""90-minute founder operating checklist sections (governed commercial day)."""

from __future__ import annotations

import os
from typing import Any

from dealix.commercial_ops.api_client import fetch_founder_dashboard, fetch_war_room_today_pack
from dealix.commercial_ops.evidence_csv import count_evidence_events, load_evidence_rows
from dealix.commercial_ops.kpi_snapshot import load_kpi_commercial_status
from dealix.commercial_ops.social_queue import format_linkedin_draft, get_post_for_date
from dealix.commercial_ops.targeting_csv import build_war_room_today, load_targets

_CALENDLY_DEFAULT = os.environ.get(
    "CALENDLY_URL",
    "https://calendly.com/sami-assiri11/dealix-demo",
)

_CHECKLIST_AR: tuple[str, ...] = (
    "0–10 د: افتح brief + digest — لا بناء ميزات قبل scope_requested",
    "10–25 د: War Room — 10 لمسات (موافقة ثم إرسال يدوي)",
    "25–40 د: مركز الموافقات — كل المسودات المعلّقة",
    "40–55 د: LinkedIn — انسخ المسودة، SOAEN، نشر يدوي، سجّل published",
    "55–70 د: مكالمات/ديمو — meeting brief + Calendly",
    "70–85 د: متابعات + شريك واحد + حدث أدلة في CSV",
    "85–90 د: تحديث war-room status + KPI من CRM إن وُجد",
)


def build_founder_90min_sections(*, api_base: str | None = None, admin_key: str | None = None) -> dict[str, Any]:
    rows = load_evidence_rows()
    evidence = count_evidence_events(rows)
    kpi = load_kpi_commercial_status()
    social = get_post_for_date()
    pack = fetch_war_room_today_pack(api_base=api_base, admin_key=admin_key)
    if pack is None:
        pack = build_war_room_today(load_targets())

    top_items = []
    if isinstance(pack, dict):
        top_items = (pack.get("targets") or {}).get("items") or pack.get("top_leads") or []
    if not top_items and isinstance(pack, dict):
        top_items = pack.get("items") or []

    dash = fetch_founder_dashboard(api_base=api_base, admin_key=admin_key)
    pending_approvals = -1
    meetings_week = 0
    meetings_is_estimate = True
    if dash:
        tiles = dash.get("tiles") or {}
        pending_approvals = int(tiles.get("pending_approvals") or 0)
        mp = tiles.get("meetings_placeholder") or tiles.get("meetings_this_week")
        if isinstance(mp, dict):
            meetings_week = int(mp.get("count") or mp.get("booked") or 0)
            meetings_is_estimate = bool(mp.get("booked_is_estimate", mp.get("is_estimate", True)))
        elif isinstance(mp, int):
            meetings_week = mp
            meetings_is_estimate = False

    return {
        "checklist_ar": list(_CHECKLIST_AR),
        "calendly_url": _CALENDLY_DEFAULT,
        "top_targets": top_items[:10],
        "social_status": (social or {}).get("status") if social else None,
        "social_title_ar": (social or {}).get("title_ar") if social else None,
        "linkedin_draft": format_linkedin_draft(social) if social else "",
        "evidence_today": evidence.get("today_total", 0),
        "pending_approvals": pending_approvals,
        "meetings_this_week": meetings_week,
        "meetings_is_estimate": meetings_is_estimate,
        "kpi_pending": kpi.get("pending_count", 0),
        "kpi_hint_ar": kpi.get("hint_ar"),
    }


def render_90min_markdown(sections: dict[str, Any]) -> str:
    lines = [
        "## خطة 90 دقيقة (المؤسس)",
        "",
    ]
    for i, step in enumerate(sections.get("checklist_ar") or [], 1):
        lines.append(f"{i}. {step}")
    lines.extend(
        [
            "",
            f"- **Calendly:** {sections.get('calendly_url')}",
            f"- **موافقات معلّقة:** {sections.get('pending_approvals')}",
            f"- **أحداث أدلة اليوم:** {sections.get('evidence_today')}",
        ]
    )
    mw = sections.get("meetings_this_week")
    est = sections.get("meetings_is_estimate")
    if mw is not None:
        suffix = " (تقدير)" if est else ""
        lines.append(f"- **اجتماعات هذا الأسبوع:** {mw}{suffix}")
    if sections.get("kpi_pending"):
        lines.append(f"- **KPI معلّق:** {sections.get('kpi_pending')} — {sections.get('kpi_hint_ar') or ''}")

    lines.extend(["", "### Top 10 أهداف", ""])
    for row in sections.get("top_targets") or []:
        co = row.get("company") or row.get("name") or "?"
        st = row.get("war_room_status") or row.get("status") or "?"
        lines.append(f"- **{co}** · `{st}`")
    if not sections.get("top_targets"):
        lines.append("- _(لا أهداف — شغّل import_war_room_targets)_")

    st = sections.get("social_status")
    if st:
        lines.extend(
            [
                "",
                f"### LinkedIn · `{st}`",
                "",
                "```",
                sections.get("linkedin_draft") or "",
                "```",
            ]
        )
    return "\n".join(lines)
