"""v7 Phase 8 hardening — web scraping must remain platform-blocked.

Three perimeter assertions:

  1. ``agent_governance.FORBIDDEN_TOOLS`` contains ``SCRAPE_WEB``.
  2. ``evaluate_action`` returns ``permitted=False`` for ``SCRAPE_WEB``
     at every defined autonomy level.
  3. ``api/main.py`` router list never imports a module named
     ``crawler`` or ``scraper``.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

from auto_client_acquisition.agent_governance import (
    AutonomyLevel,
    FORBIDDEN_TOOLS,
    ToolCategory,
    evaluate_action,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
API_MAIN = REPO_ROOT / "api" / "main.py"


def test_scrape_web_in_forbidden_tools_set():
    assert ToolCategory.SCRAPE_WEB in FORBIDDEN_TOOLS


@pytest.mark.parametrize("level", list(AutonomyLevel))
def test_evaluate_action_blocks_scrape_web_at_every_level(level: AutonomyLevel):
    result = evaluate_action(
        agent_id="prospecting",
        tool=ToolCategory.SCRAPE_WEB,
        autonomy_level=level,
        allowed_tools=[ToolCategory.SCRAPE_WEB],  # even if explicitly allowed
    )
    assert result.permitted is False, (
        f"SCRAPE_WEB must be blocked at autonomy {level.value}; "
        f"got permitted=True (reason={result.reason!r})"
    )


def test_api_main_does_not_register_crawler_or_scraper_router():
    """``api/main.py`` must not import or include a router named
    ``crawler`` or ``scraper`` — those names imply unconsented scraping
    surfaces and have no safe place in the v7 platform."""
    assert API_MAIN.exists(), f"api/main.py missing at {API_MAIN}"
    text = API_MAIN.read_text(encoding="utf-8")

    # Match either "crawler," / "scraper," in the imported-routers tuple
    # or a "from api.routers import crawler" / ".include_router(crawler"
    # form. We're conservative — any of the patterns below is a fail.
    forbidden_patterns = [
        re.compile(r"^\s*crawler\s*,?\s*$", re.MULTILINE),
        re.compile(r"^\s*scraper\s*,?\s*$", re.MULTILINE),
        re.compile(r"\bimport\s+crawler\b"),
        re.compile(r"\bimport\s+scraper\b"),
        re.compile(r"include_router\(\s*crawler\."),
        re.compile(r"include_router\(\s*scraper\."),
    ]
    hits = [p.pattern for p in forbidden_patterns if p.search(text)]
    assert not hits, (
        "api/main.py must not register a crawler or scraper router. "
        f"Matched patterns: {hits}"
    )
