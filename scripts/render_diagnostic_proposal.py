#!/usr/bin/env python3
"""Render a diagnostic proposal from templates — {{company}}, {{contact}} substitution."""

from __future__ import annotations

import argparse
import re
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROPOSALS = ROOT / "docs/commercial/operations/proposals"
TRUST_PACK = ROOT / "docs/commercial/operations/TRUST_PACK_PROPOSAL_AR.md"
OUT_DIR = ROOT / "data/founder_briefs"


def _slug(name: str) -> str:
    cleaned = re.sub(r"[^\w\s-]", "", name, flags=re.UNICODE)
    cleaned = re.sub(r"[\s_-]+", "_", cleaned.strip())
    return cleaned[:48] or "company"


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--company", required=True)
    p.add_argument("--contact", default="")
    p.add_argument(
        "--template",
        default="DIAGNOSTIC_PROPOSAL_MOTION_A_01_AR.md",
        help="Filename under docs/commercial/operations/proposals/",
    )
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    tpl_path = PROPOSALS / args.template
    if not tpl_path.is_file():
        print(f"Missing template: {tpl_path}", file=sys.stderr)
        return 1

    body = tpl_path.read_text(encoding="utf-8")
    body = body.replace("{{company}}", args.company.strip())
    body = body.replace("{{contact}}", args.contact.strip() or "—")

    trust_rel = TRUST_PACK.relative_to(ROOT).as_posix()
    if TRUST_PACK.is_file() and trust_rel not in body:
        body += (
            f"\n\n---\n\n**Trust Pack (مرفق):** [{trust_rel}]({trust_rel})\n"
        )

    date = datetime.now(UTC).date().isoformat()
    slug = _slug(args.company)
    out_path = OUT_DIR / f"proposal_{slug}_{date}.md"

    if args.dry_run:
        print(f"DRY-RUN → {out_path}")
        print(body[:500] + ("..." if len(body) > 500 else ""))
        return 0

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path.write_text(body, encoding="utf-8")
    print(f"WROTE {out_path.relative_to(ROOT)}")
    print(f"  template: {tpl_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
