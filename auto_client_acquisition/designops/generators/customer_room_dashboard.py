"""Customer Room dashboard generator.

Renders bilingual cards for: customer stage, active services, health
score, proof events count, pending approvals, blocked unsafe actions,
next best actions, weekly summary, channel policy, delivery sessions,
executive notes. If a section has no data, renders the bilingual
"no data yet" sentinel.
"""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.designops.generators.html_renderer import (
    render_artifact_html,
)
from auto_client_acquisition.designops.generators.markdown_renderer import (
    render_artifact_markdown,
)


_NO_DATA = "لا بيانات بعد / no data yet"


# Section keys define the canonical 11-card layout. Each entry is
# (payload_key, title_ar, title_en, render_kind).
# render_kind = "scalar" → render as body string
#             = "list"   → render as items list
_SECTIONS: list[tuple[str, str, str, str]] = [
    ("stage", "مرحلة العميل", "Customer stage", "scalar"),
    ("active_services", "الخدمات النشطة", "Active services", "list"),
    ("health_score", "درجة الصحّة", "Health score", "scalar"),
    ("proof_events_count", "عدد أحداث الإثبات", "Proof events count", "scalar"),
    ("pending_approvals", "موافقات معلّقة", "Pending approvals", "list"),
    (
        "blocked_unsafe_actions",
        "إجراءات محظورة غير آمنة",
        "Blocked unsafe actions",
        "list",
    ),
    ("next_best_actions", "أفضل إجراءات تالية", "Next best actions", "list"),
    ("weekly_summary", "الموجز الأسبوعيّ", "Weekly summary", "scalar"),
    ("channel_policy", "سياسة القنوات", "Channel policy", "scalar"),
    ("delivery_sessions", "جلسات التسليم", "Delivery sessions", "list"),
    ("executive_notes", "ملاحظات تنفيذيّة", "Executive notes", "list"),
]


def _is_empty(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, (list, tuple, dict, str)) and len(value) == 0:
        return True
    return False


def _render_card_ar(value: Any, kind: str) -> dict[str, Any]:
    if _is_empty(value):
        return {"body": _NO_DATA}
    if kind == "list":
        if isinstance(value, list):
            return {"items": [str(v) for v in value]}
        return {"body": str(value)}
    return {"body": str(value)}


def _render_card_en(value: Any, kind: str) -> dict[str, Any]:
    if _is_empty(value):
        return {"body": _NO_DATA}
    if kind == "list":
        if isinstance(value, list):
            return {"items": [str(v) for v in value]}
        return {"body": str(value)}
    return {"body": str(value)}


def generate_customer_room_dashboard(
    customer_handle: str,
    customer_payload: dict[str, Any],
) -> dict[str, Any]:
    """Compose a bilingual customer room dashboard artifact."""
    payload = customer_payload or {}

    sections_ar: list[dict[str, Any]] = []
    sections_en: list[dict[str, Any]] = []
    md_lines_ar: list[str] = [f"# لوحة غرفة العميل — {customer_handle}", ""]
    md_lines_en: list[str] = [f"# Customer Room — {customer_handle}", ""]

    for key, title_ar, title_en, kind in _SECTIONS:
        value = payload.get(key)
        ar_card = _render_card_ar(value, kind)
        en_card = _render_card_en(value, kind)
        sections_ar.append({"title": title_ar, **ar_card})
        sections_en.append({"title": title_en, **en_card})

        md_lines_ar.append(f"## {title_ar}")
        if "items" in ar_card:
            for it in ar_card["items"]:
                md_lines_ar.append(f"- {it}")
        else:
            md_lines_ar.append(ar_card.get("body", _NO_DATA))
        md_lines_ar.append("")

        md_lines_en.append(f"## {title_en}")
        if "items" in en_card:
            for it in en_card["items"]:
                md_lines_en.append(f"- {it}")
        else:
            md_lines_en.append(en_card.get("body", _NO_DATA))
        md_lines_en.append("")

    title_ar = f"لوحة غرفة العميل — {customer_handle}"
    title_en = f"Customer Room Dashboard — {customer_handle}"

    approval_status = "approval_required"
    audience = "internal_review"
    evidence_refs = [
        f"customer_handle={customer_handle}",
        f"sections={len(_SECTIONS)}",
    ]

    md_full = render_artifact_markdown(
        title_ar=title_ar,
        title_en=title_en,
        sections_ar=sections_ar,
        sections_en=sections_en,
        approval_status=approval_status,
        audience=audience,
        evidence_refs=evidence_refs,
    )
    html = render_artifact_html(
        title_ar=title_ar,
        title_en=title_en,
        sections_ar=sections_ar,
        sections_en=sections_en,
        approval_status=approval_status,
        audience=audience,
        evidence_refs=evidence_refs,
    )

    markdown_ar = "\n".join(md_lines_ar)
    markdown_en = "\n".join(md_lines_en)

    return {
        "markdown_ar": markdown_ar,
        "markdown_en": markdown_en,
        "markdown": md_full,
        "html": html,
        "manifest": {
            "artifact_type": "customer_room_dashboard",
            "approval_status": approval_status,
            "safe_to_send": False,
            "evidence_refs": evidence_refs,
            "audience": audience,
            "customer_handle": customer_handle,
            "section_count": len(_SECTIONS),
        },
        "sections": [
            {"key": k, "title_ar": t_ar, "title_en": t_en}
            for (k, t_ar, t_en, _kind) in _SECTIONS
        ],
    }
