from __future__ import annotations

from pathlib import Path

from offers.offer_generator import run


def build_proposal(service_id: str, segment: str, lang: str = "ar", output_dir: Path | None = None) -> Path:
    outputs = run(service_id, segment, lang=lang, out_dir=output_dir)
    return outputs["offer"]
