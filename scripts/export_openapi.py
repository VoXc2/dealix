#!/usr/bin/env python3
"""Export the FastAPI OpenAPI schema for contract review.

The script imports `api.main:app` and writes the current OpenAPI document to
`docs/architecture/openapi.json` by default. It is intentionally small and
side-effect-light so CI can use it as an API contract smoke check.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Ensure the repo root is on sys.path so local packages (e.g. platform_core)
# are importable when this script is invoked directly by CI.
_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from api.main import app  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "docs" / "architecture" / "openapi.json"


def export_openapi(output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    schema = app.openapi()
    output.write_text(
        json.dumps(schema, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    try:
        display = output.relative_to(ROOT)
    except ValueError:
        display = output
    print(f"Exported OpenAPI schema to {display}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Export Dealix OpenAPI schema")
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Output JSON path (default: docs/architecture/openapi.json)",
    )
    args = parser.parse_args()
    export_openapi(args.output if args.output.is_absolute() else ROOT / args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
