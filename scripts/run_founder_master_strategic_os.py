#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from dealix.commercial_ops.founder_master_strategic_os import run_founder_master_strategic_os
from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8


def main():
    ensure_stdout_utf8()
    p = argparse.ArgumentParser()
    p.add_argument("--skip-live", action="store_true")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    blob = run_founder_master_strategic_os(skip_live=args.skip_live)
    print(f"FOUNDER_MASTER_STRATEGIC_OS_VERDICT={blob['verdict']}")
    if args.json:
        print(json.dumps(blob, ensure_ascii=False, indent=2))
    return 0 if blob["verdict"] in ("PASS", "WARN") else 1

if __name__ == "__main__":
    raise SystemExit(main())
