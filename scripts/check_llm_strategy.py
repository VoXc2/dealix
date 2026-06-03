#!/usr/bin/env python3
"""Diagnostic script to verify Minimax-First LLM Strategy."""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from dealix.llm.strategy import LLMStrategyRouter, ModelTier, TaskType
except ImportError as e:
    print(f"[FAIL] Import error: {e}")
    print("Hint: run: pip install pydantic")
    sys.exit(1)


def main():
    print("=" * 60)
    print("DEALIX LLM STRATEGY AUDIT")
    print("=" * 60)

    api_key = os.getenv("OPENROUTER_API_KEY", "")
    masked = api_key[:12] + "..." if len(api_key) > 20 else "MISSING"
    print(f"\n[+] OPENROUTER_API_KEY: {masked}")

    base_url = os.getenv("OPENROUTER_BASE_URL", "")
    expected = "https://openrouter.ai/api/v1"
    print(f"[+] OPENROUTER_BASE_URL: {base_url}")
    ok_url = base_url == expected
    print(f"    Valid: {'YES' if ok_url else 'NO - Expected: ' + expected}")

    router = LLMStrategyRouter()

    print("\n[+] MODEL ASSIGNMENTS:")
    for tier in ModelTier:
        print(f"    [{tier.value.upper():10s}] -> {router._MODEL_IDS[tier]}")

    print("\n[+] TASK ROUTING CHAINS:")
    for task in TaskType:
        chain = router.resolve(task)
        names = " -> ".join([c.model_id.split("/")[-1] for c in chain])
        print(f"    {task.value:25s}: {names}")

    models = list(router._MODEL_IDS.values())
    minimax_count = sum(1 for m in models if m.startswith("minimax"))
    print(f"\n[+] MINIMAX COVERAGE: {minimax_count}/4 models ({minimax_count*25}%)")
    if minimax_count >= 3:
        print("    [PASS] MINIMAX-FIRST ACTIVE")
    else:
        print("    [WARN] FALLBACK-HEAVY CONFIG")

    if not api_key or len(api_key) < 20:
        print("\n[FAIL] No valid OPENROUTER_API_KEY")
        sys.exit(1)

    if not ok_url:
        print("\n[FAIL] OPENROUTER_BASE_URL incorrect")
        sys.exit(1)

    print("\n[PASS] ALL CHECKS PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
