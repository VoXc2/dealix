#!/usr/bin/env python3
"""Check Knowledge OS / embeddings pipeline readiness (no vector upload)."""

from __future__ import annotations

import os
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]


def main() -> int:
    checks: list[tuple[str, bool, str]] = []
    db = os.environ.get("DATABASE_URL", "")
    checks.append(
        (
            "DATABASE_URL",
            bool(db),
            "set for pgvector path" if db else "missing — local index only",
        )
    )
    supa = os.environ.get("SUPABASE_URL", "")
    checks.append(("SUPABASE_URL", bool(supa), "optional project memory"))

    doc = _REPO / "docs" / "EMBEDDINGS_PIPELINE.md"
    checks.append(("EMBEDDINGS_PIPELINE.md", doc.exists(), str(doc)))

    placeholder = _REPO / "scripts" / "embeddings_pipeline_placeholder.py"
    checks.append(("placeholder_script", placeholder.exists(), "run for scan summary"))

    ready = all(ok for name, ok, _ in checks if name in ("DATABASE_URL", "EMBEDDINGS_PIPELINE.md"))

    for name, ok, note in checks:
        status = "OK" if ok else "MISSING"
        print(f"{name}: {status} ({note})")

    if ready:
        print("EMBEDDINGS_READINESS: READY_FOR_WIRING")
        print("Next: implement worker per docs/EMBEDDINGS_PIPELINE.md — do not fake vectors")
        return 0
    print("EMBEDDINGS_READINESS: NOT_READY")
    return 1


if __name__ == "__main__":
    sys.exit(main())
