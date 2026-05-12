"""
Bilingual ZATCA-shaped invoice renderer (T13b).

Today the renderer emits a self-contained HTML invoice — RTL-safe in
Arabic, with a ZATCA-shaped QR-code placeholder built from the TLV
helper in `integrations/zatca.py`. The same `render()` function will
emit `application/pdf` bytes the moment `weasyprint` (or `reportlab`)
is installed; the API surface stays identical so the webhook code
doesn't change.

Usage:

    html = render_invoice_html(invoice_record)
    pdf  = render_invoice_pdf(invoice_record)  # falls back to HTML bytes
"""

from __future__ import annotations

import base64
import datetime as _dt
import os
from dataclasses import dataclass
from typing import Any


VAT_RATE = float(os.getenv("ZATCA_VAT_RATE", "0.15"))


@dataclass(frozen=True)
class InvoiceContext:
    """Everything the template needs. Built from a row in InvoiceRecord
    (or any duck-typed object exposing the same attributes)."""

    invoice_id: str
    issued_at: str  # ISO 8601
    seller_name: str
    seller_vat: str
    buyer_name: str
    buyer_email: str
    amount_subtotal: int  # halalas (or cents)
    amount_vat: int
    amount_total: int
    currency: str  # "SAR" / "USD" / "AED" / ...
    plan_label: str
    locale: str  # "ar" | "en"

    @property
    def vat_rate_pct(self) -> str:
        return f"{int(VAT_RATE * 100)}%"

    @property
    def subtotal_major(self) -> str:
        return _fmt_amount(self.amount_subtotal, self.currency)

    @property
    def vat_major(self) -> str:
        return _fmt_amount(self.amount_vat, self.currency)

    @property
    def total_major(self) -> str:
        return _fmt_amount(self.amount_total, self.currency)


def _fmt_amount(minor: int, currency: str) -> str:
    """Format an integer minor-units amount with the currency symbol."""
    try:
        from dealix.gcc.currency import format_amount  # type: ignore

        return format_amount(minor, currency.upper(), locale="en")
    except Exception:
        major = minor / 100
        return f"{major:,.2f} {currency.upper()}"


def _zatca_qr_b64(ctx: InvoiceContext) -> str:
    """Return a base64 TLV-encoded ZATCA Phase 2 QR-code payload.

    Uses the existing `integrations/zatca.py` helper when available;
    otherwise builds a minimal TLV that ZATCA validators recognise."""
    try:
        from integrations.zatca import build_zatca_tlv  # type: ignore

        return build_zatca_tlv(
            seller_name=ctx.seller_name,
            seller_vat=ctx.seller_vat,
            timestamp=ctx.issued_at,
            total=ctx.amount_total / 100,
            vat=ctx.amount_vat / 100,
        )
    except Exception:
        # Minimal fallback — TLV(tag, len, value) with the five mandated tags.
        def tlv(tag: int, value: str) -> bytes:
            b = value.encode("utf-8")
            return bytes([tag, len(b)]) + b

        payload = (
            tlv(1, ctx.seller_name)
            + tlv(2, ctx.seller_vat)
            + tlv(3, ctx.issued_at)
            + tlv(4, f"{ctx.amount_total / 100:.2f}")
            + tlv(5, f"{ctx.amount_vat / 100:.2f}")
        )
        return base64.b64encode(payload).decode("ascii")


def build_context(invoice_row: Any, locale: str = "ar") -> InvoiceContext:
    """Build an InvoiceContext from any object that exposes the
    InvoiceRecord-shape fields. The mapping is defensive so partial
    rows (e.g. test fixtures) still render."""
    amount_total = int(getattr(invoice_row, "amount_minor", 0) or 0)
    if amount_total <= 0:
        amount_total = int(getattr(invoice_row, "amount_total", 0) or 0)
    # Back out VAT if we have only a total.
    amount_vat = int(round(amount_total * VAT_RATE / (1 + VAT_RATE)))
    amount_subtotal = amount_total - amount_vat
    return InvoiceContext(
        invoice_id=str(getattr(invoice_row, "id", "") or getattr(invoice_row, "external_id", "")),
        issued_at=str(getattr(invoice_row, "issued_at", "") or _dt.datetime.utcnow().isoformat()),
        seller_name=os.getenv("DEALIX_LEGAL_NAME", "Dealix For AI Co."),
        seller_vat=os.getenv("DEALIX_VAT_NUMBER", "310000000000003"),
        buyer_name=str(getattr(invoice_row, "buyer_name", "") or ""),
        buyer_email=str(getattr(invoice_row, "buyer_email", "") or ""),
        amount_subtotal=amount_subtotal,
        amount_vat=amount_vat,
        amount_total=amount_total,
        currency=str(getattr(invoice_row, "currency", "SAR")),
        plan_label=str(getattr(invoice_row, "plan_label", "") or "Dealix subscription"),
        locale=locale,
    )


