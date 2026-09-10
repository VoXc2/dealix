"""v7 Phase 8 hardening — credential-shaped secrets must not leak.

The old guard treated the *literal prefix* ``sk_live_`` / ``ghp_`` / ``AIza``
as a secret and maintained a very large file allowlist. That made security
policy, regex definitions, redaction code, and runbooks fail merely for naming
what they protect, while the allowlist itself continuously drifted.

This guard now reuses the canonical secret scanner and distinguishes a policy
reference from a credential-shaped value. It remains fail-closed for real-looking
Moyasar live keys, GitHub PATs, and Google API keys, while never printing the raw
match in a failure message.
"""
from __future__ import annotations

from pathlib import Path

from auto_client_acquisition.security_privacy.log_redaction import (
    redact_log_entry,
)
from auto_client_acquisition.security_privacy.secret_scan_policy import (
    scan_text_for_secrets,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
_TARGET_PATTERN_IDS = {
    "moyasar_live_secret",
    "github_pat",
    "google_api_key",
}
_SKIP_PARTS = {
    ".git",
    ".claude",
    "node_modules",
    "__pycache__",
    "htmlcov",
    ".pytest_cache",
    ".venv",
    "venv",
}
_SCAN_EXTENSIONS = {
    ".py",
    ".md",
    ".sh",
    ".env",
    ".ini",
    ".toml",
    ".yaml",
    ".yml",
    ".json",
    ".js",
    ".ts",
    ".tsx",
    ".html",
}

# This exact historical fake token appears only inside legacy verifier exclusion
# regex text. It is not a credential and is normalized before scanning. Keep the
# exemption exact — never exempt a prefix, file, directory, or arbitrary line.
_HISTORICAL_SYNTHETIC_TOKEN = "sk_live_REALDANGEROUSKEYSECRET"


def _should_skip_file(rel_path: Path) -> bool:
    if set(rel_path.parts) & _SKIP_PARTS:
        return True
    # Tests intentionally construct credential-shaped values to prove guards.
    if rel_path.name.startswith("test_") or rel_path.name == "conftest.py":
        return True
    return rel_path.suffix not in _SCAN_EXTENSIONS


def _target_findings(text: str):
    sanitized = text.replace(_HISTORICAL_SYNTHETIC_TOKEN, "sk_live_EXAMPLE")
    return [
        finding
        for finding in scan_text_for_secrets(sanitized)
        if finding.pattern_id in _TARGET_PATTERN_IDS
    ]


def test_redact_log_entry_redacts_stripe_shaped_key():
    fake_secret = "sk_" + "live" + "_" + "abcdefghijklmnopqrstuvwxyz12345"
    log_line = f"event=invoice_charge attempt key={fake_secret} status=blocked"
    redacted = redact_log_entry(log_line)
    assert isinstance(redacted, str)
    assert fake_secret not in redacted, (
        f"Moyasar-shaped key leaked through redaction: {redacted!r}"
    )
    assert "[REDACTED_SECRET]" in redacted


def test_redact_log_entry_redacts_anthropic_shaped_key():
    fake_anthropic = "sk-" + "ant-" + ("a" * 35)
    log_line = f"event=llm_call provider=anthropic key={fake_anthropic}"
    redacted = redact_log_entry(log_line)
    assert isinstance(redacted, str)
    assert fake_anthropic not in redacted
    assert "[REDACTED_SECRET]" in redacted


def test_redact_log_entry_redacts_inside_dict_log_entry():
    fake_secret = "sk_" + "live" + "_" + "ZYXWVUTSRQPONMLK987654321"
    entry = {
        "event": "moyasar_attempt",
        "metadata": {"key": fake_secret, "status": "rejected"},
    }
    out = redact_log_entry(entry)
    assert isinstance(out, dict)
    flat = repr(out)
    assert fake_secret not in flat, f"secret leaked into dict redaction: {flat}"


def test_canonical_scanner_detects_target_credential_shapes():
    """Prove the repo perimeter was not weakened while removing prefix noise."""
    samples = {
        "moyasar_live_secret": "sk_" + "live" + "_" + ("A" * 24),
        "github_pat": "ghp_" + ("B" * 40),
        "google_api_key": "AIza" + ("C" * 35),
    }
    for expected, sample in samples.items():
        findings = scan_text_for_secrets(f"token={sample}")
        assert expected in {finding.pattern_id for finding in findings}
        # Findings expose only a redacted excerpt, never the raw credential.
        assert all(sample not in finding.excerpt_redacted for finding in findings)


def test_literal_policy_prefixes_are_not_credentials():
    """Naming a protected prefix in policy/runbook text is not a secret leak."""
    policy_text = "Reject sk_live_ values; redact ghp_ tokens; protect AIza keys."
    assert _target_findings(policy_text) == []


def test_no_credential_shaped_secret_in_scannable_repo_files():
    """Scan source/config/docs for real-looking target credentials.

    Failure output contains path, line, and pattern id only. The matched value is
    deliberately never included in assertion text or logs.
    """
    violations: list[str] = []
    for path in REPO_ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(REPO_ROOT)
        if _should_skip_file(rel):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for line_no, line in enumerate(text.splitlines(), start=1):
            for finding in _target_findings(line):
                violations.append(f"{rel}:{line_no}:{finding.pattern_id}")

    assert not violations, (
        "Credential-shaped secret found in tracked source/config/docs. "
        "Rotate/remove any real credential; replace examples with short placeholders. "
        "Raw matches are intentionally redacted from this report.\n"
        + "\n".join(sorted(violations))
    )
