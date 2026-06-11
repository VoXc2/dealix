"""Run AI evals in demo mode.

Usage:
    python3 scripts/run_ai_evals.py --mode demo
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from lib.ai_router import AIRouter
from lib.ai_safety import check_output, check_flags  # noqa: E402

EVALS_DIR = REPO_ROOT / "business" / "ai" / "evals"
OUT_DIR = REPO_ROOT / "reports" / "ai"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def run_eval_file(router: AIRouter, path: Path) -> list[dict]:
    cases = json.loads(path.read_text(encoding="utf-8")).get("cases", [])
    results: list[dict] = []
    for c in cases:
        task = c.get("task", "lead_scoring_explanation")
        ctx = c.get("input", {})
        result = router.call(task, task, ctx)
        check = check_output(result.output)
        flags = check_flags(result.safety_flags)
        ok = check["safe"] and flags["ok"]
        results.append({
            "id": c.get("id"),
            "task": task,
            "provider": result.provider,
            "model": result.model,
            "prompt_version": result.prompt_version,
            "output_preview": result.output[:120],
            "safe": check["safe"],
            "flags_ok": flags["ok"],
            "ok": ok,
            "findings": check["findings"],
        })
    return results


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["demo", "production"], default="demo")
    args = parser.parse_args()

    router = AIRouter(mode=args.mode)
    today = dt.date.today().isoformat()
    all_results: list[dict] = []
    for f in EVALS_DIR.glob("*.json"):
        if f.name.startswith("_"):
            continue
        try:
            r = run_eval_file(router, f)
            all_results.extend(r)
        except Exception as e:  # noqa: BLE001
            all_results.append({"file": f.name, "ok": False, "error": str(e)})

    total = len(all_results)
    ok = sum(1 for r in all_results if r.get("ok"))
    out = OUT_DIR / f"evals-{today}.md"
    lines: list[str] = []
    lines.append(f"# AI Evals — {today}")
    lines.append("")
    lines.append(f"Mode: {args.mode}")
    lines.append(f"Passed: {ok}/{total}")
    lines.append("")
    for r in all_results:
        lines.append(f"## {r.get('id', '?')}")
        for k, v in r.items():
            lines.append(f"- {k}: {v}")
        lines.append("")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {out} ({ok}/{total} passed)")
    return 0 if ok == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
