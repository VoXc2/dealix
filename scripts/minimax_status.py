#!/usr/bin/env python3
"""MiniMax factory status — read-only health snapshot.

No network. No external calls. No PII. Exits 0 on success.

Prints the model registry (entries under data/ai_ops/model_registry.yaml
conforming to schemas/model_registry.schema.json), the API key presence
(never values), the default model, cost class, allowed/forbidden tasks, and
status per entry. The output is the one-line status the founder reads every
morning.

Usage:
    python scripts/minimax_status.py
    make minimax-status
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "ai_ops" / "model_registry.yaml"


def _read_registry(path: Path) -> dict:
    """Load the YAML registry without third-party deps (with PyYAML fallback).

    The registry is intentionally small and well-formed. We try PyYAML first
    (it handles all YAML semantics correctly); if it is not installed we
    return an error so the founder sees the missing dep explicitly rather
    than silently reading the wrong shape.
    """
    if not path.exists():
        raise SystemExit(f"DEALIX_MINIMAX_STATUS=ERROR registry_missing:{path}")
    try:
        import yaml  # type: ignore
    except ImportError:
        raise SystemExit("DEALIX_MINIMAX_STATUS=ERROR pyyaml_required")
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _is_minimax_entry(entry: dict) -> bool:
    """An entry belongs to the MiniMax family if its provider is `minimax`."""
    return (entry.get("provider") or "").lower() == "minimax"


def _api_key_status_for(entry: dict, env: dict[str, str]) -> str:
    """Report api_key presence for the entry's provider. Never print values."""
    # The schema does not carry api_key_env directly; we infer:
    # provider == "minimax" -> MINIMAX_API_KEY, provider == "anthropic" -> ANTHROPIC_API_KEY.
    provider = (entry.get("provider") or "").lower()
    env_map = {
        "minimax": "MINIMAX_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
    }
    env_name = env_map.get(provider, "")
    if not env_name:
        return "n/a"
    return "yes" if env.get(env_name) else "no"


def main() -> int:
    try:
        registry = _read_registry(REGISTRY)
    except SystemExit as e:
        print(str(e))
        return 1

    entries = registry.get("entries") or []
    if not entries:
        print("DEALIX_MINIMAX_STATUS=ERROR empty_registry")
        return 1

    env = dict(os.environ)

    print("DEALIX_MINIMAX_STATUS")
    header = f"{'model_id':<32}{'provider':<14}{'api_key_set':<14}{'cost_class':<12}{'status':<12}{'allowed_tasks':<22}{'forbidden_tasks':<20}"
    print(header)
    print("-" * len(header))
    for e in entries:
        mid = e.get("model_id", "?")
        provider = e.get("provider", "?")
        api_key_set = _api_key_status_for(e, env)
        cost_class = e.get("cost_class", "?")
        status = e.get("status", "?")
        allowed = ",".join(e.get("allowed_tasks") or []) or "-"
        forbidden = ",".join(e.get("forbidden_tasks") or []) or "-"
        print(f"{mid:<32}{provider:<14}{api_key_set:<14}{cost_class:<12}{status:<12}{allowed:<22}{forbidden:<20}")

    n_minimax = sum(1 for e in entries if _is_minimax_entry(e))
    print("")
    print(f"minimax_entries: {n_minimax} of {len(entries)}")
    print("DEALIX_MINIMAX_STATUS=OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
