#!/usr/bin/env python3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from dealix.commercial_ops.founder_north_star import build_north_star_status
from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8


def main():
    ensure_stdout_utf8()
    b = build_north_star_status()
    print(f"FOUNDER_NORTH_STAR={b['verdict']}")
    for g in b.get("gaps") or []:
        print(f"  GAP: {g}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
