"""Internal renderer for command outputs (Saudi Arabic primary)."""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.integration_upgrade import hide_internal_terms


def render_brief_response(brief: dict[str, Any]) -> str:
    """Format a brief for WhatsApp display (admin-only)."""
    text = (
        f"📊 ملخّص اليوم\n"
        f"{brief.get('brief_ar', '—')}\n\n"
        f"⚠️ قرارات معلّقة: {brief.get('pending_approvals_count', 0)}\n"
        f"⏰ تجاوزات SLA: {brief.get('sla_breached_count', 0)}\n"
    )
    return hide_internal_terms(text)
