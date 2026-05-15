"""City / region normalization for Saudi contexts."""

from __future__ import annotations

_ALIASES: dict[str, str] = {
    "riyadh": "riyadh",
    "الرياض": "riyadh",
    "jeddah": "jeddah",
    "جدة": "jeddah",
    "dammam": "dammam",
    "الدمام": "dammam",
}


def normalize_saudi_city(raw: str) -> str:
    s = raw.strip().lower()
    return _ALIASES.get(s, s)


__all__ = ["normalize_saudi_city"]
