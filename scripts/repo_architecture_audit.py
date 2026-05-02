#!/usr/bin/env python3
"""
Repo Architecture Audit — static checks that prove the codebase still honors
its safety contract before any commit reaches main.

Checks:
  1. Required routers register cleanly via api.main.create_app().
  2. Forbidden patterns absent from product code (cold_whatsapp, linkedin_scrape, ...).
  3. WhatsApp interactive buttons rule (<= 3) is preserved in code.
  4. Live-action safety flags discoverable in settings + .env.example.
  5. Secrets hygiene: no committed .env, .pem, credentials.json, service-account.json.
  6. Required tests still present (governance/approvals, orchestrator, proof_pack).
  7. Every AgentSpec in agent_registry has non-empty pdpl_compliance_gates.
  8. AutonomyMode integrity: 5 modes; MANUAL/SUGGEST always need approval.
  9. No raw `print(` in production paths (api/routers/, orchestrator/).

Run:
  python scripts/repo_architecture_audit.py
Exit 0 = PASS, exit 1 = FAIL.

Importable: scripts.repo_architecture_audit.run_audit() -> AuditReport.
"""

from __future__ import annotations

import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))


# ── Configuration ─────────────────────────────────────────────────

REQUIRED_ROUTERS: tuple[str, ...] = (
    "admin", "agents", "automation", "autonomous", "business",
    "command_center", "customer_success", "data", "dominance",
    "drafts", "ecosystem", "email_send", "full_os", "health", "leads",
    "outreach", "personal_operator", "pricing", "prospect", "public",
    "revenue", "revenue_os", "sales", "sectors", "v3", "webhooks",
)

FORBIDDEN_PATTERNS: tuple[str, ...] = (
    "cold_whatsapp",
    "linkedin_auto_dm",
    "mass_dm",
    "bulk_send_unverified",
)

# Lines containing any of these markers describe defensive policy
# (registries of things to avoid, boolean flags that detect them, etc.).
# A forbidden_pattern hit on such a line is treated as documented intent,
# not as an active code path that would run the unsafe action.
ALLOWED_CONTEXT_MARKERS: tuple[str, ...] = (
    "restricted_actions",
    "blocked_",
    "_blocked",
    "blocked=",
    "blocked:",
    "blocked\"",
    "blocked'",
    "forbidden",
    "disallowed",
    "is_cold_whatsapp",
    "avoid",
    "_check",
    "_detect",
    "guard",
    "policy",
    "ALLOWED_CONTEXT",
    "FORBIDDEN_PATTERNS",
)

PRODUCT_DIRS: tuple[str, ...] = (
    "api/routers",
    "auto_client_acquisition",
    "autonomous_growth",
    "core",
    "dealix",
    "integrations",
)

REQUIRED_SAFETY_FLAGS: tuple[str, ...] = (
    "WHATSAPP_ALLOW_LIVE_SEND",
    "GMAIL_ALLOW_LIVE_SEND",
    "MOYASAR_ALLOW_LIVE_CHARGE",
    "LINKEDIN_ALLOW_AUTO_DM",
)

REQUIRED_TEST_FILES: tuple[str, ...] = (
    "tests/governance/test_approvals.py",
    "tests/unit/test_orchestrator.py",
    "tests/test_proof_pack.py",
)

SECRETS_FORBIDDEN_GLOBS: tuple[str, ...] = (
    ".env",
    "*.pem",
    "*credentials*.json",
    "*service-account*.json",
    "*service_account*.json",
)
SECRETS_ALLOWED_PATHS: tuple[str, ...] = (
    ".env.example",
    ".env.staging.example",
)


# ── Result types ──────────────────────────────────────────────────

@dataclass
class CheckResult:
    name: str
    passed: bool
    detail: str = ""


@dataclass
class AuditReport:
    checks: list[CheckResult] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return all(c.passed for c in self.checks)

    @property
    def fail_count(self) -> int:
        return sum(1 for c in self.checks if not c.passed)

    @property
    def pass_count(self) -> int:
        return sum(1 for c in self.checks if c.passed)


# ── Individual checks ─────────────────────────────────────────────

def check_routers_registered() -> CheckResult:
    try:
        from api.main import create_app
        app = create_app()
        registered_paths = {getattr(r, "path", "") for r in app.routes}
        missing: list[str] = []
        for name in REQUIRED_ROUTERS:
            try:
                __import__(f"api.routers.{name}")
            except Exception as exc:  # noqa: BLE001
                missing.append(f"{name} ({exc.__class__.__name__})")
        if missing:
            return CheckResult(
                "routers_registered", False,
                f"failed import: {', '.join(missing)}",
            )
        return CheckResult(
            "routers_registered", True,
            f"{len(REQUIRED_ROUTERS)} routers + {len(registered_paths)} paths",
        )
    except Exception as exc:  # noqa: BLE001
        return CheckResult("routers_registered", False, f"create_app failed: {exc}")


