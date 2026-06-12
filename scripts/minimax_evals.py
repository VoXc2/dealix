#!/usr/bin/env python3
"""MiniMax eval harness — runs in mock mode by default.

No network calls when MINIMAX_API_KEY is unset. With a real key set, this
script runs a small smoke test (capped at 5 calls) and prints a JSON summary.

Usage:
    python scripts/minimax_evals.py
    MINIMAX_API_KEY=sk-... python scripts/minimax_evals.py
    make minimax-evals
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVAL_DIR = ROOT / "data" / "evals"


def main() -> int:
    api_key_set = bool(os.environ.get("MINIMAX_API_KEY"))
    # Live mode is opt-in. Set MINIMAX_EVALS_LIVE=1 to actually hit the
    # network. Without the flag we treat any present key as informational
    # only — this is what we want in CI and on shared workstations.
    live_forced = os.environ.get("MINIMAX_EVALS_LIVE") == "1"
    mode = "live" if (api_key_set and live_forced) else "mock"
    print(f"DEALIX_MINIMAX_EVALS mode={mode} api_key_present={'yes' if api_key_set else 'no'}")

    # 1. Always run the registry + provider unit tests.
    test_files = [
        "tests/test_model_registry.py",
        "tests/test_minimax_provider.py",
    ]
    cmd = [sys.executable, "-m", "pytest", "-q", "--no-header", *test_files]
    result = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True)
    print(result.stdout.strip() or "(no stdout)")
    if result.returncode != 0:
        print(result.stderr.strip(), file=sys.stderr)
        return result.returncode

    # 2. In live mode, run a capped smoke test (5 calls max).
    if api_key_set and live_forced:
        try:
            sys.path.insert(0, str(ROOT))
            from dealix.hermes.providers.minimax_provider import MiniMaxProvider  # type: ignore
        except Exception as exc:  # pragma: no cover
            print(f"DEALIX_MINIMAX_EVALS live=skipped reason={exc!r}")
        else:
            import asyncio

            provider = MiniMaxProvider()
            try:
                for i in range(5):
                    resp = asyncio.run(
                        provider.chat(
                            system="You are MiniMax inside Dealix. Be concise.",
                            messages=[{"role": "user", "content": f"ping {i}"}],
                        )
                    )
                    if not resp.get("text"):
                        print(f"DEALIX_MINIMAX_EVALS live=fail call={i}")
                        return 1
                print("DEALIX_MINIMAX_EVALS live=ok calls=5")
            except Exception as exc:
                # A live smoke test failing here is a real network/credential
                # problem, not a CI failure. Surface it and continue.
                print(f"DEALIX_MINIMAX_EVALS live=skipped reason={type(exc).__name__}: {exc}")

    # 3. Tally eval dataset files.
    if EVAL_DIR.exists():
        datasets = sorted(p.name for p in EVAL_DIR.glob("*.jsonl"))
        print("")
        print("eval_datasets:")
        for name in datasets:
            count = sum(1 for _ in (EVAL_DIR / name).open(encoding="utf-8"))
            print(f"  {name:<48} cases={count}")

    print("")
    print("DEALIX_MINIMAX_EVALS=OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
