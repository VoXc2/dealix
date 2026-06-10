#!/usr/bin/env python3
"""Print market intelligence pack status (paths, pillar of week)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.market_intelligence_refs import (  # noqa: E402
    build_market_intel_digest_block,
    market_intelligence_pillars_flat,
    market_intelligence_status,
    pillar_of_week,
)
from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402


def main() -> int:
    ensure_stdout_utf8()
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    st = market_intelligence_status()
    pow_doc = pillar_of_week()
    block = build_market_intel_digest_block()
    blob = {
        "status": st,
        "pillar_of_week": pow_doc,
        "digest_block": block,
        "pillars": market_intelligence_pillars_flat(),
    }

    if args.json:
        print(json.dumps(blob, ensure_ascii=False, indent=2))
        return 0 if st["ok"] else 1

    print("== market_intelligence_status ==")
    print(f"  ok: {st['ok']}")
    print(f"  pillars: {st['pillar_count']}")
    if st["missing_paths"]:
        print(f"  MISSING: {st['missing_paths']}")
    if pow_doc:
        print(f"  pillar_of_week: {pow_doc['topic_ar']}")
        print(f"    doc: {pow_doc['doc']}")
    print(f"  index: {st.get('index')}")
    print("MARKET_INTELLIGENCE_VERDICT=PASS" if st["ok"] else "MARKET_INTELLIGENCE_VERDICT=FAIL")
    return 0 if st["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
