"""
Tiny Jinja2 renderer for the transactional templates in
`dealix/templates/{ar,en}/*.html.j2`. Auto-injects Hijri + Gregorian
dates so every template can reference them as `${gregorian_date}` and
`${hijri_date}` without per-template plumbing.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from core.logging import get_logger

log = get_logger(__name__)


def _hijri_str(d: datetime) -> str:
    """Best-effort Hijri date string using ummalqura when available."""
    try:
        from ummalqura.hijri_date import HijriDate  # type: ignore

        h = HijriDate(d.year, d.month, d.day, gr=True)
        return f"{int(h.day)}/{int(h.month)}/{int(h.year)}"
    except Exception:
        # Fall back to the Gregorian date so the template never breaks.
        return d.strftime("%Y-%m-%d")


def render_template(name: str, *, locale: str = "ar", ctx: dict[str, Any] | None = None) -> str:
    """Render `name` (e.g. "invite") to a complete HTML string.

    Returns an empty string when neither the locale-specific nor the
    English-fallback template exists. Caller decides how to react.
    """
    from dealix.templates import template_path

    try:
        path = template_path(name, locale)
    except FileNotFoundError:
        log.warning("template_missing", name=name, locale=locale)
        return ""

    try:
        from jinja2 import Environment, FileSystemLoader, select_autoescape
    except ImportError:
        # Jinja2 is in transitive deps; fall back to a string read
        # so we never silently corrupt an email if Jinja2 is absent.
        return path.read_text(encoding="utf-8")

    env = Environment(
        loader=FileSystemLoader(str(path.parent)),
        autoescape=select_autoescape(["html", "xml", "j2"]),
        keep_trailing_newline=True,
    )
    now = datetime.now(timezone.utc)
    full_ctx: dict[str, Any] = {
        "gregorian_date": now.strftime("%Y-%m-%d"),
        "hijri_date": _hijri_str(now),
        "issued_at_ar": now.strftime("%Y/%m/%d"),
        "issued_at_en": now.strftime("%b %d, %Y"),
        "issued_at_hijri": _hijri_str(now),
        "unsubscribe_url": "https://dealix.me/unsubscribe",
        **(ctx or {}),
    }
    template = env.get_template(path.name)
    return template.render(**full_ctx)
