#!/usr/bin/env python3
"""Verify Dealix public commercial surfaces agree with current commercial truth.

Default mode is repository-only and safe for CI. ``--live`` performs read-only
HTTP GETs against dealix.me. It never publishes, deploys, mutates DNS, sends
messages, or changes provider state.
"""

from __future__ import annotations

import argparse
import json
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[2]
BASE_URL = "https://dealix.me"

CANONICAL_SURFACES = {
    "/": ROOT / "landing/index.html",
    "/ai-team.html": ROOT / "landing/ai-team.html",
    "/workflow.html": ROOT / "landing/workflow.html",
    "/customer-portal.html": ROOT / "landing/customer-portal.html",
    "/saudi-opportunity-radar": ROOT / "apps/web/app/saudi-opportunity-radar/page.tsx",
}

FORBIDDEN_LEGACY_MARKERS = (
    "499 sar",
    "499 ر.س",
    "499 ريال",
    "7-day pilot",
    "7-day sprint",
    "5 وكلاء ai",
    "٥ وكلاء ai",
    "managed ai ops",
    "1,500–2,500",
    "١٬٥٠٠–٢٬٥٠٠",
    "كلّ endpoint حيّ",
    "كل endpoint حي",
    "لا vapor",
    "احجز sprint مباشرة",
)

REQUIRED_BY_PATH = {
    "/": (
        "saudi-first ai business operating system",
        "free mini diagnostic",
    ),
    "/ai-team.html": (
        "فريق ai تشغيلي داخل نظام شركة واحد",
        "لا توجد باقات ثابتة عامة",
    ),
    "/workflow.html": (
        "customer-specific quote",
        "no_live_send",
    ),
    "/customer-portal.html": (
        "noindex,nofollow",
        "dealix_retired_public_surface",
    ),
    "/saudi-opportunity-radar": (
        "public signal ≠ buyer intent ≠ relationship ≠ consent ≠ pipeline ≠ revenue",
        "research ≠ relationship",
        "readiness ≠ certification",
        "diagnostic ≠ quote",
        "moc-business-q2-2026",
        "zatca-wave25",
        "cst-ai-adoption",
        "gastat-tourism-q1-2026",
        "gastat-construction-cost-2026",
        "nca-ncnicc",
        "sama-open-banking",
    ),
}


@dataclass(frozen=True)
class SurfaceResult:
    path: str
    ok: bool
    missing_required: tuple[str, ...]
    legacy_markers: tuple[str, ...]
    fetch_error: str = ""


def evaluate_surface(path: str, text: str) -> SurfaceResult:
    lowered = text.casefold()
    required = REQUIRED_BY_PATH[path]
    missing = tuple(marker for marker in required if marker.casefold() not in lowered)
    legacy = tuple(marker for marker in FORBIDDEN_LEGACY_MARKERS if marker.casefold() in lowered)
    return SurfaceResult(
        path=path,
        ok=not missing and not legacy,
        missing_required=missing,
        legacy_markers=legacy,
    )


def _fetch(url: str, timeout: float) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Dealix-Public-Commercial-Parity/1.0",
            "Cache-Control": "no-cache",
        },
        method="GET",
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        if response.status != 200:
            raise RuntimeError(f"HTTP_{response.status}")
        return response.read(2_000_000).decode("utf-8", errors="replace")


def verify_repo() -> list[SurfaceResult]:
    results: list[SurfaceResult] = []
    for path, file_path in CANONICAL_SURFACES.items():
        if not file_path.is_file():
            results.append(
                SurfaceResult(
                    path=path,
                    ok=False,
                    missing_required=("surface_missing",),
                    legacy_markers=(),
                )
            )
            continue
        results.append(
            evaluate_surface(
                path, file_path.read_text(encoding="utf-8", errors="replace")
            )
        )
    return results


def verify_live(base_url: str = BASE_URL, timeout: float = 12.0) -> list[SurfaceResult]:
    results: list[SurfaceResult] = []
    for path in CANONICAL_SURFACES:
        url = f"{base_url.rstrip('/')}{path}"
        try:
            text = _fetch(url, timeout)
        except (OSError, RuntimeError, urllib.error.URLError) as exc:
            results.append(
                SurfaceResult(
                    path=path,
                    ok=False,
                    missing_required=(),
                    legacy_markers=(),
                    fetch_error=f"{type(exc).__name__}:{exc}",
                )
            )
            continue
        results.append(evaluate_surface(path, text))
    return results


def _all_ok(results: Iterable[SurfaceResult]) -> bool:
    return all(row.ok for row in results)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--live", action="store_true", help="Read-only checks against dealix.me"
    )
    parser.add_argument("--base-url", default=BASE_URL)
    parser.add_argument("--timeout", type=float, default=12.0)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    mode = "live" if args.live else "repo"
    results = (
        verify_live(args.base_url, args.timeout) if args.live else verify_repo()
    )
    ok = _all_ok(results)
    payload = {
        "mode": mode,
        "ok": ok,
        "canonical_path": "Free diagnostic -> Qualified Discovery -> Customer-specific Quote -> Bounded Outcome Pilot -> Proof -> STOP/EXPAND/REDESIGN",
        "results": [asdict(row) for row in results],
    }

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for row in results:
            print(f"SURFACE={row.path} STATUS={'PASS' if row.ok else 'FAIL'}")
            for marker in row.missing_required:
                print(f"  MISSING_REQUIRED={marker}")
            for marker in row.legacy_markers:
                print(f"  LEGACY_MARKER={marker}")
            if row.fetch_error:
                print(f"  FETCH_ERROR={row.fetch_error}")
        print(f"PUBLIC_COMMERCIAL_PARITY={'PASS' if ok else 'FAIL'}")
        print(f"MODE={mode}")

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