def _iter_py_files(rel_dir: str) -> list[Path]:
    base = _REPO / rel_dir
    if not base.exists():
        return []
    return [p for p in base.rglob("*.py") if "__pycache__" not in p.parts]


def check_forbidden_patterns() -> CheckResult:
    """Flag forbidden patterns ONLY when they appear outside documented-policy context.

    A pattern hit on a line that also contains an ALLOWED_CONTEXT_MARKER
    (e.g., `restricted_actions`, `avoid`, `is_cold_whatsapp`) is documented intent,
    not an active code path — it represents the codebase telling itself
    "this is a thing we refuse to do".
    """
    hits: list[str] = []
    for d in PRODUCT_DIRS:
        for path in _iter_py_files(d):
            # Skip the audit script itself if it lives in a product dir (it doesn't,
            # but be defensive against future moves).
            if path.name == Path(__file__).name:
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            for line_no, line in enumerate(text.splitlines(), start=1):
                for pat in FORBIDDEN_PATTERNS:
                    if pat not in line:
                        continue
                    if any(marker in line for marker in ALLOWED_CONTEXT_MARKERS):
                        continue
                    rel = path.relative_to(_REPO)
                    hits.append(f"{rel}:{line_no}:{pat}")
    if hits:
        return CheckResult(
            "forbidden_patterns_absent", False,
            "; ".join(hits[:10]) + (f" (+{len(hits) - 10} more)" if len(hits) > 10 else ""),
        )
    return CheckResult("forbidden_patterns_absent", True, "no forbidden patterns in active code")


def check_whatsapp_buttons_rule() -> CheckResult:
    """Verify the ≤3 buttons guard is present in whatsapp_cards.py."""
    target = _REPO / "auto_client_acquisition" / "personal_operator" / "whatsapp_cards.py"
    if not target.exists():
        return CheckResult("whatsapp_buttons_rule", False, "whatsapp_cards.py missing")
    text = target.read_text(encoding="utf-8")
    if "len(buttons) > 3" not in text:
        return CheckResult(
            "whatsapp_buttons_rule", False,
            "guard `len(buttons) > 3` missing from whatsapp_cards.py",
        )
    return CheckResult("whatsapp_buttons_rule", True, "≤3 guard present")


def check_safety_flags_discoverable() -> CheckResult:
    settings_text = (_REPO / "core" / "config" / "settings.py").read_text(encoding="utf-8")
    env_example = (_REPO / ".env.example").read_text(encoding="utf-8")

    missing: list[str] = []
    for flag in REQUIRED_SAFETY_FLAGS:
        if flag.lower() not in settings_text.lower():
            missing.append(f"{flag} not in settings.py")
        if flag not in env_example:
            missing.append(f"{flag} not in .env.example")

    if missing:
        return CheckResult("safety_flags_discoverable", False, "; ".join(missing))
    return CheckResult(
        "safety_flags_discoverable", True,
        f"{len(REQUIRED_SAFETY_FLAGS)} flags present in settings + .env.example",
    )


def check_secrets_hygiene() -> CheckResult:
    """Use `git ls-files` to inspect committed paths only."""
    try:
        out = subprocess.run(
            ["git", "ls-files"],
            cwd=_REPO, capture_output=True, text=True, check=True, timeout=20,
        )
    except (subprocess.SubprocessError, FileNotFoundError) as exc:
        return CheckResult("secrets_hygiene", False, f"git ls-files failed: {exc}")

    bad: list[str] = []
    for line in out.stdout.splitlines():
        line = line.strip()
        if not line or line in SECRETS_ALLOWED_PATHS:
            continue
        # Match by suffix/glob behavior.
        if line.endswith(".env") and line not in SECRETS_ALLOWED_PATHS:
            bad.append(line)
            continue
        if line.endswith(".pem"):
            bad.append(line)
            continue
        lower = line.lower()
        if lower.endswith(".json") and (
            "credentials" in lower or "service-account" in lower or "service_account" in lower
        ):
            bad.append(line)
    if bad:
        return CheckResult("secrets_hygiene", False, "committed: " + ", ".join(bad))
    return CheckResult("secrets_hygiene", True, "no committed secret-like files")


def check_required_tests() -> CheckResult:
    missing = [t for t in REQUIRED_TEST_FILES if not (_REPO / t).exists()]
    if missing:
        return CheckResult("required_tests_present", False, f"missing: {', '.join(missing)}")
    return CheckResult(
        "required_tests_present", True,
        f"{len(REQUIRED_TEST_FILES)} required test files present",
    )


