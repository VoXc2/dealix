"""
Tadawul — Saudi Stock Exchange (Saudi Exchange — تداول).

Read-only access to listed-company snapshots. Used by:

- the market-researcher skill (company brief)
- the lead-scorer (publicly listed → higher contractual confidence)
- the proposal-writer (financial-context paragraph for listed accounts)

Tadawul's public market-data is rate-limited; bulk + intraday access
needs a paid feed from the Saudi Tadawul Group. Inert without
`TADAWUL_API_KEY`.

Reference: https://www.saudiexchange.sa
"""

from __future__ import annotations

import os
from dataclasses import dataclass

import httpx

from core.logging import get_logger

log = get_logger(__name__)


def _base() -> str:
    return os.getenv("TADAWUL_API_BASE", "https://api.saudiexchange.sa/v1").rstrip("/")


def is_configured() -> bool:
    return bool(os.getenv("TADAWUL_API_KEY", "").strip())


@dataclass(frozen=True)
class ListedCompany:
    symbol: str
    name_ar: str
    name_en: str
    sector: str
    market_cap_sar: float | None
    last_close: float | None
    pe_ratio: float | None


async def lookup_symbol(symbol: str) -> ListedCompany | None:
    if not is_configured():
        return None
    headers = {"Authorization": f"Bearer {os.getenv('TADAWUL_API_KEY', '').strip()}"}
    try:
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.get(f"{_base()}/companies/{symbol}", headers=headers)
            if r.status_code == 404:
                return None
            r.raise_for_status()
            data = r.json()
    except Exception:
        log.exception("tadawul_lookup_failed", symbol=symbol)
        return None
    return ListedCompany(
        symbol=symbol,
        name_ar=str(data.get("nameAr", "")),
        name_en=str(data.get("nameEn", "")),
        sector=str(data.get("sector", "")),
        market_cap_sar=data.get("marketCapSar"),
        last_close=data.get("lastClose"),
        pe_ratio=data.get("peRatio"),
    )
