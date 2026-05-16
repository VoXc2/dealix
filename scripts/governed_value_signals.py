#!/usr/bin/env python3
"""Governed Value signals — North Star count, 7-gate map, proof state machine.

Standalone read-only report. Not wired into run_ceo_one_session_readiness.sh so it
can never break the one-command CEO session. Run:  python scripts/governed_value_signals.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from auto_client_acquisition.governed_value_os import (  # noqa: E402
    ALLOWED_TRANSITIONS,
    PROOF_LEVEL_LABEL,
    ProofState,
    count_decisions,
    evaluate_gates,
)


def main() -> int:
    print("=" * 64)
    print("Dealix — Governed Revenue & AI Operations — signals")
    print("=" * 64)

    print("\nNorth Star — Governed Value Decisions Created")
    print(f"  count = {count_decisions()}")

    print("\nProof state machine (governed value progression)")
    for state in ProofState:
        targets = sorted(t.value for t in ALLOWED_TRANSITIONS[state])
        arrow = ", ".join(targets) if targets else "(terminal)"
        print(f"  {PROOF_LEVEL_LABEL[state]:>13}  {state.value:<22} -> {arrow}")

    print("\n7-gate map (no live operating signals — all start unmet)")
    for gate in evaluate_gates():
        mark = "PASS" if gate["passed"] else "----"
        print(f"  [{mark}] Gate {gate['number']}: {gate['name_en']}")

    print("\nGate is read-only. The system prepares, suggests, warns, records,")
    print("verifies, classifies and drafts. The founder approves every external action.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
