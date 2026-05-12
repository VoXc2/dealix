"""
Vertical-specific sales brochure renderer (T13e).

A sales rep walking into a coffee meeting needs a single-page leave-
behind that:
 - Names the vertical.
 - Lists the agents the customer gets out-of-the-box.
 - Shows SAR pricing tiers.
 - Carries the QR-code that points back to a vertical-tagged signup.
 - Tells the truth (only agents with a registered handler appear in the
   "today" column; roadmap items go below the fold).

Uses the same HTML→PDF strategy as `dealix/billing/invoice_pdf.py`:
emits valid self-contained HTML; renders to PDF when weasyprint is
installed; falls back to HTML otherwise.
"""

from __future__ import annotations

import base64
from dataclasses import dataclass
from typing import Iterable

from dealix.agents.skills import handlers_data, handlers_llm  # noqa: F401 — register
from dealix.agents.skills.handlers import registered_ids
from dealix.verticals import Vertical, by_id


@dataclass(frozen=True)
class BrochureContext:
    vertical: Vertical
    sar_pricing: dict[str, int]  # {plan_id: sar_per_seat_per_month}
    signup_url: str
    locale: str  # "ar" | "en"

    @property
    def live_agents(self) -> list[str]:
        reg = set(registered_ids())
        return [a for a in self.vertical.agents if a in reg]

    @property
    def roadmap_agents(self) -> list[str]:
        reg = set(registered_ids())
        return [a for a in self.vertical.agents if a not in reg]


def build_context(
    vertical_id: str,
    *,
    sar_pricing: dict[str, int] | None = None,
    signup_url: str | None = None,
    locale: str = "ar",
) -> BrochureContext | None:
    v = by_id(vertical_id)
    if v is None:
        return None
    return BrochureContext(
        vertical=v,
        sar_pricing=sar_pricing
        or {"pilot": 199, "growth": 499, "scale": 999, "enterprise": 1999},
        signup_url=signup_url
        or f"https://dealix.me/onboarding?vertical={vertical_id}",
        locale=locale,
    )


def _qr_data_uri(payload: str) -> str:
    """Return a tiny QR-ish placeholder as a base64 data URI.

    Real QR rendering needs `qrcode` (optional). When absent we emit a
    SVG containing the URL string framed so the brochure still looks
    intentional; the founder reaches the same URL by clicking.
    """
    try:
        import qrcode  # type: ignore

        from io import BytesIO

        img = qrcode.make(payload)
        buf = BytesIO()
        img.save(buf, format="PNG")
        b64 = base64.b64encode(buf.getvalue()).decode("ascii")
        return f"data:image/png;base64,{b64}"
    except Exception:
        svg = (
            '<svg xmlns="http://www.w3.org/2000/svg" width="140" height="140" '
            'viewBox="0 0 140 140">'
            '<rect x="0" y="0" width="140" height="140" fill="white" stroke="#0f172a" stroke-width="2"/>'
            f'<text x="50%" y="50%" dy="6" text-anchor="middle" '
            'font-family="monospace" font-size="8" fill="#0f172a">'
            f'{payload[:32]}</text></svg>'
        )
        return "data:image/svg+xml;utf8," + svg.replace("#", "%23").replace('"', "'")


def _li(items: Iterable[str]) -> str:
    return "".join(f"<li>{x}</li>" for x in items)


