#!/usr/bin/env python3
"""Validate site routes (adapted to the Vite/react-router app): core pages,
5 system pages, 8 sector solution pages, each backed by a real component file."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import CheckResult, load_yaml, main, rel  # noqa: E402

CORE_PATHS = ["/", "/systems", "/pricing", "/diagnostic", "/start", "/contact", "/solutions"]


def check() -> CheckResult:
    r = CheckResult("site_routes")
    manifest = load_yaml("data/site/routes.yaml")
    routes = manifest.get("routes", [])
    paths = [r_["path"] for r_ in routes]

    for cp in CORE_PATHS:
        if cp not in paths:
            r.error(f"missing core route {cp}")

    system_pages = [p for p in paths if p.startswith("/systems/")]
    solution_pages = [p for p in paths if p.startswith("/solutions/")]
    r.require(len(system_pages) >= 5, f"expected >= 5 system pages, got {len(system_pages)}")
    r.require(len(solution_pages) >= 8, f"expected >= 8 solution pages, got {len(solution_pages)}")

    for route in routes:
        src = route.get("source")
        if not src or not rel(src).exists():
            r.error(f"route {route.get('path')} missing source file {src}")

    if not rel("src/siteRoutes.tsx").exists():
        r.error("missing src/siteRoutes.tsx barrel consumed by App.tsx")

    r.note(f"{len(routes)} routes: {len(system_pages)} system pages, {len(solution_pages)} solution pages")
    return r


if __name__ == "__main__":
    main(check)
