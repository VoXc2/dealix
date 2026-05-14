"""Doctrine: No scraping/crawling/harvesting engine in auto_client_acquisition/.

This is a structural test: walk the tree, and if any module file name suggests
scraping behaviour AND the file calls `requests.get(` against a non-allowlisted
domain, fail loudly.
"""
from __future__ import annotations

import os
import re
from pathlib import Path

import pytest

from auto_client_acquisition.governance_os.runtime_decision import (
    GovernanceDecision,
    decide,
)

ALLOWLIST = [
    "api.openai.com",
    "api.anthropic.com",
    "graph.facebook.com",
    "graph.whatsapp.com",
    "api.hubspot.com",
    "login.salesforce.com",
    "www.googleapis.com",
    "api.notion.com",
    "api.zoho.com",
    "sandbox.payment.com",
    "api.moyasar.com",
]

_SUSPICIOUS_NAMES = ("scraper", "crawler", "harvest")


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def test_no_scraper_modules_in_auto_client_acquisition() -> None:
    """Walk auto_client_acquisition/ and fail if scrapy-style modules exist.

    A file is offending if its name matches *scraper*/*crawler*/*harvest* AND
    its contents call `requests.get(` with a URL whose host is not on the
    allowlist.
    """
    root = _repo_root() / "auto_client_acquisition"
    offenders: list[str] = []

    for dirpath, _dirnames, filenames in os.walk(root):
        for fname in filenames:
            if not fname.endswith(".py"):
                continue
            lower = fname.lower()
            if not any(s in lower for s in _SUSPICIOUS_NAMES):
                continue

            path = Path(dirpath) / fname
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue

            if "requests.get(" not in text:
                continue

            # Pull URL-like substrings and check each one against the allowlist.
            urls = re.findall(r"https?://([A-Za-z0-9.\-]+)", text)
            non_allowed = [u for u in urls if u not in ALLOWLIST]
            if non_allowed:
                offenders.append(f"{path} -> {non_allowed}")

    assert not offenders, (
        "Forbidden scraping-style modules found in auto_client_acquisition/:\n"
        + "\n".join(offenders)
    )


def test_scraping_action_blocked() -> None:
    """Runtime decide() must BLOCK any action that declares itself as scrape."""
    result = decide(action="scrape_web", context={})
    assert result.decision == GovernanceDecision.BLOCK
