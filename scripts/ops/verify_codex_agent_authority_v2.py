#!/usr/bin/env python3
"""Verify current Dealix Codex engineering-agent authority and truth semantics."""

from __future__ import annotations

from pathlib import Path
import tomllib

ROOT = Path(__file__).resolve().parents[2]

AGENTS = {
    "engineer": ROOT / ".codex/agents/dealix-engineer.toml",
    "improve": ROOT / ".codex/agents/improve-executor.toml",
    "reviewer": ROOT / ".codex/agents/dealix-fresh-reviewer.toml",
}


def _load(path: Path) -> dict[str, object]:
    with path.open("rb") as handle:
        return tomllib.load(handle)


def _instructions(data: dict[str, object]) -> str:
    value = data.get("developer_instructions")
    assert isinstance(value, str) and value.strip(), "missing developer_instructions"
    return value


def main() -> int:
    loaded = {name: _load(path) for name, path in AGENTS.items()}
    engineer = _instructions(loaded["engineer"])
    improve = _instructions(loaded["improve"])
    reviewer = _instructions(loaded["reviewer"])

    assert loaded["engineer"].get("name") == "dealix-engineer"
    assert loaded["improve"].get("name") == "improve-executor"
    assert loaded["reviewer"].get("name") == "dealix-fresh-reviewer"

    # Current portfolio / evidence semantics.
    for required in (
        "CASH_READY_AUTONOMOUS_DEALIX_COMPANY",
        "UNKNOWN_NOT_EVIDENCE_BACKED",
        "fresh-main isolated branch/worktree",
        "customer send",
        "payment/refund/spend",
        "production, DNS, secrets",
    ):
        assert required in engineer, f"engineer missing current invariant: {required}"

    for forbidden in (
        "90-day commercial plan",
        "repo code is non-confidential",
        "free tier is fine",
    ):
        assert forbidden not in engineer.lower(), f"stale engineer authority: {forbidden}"
        assert forbidden not in improve.lower(), f"stale improve authority: {forbidden}"

    # No duplicate company architecture and no evidence-free self mutation.
    for duplicate in (
        "Company Brain",
        "Opportunity Graph",
        "Approval Center",
        "Proof Ledger",
        "scheduler",
        "Agent Council",
        "model router",
    ):
        assert duplicate in engineer, f"engineer duplicate-system guard missing: {duplicate}"
        assert duplicate in improve, f"improve duplicate-system guard missing: {duplicate}"

    for required in (
        "STALE_PLAN_REQUIRES_RECONCILIATION",
        "SUPERSEDED_NO_CHANGE_REQUIRED",
        "simulated",
        "UNVERIFIED",
        "UNKNOWN_NOT_EVIDENCE_BACKED",
        "isolated branch/worktree",
    ):
        assert required in improve, f"improve executor missing guard: {required}"

    # Independent review remains an explicit acceptance boundary for non-trivial work.
    assert "fresh read-only reviewer" in engineer
    assert "read-only" in reviewer.lower()
    assert "Never use `ship`" in reviewer

    print("PASS: Codex engineering agents use current Dealix authority/truth contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
