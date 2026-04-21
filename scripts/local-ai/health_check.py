#!/usr/bin/env python3
"""
Local AI health check — usable as a standalone script.

Prints a bilingual (AR/EN) summary of Ollama status + recommended models.
Exits 0 if healthy, 1 otherwise, 2 if disabled.

    python scripts/local-ai/health_check.py
    LOCAL_LLM_BASE_URL=http://localhost:11434 python scripts/local-ai/health_check.py
"""
from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path

# Allow running from repo root without PYTHONPATH gymnastics.
_BACKEND = Path(__file__).resolve().parents[2] / "backend"
if str(_BACKEND) not in sys.path:
    sys.path.insert(0, str(_BACKEND))

from app.services.local_ai.catalog import (  # noqa: E402
    detect_server_tier,
    recommended_install_plan,
    select_models_for_tier,
)
from app.services.local_ai.client import OllamaClient  # noqa: E402


async def main() -> int:
    base = os.environ.get("LOCAL_LLM_BASE_URL", "http://localhost:11434")
    enabled = os.environ.get("LOCAL_LLM_ENABLED", "").lower() in {"1", "true", "yes"}
    capacity = detect_server_tier()

    print("═══ Dealix Local AI Health Check ═══")
    print(f"LOCAL_LLM_ENABLED : {enabled}")
    print(f"LOCAL_LLM_BASE_URL: {base}")
    print(
        f"Host: RAM={capacity.total_ram_gb:.1f} GB, "
        f"avail={capacity.available_ram_gb:.1f} GB, "
        f"disk={capacity.free_disk_gb:.1f} GB, "
        f"gpu={capacity.has_gpu}, tier={capacity.tier.value}"
    )

    client = OllamaClient(base_url=base)
    healthy = await client.health(force=True)
    print(f"Ollama daemon    : {'OK (متصل)' if healthy else 'UNREACHABLE (غير متاح)'}")

    if healthy:
        tags = [m.get("name") or m.get("model") for m in await client.list_models()]
        print(f"Pulled models    : {', '.join(tags) if tags else '<none>'}")

    eligible = select_models_for_tier(capacity.tier)
    plan = recommended_install_plan(capacity)
    print("Eligible tags     :")
    for m in eligible:
        print(f"  • {m.ollama_tag:<28}  ~{m.approx_size_gb:>4.1f} GB  tier={m.tier.value}")
    print("Recommended pulls :")
    for m in plan:
        print(f"  • {m.ollama_tag}  (≈ {m.approx_size_gb:.1f} GB)")

    if not enabled:
        return 2
    return 0 if healthy else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
