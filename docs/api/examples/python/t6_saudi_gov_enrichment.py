"""
T6 example — enrich a Saudi lead with government data.

Runs the canonical Saudi-sovereign enrichment chain at lead-capture:

  1. Wathq commercial-registry lookup (already in T2).
  2. Maroof consumer-reputation badge.
  3. Najiz commercial-risk snapshot.
  4. Tadawul listed-equity profile (if a symbol was supplied).

Every endpoint 503s with `<service>_not_configured` when its API key
is unset, so this script also doubles as a runtime probe — useful for
ops to verify which Saudi-gov sub-processors a deployment actually has
keys for.
"""

from __future__ import annotations

import os
from typing import Any

import httpx

BASE = os.environ.get("DEALIX_API_BASE", "https://api.dealix.me").rstrip("/")
API_KEY = os.environ.get("DEALIX_API_KEY", "")

HEADERS = {"X-API-Key": API_KEY}


def _get(path: str) -> dict[str, Any] | None:
    r = httpx.get(f"{BASE}{path}", headers=HEADERS, timeout=15)
    if r.status_code == 503:
        print(f"  · {path}  →  service not configured")
        return None
    if r.status_code == 404:
        print(f"  · {path}  →  not found")
        return None
    if r.status_code >= 400:
        print(f"  · {path}  →  HTTP {r.status_code} {r.text[:80]}")
        return None
    return r.json()


def enrich(cr_number: str, tadawul_symbol: str | None = None) -> dict[str, Any]:
    print(f"Enriching CR {cr_number}…")
    result: dict[str, Any] = {"cr_number": cr_number}

    maroof = _get(f"/api/v1/saudi-gov/maroof/{cr_number}")
    if maroof:
        result["maroof"] = maroof

    judicial = _get(f"/api/v1/saudi-gov/judicial/{cr_number}")
    if judicial:
        result["judicial"] = judicial

    if tadawul_symbol:
        tdw = _get(f"/api/v1/saudi-gov/tadawul/{tadawul_symbol}")
        if tdw:
            result["tadawul"] = tdw

    return result


if __name__ == "__main__":
    out = enrich("1010101010", tadawul_symbol="2222")
    print()
    import json

    print(json.dumps(out, indent=2, ensure_ascii=False))
