"""AEO (agent/engine discovery) metadata for /api/v1/meta — no secrets."""

from __future__ import annotations

from typing import Any

from dealix.commercial_ops.paths import REPO_ROOT

AEO_CALENDAR = REPO_ROOT / "docs" / "commercial" / "operations" / "AEO_CONTENT_CALENDAR_AR.md"


def _learn_slugs() -> list[str]:
    slug_dir = REPO_ROOT / "frontend" / "src" / "app" / "[locale]" / "learn" / "[slug]"
    if not slug_dir.is_dir():
        return []
    return sorted(
        child.name for child in slug_dir.iterdir() if child.is_dir() and (child / "page.tsx").is_file()
    )


def build_aeo_snapshot() -> dict[str, Any]:
    slugs = _learn_slugs()
    return {
        "learn_article_count": len(slugs),
        "learn_slugs_sample": slugs[:12],
        "learn_hub_path": "/[locale]/learn",
        "content_calendar_doc": (
            "docs/commercial/operations/AEO_CONTENT_CALENDAR_AR.md"
            if AEO_CALENDAR.is_file()
            else None
        ),
        "token_to_value_hints": [
            "GET /api/v1/revenue-os/catalog",
            "GET /api/v1/decision-passport/golden-chain",
            "GET /api/v1/meta",
            "GET /openapi.json",
        ],
        "discovery_note_ar": (
            "Dealix — Revenue OS سعودي؛ كل إجراء خارجي يتطلب موافقة وجواز قرار."
        ),
    }
