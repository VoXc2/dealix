"""
Prompt-injection defense — Lakera Guard primary, Rebuff OSS fallback,
heuristic sanity check when neither is configured.

Every user-supplied text that ends up in an agent prompt should pass
through `defend()` first.

Reference: https://docs.lakera.ai/category/guard-api
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass

import httpx

from core.logging import get_logger

log = get_logger(__name__)


@dataclass
class DefenseResult:
    safe: bool
    score: float  # 0.0 safe → 1.0 hostile
    reason: str
    provider: str


# Common injection patterns the heuristic catches when no vendor is configured.
_HEURISTIC_PATTERNS = [
    re.compile(r"ignore (all|previous|prior) instructions", re.I),
    re.compile(r"disregard (your|the) (system|previous) prompt", re.I),
    re.compile(r"you are now (a )?(jailbroken|developer|admin)", re.I),
    re.compile(r"reveal your (system )?prompt", re.I),
    re.compile(r"(انس|تجاهل) (التعليمات|التوجيهات) السابقة", re.I),
]


async def defend(text: str) -> DefenseResult:
    if not text or len(text.strip()) < 4:
        return DefenseResult(safe=True, score=0.0, reason="empty", provider="none")

    lakera_key = os.getenv("LAKERA_API_KEY", "").strip()
    if lakera_key:
        try:
            async with httpx.AsyncClient(timeout=5) as c:
                r = await c.post(
                    "https://api.lakera.ai/v2/guard",
                    headers={"Authorization": f"Bearer {lakera_key}"},
                    json={"messages": [{"role": "user", "content": text}]},
                )
                r.raise_for_status()
                data = r.json()
            flagged = bool(data.get("flagged"))
            score = float(data.get("payload", [{}])[0].get("score") or 0.0)
            return DefenseResult(
                safe=not flagged,
                score=score,
                reason="lakera_flagged" if flagged else "lakera_clean",
                provider="lakera",
            )
        except Exception:
            log.exception("lakera_guard_failed")

    # Rebuff (OSS) — optional client, identical contract.
    rebuff_key = os.getenv("REBUFF_API_KEY", "").strip()
    if rebuff_key:
        try:
            async with httpx.AsyncClient(timeout=5) as c:
                r = await c.post(
                    "https://api.rebuff.ai/api/detect",
                    headers={"Authorization": f"Bearer {rebuff_key}"},
                    json={"userInput": text},
                )
                r.raise_for_status()
                data = r.json()
            score = float(data.get("heuristicScore") or 0.0)
            return DefenseResult(
                safe=score < 0.7,
                score=score,
                reason="rebuff",
                provider="rebuff",
            )
        except Exception:
            log.exception("rebuff_failed")

    # Heuristic fallback — fast, deterministic, never 5xx.
    for pat in _HEURISTIC_PATTERNS:
        if pat.search(text):
            return DefenseResult(
                safe=False,
                score=0.85,
                reason="heuristic_pattern_match",
                provider="heuristic",
            )
    return DefenseResult(safe=True, score=0.0, reason="heuristic_clean", provider="heuristic")
