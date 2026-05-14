#!/usr/bin/env python3
"""Generate capital-assets/CAPITAL_ASSET_INDEX.json — Wave 19.

Reads `auto_client_acquisition.capital_os.capital_asset_registry.CAPITAL_ASSETS`
and writes the canonical index file the founder commits to the repo.

Idempotent. Re-running overwrites the file with current registry state.
"""
from __future__ import annotations

import json
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))


def main() -> int:
    from auto_client_acquisition.capital_os.capital_asset_registry import (
        CAPITAL_ASSETS,
    )

    out_dir = REPO_ROOT / "capital-assets"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "CAPITAL_ASSET_INDEX.json"

    payload = {
        "version": "1.0",
        "wave": "19",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_of_truth": "auto_client_acquisition/capital_os/capital_asset_registry.py",
        "asset_count": len(CAPITAL_ASSETS),
        "public_count": sum(1 for a in CAPITAL_ASSETS if a.public),
        "by_type": _by_type(CAPITAL_ASSETS),
        "by_maturity": _by_maturity(CAPITAL_ASSETS),
        "assets": [
            {
                "asset_id": a.asset_id,
                "name": a.name,
                "type": a.type,
                "strategic_role": a.strategic_role,
                "file_paths": list(a.file_paths),
                "buyer_relevance": list(a.buyer_relevance),
                "commercial_use": list(a.commercial_use),
                "maturity": a.maturity,
                "linked_non_negotiables": list(a.linked_non_negotiables),
                "proof_level": a.proof_level,
                "last_reviewed": a.last_reviewed,
                "public": a.public,
            }
            for a in CAPITAL_ASSETS
        ],
    }

    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✓ Wrote {len(CAPITAL_ASSETS)} assets to {out_path.relative_to(REPO_ROOT)}")
    print(f"  Public-safe: {payload['public_count']}")
    print(f"  By type: {payload['by_type']}")
    return 0


def _by_type(assets) -> dict[str, int]:
    out: dict[str, int] = {}
    for a in assets:
        out[a.type] = out.get(a.type, 0) + 1
    return dict(sorted(out.items()))


def _by_maturity(assets) -> dict[str, int]:
    out: dict[str, int] = {}
    for a in assets:
        out[a.maturity] = out.get(a.maturity, 0) + 1
    return dict(sorted(out.items()))


if __name__ == "__main__":
    raise SystemExit(main())
