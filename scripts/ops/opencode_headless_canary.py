#!/usr/bin/env python3
"""Bounded real-runtime canary for the headless OpenCode executor.

Runs one tiny, control-path-isolated OpenCode job through the exact factory
code path (``session_factory.execute_opencode``) in a throwaway directory. It
never edits the repo, never sends/publishes, and uses the broker-selected
(included) model, so there is no paid spill.

Usage:
    python3 scripts/ops/opencode_headless_canary.py
    python3 scripts/ops/opencode_headless_canary.py --timeout 180

Exit: 0 == OPENCODE_HEADLESS_CANARY=PASS, 1 == FAIL.
"""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

import session_factory as factory

PROMPT = "Reply with exactly OPENCODE_HEADLESS_CANARY_OK. Do not use tools or modify files."


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Bounded headless OpenCode canary")
    parser.add_argument("--timeout", type=int, default=120)
    args = parser.parse_args(argv)
    with tempfile.TemporaryDirectory(prefix="opencode-canary-") as tmp:
        work = Path(tmp)
        job = factory.make_job(
            owner_agent="dealix-engineer",
            business_goal="headless opencode canary",
            job_class="REVIEW",
            authority_level="L2",
            modifying=False,
            executor={"prompt": PROMPT},
        )
        job["TIME_BUDGET"] = args.timeout
        result = factory.execute_opencode(job, work, db_dir=work / "control")
        ok = bool(result.get("ok")) and "OPENCODE_HEADLESS_CANARY_OK" in (
            result.get("stdout") or ""
        )
        payload = {
            "schema": "dealix.opencode_headless_canary.v1",
            "returncode": result.get("returncode"),
            "duration_s": result.get("duration_s"),
            "stdout": (result.get("stdout") or "").strip()[:200],
            "stderr": (result.get("stderr") or "")[:300],
            "argv": result.get("argv"),
            "external_effect": "NONE",
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        print("OPENCODE_HEADLESS_CANARY=" + ("PASS" if ok else "FAIL"))
        return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
