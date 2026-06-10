#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from dealix.commercial_ops.phase_01_close_path import build_phase_01_close_path
from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8


def main():
    ensure_stdout_utf8()
    p = argparse.ArgumentParser()
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    b = build_phase_01_close_path()
    print(f"PHASE_01_CLOSE_VERDICT={b['verdict']}")
    for x in b.get("blockers_ar") or []:
        print(f"  BLOCKER: {x}")
    if args.json:
        print(json.dumps(b, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
