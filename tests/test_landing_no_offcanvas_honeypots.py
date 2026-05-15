"""Guardrail: hidden honeypot fields must not create horizontal overflow.

Why this test exists:
- A prior regression used off-canvas honeypots (`left:-9999px`), which
  inflated `documentElement.scrollWidth` and broke Playwright Tier-1 smoke.
- Hidden anti-spam fields are still allowed, but must use clip-based
  visually-hidden styles that do not expand layout width.
"""
from __future__ import annotations

import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
LANDING_DIR = REPO_ROOT / "landing"

FORBIDDEN_OFFCANVAS = (
    re.compile(r"left\s*:\s*-9999px", re.IGNORECASE),
    re.compile(r"top\s*:\s*-9999px", re.IGNORECASE),
)

TIER1_FORM_PAGES = (
    LANDING_DIR / "start.html",
    LANDING_DIR / "diagnostic.html",
    LANDING_DIR / "diagnostic-real-estate.html",
)


def test_landing_has_no_offcanvas_minus_9999_positioning():
    """No landing HTML/CSS may use `-9999px` off-canvas hiding."""
    violations: list[str] = []
    scan_files = sorted(LANDING_DIR.glob("*.html")) + [LANDING_DIR / "styles.css"]
    for path in scan_files:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for line_no, line in enumerate(text.splitlines(), start=1):
            for pattern in FORBIDDEN_OFFCANVAS:
                if pattern.search(line):
                    violations.append(f"{path.relative_to(REPO_ROOT)}:{line_no}: {line.strip()}")

    assert not violations, (
        "Found forbidden off-canvas -9999px positioning in landing surface:\n"
        + "\n".join(violations)
        + "\nUse clip-based visually-hidden styles instead."
    )


def test_tier1_honeypots_use_clip_hidden_pattern():
    """Tier-1 forms keep honeypot anti-spam without layout overflow."""
    missing: list[str] = []
    for path in TIER1_FORM_PAGES:
        text = path.read_text(encoding="utf-8", errors="replace")
        # We require clip-path for the inline hidden honeypot style to ensure
        # no off-canvas positioning reappears.
        if "clip-path:inset(50%)" not in text:
            missing.append(str(path.relative_to(REPO_ROOT)))
    assert not missing, (
        "Tier-1 form honeypots must keep clip-based hidden style. Missing in:\n"
        + "\n".join(missing)
    )
