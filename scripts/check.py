#!/usr/bin/env python3
"""Dealix System Check - Validates entire setup."""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

print("=" * 55)
print("  DEALIX SYSTEM CHECK v3.0")
print("=" * 55)

checks_passed = 0
checks_total = 0

# 1. Python version
checks_total += 1
print(f"\n[1] Python: {sys.version.split()[0]}", end=" ")
if sys.version_info >= (3, 11):
    print("[OK]")
    checks_passed += 1
else:
    print("[WARN] Python 3.11+ recommended")

# 2. .env.local
checks_total += 1
env_file = Path(__file__).parent.parent / ".env.local"
print("[2] .env.local: ", end="")
if env_file.exists():
    content = env_file.read_text(encoding="utf-8")
    has_key = "OPENROUTER_API_KEY=sk-or-v1-" in content
    has_url = "OPENROUTER_BASE_URL" in content
    has_g1 = "GEAR1_MODEL" in content
    if has_key and has_url and has_g1:
        print("[OK]")
        checks_passed += 1
    else:
        print("[WARN] Missing fields")
else:
    print("[FAIL] File not found")

# 3. Engine module
checks_total += 1
print("[3] LLM Engine: ", end="")
try:
    from dealix.llm.engine import DealixEngine, Gear
    cfg = DealixEngine.get(Gear.DAILY)
    print(f"[OK] Gear 1: {cfg.model_id}")
    checks_passed += 1
except Exception as e:
    print(f"[FAIL] {e}")

# 4. Strategy module
checks_total += 1
print("[4] LLM Strategy: ", end="")
try:
    from dealix.llm.strategy import LLMStrategyRouter, TaskType
    chain = LLMStrategyRouter().resolve(TaskType.CODE_GENERATION)
    names = " -> ".join([c.model_id.split("/")[-1] for c in chain])
    print(f"[OK] {names}")
    checks_passed += 1
except Exception as e:
    print(f"[FAIL] {e}")

# 5. Aider config
checks_total += 1
print("[5] Aider config: ", end="")
aider_conf = Path(__file__).parent.parent / ".aider.conf.yml"
if aider_conf.exists():
    print("[OK]")
    checks_passed += 1
else:
    print("[WARN] Not found (run aider to create)")

# 6. Aiderignore
checks_total += 1
print("[6] Aiderignore: ", end="")
aider_ign = Path(__file__).parent.parent / ".aiderignore"
if aider_ign.exists():
    lines = aider_ign.read_text(encoding="utf-8").strip().splitlines()
    print(f"[OK] {len(lines)} rules")
    checks_passed += 1
else:
    print("[WARN] Not found")

# 7. Git config
checks_total += 1
print("[7] Git encoding: ", end="")
import subprocess

try:
    qp = subprocess.run(["git", "config", "--global", "core.quotepath"], capture_output=True, text=True).stdout.strip()
    enc = subprocess.run(["git", "config", "--global", "i18n.logOutputEncoding"], capture_output=True, text=True).stdout.strip()
    if qp == "off" and enc == "utf-8":
        print("[OK]")
        checks_passed += 1
    else:
        print(f"[WARN] quotepath={qp}, encoding={enc}")
except:
    print("[WARN] Git not configured")

# 8. OpenRouter connection
checks_total += 1
print("[8] OpenRouter: ", end="")
try:
    import json
    from urllib.request import Request, urlopen
    api_key = os.getenv("OPENROUTER_API_KEY", "")
    if not api_key or len(api_key) < 20:
        # Try loading from .env.local
        if env_file.exists():
            for line in env_file.read_text(encoding="utf-8").splitlines():
                if line.startswith("OPENROUTER_API_KEY="):
                    api_key = line.split("=", 1)[1].strip()
    if api_key and len(api_key) > 20:
        req = Request("https://openrouter.ai/api/v1/auth/key", headers={"Authorization": f"Bearer {api_key}"})
        with urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            print("[OK] Connected")
            checks_passed += 1
    else:
        print("[WARN] No API key")
except Exception as e:
    print(f"[WARN] {str(e)[:40]}")

# Summary
print(f"\n{'=' * 55}")
print(f"  RESULT: {checks_passed}/{checks_total} checks passed")
if checks_passed >= 6:
    print("  STATUS: READY TO LAUNCH")
    sys.exit(0)
else:
    print("  STATUS: NEEDS ATTENTION")
    sys.exit(1)
