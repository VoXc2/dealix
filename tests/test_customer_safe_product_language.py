"""Phase 1 — Customer-safe language enforcement.

Asserts that customer-facing pages + customer-facing API payloads
NEVER expose internal terminology (v10/v11/v12/v13/v14/beast/
growth_beast/revops/etc.).

Documentation files in docs/ are EXEMPT (engineers read those).
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest


# Customer-facing pages — checked for internal terms.
# `workflow.html`, `dealix-beast-power.html`, `ai-team.html` intentionally
# display endpoint paths as a feature demonstrating engineering depth
# (technical-prospect-facing pages), so excluded from this strict check.
CUSTOMER_FACING_HTML = [
    "landing/customer-portal.html",
    "landing/executive-command-center.html",
    "landing/launchpad.html",
    "landing/diagnostic.html",
    "landing/diagnostic-real-estate.html",
    "landing/start.html",
    "landing/pricing.html",
    "landing/compare.html",
    "landing/proof.html",
    "landing/index.html",
]

# Forbidden internal terms in customer-facing surfaces
# (whole-word matches; case-insensitive where appropriate)
_FORBIDDEN_PATTERNS = [
    re.compile(r"\bv11\b", re.IGNORECASE),
    re.compile(r"\bv12(?:\.5)?\b", re.IGNORECASE),
    re.compile(r"\bv13\b", re.IGNORECASE),
    re.compile(r"\bv14\b", re.IGNORECASE),
    re.compile(r"\bgrowth_beast\b", re.IGNORECASE),
    re.compile(r"\brevops\b", re.IGNORECASE),
    re.compile(r"\bcompliance_os_v12\b", re.IGNORECASE),
    re.compile(r"\bauto_client_acquisition\b", re.IGNORECASE),
    re.compile(r"\bcustomer_inbox_v10\b", re.IGNORECASE),
    re.compile(r"\bstacktrace\b", re.IGNORECASE),
    re.compile(r"\bpytest\b", re.IGNORECASE),
    re.compile(r"\binternal_error\b", re.IGNORECASE),
]


def _strip_comments_and_meta(html: str) -> str:
    """Strip HTML comments + script/style sections to focus on visible text.

    Internal version markers in <meta>/<script> tags don't reach customers."""
    # Remove HTML comments
    html = re.sub(r"<!--.*?-->", "", html, flags=re.DOTALL)
    # Remove <script>...</script> blocks (engineers' code, not customer-visible)
    html = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)
    # Remove <style>...</style> blocks (CSS, not customer-visible)
    html = re.sub(r"<style[^>]*>.*?</style>", "", html, flags=re.DOTALL | re.IGNORECASE)
    return html


@pytest.mark.parametrize("page", CUSTOMER_FACING_HTML)
def test_no_internal_terms_in_customer_html(page: str) -> None:
    path = Path(page)
    if not path.exists():
        pytest.skip(f"page not found: {page}")
    html = path.read_text(encoding="utf-8")
    visible = _strip_comments_and_meta(html)
    for pattern in _FORBIDDEN_PATTERNS:
        match = pattern.search(visible)
        assert match is None, (
            f"customer-facing page {page} leaks internal term: "
            f"{pattern.pattern!r} (found: {match.group() if match else ''})"
        )


def test_customer_portal_api_no_internal_leakage() -> None:
    """Re-asserts the constitutional gate via API payload check.

    Uses word-boundary patterns so benign substrings (e.g. `customer_safe_labels`)
    don't match the strict-leak terms.
    """
    import asyncio
    from httpx import ASGITransport, AsyncClient

    async def go():
        from api.main import app
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as c:
            r = await c.get("/api/v1/customer-portal/lang-check-test")
        return r.json()

    body = asyncio.run(go())
    serialized = json.dumps(body, ensure_ascii=False).lower()
    for pattern in [
        r"\bv11\b", r"\bv12\.5\b", r"\bstacktrace\b", r"\bpytest\b",
        r"\binternal_error\b", r"\bgrowth_beast\b", r"\brevops\b",
        r"\bcompliance_os_v12\b", r"\bauto_client_acquisition\b",
    ]:
        assert not re.search(pattern, serialized), (
            f"customer-portal API leaks: {pattern}"
        )


def test_executive_command_center_api_no_internal_leakage() -> None:
    import asyncio
    from httpx import ASGITransport, AsyncClient

    async def go():
        from api.main import app
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as c:
            r = await c.get("/api/v1/executive-command-center/lang-check-test")
        return r.json()

    body = asyncio.run(go())
    serialized = json.dumps(body, ensure_ascii=False).lower()
    for pattern in [
        r"\bv11\b", r"\bv12\.5\b", r"\bstacktrace\b", r"\bpytest\b",
        r"\binternal_error\b", r"\bgrowth_beast\b",
    ]:
        assert not re.search(pattern, serialized), f"ECC API leaks: {pattern}"


def test_4_external_names_documented() -> None:
    """Phase 1 doc must cite the 4 customer-facing names."""
    doc = Path("docs/DEALIX_PRODUCT_SIMPLIFICATION_MAP.md").read_text(encoding="utf-8")
    assert "Dealix Radar" in doc
    assert "Dealix AI Team" in doc
    assert "Dealix Portal" in doc
    assert "Dealix Proof" in doc
