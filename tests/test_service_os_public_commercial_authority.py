from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "apps/web/app/service-os/page.tsx"
SNAPSHOT = ROOT / "apps/web/lib/service-os-snapshot.ts"


def test_service_os_public_surface_is_quote_only_after_free_diagnostic() -> None:
    text = PAGE.read_text(encoding="utf-8") + "\n" + SNAPSHOT.read_text(encoding="utf-8")
    lowered = text.lower()
    assert 'href="/book"' in text
    assert "التشخيص التنفيذي المجاني" in text
    assert "qualified discovery" in lowered
    assert "customer-specific" in lowered
    assert "approved quote" in lowered


def test_service_os_cannot_emit_public_fixed_price_or_duration_authority() -> None:
    text = PAGE.read_text(encoding="utf-8") + "\n" + SNAPSHOT.read_text(encoding="utf-8")
    assert "باقات جاهزة للبيع" not in text
    assert not re.search(r"\d+(?:k|,?\d{3})?(?:\s*[-–]\s*\d+(?:k|,?\d{3})?)?\s*SAR", text, re.I)
    assert not re.search(r"\d+(?:\s*[-–]\s*\d+)?\s*days?", text, re.I)
    assert "offer.price" not in text
    assert "offer.timeline" not in text
