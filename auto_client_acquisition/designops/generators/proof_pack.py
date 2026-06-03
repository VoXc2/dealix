"""Proof Pack generator.

Wraps ``proof_snippet_engine.render_pack`` inside design-system HTML +
bilingual markdown. Audience defaults to ``internal_only`` unless every
event carries ``consent_for_publication=True`` AND no event was blocked.
"""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.designops.generators.html_renderer import (
    render_artifact_html,
)
from auto_client_acquisition.designops.generators.markdown_renderer import (
    render_artifact_markdown,
)


def generate_proof_pack(
    customer_handle: str,
    events: list[dict[str, Any]],
    period_label: str = "",
) -> dict[str, Any]:
    """Compose a bilingual Proof Pack artifact.

    Returns a dict with ``markdown_ar``, ``markdown_en``, ``html``,
    ``manifest``. The manifest tags ``safe_to_send=False`` and
    ``approval_status=approval_required`` regardless of consent.
    """
    pack: dict[str, Any] = {}
    try:
        from auto_client_acquisition.self_growth_os.proof_snippet_engine import (
            render_pack,
        )

        pack = render_pack(
            events=list(events or []),
            customer_handle=customer_handle,
            period_label=period_label,
        )
    except Exception:
        pack = {
            "decision": "blocked",
            "audience": "invalid",
            "markdown_ar": "",
            "markdown_en": "",
            "events": [],
            "notes": "proof_snippet_engine not available",
        }

    markdown_ar = pack.get("markdown_ar") or ""
    markdown_en = pack.get("markdown_en") or ""

    # Pack-level audience decision per spec:
    #   internal_only unless ALL events consented AND no event blocked.
    decision = pack.get("decision", "blocked")
    pack_audience = pack.get("audience", "internal_only")
    has_blocked = decision == "blocked"
    all_consented = bool(events) and all(
        bool(e.get("consent_for_publication")) for e in events
    )
    if has_blocked or not all_consented:
        audience = "internal_only"
    else:
        audience = pack_audience or "public_with_consent"

    title_ar = f"حزمة الأدلّة — {customer_handle}"
    title_en = f"Proof Pack — {customer_handle}"
    if period_label:
        title_ar += f" ({period_label})"
        title_en += f" ({period_label})"

    n_events = len(pack.get("events") or events or [])
    sections_ar = [
        {
            "title": "السياق",
            "body": (
                f"العميل: {customer_handle}\nالفترة: {period_label or '—'}\n"
                f"عدد الأحداث: {n_events}"
            ),
        },
        {"title": "حالة المراجعة", "body": pack.get("notes") or "—"},
        {"title": "الوثيقة", "body": markdown_ar or "لا بيانات بعد / no data yet"},
    ]
    sections_en = [
        {
            "title": "Context",
            "body": (
                f"Customer: {customer_handle}\nPeriod: {period_label or '-'}\n"
                f"Event count: {n_events}"
            ),
        },
        {"title": "Review status", "body": pack.get("notes") or "-"},
        {"title": "Document", "body": markdown_en or "no data yet"},
    ]

    approval_status = "approval_required"
    evidence_refs = [
        f"proof_snippet_engine.render_pack(customer={customer_handle!r})",
        f"events={n_events}",
        f"decision={decision}",
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

    return {
        "markdown_ar": markdown_ar,
        "markdown_en": markdown_en,
        "markdown": md_full,
        "html": html,
        "pack": pack,
        "manifest": {
            "artifact_type": "proof_pack",
            "approval_status": approval_status,
            "safe_to_send": False,
            "evidence_refs": evidence_refs,
            "audience": audience,
            "customer_handle": customer_handle,
            "period_label": period_label,
            "event_count": n_events,
        },
    }
