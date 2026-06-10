#!/usr/bin/env python3
"""Generate per-target client pack (proposal + deck notes) — manual send only."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.client_pack import build_client_pack


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--company", help="Target company name (matches CSV)")
    p.add_argument("--lead-id", help="War Room lead id or slug")
    p.add_argument("--no-write", action="store_true", help="Return JSON only; do not write data/client_packs/")
    args = p.parse_args()
    if not args.company and not args.lead_id:
        print("Provide --company or --lead-id")
        return 2
    try:
        pack = build_client_pack(
            company=args.company,
            lead_id=args.lead_id,
            write_disk=not args.no_write,
        )
    except ValueError:
        print("CLIENT_PACK: FAIL target_not_found")
        return 1
    slim = {k: v for k, v in pack.items() if k != "proposal"}
    slim["proposal_markdown_preview"] = (pack.get("proposal") or {}).get("title_ar", "")
    print(json.dumps(slim, ensure_ascii=False, indent=2))
    print(f"CLIENT_PACK: OK company={pack.get('company')}")
    if pack.get("paths"):
        print(f"  dir: {pack['paths'].get('directory')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
