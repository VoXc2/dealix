"""Article 13 compliance — no Wave 4 architecture before 3 paid pilots.

Per `docs/DEALIX_OPERATING_CONSTITUTION.md` Article 13 + the 30-day
plan in `/root/.claude/plans/vivid-baking-quokka.md`, the following
architectural pieces are explicitly OUT-OF-SCOPE until 3 paid pilots
trigger Wave 4:

- Multi-tenant Postgres RLS
- Live HubSpot/Zoho/Salesforce CRM connectors
- Self-serve CSV bulk upload UI
- Calendly webhook handler
- ZATCA Phase 2 e-invoicing automation
- LangFuse / OpenTelemetry deep instrumentation
- Full Next.js frontend rebuild

This test fails CI if any of these surfaces appears in customer-facing
or production code (excluding deferred-roadmap docs which legitimately
discuss them).

The test scans `api/`, `landing/`, `core/`, `auto_client_acquisition/`
for forbidden patterns. Allowlists are explicit.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]


# Patterns that — if present in production code — indicate a Wave 4
# architectural piece has been built prematurely.
FORBIDDEN_PATTERNS: list[tuple[str, re.Pattern[str], str]] = [
    (
        "multi_tenant_rls",
        re.compile(r"\bCREATE\s+POLICY\b|\bENABLE\s+ROW\s+LEVEL\s+SECURITY\b", re.IGNORECASE),
        "Postgres RLS policies — Wave 4 only after Pilot #2",
    ),
    (
        "calendly_webhook",
        re.compile(r"calendly[._-]?webhook|/api/v1/webhooks/calendly", re.IGNORECASE),
        "Calendly webhook handler — Wave 4 deferral",
    ),
    (
        "zatca_phase2_automation",
        re.compile(r"zatca[._-]?phase[_-]?2[._-]?automation|zatca_einvoice_send", re.IGNORECASE),
        "ZATCA Phase 2 automation — Wave 4 deferral",
    ),
]


# Files and dirs allowed to mention these terms (docs, planning, tests).
ALLOWLIST_PATHS: list[str] = [
    "docs/",
    "tests/test_article_13_compliance.py",
    ".claude/",
    "node_modules/",
    "__pycache__",
    ".git/",
    # Pre-existing webhook receiver stubs — receive-only, manual downstream
    # action (per Wave 10.6 report: "Calendly webhook handler — manual
    # logging via dealix_demo_outcome.py"). Article 13 forbids automated
    # demo→delivery pipelines, NOT the bare receiving endpoint.
    "api/routers/webhooks.py",
    "api/security/webhook_signatures.py",
    # Founder launch-status panel only *reports* whether CALENDLY_WEBHOOK_SECRET
    # is set (a read-only env-var status field) — it builds no Calendly webhook
    # handler. The forbidden-pattern regex over-matches the env-var name.
    "api/routers/founder_launch_status.py",
]


def _is_allowlisted(path: Path) -> bool:
    rel = path.relative_to(REPO).as_posix()
    return any(rel.startswith(p) or p in rel for p in ALLOWLIST_PATHS)


def _scan_dir(root: Path, suffixes: tuple[str, ...]) -> list[tuple[str, str, str]]:
    """Return list of (file, pattern_name, message)."""
    violations: list[tuple[str, str, str]] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix not in suffixes:
            continue
        if _is_allowlisted(path):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for name, pattern, message in FORBIDDEN_PATTERNS:
            if pattern.search(text):
                violations.append((path.relative_to(REPO).as_posix(), name, message))
    return violations


def test_no_wave4_architecture_in_production_code():
    """Scan api/, core/, auto_client_acquisition/ for Wave 4 surfaces."""
    targets = [
        REPO / "api",
        REPO / "core",
        REPO / "auto_client_acquisition",
        REPO / "db" / "migrations",
    ]
    suffixes = (".py", ".sql")
    all_violations: list[tuple[str, str, str]] = []
    for target in targets:
        if not target.exists():
            continue
        all_violations.extend(_scan_dir(target, suffixes))
    assert not all_violations, (
        "Article 13 violation — Wave 4 architecture detected in production code "
        "before 3 paid pilots. See docs/DEALIX_OPERATING_CONSTITUTION.md Article 13.\n"
        + "\n".join(f"  {f}: {n} — {m}" for f, n, m in all_violations)
    )


def test_no_wave4_architecture_in_landing():
    """Scan landing/ for Wave 4 surfaces."""
    landing = REPO / "landing"
    if not landing.exists():
        pytest.skip("landing/ not present")
    suffixes = (".html", ".js")
    violations = _scan_dir(landing, suffixes)
    assert not violations, (
        "Article 13 violation — Wave 4 surface in customer-facing landing code.\n"
        + "\n".join(f"  {f}: {n} — {m}" for f, n, m in violations)
    )


def test_30day_plan_file_exists():
    """The plan file documents the Article 13 boundary; if it disappears,
    we lose the audit trail."""
    plan = Path("/root/.claude/plans/vivid-baking-quokka.md")
    if not plan.exists():
        pytest.skip("Plan file not present in this environment")
    text = plan.read_text(encoding="utf-8")
    assert "Article 13" in text, "Plan file must reference Article 13"
    assert "Wave 4" in text, "Plan file must reference Wave 4 deferral"
    assert "3 paid pilots" in text or "3 pilots" in text, (
        "Plan file must reference the 3-pilot trigger"
    )
