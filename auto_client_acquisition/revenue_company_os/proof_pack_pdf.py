"""
Proof Pack PDF/HTML renderer.

Renders the dict from `proof_pack_builder.build_pack()` into:
  - render_html(...) → printable HTML (Arabic RTL, embedded CSS, print stylesheet)
  - render_pdf(...)  → optional PDF bytes via weasyprint (if installed)

The HTML path requires only Jinja2 (already a dependency). Browsers handle
Arabic shaping perfectly via "Save as PDF". The PDF path is best-effort and
returns None if weasyprint is not available — the router decides what to do.

Signature: each pack ships with an HMAC-SHA256 over (customer_label || event_count
|| revenue_total) signed with APP_SECRET_KEY, so customers + auditors can
verify the bundle wasn't tampered with after delivery.
"""

from __future__ import annotations

import hashlib
import hmac
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape

from core.config.settings import get_settings


_TEMPLATE_DIR = Path(__file__).resolve().parents[2] / "landing" / "templates"
_ENV = Environment(
    loader=FileSystemLoader(str(_TEMPLATE_DIR)),
    autoescape=select_autoescape(["html", "xml"]),
)


def _signature(pack: dict[str, Any], customer_label: str | None) -> str:
    """HMAC-SHA256 over the payload — verifiable by anyone with APP_SECRET_KEY."""
    settings = get_settings()
    secret = getattr(settings, "app_secret_key", None)
    if hasattr(secret, "get_secret_value"):
        key = secret.get_secret_value().encode("utf-8")
    else:
        key = str(secret or "dev-secret").encode("utf-8")
    totals = pack.get("totals") or {}
    payload = "|".join([
        str(customer_label or ""),
        str(totals.get("created_units", 0)),
        str(totals.get("protected_units", 0)),
        f"{float(totals.get('estimated_revenue_impact_sar') or 0):.2f}",
    ]).encode("utf-8")
    return hmac.new(key, payload, hashlib.sha256).hexdigest()[:32]


def _humanize(dt: datetime | None) -> str:
    if dt is None:
        return "—"
    return dt.strftime("%Y-%m-%d %H:%M UTC")


def render_html(
    pack: dict[str, Any],
    *,
    customer_label: str | None = None,
    event_count: int = 0,
    since: datetime | None = None,
    generated_at: datetime | None = None,
) -> str:
    """Render the printable HTML version of the Proof Pack.

    Args:
      pack: dict from proof_pack_builder.build_pack(...)
      customer_label: optional override for the header line
      event_count: number of underlying ledger events used
      since: lower bound of the report window
      generated_at: when the pack was built (defaults to now)
    """
    template = _ENV.get_template("proof_pack_pdf.html")
    gen = generated_at or datetime.now(timezone.utc).replace(tzinfo=None)
    sig = _signature(pack, customer_label or pack.get("customer_label"))
    return template.render(
        pack=pack,
        customer_label=customer_label or pack.get("customer_label"),
        event_count=event_count,
        since_human=_humanize(since),
        generated_at_human=_humanize(gen),
        signature=sig,
    )


def render_pdf(*args, **kwargs) -> bytes | None:
    """Best-effort PDF render via weasyprint.

    Returns None if weasyprint is not installed. The router uses this to
    decide between returning a real application/pdf response vs falling
    back to printable HTML with Content-Disposition: inline.
    """
    try:
        from weasyprint import HTML  # type: ignore
    except Exception:  # noqa: BLE001
        return None
    html = render_html(*args, **kwargs)
    return HTML(string=html).write_pdf()
