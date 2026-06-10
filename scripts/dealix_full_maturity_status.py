#!/usr/bin/env python3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from dealix.commercial_ops.founder_master_strategic_os import run_founder_master_strategic_os
from dealix.commercial_ops.phase_01_close_path import build_phase_01_close_path
from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8


def main():
    ensure_stdout_utf8()
    s = run_founder_master_strategic_os(skip_live=True)
    p = build_phase_01_close_path()
    print(f"DEALIX_FULL_MATURITY_VERDICT={s['verdict']}")
    print(f"  phase_01: {p['verdict']} gate_open={p['gate_open']}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
