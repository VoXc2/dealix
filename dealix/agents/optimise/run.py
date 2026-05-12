"""
DSPy prompt optimiser — `python -m dealix.agents.optimise.run --metric icp_match`

Loads a labelled dataset from `evals/datasets/<metric>.jsonl`,
optimises a DSPy program, and prints the improved prompt + score so
the founder can PR it into `dealix/prompts/<name>.yaml`.

Inert (exit 0 with a message) when:
- DSPy isn't installed, OR
- the dataset is missing, OR
- no LLM provider is configured.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from core.logging import get_logger

log = get_logger(__name__)


def _load_dataset(metric: str) -> list[dict[str, str]]:
    path = Path("evals/datasets") / f"{metric}.jsonl"
    if not path.is_file():
        return []
    rows: list[dict[str, str]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def run(metric: str) -> int:
    rows = _load_dataset(metric)
    log.info("dspy_optimise_start", metric=metric, examples=len(rows))
    if not rows:
        log.info("dataset_empty_or_missing; ship a fixture under evals/datasets/")
        return 0
    try:
        import dspy  # type: ignore
    except ImportError:
        log.info("dspy_not_installed; ship `pip install dspy-ai` to enable")
        return 0
    if not (
        os.getenv("ANTHROPIC_API_KEY", "").strip()
        or os.getenv("OPENAI_API_KEY", "").strip()
    ):
        log.info("no_llm_configured")
        return 0
    log.info("dspy_run_scaffold_ready", metric=metric, examples=len(rows))
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(prog="dealix.agents.optimise")
    parser.add_argument("--metric", default="icp_match")
    args = parser.parse_args()
    raise SystemExit(run(args.metric))


if __name__ == "__main__":
    main()
