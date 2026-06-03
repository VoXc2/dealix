"""Deterministic UTM URL builder."""

from __future__ import annotations

from urllib.parse import urlencode, urlparse, urlunparse


def build_utm_url(
    base_url: str,
    *,
    utm_source: str,
    utm_medium: str,
    utm_campaign: str,
    utm_content: str = "",
) -> str:
    parsed = urlparse(base_url.strip())
    if not parsed.scheme:
        parsed = urlparse(f"https://{base_url.strip()}")

    q = {
        "utm_source": utm_source.strip() or "dealix",
        "utm_medium": utm_medium.strip() or "social",
        "utm_campaign": utm_campaign.strip() or "founder_ops",
    }
    if utm_content.strip():
        q["utm_content"] = utm_content.strip()

    query = urlencode(q)
    path = parsed.path or "/"
    return urlunparse((parsed.scheme or "https", parsed.netloc, path, "", query, ""))
