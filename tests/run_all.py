#!/usr/bin/env python3
"""
Minimal stdlib test runner for Dealix Agent #2 tests.

Why: this repo has no pytest installed. These tests are written to be runnable
BOTH by pytest (def test_*) and by this runner. Run:  python3 tests/run_all.py
"""
import importlib.util
import sys
import traceback
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent
ROOT = TESTS_DIR.parent
for p in (str(ROOT), str(ROOT / "scripts"), str(TESTS_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    files = sorted(TESTS_DIR.glob("test_*.py"))
    passed = failed = 0
    failures = []
    for f in files:
        mod = load_module(f)
        for name in dir(mod):
            if name.startswith("test_") and callable(getattr(mod, name)):
                fn = getattr(mod, name)
                try:
                    fn()
                    passed += 1
                    print(f"  PASS  {f.name}::{name}")
                except Exception as e:  # noqa: BLE001
                    failed += 1
                    failures.append((f.name, name, e, traceback.format_exc()))
                    print(f"  FAIL  {f.name}::{name}  -> {e}")
    print("-" * 70)
    print(f"  {passed} passed, {failed} failed")
    if failures:
        print("\nFAILURE DETAILS:")
        for fname, tname, _e, tb in failures:
            print(f"\n### {fname}::{tname}\n{tb}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