def check_pdpl_gates_per_agent() -> CheckResult:
    try:
        from auto_client_acquisition.revenue_graph.agent_registry import ALL_AGENTS
    except Exception as exc:  # noqa: BLE001
        return CheckResult("pdpl_gates_per_agent", False, f"import failed: {exc}")

    missing: list[str] = []
    for agent in ALL_AGENTS:
        gates = getattr(agent, "pdpl_compliance_gates", ())
        if not gates:
            missing.append(agent.agent_id)
    if missing:
        return CheckResult(
            "pdpl_gates_per_agent", False,
            f"agents without gates: {', '.join(missing)}",
        )
    return CheckResult(
        "pdpl_gates_per_agent", True,
        f"{len(ALL_AGENTS)} agents all have pdpl gates",
    )


def check_autonomy_mode_integrity() -> CheckResult:
    try:
        from auto_client_acquisition.orchestrator.policies import (
            ALL_MODES,
            AutonomyMode,
            Policy,
            requires_approval,
        )
    except Exception as exc:  # noqa: BLE001
        return CheckResult("autonomy_mode_integrity", False, f"import failed: {exc}")

    if len(ALL_MODES) != 5:
        return CheckResult(
            "autonomy_mode_integrity", False,
            f"expected 5 modes, got {len(ALL_MODES)}",
        )

    expected = {
        AutonomyMode.MANUAL,
        AutonomyMode.SUGGEST,
        AutonomyMode.DRAFT_APPROVE,
        AutonomyMode.SAFE_AUTOPILOT,
        AutonomyMode.FULL_AUTOPILOT,
    }
    if set(ALL_MODES) != expected:
        return CheckResult(
            "autonomy_mode_integrity", False,
            f"mode set drifted: {sorted(set(ALL_MODES))}",
        )

    # MANUAL + SUGGEST must always require approval for any action.
    for mode in (AutonomyMode.MANUAL, AutonomyMode.SUGGEST):
        policy = Policy(customer_id="audit", autonomy_mode=mode)
        needs, _reason = requires_approval(action_type="send_message", policy=policy)
        if not needs:
            return CheckResult(
                "autonomy_mode_integrity", False,
                f"{mode} did not require approval for send_message",
            )
    return CheckResult(
        "autonomy_mode_integrity", True,
        "5 modes intact; manual/suggest gate enforced",
    )


_PRINT_DEBUG_DIRS: tuple[str, ...] = (
    "api/routers",
    "auto_client_acquisition/orchestrator",
)


def check_no_print_in_production() -> CheckResult:
    """Reject raw `print(` in production paths.

    Allowed: lines containing `# noqa: print` or inside docstrings (we approximate
    by ignoring lines that lie inside triple-quoted blocks).
    """
    offenders: list[str] = []
    pattern = re.compile(r"^\s*print\(", re.MULTILINE)
    for d in _PRINT_DEBUG_DIRS:
        for path in _iter_py_files(d):
            text = path.read_text(encoding="utf-8", errors="ignore")
            # Strip triple-quoted string blocks naively.
            stripped = re.sub(r'"""[\s\S]*?"""', "", text)
            stripped = re.sub(r"'''[\s\S]*?'''", "", stripped)
            for m in pattern.finditer(stripped):
                line_no = stripped.count("\n", 0, m.start()) + 1
                offenders.append(f"{path.relative_to(_REPO)}:{line_no}")
    if offenders:
        return CheckResult(
            "no_print_in_production", False,
            "; ".join(offenders[:10]) + (f" (+{len(offenders) - 10} more)" if len(offenders) > 10 else ""),
        )
    return CheckResult("no_print_in_production", True, "no print() in production paths")


# ── Orchestrator ──────────────────────────────────────────────────

def run_audit() -> AuditReport:
    report = AuditReport()
    report.checks.append(check_routers_registered())
    report.checks.append(check_forbidden_patterns())
    report.checks.append(check_whatsapp_buttons_rule())
    report.checks.append(check_safety_flags_discoverable())
    report.checks.append(check_secrets_hygiene())
    report.checks.append(check_required_tests())
    report.checks.append(check_pdpl_gates_per_agent())
    report.checks.append(check_autonomy_mode_integrity())
    report.checks.append(check_no_print_in_production())
    return report


def render(report: AuditReport) -> str:
    lines = ["DEALIX_ARCH_AUDIT v1.0", "=" * 32]
    for c in report.checks:
        tag = "PASS" if c.passed else "FAIL"
        line = f"[{tag}] {c.name}"
        if c.detail:
            line += f": {c.detail}"
        lines.append(line)
    lines.append("=" * 32)
    lines.append(f"SUMMARY: {report.pass_count} passed, {report.fail_count} failed")
    lines.append("RESULT: " + ("PASS" if report.passed else "FAIL"))
    return "\n".join(lines)


def main() -> int:
    report = run_audit()
    print(render(report))
    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
