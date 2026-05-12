"""
Crawl4AI — AI-friendly web extraction (markdown-clean, schema-aware).

Used by the RAG ingest pipeline when the customer drops a public URL.
Inert without `crawl4ai` installed; we fall back to httpx + a naive
HTML-stripper so the path keeps working in dev.

Reference: https://github.com/unclecode/crawl4ai
"""

from __future__ import annotations

import re
from dataclasses import dataclass

import httpx

from core.logging import get_logger

log = get_logger(__name__)


@dataclass
class CrawlResult:
    url: str
    markdown: str
    title: str | None
    success: bool
    error: str | None = None


_HTML_TAG = re.compile(r"<[^>]+>")
_WHITESPACE = re.compile(r"\s+")


async def fetch(url: str, *, max_chars: int = 60_000) -> CrawlResult:
    try:
        from crawl4ai import AsyncWebCrawler  # type: ignore
    except ImportError:
        return await _naive_fetch(url, max_chars=max_chars)
    try:
        async with AsyncWebCrawler(verbose=False) as crawler:
            result = await crawler.arun(url=url)
        return CrawlResult(
            url=url,
            markdown=(result.markdown or "")[:max_chars],
            title=getattr(result, "metadata", {}).get("title"),
            success=True,
        )
    except Exception as exc:
        log.exception("crawl4ai_failed", url=url)
        return CrawlResult(url=url, markdown="", title=None, success=False, error=str(exc))


async def _naive_fetch(url: str, *, max_chars: int) -> CrawlResult:
    try:
        async with httpx.AsyncClient(timeout=15, follow_redirects=True) as c:
            r = await c.get(url, headers={"User-Agent": "DealixCrawler/1.0"})
            r.raise_for_status()
            html = r.text
    except Exception as exc:
        return CrawlResult(url=url, markdown="", title=None, success=False, error=str(exc))
    # Strip tags + collapse whitespace. Naive but defensive.
    text = _WHITESPACE.sub(" ", _HTML_TAG.sub(" ", html)).strip()
    return CrawlResult(
        url=url,
        markdown=text[:max_chars],
        title=None,
        success=True,
    )
