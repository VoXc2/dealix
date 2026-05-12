"""
Public marketing router (T13e).

    GET /api/v1/marketing/brochure/{vertical_id}.pdf
        Renders a single-page sales brochure for the requested
        vertical. PDF when weasyprint is installed, HTML otherwise.
        Public read — the founder hands the URL out at events.

    GET /api/v1/marketing/brochure/{vertical_id}.html
        Same content, always served as HTML — useful for preview /
        email-embed.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query, Response

from core.logging import get_logger
from dealix.marketing.brochure_pdf import build_context, render_brochure_pdf, render_brochure_html

router = APIRouter(prefix="/api/v1/marketing", tags=["marketing"])
log = get_logger(__name__)


def _render(vertical_id: str, locale: str, force_html: bool = False) -> Response:
    ctx = build_context(vertical_id, locale=locale)
    if ctx is None:
        raise HTTPException(404, "vertical_not_found")
    if force_html:
        body = render_brochure_html(ctx).encode("utf-8")
        ct = "text/html; charset=utf-8"
    else:
        body, ct = render_brochure_pdf(ctx)
    disposition = "inline" if ct.startswith("text/") else "inline"
    return Response(
        content=body,
        media_type=ct,
        headers={
            "Content-Disposition": f'{disposition}; filename="dealix-{vertical_id}.pdf"',
            "Cache-Control": "public, max-age=300",
        },
    )


@router.get("/brochure/{vertical_id}.pdf")
async def brochure_pdf(
    vertical_id: str, locale: str = Query(default="ar")
) -> Any:
    return _render(vertical_id, locale)


@router.get("/brochure/{vertical_id}.html")
async def brochure_html(
    vertical_id: str, locale: str = Query(default="ar")
) -> Any:
    return _render(vertical_id, locale, force_html=True)
