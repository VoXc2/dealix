#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from dealix.commercial_ops.founder_agent_tasks import analyze_agent_queue_status, seed_today_queue
from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8


def main():
    ensure_stdout_utf8()
    p = argparse.ArgumentParser()
    p.add_argument("--seed-today", action="store_true")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    if args.seed_today:
        seed_today_queue(dry_run=False)
    b = analyze_agent_queue_status()
    print(f"FOUNDER_AGENT_QUEUE={b['verdict']} P0={b.get('p0_count')}")
    if args.json:
        print(json.dumps(b, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
