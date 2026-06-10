#!/usr/bin/env python3
"""Initialize a founder meeting debrief YAML from template."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402

ensure_stdout_utf8()


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--company", required=True)
    p.add_argument("--contact", default="")
    p.add_argument("--motion", default="A", choices=["A", "B", "C", "D"])
    p.add_argument("--offer-id", default="ten_lead_audit")
    p.add_argument("--type", default="discovery", choices=["discovery", "demo", "partner"])
    p.add_argument("--date", default=None)
    args = p.parse_args()

    from dealix.commercial_ops.founder_debrief import init_debrief

    path = init_debrief(
        company=args.company,
        contact=args.contact,
        motion=args.motion,
        offer_id=args.offer_id,
        meeting_type=args.type,
        date_str=args.date,
    )
    print(f"DEBRIEF_PATH={path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
