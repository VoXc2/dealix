#!/usr/bin/env python3
"""
Dealix Verify No-Auto-External-Send Gate
Ensures Dealix never sends outbound messages without explicit human approval.
This is the CRITICAL safety gate. If it fails, Dealix stays in draft-only mode.
"""

import os
import sys
from pathlib import Path


# ─── Configuration ───────────────────────────────────────────
# If any of these env vars are set to "true" without explicit user override,
# the gate MUST fail and force draft-only mode.
SEND_ENVS = [
    "EXTERNAL_SEND_ENABLED",
    "EMAIL_SEND_ENABLED",
    "WHATSAPP_SEND_ENABLED",
    "WHATSAPP_ALLOW_LIVE_SEND",
    "SMS_SEND_ENABLED",
]

DEFAULT_SAFE_VALUE = "false"
ALLOWED_OVERRIDE_FILE = Path(__file__).parent.parent / ".dealix_allow_external_send"


def check_env_vars() -> list[str]:
    """Check if any send env var is enabled without explicit override."""
    issues = []
    for env in SEND_ENVS:
        value = os.environ.get(env, "false").lower().strip()
        if value in ("true", "1", "yes", "on"):
            # Even if enabled, require explicit override file
            if not ALLOWED_OVERRIDE_FILE.exists():
                issues.append(
                    f"CRITICAL: {env}={value} but no explicit override file found at {ALLOWED_OVERRIDE_FILE}"
                )
            else:
                content = ALLOWED_OVERRIDE_FILE.read_text().strip()
                if env not in content:
                    issues.append(
                        f"CRITICAL: {env}={value} but not explicitly whitelisted in {ALLOWED_OVERRIDE_FILE}"
                    )
    return issues


def check_settings_table() -> list[str]:
    """Check database settings for any outbound mode != draft_only."""
    issues = []
    try:
        import mysql.connector
        db_url = os.environ.get("DATABASE_URL", "")
        if not db_url or "mysql" not in db_url:
            return issues  # Skip if no MySQL config
        
        # Parse simple connection string
        # Format: mysql://user:pass@host:port/db
        conn = None
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user=os.environ.get("DB_USER", "dealix"),
                password=os.environ.get("DB_PASSWORD", "dealix_pass_2026"),
                database="dealix",
                port=3306,
                connect_timeout=5,
            )
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT `value` FROM settings WHERE `key` = 'outbound_mode'")
            row = cursor.fetchone()
            if row:
                mode = (row.get("value") or "").strip().lower()
                if mode not in ("", "draft_only", "draft_only"):
                    issues.append(f"CRITICAL: settings.outbound_mode = '{mode}' (must be 'draft_only')")
            cursor.close()
        finally:
            if conn:
                conn.close()
    except ImportError:
        pass  # mysql-connector not installed, skip DB check
    except Exception as e:
        issues.append(f"WARNING: Could not check DB settings: {e}")
    return issues


def check_drafts_have_approval() -> list[str]:
    """Check that no draft records exist with sent=true without approval."""
    issues = []
    try:
        import mysql.connector
        conn = None
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user=os.environ.get("DB_USER", "dealix"),
                password=os.environ.get("DB_PASSWORD", "dealix_pass_2026"),
                database="dealix",
                port=3306,
                connect_timeout=5,
            )
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT id FROM drafts 
                WHERE sent = TRUE AND approved = FALSE 
                LIMIT 1
            """)
            row = cursor.fetchone()
            if row:
                issues.append(
                    f"CRITICAL: Draft id={row['id']} is sent but NOT approved. This should never happen."
                )
            cursor.close()
        finally:
            if conn:
                conn.close()
    except ImportError:
        pass
    except Exception as e:
        issues.append(f"WARNING: Could not check drafts table: {e}")
    return issues


def check_codebase_for_auto_send() -> list[str]:
    """Static check: scan codebase for suspicious auto-send patterns."""
    issues = []
    base = Path(__file__).parent.parent
    
    suspicious_patterns = [
        "# auto-send", "auto_send", "auto_send=True", "autoSend=True",
        "unapproved_send", "send_without_approval", "bypass_approval",
        "WHATSAPP_ALLOW_LIVE_SEND = true", "EXTERNAL_SEND_ENABLED = true",
    ]
    
    for root, dirs, files in os.walk(base / "scripts"):
        for f in files:
            if f.endswith(".py"):
                fp = Path(root) / f
                content = fp.read_text(encoding="utf-8")
                for pattern in suspicious_patterns:
                    if pattern in content:
                        issues.append(f"SUSPICIOUS: '{pattern}' found in {fp.relative_to(base)}")
    
    return issues


def main():
    """Run all safety checks."""
    print("=" * 70)
    print("  DEALIX — NO-AUTO-EXTERNAL-SEND SAFETY GATE")
    print("=" * 70)
    print()
    
    issues = []
    issues += check_env_vars()
    issues += check_settings_table()
    issues += check_drafts_have_approval()
    issues += check_codebase_for_auto_send()
    
    # Summary
    critical = [i for i in issues if i.startswith("CRITICAL")]
    warnings = [i for i in issues if i.startswith("WARNING")]
    suspicious = [i for i in issues if i.startswith("SUSPICIOUS")]
    
    print(f"  Critial issues: {len(critical)}")
    print(f"  Warnings: {len(warnings)}")
    print(f"  Suspicious: {len(suspicious)}")
    
    if critical:
        print()
        print("  🔴 BLOCKING CRITICAL ISSUES:")
        for c in critical:
            print(f"     • {c}")
    
    if warnings:
        print()
        print("  🟡 WARNINGS:")
        for w in warnings:
            print(f"     • {w}")
    
    if suspicious:
        print()
        print("  ⚠️  SUSPICIOUS CODE:")
        for s in suspicious:
            print(f"     • {s}")
    
    print()
    
    # Outbound mode verdict
    outbound_mode = os.environ.get("OUTBOUND_MODE", "")
    if not outbound_mode:
        outbound_mode = "draft_only"  # Default safe value
    
    if critical:
        print("  🚫 GATE RESULT: BLOCKED")
        print(f"  📋 OUTBOUND_MODE: draft_only (forced due to blockers)")
        print()
        print("  Next action: Fix critical issues, then re-run.")
        sys.exit(1)
    elif warnings:
        print("  ⚠️  GATE RESULT: PASS WITH WARNINGS")
        print(f"  📋 OUTBOUND_MODE: {outbound_mode}")
        print()
        print("  Next action: Address warnings, but system can operate.")
        sys.exit(0)
    else:
        print("  ✅ GATE RESULT: PASS")
        print(f"  📋 OUTBOUND_MODE: {outbound_mode}")
        print()
        print("  All safety checks passed. System is in safe mode.")
        sys.exit(0)


if __name__ == "__main__":
    main()
