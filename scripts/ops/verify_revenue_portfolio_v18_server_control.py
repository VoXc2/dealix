#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "ops" / "activate_revenue_portfolio_v18.sh"
GATE = ROOT / "dealix" / "config" / "first_launch_offer_gate.yaml"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def main() -> int:
    require(SCRIPT.exists(), "activation script missing")
    require(GATE.exists(), "first launch gate missing")

    text = SCRIPT.read_text(encoding="utf-8")
    gate = GATE.read_text(encoding="utf-8")

    fail_closed = (
        "external_send_allowed: false" in gate
        and "warm_consented_only" in gate
    )
    channel_governed = (
        "external_send_allowed: true" in gate
        and "channel_eligible_evidence_backed" in gate
    )
    require(
        fail_closed or channel_governed,
        "launch gate must match a recognized Dealix authority mode",
    )

    required_tokens = [
        "FIRST_VERIFIED_PAID_PILOT",
        "FAIL_CLOSED",
        "CHANNEL_GOVERNED_OPEN",
        "SERVER_CONTROL_EXTERNAL_SEND=BLOCKED",
        "HERMES_FOREGROUND_EXECUTION=DISABLED",
        "DAILY_OPS_FOREGROUND_EXECUTION=DISABLED",
        "research_is_not_relationship",
        "payment_requires_evidence",
        "synthetic_is_not_customer_proof",
        "self_test_never_qualifies",
        "provider_acceptance_is_not_delivery",
        "new_timer_created\":False",
        "new_cron_created\":False",
        "new_agent_created\":False",
        "1277",
        "1273",
        "1274",
        "1275",
        "1276",
        "1281",
        "1283",
    ]
    for token in required_tokens:
        require(token in text, f"missing required V18.1 contract token: {token}")

    forbidden_patterns = {
        "new timer creation": r"systemctl\s+enable\s+--now|systemctl\s+enable\s+.*timer",
        "cron creation": r"hermes\s+cron\s+create|crontab\s+-",
        "main merge": r"git\s+merge\s+.*main|gh\s+pr\s+merge",
        "production deploy": r"railway\s+up|vercel\s+deploy|docker\s+compose\s+up",
        "external email send": r"gmail.*send|send_message",
        "payment mutation": r"moyasar|stripe.*charge|payment.*capture",
        "foreground hermes chat": r"hermes.*chat\s+--query-file|\$HERMES.*chat\s+--query-file",
        "foreground daily ops": r"python3\s+.*run_dealix_daily_ops\.py",
    }
    for label, pattern in forbidden_patterns.items():
        require(
            re.search(pattern, text, re.IGNORECASE) is None,
            f"activation script contains forbidden {label}",
        )

    require(
        "timeout 900 as_dealix" not in text,
        "timeout cannot execute shell function as_dealix",
    )
    require(
        'runuser -u "$RUN_USER"' in text,
        "bounded runuser execution missing",
    )
    require("flock -n 9" in text, "single-run lock missing")
    require(
        "ACTIVE_COMMERCIAL_AUTHORITY_MODE" in text,
        "authority mode must be recorded",
    )
    require(
        "TRUTH_FIREWALL_ATTENTION" in text,
        "economic-truth mismatch must be surfaced",
    )

    print("PASS: V18.1 server control safety/authority contract")
    return 0


if __name__ == "__main__":
    sys.exit(main())
