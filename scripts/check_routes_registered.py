#!/usr/bin/env python3
"""
check_routes_registered.py — Layer-4 verification.

Asserts every router file in api/routers/*.py is included in api/main.py
via app.include_router(). Catches the bug where you create a router but
forget to register it (in which case all its endpoints silently 404).

Usage:
    python scripts/check_routes_registered.py
Exit codes:
    0 — all routers registered
    1 — at least one router file unregistered (lists which)
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ROUTERS_DIR = REPO / "api" / "routers"
MAIN_PY = REPO / "api" / "main.py"

# Router files that ARE imported but DON'T need include_router
# (e.g. they only export helpers, no APIRouter at module top-level)
KNOWN_NON_ROUTERS = {
    "__init__",
    "_helpers",
}


def main() -> int:
    if not ROUTERS_DIR.is_dir():
        print(f"FAIL: {ROUTERS_DIR} is not a directory")
        return 1
    if not MAIN_PY.exists():
        print(f"FAIL: {MAIN_PY} does not exist")
        return 1

    main_text = MAIN_PY.read_text(encoding="utf-8")

    # Discover all router modules
    modules = []
    for f in sorted(ROUTERS_DIR.glob("*.py")):
        stem = f.stem
        if stem in KNOWN_NON_ROUTERS:
            continue
        # Confirm the file actually defines an APIRouter (not a helper)
        text = f.read_text(encoding="utf-8")
        if "APIRouter(" not in text and "router = APIRouter" not in text:
            continue
        modules.append(stem)

    # Each module should be both imported in `from api.routers import (...)`
    # AND registered via app.include_router(<module>.router) somewhere.
    # We accept aliases: e.g. `import calls as calls_router` paired with
    # `app.include_router(calls_router.router)`.
    missing_register = []
    for mod in modules:
        # Try to find include_router patterns:
        #   app.include_router(<mod>.router)
        #   app.include_router(<alias>.router)  where alias was set via
        #     `<mod> as <alias>`
        patterns = [rf"app\.include_router\(\s*{re.escape(mod)}\.router"]
        # detect alias rename
        alias_match = re.search(rf"{re.escape(mod)}\s+as\s+(\w+)", main_text)
        if alias_match:
            alias = alias_match.group(1)
            patterns.append(rf"app\.include_router\(\s*{re.escape(alias)}\.router")
        if not any(re.search(p, main_text) for p in patterns):
            missing_register.append(mod)

    if missing_register:
        print(f"FAIL: {len(missing_register)} router(s) not registered in api/main.py:")
        for m in missing_register:
            print(f"  - {m}.py — add `app.include_router({m}.router)`")
        return 1

    print(f"OK: {len(modules)} router(s) all registered")
    return 0


if __name__ == "__main__":
    sys.exit(main())
