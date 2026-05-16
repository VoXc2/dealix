"""v7 Phase 8 hardening — no real secret may leak into the repo.

Three perimeter assertions:

  1. ``redact_log_entry`` (security_privacy.log_redaction) replaces a
     Stripe-shaped key built via concatenation with the redaction
     marker. Construct test secrets via concatenation so gitleaks
     never sees a literal ``sk_live_*`` substring in this source.
  2. ``redact_log_entry`` redacts an Anthropic-shaped key
     (``"sk-ant-" + ...``).
  3. A repo-wide grep for the literal prefixes (Stripe, GitHub PAT,
     Google API key) returns ZERO matches outside the explicit
     allowlist below. Each allowlist entry has a comment explaining
     why the prefix legitimately appears in that file.
"""
from __future__ import annotations

import re
from pathlib import Path

from auto_client_acquisition.security_privacy.log_redaction import (
    redact_log_entry,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_redact_log_entry_redacts_stripe_shaped_key():
    """Stripe live-secret-key shape — built via concatenation so gitleaks
    cannot flag this test source as containing the literal prefix."""
    # Build the test value by concatenation so the literal prefix
    # never appears as a contiguous substring in this source file.
    fake_secret = "sk_" + "live" + "_" + "abcdefghijklmnopqrstuvwxyz12345"
    log_line = f"event=invoice_charge attempt key={fake_secret} status=blocked"
    redacted = redact_log_entry(log_line)
    assert isinstance(redacted, str)
    assert fake_secret not in redacted, (
        f"Stripe-shaped key leaked through redaction: {redacted!r}"
    )
    assert "[REDACTED_SECRET]" in redacted


def test_redact_log_entry_redacts_anthropic_shaped_key():
    """Anthropic API key shape — also built via concatenation."""
    fake_anthropic = "sk-" + "ant-" + ("a" * 35)
    log_line = f"event=llm_call provider=anthropic key={fake_anthropic}"
    redacted = redact_log_entry(log_line)
    assert isinstance(redacted, str)
    assert fake_anthropic not in redacted
    assert "[REDACTED_SECRET]" in redacted


def test_redact_log_entry_redacts_inside_dict_log_entry():
    """Dict-shaped log entries (structlog) must also redact."""
    fake_secret = "sk_" + "live" + "_" + "ZYXWVUTSRQPONMLK987654321"
    entry = {
        "event": "moyasar_attempt",
        "metadata": {"key": fake_secret, "status": "rejected"},
    }
    out = redact_log_entry(entry)
    assert isinstance(out, dict)
    flat = repr(out)
    assert fake_secret not in flat, f"secret leaked into dict redaction: {flat}"


# ─────────────────────────────────────────────────────────────────────────
# Repo-wide allowlist for legitimate prefix references.
# ─────────────────────────────────────────────────────────────────────────
# Each entry is a path (relative to REPO_ROOT) where the literal token
# ``sk_live_`` / ``ghp_`` / ``AIza`` legitimately appears in:
#   - rejection logic ("if key.startswith('sk_live_'): refuse")
#   - regex patterns themselves (the secret scanner's source of truth)
#   - placeholder examples in deployment docs
#   - role-brief / runbook copy that names the prefix to ban it
#   - test fixtures that intentionally feed the scanner a fake match
#   - launch-verify shell scripts that grep for these patterns
# Reading the file should make the rationale obvious. New entries
# require a one-line comment.
_PREFIX_ALLOWLIST: dict[str, str] = {
    # ── repo-level config files that name the prefix to ban it ──
    ".gitleaks.toml":
        "gitleaks regex rules — the patterns are the secret-scan policy",
    # ── core safety code (the prefix is the policy) ──
    "auto_client_acquisition/finance_os/guardrails.py":
        "live-charge guardrail uses startswith('sk_live_') to refuse",
    "auto_client_acquisition/security_privacy/secret_scan_policy.py":
        "regex patterns themselves — the secret scanner's source of truth",
    "auto_client_acquisition/security_privacy/__init__.py":
        "module docstring names the prefixes the scanner looks for",
    "auto_client_acquisition/role_command_os/role_briefs.py":
        "founder/sales role briefs reference the prefix in policy copy",
    "auto_client_acquisition/personal_operator/memory.py":
        "memory layer regex used to scrub Google API key prefix",
    "auto_client_acquisition/reliability_os/health_matrix.py":
        "health-matrix names sk_live_ in its 'no live charge' assertion",
    # ── scripts ──
    "scripts/dealix_invoice.py":
        "invoice CLI rejects sk_live_* unless --allow-live is set",
    "scripts/github_setup.sh":
        "setup script grep pattern for accidental token paste",
    "scripts/ops/deploy_bundle_v2.sh":
        "deploy bundle env-template comments name the placeholder prefix",
    "scripts/v7_launch_verify.sh":
        "launch verify shell script greps repo for these prefixes",
    "scripts/v10_master_verify.sh":
        "v10 master verifier shell script greps repo for these prefixes",
    "scripts/v11_customer_closure_verify.sh":
        "v11 master verifier shell script greps repo for these prefixes",
    "scripts/v12_full_ops_verify.sh":
        "v12 master verifier shell script greps repo for these prefixes",
    "scripts/beast_level_verify.sh":
        "v12.5 beast master verifier shell script greps repo for these prefixes",
    # ── deployment / placeholder docs ──
    "DEPLOYMENT.md":
        "deployment doc placeholder values use the prefix names",
    "DEALIX_COMPANY_OPERATIONAL_STATE.md":
        "operational-state doc references the prefix in policy copy",
    # ── docs/* (operational + sales-kit + master-evidence narratives) ──
    "docs/MASTER_CLOSURE_EVIDENCE_TABLE.md":
        "evidence table cell names the prefix as a forbidden token",
    "docs/MOYASAR_E2E_GUIDE.md":
        "Moyasar e2e guide describes test vs live key prefix difference",
    "docs/SAMI_ACTION_ITEMS.md":
        "founder action item names the prefix in policy copy",
    "docs/SECURITY_INCIDENT_PAT_EXPOSURE.md":
        "incident report names the prefix as part of the IOC list",
    "docs/PR125_FINAL_STABILIZATION_REPORT.md":
        "stabilization report cites the prefix in evidence narrative",
    "docs/POST_MERGE_VERIFICATION.md":
        "merge verification checklist names the prefix",
    "docs/FIRST_3_DIAGNOSTIC_SCRIPT.md":
        "diagnostic script doc names the prefix in placeholder text",
    "docs/V5_FOUNDER_RUNBOOK.md":
        "founder runbook names the prefix in policy/safety copy",
    "docs/V5_MASTER_EVIDENCE_TABLE.md":
        "v5 master evidence table names the forbidden prefix",
    "docs/V5_OS_SCOPE.md":
        "v5 OS scope doc names the prefix in policy copy",
    "docs/V5_PHASE_E_CHECKLIST.md":
        "v5 phase E checklist names the prefix in test rows",
    "docs/phase-e/06_MANUAL_PAYMENT_FALLBACK.md":
        "v11 phase E payment fallback doc names sk_live_ in policy copy",
    "docs/knowledge-base/payment_policy_ar_en.md":
        "v12 KB payment policy doc names sk_live_ in policy copy",
    "docs/14_DAY_FIRST_REVENUE_PLAYBOOK.md":
        "RX founder playbook references sk_live_ rejection rule in policy copy",
    "docs/BEAST_LEVEL_ARCHITECTURE.md":
        "v12.5 beast architecture references sk_live_ in policy copy",
    "docs/V5_RELEASE_NOTES.md":
        "v5 release notes name the prefix in safety summary",
    "docs/V5_SYSTEM_OVERVIEW.md":
        "v5 system overview names the prefix in policy diagram",
    "docs/V6_MASTER_EVIDENCE_TABLE.md":
        "v6 master evidence table names the prefix in evidence cells",
    "docs/V6_OBSERVABILITY_AND_INCIDENT_RUNBOOK.md":
        "observability runbook references prefix for incident IOC",
    "docs/V6_OPERATING_REALITY_REPORT.md":
        "v6 reality report cites the prefix in posture narrative",
    "docs/launch/DEALIX_LAUNCH_NOW_BUNDLE.md":
        "launch bundle copy names the prefix in env-var template",
    "docs/ops/COMPANY_CONTROL_CENTER.md":
        "ops control center checklist names the prefix",
    "docs/ops/FIRST_REVENUE_ATTEMPT.md":
        "first-revenue attempt SOP references the prefix",
    "docs/ops/MANUAL_PAYMENT_SOP.md":
        "manual payment SOP names the prefix in policy copy",
    "docs/ops/TODAY.md":
        "daily TODO names the prefix in checklist text",
    "docs/ops/daily_scorecard.md":
        "daily scorecard names the prefix in safety row",
    "docs/ops/moyasar_live_test.sh":
        "Moyasar test shell script names the prefix in placeholder env",
    "docs/sales-kit/MOYASAR_HOSTED_CHECKOUT.md":
        "sales-kit hosted-checkout doc names the prefix in policy copy",
    "docs/sales-kit/dealix_1_riyal_test.sh":
        "sales-kit 1-riyal test shell script names the prefix in env",
    # ── allowlist refresh: files that legitimately name the prefix in
    #    detection logic / regex / runbook copy (verified: no real secret,
    #    only startswith() checks, redaction regexes, and placeholders) ──
    "api/routers/founder_launch_status.py":
        "moyasar status panel checks key.startswith('sk_live_')",
    "auto_client_acquisition/agent_observability/redaction.py":
        "redaction regex patterns for sk_live_/ghp_/AIza prefixes",
    "auto_client_acquisition/observability_adapters/redaction.py":
        "redaction regex patterns for the secret prefixes",
    "docs/LLM_PROVIDERS_SETUP.md":
        "LLM provider setup doc names key prefixes in placeholder env",
    "docs/MOYASAR_LIVE_CUTOVER.md":
        "Moyasar live-cutover doc names sk_live_ in policy copy",
    "docs/RAILWAY_DEPLOY_CHECKLIST.md":
        "Railway deploy checklist names the prefix in env-var template",
    "docs/WAVE11_FIRST3_PAID_PILOTS_EVIDENCE_TABLE.md":
        "evidence table names the prefix as a forbidden token",
    "docs/integrations/PAYMENT_MOYASAR_LIVE.md":
        "Moyasar live payment doc names sk_live_ in policy copy",
    "docs/ops/GO_LIVE_INDEX.md":
        "go-live index names the prefix in the checklist",
    "docs/ops/MOYASAR_KYC_CHECKLIST.md":
        "Moyasar KYC checklist names the prefix in policy copy",
    "docs/ops/PRODUCTION_ENV_TEMPLATE.md":
        "production env template names the placeholder prefix",
    "docs/security/KEY_ROTATION.md":
        "key-rotation doc names sk_live_ in the rotation procedure",
    "scripts/dealix_integration_plan_quality_check.py":
        "integration quality checker regex for the secret prefixes",
    "scripts/dealix_master_full_execution_verify.sh":
        "master verifier shell script greps repo for these prefixes",
    "scripts/generate_production_env.sh":
        "env generator names the placeholder prefix in the template",
    "scripts/integration_upgrade_verify.sh":
        "integration-upgrade verify script greps repo for prefixes",
    "scripts/moyasar_live_cutover.py":
        "live-cutover CLI checks/rejects an sk_live_ key",
    "scripts/preflight_check.py":
        "preflight check names sk_live_ in env-var doc text",
    "scripts/reconcile_moyasar.py":
        "reconcile CLI names sk_live_ in env-var help text",
    "scripts/ultimate_upgrade_verify.sh":
        "ultimate-upgrade verify script greps repo for prefixes",
    "scripts/wave11_first3_paid_pilots_verify.sh":
        "wave11 verify script greps repo for the prefixes",
    "scripts/wave12_saudi_revenue_command_center_verify.sh":
        "wave12 verify script greps repo for the prefixes",
    "scripts/wave6_revenue_activation_verify.sh":
        "wave6 verify script greps repo for the prefixes",
    "scripts/wave7_5_service_truth_verify.sh":
        "wave7.5 verify script greps repo for the prefixes",
    "scripts/wave8_customer_data_boundary_check.sh":
        "wave8 data-boundary check greps repo for the prefixes",
    "scripts/wave8_customer_ready_verify.sh":
        "wave8 customer-ready verify script greps repo for prefixes",
}


# Filename patterns we ignore entirely:
#   - any file with ``test_`` in its name (test fixtures may construct
#     fake-shaped values via concatenation; gitleaks won't flag them
#     because we always concatenate)
#   - non-source artifacts (caches, htmlcov, etc.)
_SKIP_PARTS = {".git", ".claude", "node_modules", "__pycache__", "htmlcov", ".pytest_cache", ".venv", "venv"}


def _should_skip_file(rel_path: Path) -> bool:
    parts = set(rel_path.parts)
    if parts & _SKIP_PARTS:
        return True
    name = rel_path.name
    # Tests are exempt — they construct via concatenation.
    if name.startswith("test_") or name == "conftest.py":
        return True
    return False


def test_no_secret_prefix_outside_allowlist():
    """Repo-wide grep for the three forbidden literal prefixes.

    Each match outside the allowlist is a regression — either a real
    secret slipped in, or a new file legitimately needs to reference
    the prefix and should be added to ``_PREFIX_ALLOWLIST`` with a
    reason comment.
    """
    pattern = re.compile(r"sk_live_|ghp_|AIza")

    extensions = {".py", ".md", ".sh", ".env", ".ini", ".toml", ".yaml", ".yml"}
    violations: list[str] = []

    for path in REPO_ROOT.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix not in extensions:
            continue
        rel = path.relative_to(REPO_ROOT)
        if _should_skip_file(rel):
            continue
        if str(rel) in _PREFIX_ALLOWLIST:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if pattern.search(text):
            violations.append(str(rel))

    assert not violations, (
        "Forbidden secret prefix found outside allowlist. Either:\n"
        "  - a real secret leaked (rotate it + remove from history), OR\n"
        "  - a new file legitimately references the prefix in policy/"
        "regex/runbook copy — add it to _PREFIX_ALLOWLIST with a "
        "one-line reason.\n"
        "Files:\n" + "\n".join(sorted(violations))
    )


def test_prefix_allowlist_entries_actually_exist():
    """Catch stale allowlist entries — if a file no longer contains
    the prefix, drop it from the allowlist to keep the perimeter tight."""
    pattern = re.compile(r"sk_live_|ghp_|AIza")
    stale: list[str] = []
    for rel_path in _PREFIX_ALLOWLIST:
        path = REPO_ROOT / rel_path
        if not path.exists():
            stale.append(f"{rel_path}: file no longer present")
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if not pattern.search(text):
            stale.append(f"{rel_path}: prefix no longer in file")
    assert not stale, (
        "Stale entries in _PREFIX_ALLOWLIST — remove them:\n"
        + "\n".join(stale)
    )
