#!/usr/bin/env python3
"""Embeddings pipeline — local index summary + manifest (vectors upload deferred)."""

from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
_MANIFEST = _REPO / "dealix/transformation/embeddings_manifest.json"
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from auto_client_acquisition.v3.project_intelligence import build_index_summary, scan_project  # noqa: E402


def main() -> int:
    docs = scan_project(_REPO)
    summary = build_index_summary(docs)
    manifest = {
        "updated_at": datetime.now(UTC).isoformat(),
        "documents_indexed": summary.get("document_count", len(docs)),
        "vectors_uploaded": 0,
        "status": "local_scan_only",
        "next": "wire worker + pgvector per docs/EMBEDDINGS_PIPELINE.md",
    }
    _MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    _MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print("EMBEDDINGS_PIPELINE")
    print(json.dumps(manifest, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
