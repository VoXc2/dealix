#!/usr/bin/env python3
"""Fail fast on silent import breakage.

Eleven `_os` modules and two routers once broke at import time and went
undetected because `api/main.py` imports some routers defensively
(try/except → `_OPTIONAL_ROUTER_ERRORS`). `compileall` only checks syntax,
not import resolution.

This guard:
  1. Imports every module under `api/routers/` — fails on any ImportError.
  2. Builds the app and asserts `_OPTIONAL_ROUTER_ERRORS` is empty, so a
     defensively-imported router can no longer rot silently.

Exit 0 = all imports clean. Exit 1 = at least one module failed.
"""

from __future__ import annotations

import importlib
import sys
import traceback
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

ROUTERS_DIR = _REPO / "api" / "routers"


def main() -> int:
    failures: list[tuple[str, str]] = []

    for path in sorted(ROUTERS_DIR.glob("*.py")):
        if path.name == "__init__.py":
            continue
        module = f"api.routers.{path.stem}"
        try:
            importlib.import_module(module)
        except Exception:  # noqa: BLE001 — report every failure, don't abort
            failures.append((module, traceback.format_exc()))

    try:
        from api.main import _OPTIONAL_ROUTER_ERRORS, create_app

        create_app()
        for name, err in _OPTIONAL_ROUTER_ERRORS.items():
            failures.append((f"api.routers.{name} (optional)", err))
    except Exception:  # noqa: BLE001
        failures.append(("api.main", traceback.format_exc()))

    if failures:
        print(f"FAIL — {len(failures)} module(s) failed to import:\n")
        for module, err in failures:
            print(f"  ✗ {module}")
            print("    " + err.strip().replace("\n", "\n    "))
            print()
        return 1

    print("OK — all api/routers modules import cleanly.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
