#!/usr/bin/env python3
"""CLI: render Proof Pack markdown/PDF for an engagement (no external send)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from auto_client_acquisition.proof_architecture_os.proof_pack_render import (  # noqa: E402
    proof_pack_to_markdown,
    proof_pack_to_pdf,
)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--engagement-json", type=Path, help="JSON file with proof pack sections")
    p.add_argument("--customer-handle", required=True)
    p.add_argument("--out-md", type=Path)
    p.add_argument("--out-pdf", type=Path)
    args = p.parse_args()

    pack: dict | None = None
    if args.engagement_json and args.engagement_json.is_file():
        pack = json.loads(args.engagement_json.read_text(encoding="utf-8"))

    md = proof_pack_to_markdown(pack, customer_handle=args.customer_handle)
    if args.out_md:
        args.out_md.parent.mkdir(parents=True, exist_ok=True)
        args.out_md.write_text(md, encoding="utf-8")
        print(f"PROOF_PACK_MD={args.out_md}")

    if args.out_pdf:
        pdf = proof_pack_to_pdf(pack, customer_handle=args.customer_handle)
        if pdf is None:
            print("PROOF_PACK_PDF=SKIP (no PDF renderer — use --out-md only)")
            return 1
        args.out_pdf.parent.mkdir(parents=True, exist_ok=True)
        args.out_pdf.write_bytes(pdf)
        print(f"PROOF_PACK_PDF={args.out_pdf}")

    if not args.out_md and not args.out_pdf:
        print(md[:2000])
    print("PROOF_PACK_RENDER=OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
