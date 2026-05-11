from __future__ import annotations

from pathlib import Path

from saudi_ai_provider.offers import generate_offer


def run(service_id: str, segment: str, lang: str = "ar", out_dir: Path | None = None) -> dict[str, Path]:
    return generate_offer(service_id, segment, lang=lang, output_dir=out_dir)
