#!/usr/bin/env python3
"""Static fail-closed verifier for Dealix trust incident #1440 remediation."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "dealix/commercial/external_execution_gate.py"
GMAIL = ROOT / "dealix/commercial/gmail_guarded_provider.py"
LEGACY_GMAIL = ROOT / "auto_client_acquisition/email/gmail_send.py"
LEGACY_EMAIL = ROOT / "integrations/email.py"
EMAIL_ROUTE = ROOT / "api/routers/email_send.py"
LEDGER = ROOT / "dealix/commercial/idempotency_ledger.py"
DISPATCH = ROOT / "scripts/ops/living_fleet_dispatch.sh"
FLEET_ACCEPTANCE = ROOT / "tests/test_living_fleet_acceptance_v4.py"
FLEET_CONCURRENCY = ROOT / "tests/test_living_fleet_concurrency_v1.py"
FLEET_CRASH_RECOVERY = ROOT / "tests/test_living_fleet_terminal_crash_recovery_v1.py"
FABRIC_TESTS = ROOT / "tests/test_commercial_execution_fabric_v2.py"
TRUST_TESTS = ROOT / "tests/test_external_execution_trust_v1.py"
APPROVAL = ROOT / "docs/ops/APPROVAL_FINGERPRINT_CONTRACT.md"


def require(text: str, token: str) -> None:
    assert token in text, f"missing required trust invariant: {token}"


def _assert_no_direct_email_provider_surface() -> None:
    # Scan executable source types across runtime roots. Skip this verifier so
    # forbidden signatures cannot self-trigger the guard.
    forbidden = (
        "gmail.googleapis.com/gmail/v1/users/me/messages/send",
        ".messages().send(",
        "gmail.users.messages.send(",
        "api.resend.com/emails",
        "resend.emails.send(",
        "api.sendgrid.com/v3/mail/send",
        "sendgridapiclient(",
        "smtplib.smtp(",
        "smtplib.smtp_ssl(",
        "nodemailer",
        "transporter.sendmail(",
        "aiosmtplib",
        "yagmail",
    )
    executable_suffixes = {
        ".py", ".pyw", ".sh", ".bash", ".js", ".jsx",
        ".mjs", ".cjs", ".ts", ".tsx",
    }
    ignored_directories = {
        ".git", ".venv", "node_modules", "__pycache__",
        ".next", "dist", "build", "coverage",
    }
    roots = (
        ROOT / "api",
        ROOT / "auto_client_acquisition",
        ROOT / "autonomous_growth",
        ROOT / "core",
        ROOT / "dealix",
        ROOT / "frontend",
        ROOT / "integrations",
        ROOT / "scripts",
    )
    verifier_path = Path(__file__).resolve()
    violations: list[str] = []
    for source_root in roots:
        if not source_root.exists():
            continue
        for path in source_root.rglob("*"):
            if (
                not path.is_file()
                or path.resolve() == verifier_path
                or path.suffix.lower() not in executable_suffixes
                or ignored_directories.intersection(path.parts)
            ):
                continue
            text = path.read_text(encoding="utf-8", errors="replace").lower()
            for token in forbidden:
                if token in text:
                    violations.append(f"{path.relative_to(ROOT)}::{token}")
    assert not violations, "direct email provider surface remains: " + ", ".join(violations)


def main() -> int:
    gate = GATE.read_text(encoding="utf-8")
    gmail = GMAIL.read_text(encoding="utf-8")
    legacy_gmail = LEGACY_GMAIL.read_text(encoding="utf-8")
    legacy_email = LEGACY_EMAIL.read_text(encoding="utf-8")
    email_route = EMAIL_ROUTE.read_text(encoding="utf-8")
    ledger = LEDGER.read_text(encoding="utf-8")
    dispatch = DISPATCH.read_text(encoding="utf-8")
    fleet = FLEET_ACCEPTANCE.read_text(encoding="utf-8")
    concurrency = FLEET_CONCURRENCY.read_text(encoding="utf-8")
    crash_recovery = FLEET_CRASH_RECOVERY.read_text(encoding="utf-8")
    fabric_tests = FABRIC_TESTS.read_text(encoding="utf-8")
    trust_tests = TRUST_TESTS.read_text(encoding="utf-8")
    approval = APPROVAL.read_text(encoding="utf-8")

    for token in (
        "canonical_action_hash",
        "packet_integrity_sha256",
        "schema_version: Literal[\"dealix.external-action-packet.v2\"]",
        '"schema_version": schema_version.strip()',
        "recompute_packet_integrity",
        "recompute_action_hash",
        "UNSUPPORTED_PACKET_SCHEMA",
        "CanonicalAuthorityResolver",
        "CANONICAL_FRESH_AUTHORITY_NOT_RESOLVED",
        "APPROVAL_STATE_STALE",
        "approval_evidence_valid",
    ):
        require(gate, token)

    require(
        gmail,
        "LIVE_PROVIDER_QUARANTINED_CANONICAL_PROVIDER_DEPENDENCIES_NOT_WIRED",
    )
    require(gmail, "accepts NO resolver")
    assert ("." + "messages()." + "send(") not in gmail
    assert "authority_resolver" not in gmail
    assert "idempotency_ledger" not in gmail

    require(
        legacy_gmail,
        "LIVE_GMAIL_SEND_QUARANTINED_CANONICAL_GOVERNANCE_PROVIDER_NOT_WIRED",
    )
    send_surface = legacy_gmail.split("async def send_email", 1)[1].split(
        "async def create_draft", 1
    )[0]
    assert "client.post" not in send_surface
    assert "_refresh_access_token" not in send_surface

    require(
        legacy_email,
        "LIVE_EMAIL_PROVIDER_QUARANTINED_CANONICAL_GOVERNANCE_PROVIDER_NOT_WIRED",
    )
    for token in (
        "async def send(",
        "async def _send_resend(",
        "async def _send_sendgrid(",
        "async def _send_smtp(",
    ):
        require(legacy_email, token)
    assert "httpx" not in legacy_email
    assert "smtplib" not in legacy_email
    _assert_no_direct_email_provider_surface()

    require(email_route, "def _legacy_external_send_quarantine")
    require(email_route, "LIVE_GMAIL_SEND_QUARANTINE_REASON")
    assert email_route.count("return _legacy_external_send_quarantine()") >= 2

    for token in (
        "BEGIN IMMEDIATE",
        "RESERVED",
        "COMMITTED",
        "UNKNOWN",
        "ABORTED",
        "CONFLICT",
        "REPLAY_COMMITTED",
        "RECONCILED_NOT_DELIVERED",
        "reconcile_unknown_committed",
        "reconcile_unknown_not_delivered",
        "CONFIRMED_DELIVERED",
        "CONFIRMED_NOT_DELIVERED",
        "sqlite_master",
        "_v2_rebuild",
        "DROP TABLE",
        "RENAME TO",
    ):
        require(ledger, token)

    require(
        approval,
        "ACTION_HASH = sha256(action_type|target|environment|payload)[0:16]",
    )
    require(approval, "UNKNOWN -> COMMITTED")
    require(approval, "UNKNOWN -> ABORTED")
    require(approval, "at-most-once")

    assert "pytest.mark.skip" not in fleet
    for token in (
        'force="0"',
        "test_identical_force_zero_dispatch_executes_real_owner_once",
        "test_none_to_real_force_zero_invalidates_dedupe_and_supersedes_handoff",
        "test_real_to_real_rotation_executes_at_force_zero",
        "test_post_dispatch_collect_is_idempotent_after_terminalization",
    ):
        require(fleet, token)

    for token in (
        'exec 8>"$role_lock"',
        "COLLECT_SKIP_LOCKED",
        "counter_once",
        "COUNTER_BEFORE",
        "TERMINAL_COUNTER_DRIFT",
        "COUNTER_FILE",
        "TERMINAL_MARKER_COUNTER_MISMATCH",
        ".timeout_count",
        "timeout.json",
        "flock -n 8",
        "if [[ ! -f \"$jf\" ]]",
    ):
        require(dispatch, token)
    require(
        concurrency,
        "test_concurrent_dispatch_and_collect_share_role_lock_and_terminalize_once",
    )
    require(concurrency, "COLLECT_SKIP_LOCKED")
    require(
        crash_recovery,
        "test_collect_recovers_after_counter_applied_before_pending_move",
    )
    require(
        fabric_tests,
        "test_caller_time_overrides_cannot_make_stale_authority_fresh",
    )

    for token in (
        "test_schema_version_is_literal_and_bound_into_integrity_and_action_hash",
        "test_legacy_gmail_send_surface_is_quarantined_without_network_effect",
        "test_unified_resend_sendgrid_smtp_paths_are_all_quarantined",
        "test_unknown_can_be_audited_to_committed_and_then_replayed_without_side_effect",
        "test_unknown_confirmed_not_delivered_aborts_key_and_requires_new_action",
        "test_legacy_sqlite_check_constraint_is_rebuilt_before_aborted_transition",
        "test_reconcile_committed_rejects_empty_provider_receipt",
    ):
        require(trust_tests, token)

    print("DEALIX_P0_TRUST_REMEDIATION_V5=PASS")
    print("INCIDENT=1440")
    print("PUBLIC_GMAIL_PROVIDER=QUARANTINED")
    print("LEGACY_GMAIL_EXECUTABLE_PATHS=QUARANTINED")
    print("LEGACY_RESEND_SENDGRID_SMTP_PATHS=QUARANTINED")
    print("EXECUTABLE_EMAIL_SURFACE_SCAN=PASS")
    print("TRUSTED_CLOCK_OVERRIDE_REGRESSION=PASS")
    print("CANONICAL_ACTION_HASH_AND_SCHEMA_INTEGRITY=PASS")
    print("DURABLE_IDEMPOTENCY_RECONCILIATION=PASS")
    print("LEGACY_LEDGER_SCHEMA_MIGRATION=PASS")
    print("FLEET_SHARED_ROLE_LOCK=PASS")
    print("FLEET_FORCE0_SUPERSEDE_CONCURRENT_EXACT_ONCE_COVERAGE=PASS")
    print("FLEET_CRASH_RECOVERY_COUNTER_MARKER=PASS")
    print("MERGE_AUTHORITY=NOT_GRANTED_BY_THIS_VERIFIER")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
