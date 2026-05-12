"""Arabic-first transactional email templates (Jinja2)."""
from __future__ import annotations

from pathlib import Path

TEMPLATES_DIR = Path(__file__).parent
AR_DIR = TEMPLATES_DIR / "ar"
EN_DIR = TEMPLATES_DIR / "en"


def template_path(name: str, locale: str = "ar") -> Path:
    base = AR_DIR if locale.startswith("ar") else EN_DIR
    path = base / f"{name}.html.j2"
    if not path.is_file():
        # Fall back to English when the Arabic template is missing,
        # and to a generic placeholder when both are missing.
        alt = EN_DIR / f"{name}.html.j2"
        if alt.is_file():
            return alt
        raise FileNotFoundError(f"template_not_found:{name}")
    return path
