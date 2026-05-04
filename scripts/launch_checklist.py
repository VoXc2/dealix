#!/usr/bin/env python3
"""
DEALIX_LAUNCH_CHECKLIST — comprehensive pre-launch validation.

Builds on launch_readiness_check (which validates the *technical* contract)
and adds *commercial* validations that the Saudi Revenue Command OS needs
before pointing real customers at it:

    1. Static foundation — runs launch_readiness_check (compileall, pytest,
       routes, smoke, arch audit, env sanity, files exist).
    2. Frontend audit    — runs forbidden_claims_audit on all 16 pages.
    3. Service Tower     — every contract in catalog scores >= 80 (sellable).
    4. Live-action gates — all 8 default-False flags resolve False.
    5. Commercial endpoints smoke — hits the new APIs in-process so we know
       they wire end-to-end:
          /api/v1/services/catalog
          /api/v1/cards/feed?role=ceo
          /api/v1/role-briefs/daily?role=sales_manager
          /api/v1/whatsapp/brief?role=growth_manager
          /api/v1/proof-ledger/units
          /api/v1/self-growth/today
          /api/v1/observability/quality
          /api/v1/daily-ops/windows
          /api/v1/calls/dial-live  (must return 403)
          /api/v1/whatsapp/brief/send-internal  (must return 403)

Result codes:
    LAUNCH_READY    — all green; safe to point staging traffic at it
    BLOCKED         — at least one check failed; do NOT point customers
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO))


@dataclass
class CheckResult:
    name: str
    passed: bool
    detail: str = ""


@dataclass
class ChecklistReport:
    checks: list[CheckResult] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return all(c.passed for c in self.checks)

    @property
    def fail_count(self) -> int:
        return sum(1 for c in self.checks if not c.passed)


def _set_test_env() -> None:
    """Force in-process safe defaults so this script can run anywhere."""
    os.environ.setdefault("APP_ENV", "test")
    os.environ.setdefault("APP_DEBUG", "false")
    os.environ.setdefault("ANTHROPIC_API_KEY", "test")
    os.environ.setdefault("DEEPSEEK_API_KEY", "test")
    os.environ.setdefault("GROQ_API_KEY", "test")
    os.environ.setdefault("GLM_API_KEY", "test")
    os.environ.setdefault("GOOGLE_API_KEY", "test")
    os.environ.setdefault("WHATSAPP_ALLOW_LIVE_SEND", "false")
    os.environ.setdefault("GMAIL_ALLOW_LIVE_SEND", "false")
    os.environ.setdefault("MOYASAR_ALLOW_LIVE_CHARGE", "false")
    os.environ.setdefault("LINKEDIN_ALLOW_AUTO_DM", "false")
    os.environ.setdefault("RESEND_ALLOW_LIVE_SEND", "false")
    os.environ.setdefault("WHATSAPP_ALLOW_INTERNAL_SEND", "false")
    os.environ.setdefault("WHATSAPP_ALLOW_CUSTOMER_SEND", "false")
    os.environ.setdefault("CALLS_ALLOW_LIVE_DIAL", "false")
    # Reuse the test conftest's in-memory SQLite so DB writes don't need PG.
    os.environ.setdefault(
        "DATABASE_URL",
        "sqlite+aiosqlite:///file:dealix_checklist?mode=memory&cache=shared&uri=true",
    )


# ── Step 1: launch_readiness_check ────────────────────────────────


def step_launch_readiness() -> CheckResult:
    """Lighter version: run the static checks but skip pytest (already covered
    by CI). We still want compileall + routes + smoke + arch_audit + env."""
    from scripts.launch_readiness_check import run_checks
    report = run_checks(skip_pytest=True)
    if report.passed:
        return CheckResult("launch_readiness", True,
                           f"GO_PRIVATE_BETA ({len(report.steps)} checks)")
    fails = [s.name for s in report.steps if not s.passed]
    return CheckResult("launch_readiness", False, "fails: " + ", ".join(fails))


# ── Step 2: forbidden_claims_audit ────────────────────────────────


def step_frontend_audit() -> CheckResult:
    from scripts.forbidden_claims_audit import run_audit
    report = run_audit()
    if report.passed:
        return CheckResult("frontend_audit", True,
                           f"{report.pass_count}/{report.pass_count + report.fail_count} PASS")
    return CheckResult("frontend_audit", False, f"{report.fail_count} fails")


# ── Step 3: Service Tower excellence ─────────────────────────────


def step_service_tower_excellence() -> CheckResult:
    from auto_client_acquisition.service_tower.excellence_score import all_excellence
    out = all_excellence()
    summary = out["summary"]
    if summary["internal_only"] > 0 or summary["beta_only"] > 0:
        return CheckResult(
            "service_tower_excellence", False,
            f"internal_only={summary['internal_only']} beta_only={summary['beta_only']}",
        )
    return CheckResult(
        "service_tower_excellence", True,
        f"all {summary['total']} sellable, avg={summary['average_score']}",
    )


# ── Step 4: Live-action gates (re-affirm all 8 are False) ────────


_GATES = (
    "whatsapp_allow_live_send",
    "gmail_allow_live_send",
    "moyasar_allow_live_charge",
    "linkedin_allow_auto_dm",
    "resend_allow_live_send",
    "whatsapp_allow_internal_send",
    "whatsapp_allow_customer_send",
    "calls_allow_live_dial",
)


def step_live_action_gates() -> CheckResult:
    from core.config.settings import Settings
    s = Settings()
    bad = [g for g in _GATES if getattr(s, g, None) is True]
    if bad:
        return CheckResult("live_action_gates", False, "flipped on: " + ", ".join(bad))
    return CheckResult("live_action_gates", True, f"all {len(_GATES)} gates False")


# ── Step 5: Commercial endpoints smoke (in-process) ──────────────


_ENDPOINTS_GET: tuple[tuple[str, int], ...] = (
    ("/api/v1/services/catalog", 200),
    ("/api/v1/cards/feed?role=ceo", 200),
    ("/api/v1/role-briefs/daily?role=sales_manager", 200),
    ("/api/v1/whatsapp/brief?role=growth_manager", 200),
    ("/api/v1/proof-ledger/units", 200),
    ("/api/v1/self-growth/today", 200),
    ("/api/v1/observability/quality?days=7", 200),
    ("/api/v1/daily-ops/windows", 200),
    ("/api/v1/auth/me", 401),  # no session — must reject
)

_ENDPOINTS_POST_403: tuple[str, ...] = (
    "/api/v1/calls/dial-live",
    "/api/v1/whatsapp/brief/send-internal",
)


async def _smoke_endpoints() -> list[str]:
    from httpx import ASGITransport, AsyncClient
    from api.main import app
    from db.session import init_db

    # Ensure all tables exist in the in-memory SQLite (we run outside pytest).
    try:
        await init_db()
    except Exception:
        pass  # DB might already be initialized

    transport = ASGITransport(app=app)
    failures: list[str] = []
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        for path, expected in _ENDPOINTS_GET:
            r = await client.get(path)
            if r.status_code != expected:
                failures.append(f"GET {path} → {r.status_code} (expected {expected})")
        for path in _ENDPOINTS_POST_403:
            r = await client.post(path, json={"role": "sales_manager"})
            if r.status_code != 403:
                failures.append(f"POST {path} → {r.status_code} (expected 403)")
    return failures


def step_commercial_endpoints() -> CheckResult:
    try:
        failures = asyncio.run(_smoke_endpoints())
    except Exception as exc:  # noqa: BLE001
        return CheckResult("commercial_endpoints", False, f"smoke error: {exc}")
    if failures:
        return CheckResult("commercial_endpoints", False, "; ".join(failures[:5]))
    return CheckResult(
        "commercial_endpoints", True,
        f"{len(_ENDPOINTS_GET) + len(_ENDPOINTS_POST_403)} endpoints OK",
    )


# ── Orchestrator ─────────────────────────────────────────────────


def run() -> ChecklistReport:
    _set_test_env()
    rep = ChecklistReport()
    rep.checks.append(step_launch_readiness())
    rep.checks.append(step_frontend_audit())
    rep.checks.append(step_service_tower_excellence())
    rep.checks.append(step_live_action_gates())
    rep.checks.append(step_commercial_endpoints())
    return rep


def main() -> int:
    report = run()
    print("DEALIX_LAUNCH_CHECKLIST v1.0")
    print("=" * 50)
    for c in report.checks:
        flag = "OK  " if c.passed else "FAIL"
        print(f"[{flag}] {c.name:30s}  — {c.detail}")
    print("=" * 50)
    print("RESULT:", "LAUNCH_READY" if report.passed else "BLOCKED")
    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
