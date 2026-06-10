"""Parses `design-systems/dealix/DESIGN.md` into a token dict.

The DESIGN.md file is the canonical source. This loader extracts:

- ``colors``         — token name → role description
- ``typography``     — token name → font / size / weight
- ``spacing``        — sorted list of int (px)
- ``status_chips``   — list of canonical chip names
- ``forbidden_copy`` — list of phrases that may not appear in
                       positive context

The parser is intentionally lightweight; it relies on the section
headings in DESIGN.md (``## 2.``, ``## 3.``, etc.) staying stable.
A schema test in `tests/test_dealix_design_system.py` enforces that.
"""
from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parents[2]
_DESIGN_MD = _REPO_ROOT / "design-systems" / "dealix" / "DESIGN.md"


def _extract_section(md: str, heading_starts_with: str) -> str:
    """Return the body of the first ``## …`` section whose heading
    starts with *heading_starts_with*. Empty string if not found.
    """
    lines = md.splitlines()
    start: int | None = None
    for i, line in enumerate(lines):
        if line.startswith("## ") and heading_starts_with in line:
            start = i + 1
            break
    if start is None:
        return ""
    end = len(lines)
    for j in range(start, len(lines)):
        if lines[j].startswith("## "):
            end = j
            break
    return "\n".join(lines[start:end])


def _parse_color_table(section: str) -> dict[str, str]:
    """Pull token name → role from the markdown table in §2."""
    colors: dict[str, str] = {}
    for line in section.splitlines():
        # Table rows look like: | `primary` | role | hex | hex |
        m = re.match(r"\|\s*`([a-z\-]+)`\s*\|\s*([^|]+?)\s*\|", line)
        if m:
            colors[m.group(1)] = m.group(2).strip()
    return colors


def _parse_typography_table(section: str) -> dict[str, dict[str, str]]:
    """Pull token name → {family,size,weight,line_h} from §3."""
    typography: dict[str, dict[str, str]] = {}
    for line in section.splitlines():
        m = re.match(
            r"\|\s*`([a-z\-]+)`\s*\|\s*([^|]+?)\s*\|"
            r"\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|",
            line,
        )
        if m:
            typography[m.group(1)] = {
                "family": m.group(2).strip(),
                "size": m.group(3).strip(),
                "weight": m.group(4).strip(),
                "line_height": m.group(5).strip(),
            }
    return typography


def _parse_spacing(section: str) -> list[int]:
    """Pull the spacing scale ints from §4."""
    nums: list[int] = []
    # Look for a backticked scale line like `4 / 8 / 12 / 16 / 24 / 32 / 48`.
    for line in section.splitlines():
        m = re.search(r"`([\d\s/]+)`", line)
        if m and "/" in m.group(1):
            for chunk in m.group(1).split("/"):
                chunk = chunk.strip()
                if chunk.isdigit():
                    nums.append(int(chunk))
            if nums:
                break
    return sorted(set(nums))


def _parse_status_chips(section: str) -> list[str]:
    """Pull the canonical chip names from §6."""
    chips: list[str] = []
    # Names are inside backticks on the bullet/paragraph lines.
    for m in re.finditer(r"`([A-Z][A-Za-z ]+)`", section):
        name = m.group(1).strip()
        if name and name not in chips:
            chips.append(name)
    return chips


def _parse_forbidden_copy(section: str) -> list[str]:
    """Pull the verbatim forbidden strings from §7."""
    items: list[str] = []
    for line in section.splitlines():
        line = line.strip()
        if not line.startswith("- "):
            continue
        m = re.match(r"-\s*`([^`]+)`", line)
        if m:
            items.append(m.group(1))
    return items


@lru_cache(maxsize=1)
def load_design_system() -> dict[str, Any]:
    """Read DESIGN.md and return a structured token dict.

    Keys:
        colors, typography, spacing, status_chips, forbidden_copy,
        source_path.
    """
    if not _DESIGN_MD.is_file():
        raise FileNotFoundError(
            f"design-system spec missing at {_DESIGN_MD}"
        )
    md = _DESIGN_MD.read_text(encoding="utf-8")
    return {
        "colors": _parse_color_table(_extract_section(md, "Color Tokens")),
        "typography": _parse_typography_table(
            _extract_section(md, "Typography Tokens")
        ),
        "spacing": _parse_spacing(_extract_section(md, "Spacing Scale")),
        "status_chips": _parse_status_chips(
            _extract_section(md, "Status Chip Names")
        ),
        "forbidden_copy": _parse_forbidden_copy(
            _extract_section(md, "Forbidden Copy List")
        ),
        "source_path": str(_DESIGN_MD),
    }