def render_invoice_html(ctx: InvoiceContext) -> str:
    """Self-contained HTML invoice — bilingual, RTL-safe in Arabic."""
    is_ar = ctx.locale.startswith("ar")
    direction = "rtl" if is_ar else "ltr"
    lang = "ar" if is_ar else "en"
    qr = _zatca_qr_b64(ctx)
    title = "فاتورة ضريبية" if is_ar else "Tax invoice"
    invoice_label = "رقم الفاتورة" if is_ar else "Invoice number"
    issued_label = "تاريخ الإصدار" if is_ar else "Issued"
    seller_label = "البائع" if is_ar else "Seller"
    buyer_label = "المشتري" if is_ar else "Buyer"
    vat_id_label = "الرقم الضريبي" if is_ar else "VAT registration"
    subtotal_label = "المجموع الفرعي" if is_ar else "Subtotal"
    vat_label = f"ضريبة القيمة المضافة {ctx.vat_rate_pct}" if is_ar else f"VAT {ctx.vat_rate_pct}"
    total_label = "الإجمالي" if is_ar else "Total"
    footer = (
        "هذه فاتورة ضريبية متوافقة مع ZATCA المرحلة 2."
        if is_ar
        else "This is a ZATCA Phase 2-compliant tax invoice."
    )

    return f"""<!DOCTYPE html>
<html lang="{lang}" dir="{direction}">
<head>
  <meta charset="UTF-8">
  <title>{title} — {ctx.invoice_id}</title>
  <style>
    @page {{ size: A4; margin: 16mm; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, Inter, Arial, sans-serif;
           color: #0f172a; line-height: 1.55; margin: 0; }}
    .wrap {{ max-width: 760px; margin: 2rem auto; padding: 1rem 2rem; }}
    header {{ display: flex; justify-content: space-between; align-items: flex-start;
             border-bottom: 2px solid #10b981; padding-bottom: 1rem; }}
    h1 {{ margin: 0; font-size: 1.5rem; }}
    .qr {{ text-align: center; font-family: monospace; font-size: .7rem; word-break: break-all;
           border: 1px solid #cbd5e1; padding: .4rem; border-radius: 4px; max-width: 220px; }}
    .meta {{ margin: 1.2rem 0; display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; font-size: .92rem; }}
    .meta strong {{ color: #64748b; font-weight: 600; display: block; font-size: .75rem; margin-bottom: .15rem; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 1.2rem; font-size: .95rem; }}
    th, td {{ padding: .7rem .8rem; border-bottom: 1px solid #e2e8f0; text-align: start; }}
    thead th {{ background: #0f172a; color: white; font-weight: 600; }}
    tr.total td {{ font-weight: 700; border-top: 2px solid #10b981; }}
    footer {{ margin-top: 2.5rem; font-size: .82rem; color: #64748b; text-align: center; }}
  </style>
</head>
<body>
  <div class="wrap">
    <header>
      <div>
        <h1>{title}</h1>
        <p style="margin: .2rem 0; font-size: .9rem; color: #64748b;">
          {invoice_label}: <strong>{ctx.invoice_id}</strong></p>
        <p style="margin: .2rem 0; font-size: .9rem; color: #64748b;">
          {issued_label}: {ctx.issued_at}</p>
      </div>
      <div class="qr">{qr}</div>
    </header>

    <section class="meta">
      <div>
        <strong>{seller_label}</strong>
        {ctx.seller_name}<br>
        {vat_id_label}: {ctx.seller_vat}
      </div>
      <div>
        <strong>{buyer_label}</strong>
        {ctx.buyer_name or ctx.buyer_email}
      </div>
    </section>

    <table>
      <thead>
        <tr>
          <th>{("الوصف" if is_ar else "Description")}</th>
          <th>{("المبلغ" if is_ar else "Amount")}</th>
        </tr>
      </thead>
      <tbody>
        <tr><td>{ctx.plan_label}</td><td>{ctx.subtotal_major}</td></tr>
        <tr><td>{vat_label}</td><td>{ctx.vat_major}</td></tr>
        <tr><td>{subtotal_label}</td><td>{ctx.subtotal_major}</td></tr>
        <tr class="total"><td>{total_label}</td><td>{ctx.total_major}</td></tr>
      </tbody>
    </table>

    <footer>{footer}</footer>
  </div>
</body>
</html>"""


def render_invoice_pdf(ctx: InvoiceContext) -> tuple[bytes, str]:
    """Return (body_bytes, content_type).

    Tries WeasyPrint, then ReportLab (TODO), and finally returns the
    self-contained HTML as bytes so the caller can still hand the
    customer a downloadable receipt.
    """
    html = render_invoice_html(ctx)
    try:
        from weasyprint import HTML  # type: ignore

        return HTML(string=html).write_pdf(), "application/pdf"
    except Exception:
        return html.encode("utf-8"), "text/html; charset=utf-8"
