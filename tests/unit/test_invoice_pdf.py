"""Unit tests for dealix/billing/invoice_pdf.py (T13b)."""

from __future__ import annotations

from dealix.billing.invoice_pdf import (
    InvoiceContext,
    build_context,
    render_invoice_html,
    render_invoice_pdf,
)


def _ctx(locale: str = "ar") -> InvoiceContext:
    return InvoiceContext(
        invoice_id="inv_test_001",
        issued_at="2026-05-12T10:00:00+03:00",
        seller_name="Dealix For AI Co.",
        seller_vat="310000000000003",
        buyer_name="Acme Real Estate",
        buyer_email="buyer@acme-re.sa",
        amount_subtotal=43391,  # halalas
        amount_vat=6509,
        amount_total=49900,
        currency="SAR",
        plan_label="Growth OS — monthly",
        locale=locale,
    )


def test_arabic_html_has_rtl_direction() -> None:
    html = render_invoice_html(_ctx("ar"))
    assert 'dir="rtl"' in html
    assert 'lang="ar"' in html
    assert "فاتورة ضريبية" in html
    assert "ضريبة القيمة المضافة" in html


def test_english_html_has_ltr_direction() -> None:
    html = render_invoice_html(_ctx("en"))
    assert 'dir="ltr"' in html
    assert 'lang="en"' in html
    assert "Tax invoice" in html
    assert "VAT" in html


def test_html_includes_invoice_id_and_amounts() -> None:
    html = render_invoice_html(_ctx("en"))
    assert "inv_test_001" in html
    # Total should appear (formatted via dealix.gcc.currency).
    assert "SAR" in html or "ر.س" in html


def test_html_includes_zatca_qr_block() -> None:
    html = render_invoice_html(_ctx("ar"))
    # QR div is always rendered (with TLV payload or fallback).
    assert 'class="qr"' in html


def test_pdf_render_returns_bytes_and_content_type() -> None:
    body, ct = render_invoice_pdf(_ctx("ar"))
    assert isinstance(body, bytes)
    assert ct in {"application/pdf", "text/html; charset=utf-8"}
    assert len(body) > 200


def test_build_context_back_calculates_vat_from_total() -> None:
    class _Row:
        id = "inv_test_002"
        amount_minor = 49900  # 499 SAR
        currency = "SAR"
        buyer_name = ""
        buyer_email = "buyer@example.sa"
        issued_at = "2026-05-12T10:00:00+03:00"
        plan_label = "Sprint"

    ctx = build_context(_Row(), locale="ar")
    # VAT inclusive of total: subtotal + vat = total (within rounding).
    assert ctx.amount_subtotal + ctx.amount_vat == ctx.amount_total
    # VAT must be 15 % of subtotal — i.e. ~13 % of total.
    assert abs(ctx.amount_vat - 6509) <= 2


def test_build_context_defaults_when_fields_missing() -> None:
    class _SparseRow:
        id = "inv_sparse"
        amount_minor = 9900

    ctx = build_context(_SparseRow(), locale="en")
    assert ctx.invoice_id == "inv_sparse"
    assert ctx.amount_total == 9900
    assert ctx.currency == "SAR"  # default
