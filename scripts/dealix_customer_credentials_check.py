#!/usr/bin/env python3
"""Wave 8 §3 — Customer Credential Readiness Check.

Prints PRESENT / MISSING / OPTIONAL / BLOCKED_BY_POLICY / DEMO_FALLBACK.
NEVER prints actual credential values.

Usage:
    py scripts/dealix_customer_credentials_check.py
    py scripts/dealix_customer_credentials_check.py --check langfuse
    py scripts/dealix_customer_credentials_check.py --json
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# ── Credential definitions ──────────────────────────────────────────────────
CREDENTIALS = [
    # (env_var, category, status_policy, required_for_first_customer, notes)
    ("APP_SECRET_KEY",          "core",       "required",              True,  "Generate: python -c \"import secrets; print(secrets.token_hex(32))\""),
    ("DATABASE_URL",            "core",       "required",              True,  "Auto-provided by Railway Postgres"),
    ("ENVIRONMENT",             "core",       "required",              True,  "Set to: production"),
    ("APP_URL",                 "core",       "required",              True,  "e.g. https://dealix.sa"),
    ("MOYASAR_SECRET_KEY",      "payments",   "blocked_by_policy",     False, "NO_LIVE_CHARGE — do not configure until founder approves"),
    ("MOYASAR_WEBHOOK_SECRET",  "payments",   "blocked_by_policy",     False, "NO_LIVE_CHARGE — bank transfer is safe default"),
    ("CALENDLY_URL",            "scheduling", "required",              True,  "Already in .env.example"),
    ("CALENDLY_WEBHOOK_SECRET", "scheduling", "optional",              False, ""),
    ("WHATSAPP_VERIFY_TOKEN",   "whatsapp",   "required",              False, "For inbound webhook only"),
    ("WHATSAPP_APP_SECRET",     "whatsapp",   "optional",              False, ""),
    ("WHATSAPP_ACCESS_TOKEN",   "whatsapp",   "optional",              False, "Safe default: personal WA"),
    ("WHATSAPP_PHONE_NUMBER_ID","whatsapp",   "optional",              False, ""),
    ("ANTHROPIC_API_KEY",       "llm",        "optional",              False, "At least one LLM key recommended"),
    ("OPENAI_API_KEY",          "llm",        "optional",              False, ""),
    ("GROQ_API_KEY",            "llm",        "optional",              False, ""),
    ("LANGFUSE_SECRET_KEY",     "observability","optional",            False, ""),
    ("LANGFUSE_PUBLIC_KEY",     "observability","optional",            False, ""),
    ("LANGFUSE_HOST",           "observability","optional",            False, "Defaults to cloud.langfuse.com"),
    ("SENTRY_DSN",              "observability","optional",            False, ""),
    ("POSTHOG_API_KEY",         "observability","optional",            False, ""),
    ("OTEL_EXPORTER_OTLP_ENDPOINT","observability","optional",        False, ""),
    ("RESEND_API_KEY",          "email",      "optional",              False, ""),
    ("HUBSPOT_API_KEY",         "crm",        "optional",              False, ""),
    ("SLACK_BOT_TOKEN",         "notifications","optional",            False, ""),
    ("SLACK_CHANNEL_ID",        "notifications","optional",            False, ""),
    ("GOOGLE_SERVICE_ACCOUNT_JSON","google",  "optional",              False, ""),
    ("API_KEYS",                "security",   "required",              True,  "Comma-separated API keys"),
    ("ADMIN_API_KEYS",          "security",   "required",              True,  "Admin-only key"),
    ("CORS_ORIGINS",            "security",   "required",              True,  ""),
]

# Integration-specific check aliases
INTEGRATION_CHECKS = {
    "google_sheets":    ["GOOGLE_SERVICE_ACCOUNT_JSON"],
    "google_drive":     ["GOOGLE_SERVICE_ACCOUNT_JSON"],
    "hubspot":          ["HUBSPOT_API_KEY"],
    "gmail_drafts":     [],  # Always draft_only — no credential needed
    "whatsapp":         ["WHATSAPP_VERIFY_TOKEN", "WHATSAPP_ACCESS_TOKEN"],
    "moyasar":          ["MOYASAR_SECRET_KEY"],
    "resend":           ["RESEND_API_KEY"],
    "slack":            ["SLACK_BOT_TOKEN", "SLACK_CHANNEL_ID"],
    "notion":           [],
    "chatwoot":         [],
    "calcom":           ["CALENDLY_URL"],
    "langfuse":         ["LANGFUSE_SECRET_KEY", "LANGFUSE_PUBLIC_KEY"],
    "otel":             ["OTEL_EXPORTER_OTLP_ENDPOINT"],
    "posthog":          ["POSTHOG_API_KEY"],
    "qdrant":           [],
    "pgvector":         ["DATABASE_URL"],
    "sentry":           ["SENTRY_DSN"],
    "meta_templates":   ["WHATSAPP_ACCESS_TOKEN", "WHATSAPP_PHONE_NUMBER_ID"],
    "railway":          [],
    "github_actions":   [],
}


def _mask(value: str) -> str:
    """Never return actual value — always mask."""
    if not value:
        return ""
    return "***" + value[-4:] if len(value) > 4 else "***"


def check_credential(env_var: str, policy: str) -> str:
    """Return status string. NEVER returns actual value."""
    if policy == "blocked_by_policy":
        return "BLOCKED_BY_POLICY"
    value = os.environ.get(env_var, "")
    if not value:
        return "DEMO_FALLBACK" if policy == "optional" else "MISSING"
    return "PRESENT"


def run_full_check(*, as_json: bool = False) -> int:
    """Run full credential check. Returns 0 if all required present, 1 otherwise."""
    results = []
    has_error = False

    for (env_var, category, policy, first_customer, notes) in CREDENTIALS:
        status = check_credential(env_var, policy)
        if status == "MISSING" and first_customer:
            has_error = True
        results.append({
            "env_var": env_var,
            "category": category,
            "policy": policy,
            "first_customer_needed": first_customer,
            "status": status,
            "notes": notes,
        })

    if as_json:
        print(json.dumps({"credentials": results, "has_error": has_error}, indent=2))
        return 1 if has_error else 0

    # Human-readable output
    print("\n=== Wave 8 — Customer Credential Readiness Check ===\n")
    prev_cat = None
    for r in results:
        if r["category"] != prev_cat:
            print(f"\n  [{r['category'].upper()}]")
            prev_cat = r["category"]
        status_icon = {
            "PRESENT":          "✅",
            "MISSING":          "❌",
            "OPTIONAL":         "⚙️ ",
            "DEMO_FALLBACK":    "🔶",
            "BLOCKED_BY_POLICY":"🚫",
        }.get(r["status"], "?")
        fc = " (FIRST_CUSTOMER_NEEDED)" if r["first_customer_needed"] else ""
        note = f"  # {r['notes']}" if r["notes"] else ""
        print(f"  {status_icon} {r['status']:<22} {r['env_var']}{fc}{note}")

    print()
    if has_error:
        print("❌ RESULT: MISSING required credentials for first customer launch.")
        print("   Fix above MISSING items before go-live.")
    else:
        print("✅ RESULT: All required credentials are PRESENT or OPTIONAL.")
    print()
    return 1 if has_error else 0


def run_integration_check(integration: str) -> int:
    """Check credentials for a specific integration."""
    if integration not in INTEGRATION_CHECKS:
        print(f"Unknown integration: {integration}")
        print(f"Available: {', '.join(INTEGRATION_CHECKS.keys())}")
        return 2

    required_vars = INTEGRATION_CHECKS[integration]
    if not required_vars:
        print(f"✅ {integration}: no credentials required (or always available)")
        return 0

    # Special case: Moyasar
    if integration == "moyasar":
        print(f"🚫 {integration}: BLOCKED_BY_POLICY — NO_LIVE_CHARGE gate active")
        return 0

    missing = []
    for var in required_vars:
        val = os.environ.get(var, "")
        if not val:
            missing.append(var)
            print(f"  ❌ MISSING: {var}")
        else:
            print(f"  ✅ PRESENT: {var}")

    if missing:
        print(f"\n❌ {integration}: NOT_CONFIGURED — {len(missing)} credential(s) missing")
        return 1
    print(f"\n✅ {integration}: CONFIGURED")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Dealix Customer Credential Readiness Check")
    parser.add_argument("--check", default=None, help="Check a specific integration")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    if args.check:
        return run_integration_check(args.check)
    return run_full_check(as_json=args.json)


if __name__ == "__main__":
    sys.exit(main())
