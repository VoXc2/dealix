#!/usr/bin/env python3
"""Fail-closed checks for privileged repository workflows.

This verifier is intentionally small and dependency-free. It checks only
invariants that can be validated from workflow text; it does not claim to
replace GitHub's permission model or a security review.
"""

from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]


def require(text: str, pattern: str, label: str) -> None:
    if not re.search(pattern, text, flags=re.MULTILINE):
        raise SystemExit(f"WORKFLOW_TRUST_CONTRACT=FAIL\nMISSING={label}")


def main() -> int:
    gate_path = ROOT / ".github/workflows/agentic-security-gate.yml"
    claude_path = ROOT / ".github/workflows/claude-code.yml"

    gate = gate_path.read_text(encoding="utf-8")
    claude = claude_path.read_text(encoding="utf-8")

    audit = gate.split("  workflow-audit:", 1)
    if len(audit) != 2:
        raise SystemExit("WORKFLOW_TRUST_CONTRACT=FAIL\nMISSING=workflow-audit-job")
    audit_job = audit[1]

    require(audit_job, r"actions/checkout@", "workflow-audit-checkout")
    require(
        audit_job,
        r"WORKFLOW_COUNT=.*find \.github/workflows",
        "workflow-audit-count",
    )
    require(audit_job, r'test "\$WORKFLOW_COUNT" -gt 0', "workflow-audit-nonempty")

    if "id-token: write" in claude:
        raise SystemExit(
            "WORKFLOW_TRUST_CONTRACT=FAIL\n"
            "REASON=claude-workflow-does-not-declare-unneeded-id-token"
        )

    if "contains(${{" in claude:
        raise SystemExit(
            "WORKFLOW_TRUST_CONTRACT=FAIL\n"
            "REASON=claude-if-uses-nested-expression-syntax"
        )

    require(claude, r"author_association", "claude-trusted-author-gate")
    for association in ("OWNER", "MEMBER", "COLLABORATOR"):
        require(
            claude,
            rf"author_association == '{association}'",
            f"claude-{association.lower()}",
        )

    for event_body in (
        "github.event.comment.body",
        "github.event.review.body",
        "github.event.issue.body",
    ):
        require(
            claude,
            rf"contains\({re.escape(event_body)}, '@claude'\)",
            f"claude-safe-contains-{event_body.split('.')[-2]}",
        )

    require(
        claude,
        r"jobs:\s*\n\s+claude:\s*\n(?:.*\n){0,8}\s+permissions:",
        "claude-job-permissions",
    )
    require(claude, r"contents: write", "claude-content-write")
    require(claude, r"pull-requests: write", "claude-pr-write")
    require(claude, r"issues: write", "claude-issue-write")

    print("WORKFLOW_TRUST_CONTRACT=PASS")
    print("WORKFLOW_AUDIT_CHECKOUT=1")
    print("WORKFLOW_AUDIT_NONEMPTY=1")
    print("CLAUDE_TRUSTED_AUTHOR_GATE=1")
    print("CLAUDE_ID_TOKEN_WRITE=0")
    print("CLAUDE_IF_EXPRESSION_SYNTAX=CANONICAL")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
