#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from dealix.commercial_ops.platform_v10_readiness import analyze_platform_v10_readiness
from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8


def main():
    ensure_stdout_utf8()
    p = argparse.ArgumentParser()
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    b = analyze_platform_v10_readiness()
    print(f"PLATFORM_V10_READINESS={b['verdict']}")
    if b.get("message_ar"):
        print(f"  {b['message_ar']}")
    if args.json:
        print(json.dumps(b, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
