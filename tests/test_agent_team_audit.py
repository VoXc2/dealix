"""Tests for the agent-team governance tooling.

These tests double as a guard: if a governance doc or an agent surface is removed,
the audit verdict flips to FAIL and this test catches it — the same protection the
`agent-team-audit` workflow gives on a PR.
"""

from __future__ import annotations

from scripts.audit_agent_team import build_report, main, render_markdown
from scripts.triage_open_prs import build_buckets, classify


def test_agent_team_audit_passes() -> None:
    report = build_report()
    assert report["verdict"] == "PASS", f"gaps: {report['gaps']}"


def test_claude_codex_registry_parity() -> None:
    report = build_report()
    parity = report["compatibility_agent_files"]
    assert parity["in_sync"], (
        f"claude_only={parity['claude_only']} codex_only={parity['codex_only']}"
    )
    # The five company-agent aliases remain mirrored compatibility surfaces;
    # logical-fleet authority lives in Agentic Holding, not this file count.
    for name in ("dealix-pm", "dealix-sales", "dealix-delivery", "dealix-engineer", "dealix-content"):
        assert name in parity["claude"]
        assert name in parity["codex"]

    specialists = report["platform_specific_specialists"]
    assert specialists["codex"] == ["dealix-fresh-reviewer", "improve-executor"]
    assert specialists["codex"] == specialists["declared_codex"]
    assert specialists["authority"] == "bounded_host_specialists_not_permanent_company_agents"
    assert not set(specialists["codex"]).intersection(parity["codex"])


def test_every_claude_agent_has_identity() -> None:
    report = build_report()
    for name, info in report["agent_frontmatter"].items():
        assert info["ok"], f"{name} missing frontmatter: {info['missing']}"


def test_required_governance_docs_present() -> None:
    report = build_report()
    missing = [doc for doc, ok in report["required_docs"].items() if not ok]
    assert not missing, f"missing governance docs: {missing}"


def test_doctrine_guard_tests_present() -> None:
    report = build_report()
    assert report["doctrine_guard_tests"]["ok"]


def test_render_markdown_contains_verdict() -> None:
    report = build_report()
    md = render_markdown(report)
    assert "Dealix Agent Governance Audit" in md
    assert "Verdict" in md


def test_main_exit_codes() -> None:
    assert main([]) == 0
    # Strict mode also returns 0 because the real repo passes the audit.
    assert main(["--strict"]) == 0


def test_pr_triage_classification() -> None:
    assert classify({"isDraft": True, "title": "anything"}) == "draft"
    assert classify({"title": "Fix security auth bypass"}) == "security"
    assert classify({"title": "Bump requests from 2.0 to 2.1"}) == "dependencies"
    assert classify({"title": "Add claude agent registry"}) == "agent"
    assert classify({"title": "docs: update runbook"}) == "docs"
    assert classify({"title": "Refactor lead pipeline"}) == "needs_review"
    # Bucket order: draft wins over security.
    assert classify({"isDraft": True, "title": "security fix"}) == "draft"


def test_pr_triage_buckets_cover_all_prs() -> None:
    prs = [
        {"number": 1, "title": "docs: x", "updatedAt": "2026-01-01"},
        {"number": 2, "title": "security fix", "updatedAt": "2026-01-02"},
        {"number": 3, "title": "feature", "isDraft": True, "updatedAt": "2026-01-03"},
    ]
    buckets = build_buckets(prs)
    assert sum(len(items) for items in buckets.values()) == len(prs)
