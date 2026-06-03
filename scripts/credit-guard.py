#!/usr/bin/env python3
"""Dealix Credit Guard - Checks OpenRouter balance before starting."""

import json
import os
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

# Load .env.local if exists
env_file = Path(__file__).parent.parent / ".env.local"
if env_file.exists():
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, value = line.partition("=")
            os.environ[key.strip()] = value.strip()

api_key = os.getenv("OPENROUTER_API_KEY", "")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

if not api_key or len(api_key) < 20:
    print("[CRITICAL] OPENROUTER_API_KEY not set or too short!")
    print("[HINT] Add your key to .env.local")
    sys.exit(1)

print("=" * 55)
print("  DEALIX CREDIT GUARD")
print("=" * 55)

try:
    req = Request(
        f"{base_url.rstrip('/')}/auth/key",
        headers={"Authorization": f"Bearer {api_key}"}
    )
    with urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    label = data.get("data", {}).get("label", "unknown")
    usage = data.get("data", {}).get("usage", 0)
    limit = data.get("data", {}).get("limit")
    rate_limit = data.get("data", {}).get("rate_limit", {})
    requests_per_min = rate_limit.get("requests", "?")
    interval = rate_limit.get("interval", "?")

    print(f"  Key:        {label}")
    print(f"  Usage:      ${usage:.4f}")
    print(f"  Limit:      {'Unlimited' if limit is None else f'${limit:.2f}'}")
    print(f"  Rate Limit: {requests_per_min} requests/{interval}")

    if limit is not None and limit > 0:
        remaining = limit - usage
        pct = (remaining / limit) * 100
        print(f"  Remaining:  ${remaining:.4f} ({pct:.1f}%)")

        if pct < 10:
            print("")
            print("  [CRITICAL] Less than 10% credits remaining!")
            print("  [ACTION] Switching to GEAR 1 (DeepSeek) only")
            print("  [ACTION] Top up at: https://openrouter.ai/settings/credits")
        elif pct < 30:
            print("")
            print("  [WARNING] Less than 30% credits remaining")
            print("  [HINT] Consider using GEAR 1 more often")
        else:
            print("")
            print("  [OK] Credits are healthy")

except HTTPError as e:
    if e.code == 401:
        print("  [FAIL] Invalid API key")
        sys.exit(1)
    elif e.code == 402:
        print("  [FAIL] Insufficient credits")
        print("  [ACTION] Top up at: https://openrouter.ai/settings/credits")
        sys.exit(1)
    else:
        print(f"  [FAIL] HTTP {e.code}: {e.reason}")
        sys.exit(1)
except URLError:
    print("  [FAIL] Cannot reach OpenRouter")
    print("  [HINT] Check internet connection")
    sys.exit(1)
except Exception as e:
    print(f"  [FAIL] {e}")
    sys.exit(1)

print("=" * 55)
sys.exit(0)
