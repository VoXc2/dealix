"""Verify readiness for controlled-live outbound activation.

The verifier is intentionally fail-closed. Draft-only operation can remain
healthy while this command returns NOT_READY. Exit 0 is reserved for a future
state where every live-send prerequisite, including durable suppression, is
independently proven.

Checks:
1. Policy gate exists and enforces required gates.
2. Defaults remain fail-closed.
3. Blocked claims are populated.
4. Consent, suppression, and rate-limit guards are importable.
5. Suppression durability is proven before controlled-live eligibility.
6. Channel coverage exists.
7. Draft-mode evaluation remains blocked from external execution.
8. Company Intelligence safety invariants remain intact.
9. Source code does not hardcode EXTERNAL_SEND_ENABLED=true.

Exit 0 = READY, exit 1 = NOT READY.
"""
from __future__ import annotations

import importlib
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))

PASS = 0
FAIL = 0


def check(label: str, condition: bool, detail: str = "") -> None:
    global PASS, FAIL
    if condition:
        PASS += 1
        print(f"  PASS {label}")
    else:
        FAIL += 1
        msg = f"  FAIL {label}"
        if detail:
            msg += f" - {detail}"
        print(msg)


print("=== Controlled-Live Outbound Readiness ===\n")

print("[1] Policy gate")
try:
    from app.outbound.policy_gate import (
        BLOCKED_CLAIMS,
        CHANNELS,
        default_safety_status,
        evaluate_email_send,
        get_outbound_mode,
        is_external_send_enabled,
    )

    check("policy_gate imports", True)
except ImportError as exc:
    check("policy_gate imports", False, str(exc))
    print("CONTROLLED_LIVE_READINESS=NOT_READY (policy gate unavailable)")
    raise SystemExit(1) from exc

print("\n[2] Fail-closed defaults")
safe_env: dict[str, str] = {}
check(
    "EXTERNAL_SEND_ENABLED defaults false",
    not is_external_send_enabled(safe_env),
)
check(
    "OUTBOUND_MODE defaults draft_only",
    get_outbound_mode(safe_env) == "draft_only",
)
status = default_safety_status(safe_env)
check("safe_to_send defaults false", status["safe_to_send"] is False)
check("email_send_enabled defaults false", status["email_send_enabled"] is False)
check("whatsapp_send_enabled defaults false", status["whatsapp_send_enabled"] is False)
check("sms_send_enabled defaults false", status["sms_send_enabled"] is False)

print("\n[3] Content safety")
check("blocked_claims populated", len(BLOCKED_CLAIMS) >= 5)
check("'guaranteed roi' in blocked", "guaranteed roi" in BLOCKED_CLAIMS)
check("'مضمون' in blocked", "مضمون" in BLOCKED_CLAIMS)

print("\n[4] Cross-cutting guards")
for mod_name in [
    "app.outbound.consent",
    "app.outbound.rate_limiter",
    "app.outbound.suppression",
]:
    try:
        importlib.import_module(mod_name)
        check(f"{mod_name} importable", True)
    except ImportError as exc:
        check(f"{mod_name} importable", False, str(exc))

print("\n[5] Suppression durability")
try:
    from app.outbound.suppression import (
        persistent_suppression_ready,
        suppression_backend_kind,
    )

    backend = suppression_backend_kind()
    durable = persistent_suppression_ready()
    check(
        "suppression backend is not process memory",
        backend != "memory",
        f"active backend={backend}",
    )
    check("persistent suppression is proven", durable)
except ImportError as exc:
    check("suppression durability API imports", False, str(exc))

print("\n[6] Channel coverage")
check("email channel", "email" in CHANNELS)
check("whatsapp channel", "whatsapp" in CHANNELS)
check("sms channel", "sms" in CHANNELS)

print("\n[7] Draft-mode evaluation (no env vars)")
eval_result = evaluate_email_send(
    message={"status": "approved", "body": "test opt-out إيقاف"},
    contact={
        "email": "test@example.com",
        "verification_status": "approved_to_send",
        "source_url": "https://example.com",
    },
    env={},
)
check("email blocked from external send in draft mode", not eval_result.safe_to_send)
check("mode is draft_only", eval_result.mode == "draft_only")

print("\n[8] Company Intelligence safety invariants")
try:
    from datetime import date

    from dealix.company_intelligence.daily_command_engine import (
        DailyCommandBrief,
        DailyHealthAssessment,
    )

    try:
        DailyCommandBrief(
            tenant_id="test",
            brief_id="test",
            brief_date=date.today(),
            health=DailyHealthAssessment(),
            execution_allowed=True,
            source_id="test",
        )
        check("execution_allowed=True rejected", False, "should have raised")
    except ValueError:
        check("execution_allowed=True rejected", True)
except ImportError as exc:
    check("company intelligence import", False, str(exc))

try:
    from dealix.company_intelligence.pipeline_engine import RevenueForecast

    try:
        RevenueForecast(
            tenant_id="test",
            forecast_id="test",
            forecast_period="q1",
            recognized_revenue=True,
            source_id="test",
        )
        check("recognized_revenue=True rejected", False, "should have raised")
    except ValueError:
        check("recognized_revenue=True rejected", True)
except ImportError as exc:
    check("pipeline engine import", False, str(exc))

print("\n[9] No hardcoded live-send in source code")
dangerous_patterns = [
    "EXTERNAL_SEND_ENABLED=true",
    'EXTERNAL_SEND_ENABLED="true"',
    "EXTERNAL_SEND_ENABLED='true'",
]
source_dirs = [ROOT / "api", ROOT / "app", ROOT / "core", ROOT / "dealix"]
found_hardcoded = False
for directory in source_dirs:
    if not directory.exists():
        continue
    for path in directory.rglob("*.py"):
        content = path.read_text(errors="ignore")
        for line_num, line in enumerate(content.splitlines(), 1):
            stripped = line.strip()
            if (
                stripped.startswith("#")
                or stripped.startswith('"""')
                or stripped.startswith("'''")
            ):
                continue
            for pattern in dangerous_patterns:
                if pattern in line:
                    check(
                        f"no hardcoded {pattern}",
                        False,
                        f"found in {path.relative_to(ROOT)}:{line_num}",
                    )
                    found_hardcoded = True
if not found_hardcoded:
    check("no hardcoded EXTERNAL_SEND_ENABLED=true", True)

print(f"\n{'=' * 50}")
if FAIL == 0:
    print(f"CONTROLLED_LIVE_READINESS=READY ({PASS} checks passed)")
    raise SystemExit(0)

print(f"CONTROLLED_LIVE_READINESS=NOT_READY ({FAIL} failed, {PASS} passed)")
raise SystemExit(1)
