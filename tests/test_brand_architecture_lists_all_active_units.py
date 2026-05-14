"""Every BU in `data/business_units.json` whose status is one of
{BUILD, PILOT, SCALE, SPINOUT} must surface on `landing/group.html` via
the static portfolio JSON. HOLD and KILL units are deliberately hidden.
"""
from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRY = REPO_ROOT / "data" / "business_units.json"
PORTFOLIO = REPO_ROOT / "landing" / "assets" / "data" / "holding-portfolio.json"

VISIBLE_STATUSES = {"BUILD", "PILOT", "SCALE", "SPINOUT"}


def _registry_visible_slugs() -> set[str]:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    return {
        str(e.get("slug") or "")
        for e in (data.get("entries") or [])
        if str(e.get("status") or "") in VISIBLE_STATUSES
    }


def _portfolio_slugs() -> set[str]:
    data = json.loads(PORTFOLIO.read_text(encoding="utf-8"))
    return {str(e.get("slug") or "") for e in (data.get("entries") or [])}


def test_portfolio_json_lists_every_visible_bu():
    missing = _registry_visible_slugs() - _portfolio_slugs()
    assert not missing, (
        f"portfolio JSON missing visible BUs: {missing}. "
        f"Run `python scripts/render_holding_portfolio.py`."
    )


def test_portfolio_json_does_not_list_hidden_units():
    """HOLD / KILL units must NEVER appear in the public projection."""
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    hidden = {
        str(e.get("slug") or "")
        for e in (data.get("entries") or [])
        if str(e.get("status") or "") in ("HOLD", "KILL")
    }
    portfolio = _portfolio_slugs()
    leaked = hidden & portfolio
    assert not leaked, f"hidden BUs leaked to public portfolio: {leaked}"


def test_portfolio_json_only_has_safe_fields():
    """Each entry in the public projection has only the allowed fields."""
    allowed = {"slug", "name", "status", "sector", "doctrine_version", "charter_path"}
    data = json.loads(PORTFOLIO.read_text(encoding="utf-8"))
    for e in (data.get("entries") or []):
        leaked = set(e.keys()) - allowed
        assert not leaked, f"public portfolio leaked extra fields: {leaked}"


def test_group_landing_page_exists():
    assert (REPO_ROOT / "landing" / "group.html").exists()


def test_group_landing_references_portfolio_json():
    text = (REPO_ROOT / "landing" / "group.html").read_text(encoding="utf-8")
    assert "assets/data/holding-portfolio.json" in text