def render_brochure_html(ctx: BrochureContext) -> str:
    v = ctx.vertical
    is_ar = ctx.locale.startswith("ar")
    direction = "rtl" if is_ar else "ltr"
    lang = "ar" if is_ar else "en"
    label = v.label_ar if is_ar else v.label_en
    description = v.description_ar if is_ar else v.description_en
    qr = _qr_data_uri(ctx.signup_url)

    title = f"{label} — Dealix"
    plan_title = "خطط الاشتراك (SAR / مقعد / شهر)" if is_ar else "Plans (SAR / seat / month)"
    agents_title = "الوكلاء الجاهزون اليوم" if is_ar else "Agents available today"
    roadmap_title = "خارطة الطريق" if is_ar else "Roadmap"
    workflows_title = "المسارات الجاهزة" if is_ar else "Workflows out-of-the-box"
    cta_title = "ابدأ اليوم" if is_ar else "Start today"
    cta_copy = (
        "اشترك في 14 يوم — بدون بطاقة. ندخل بياناتك ونرسل لك Proof Pack جاهز يوم 7."
        if is_ar
        else "14-day no-card pilot. We onboard your data and ship a Proof Pack on day 7."
    )

    plans_html = "".join(
        f'<div class="plan"><h3>{name.title()}</h3>'
        f'<p class="price">SAR {price:,}</p></div>'
        for name, price in ctx.sar_pricing.items()
    )

    return f"""<!DOCTYPE html>
<html lang="{lang}" dir="{direction}">
<head>
  <meta charset="UTF-8">
  <title>{title}</title>
  <style>
    @page {{ size: A4; margin: 14mm; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, Inter, Arial, sans-serif;
           color: #0f172a; line-height: 1.55; margin: 0; }}
    .wrap {{ max-width: 760px; margin: 1.5rem auto; padding: 1rem 2rem; }}
    header {{ display: flex; justify-content: space-between; align-items: flex-start;
             border-bottom: 3px solid #10b981; padding-bottom: 1rem; }}
    h1 {{ margin: 0 0 .3rem; font-size: 1.7rem; color: #047857; }}
    h2 {{ font-size: 1.05rem; margin: 1.4rem 0 .4rem; color: #0f172a; }}
    h3 {{ margin: 0 0 .2rem; font-size: .95rem; color: #0f172a; }}
    .pitch {{ color: #475569; font-size: .96rem; margin: .3rem 0 0; }}
    .qr {{ width: 120px; height: 120px; }}
    .plans {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: .6rem;
              margin-top: .5rem; }}
    .plan {{ background: #ecfdf5; border: 1px solid #a7f3d0; border-radius: 10px;
            padding: .6rem .7rem; text-align: center; }}
    .plan .price {{ font-weight: 700; color: #047857; margin: .2rem 0 0; }}
    .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }}
    ul {{ padding-{('right' if is_ar else 'left')}: 1.1rem; margin: .25rem 0; }}
    li {{ font-size: .9rem; margin-bottom: .15rem; }}
    .cta {{ margin-top: 1.5rem; background: #0f172a; color: white; padding: 1rem 1.2rem;
           border-radius: 12px; text-align: center; }}
    .cta strong {{ color: #34d399; }}
    .cta a {{ color: #34d399; text-decoration: none; }}
    footer {{ margin-top: 1.5rem; font-size: .78rem; color: #64748b; text-align: center; }}
  </style>
</head>
<body>
  <div class="wrap">
    <header>
      <div>
        <h1>{label}</h1>
        <p class="pitch">{description}</p>
      </div>
      <img class="qr" src="{qr}" alt="signup QR" />
    </header>

    <h2>{plan_title}</h2>
    <div class="plans">{plans_html}</div>

    <div class="grid">
      <div>
        <h2>{agents_title}</h2>
        <ul>{_li(ctx.live_agents) or '<li>—</li>'}</ul>
      </div>
      <div>
        <h2>{workflows_title}</h2>
        <ul>{_li(v.workflows) or '<li>—</li>'}</ul>
      </div>
    </div>

    {('<h2>' + roadmap_title + '</h2><ul>' + _li(ctx.roadmap_agents) + '</ul>') if ctx.roadmap_agents else ''}

    <div class="cta">
      <strong>{cta_title}</strong> · {cta_copy}<br>
      <a href="{ctx.signup_url}">{ctx.signup_url}</a>
    </div>

    <footer>
      Dealix For AI Co. — Riyadh · sales@ai-company.sa · status.dealix.me
    </footer>
  </div>
</body>
</html>"""


def render_brochure_pdf(ctx: BrochureContext) -> tuple[bytes, str]:
    """Returns (body_bytes, content_type) — PDF when weasyprint is
    installed, else HTML."""
    html = render_brochure_html(ctx)
    try:
        from weasyprint import HTML  # type: ignore

        return HTML(string=html).write_pdf(), "application/pdf"
    except Exception:
        return html.encode("utf-8"), "text/html; charset=utf-8"
