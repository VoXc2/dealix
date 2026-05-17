"""Truth Report — start from truth, not from building.

Every week, before claiming the system is ready, answer: is production the
version I think is running? Are the hard gates still locked? Is there real
revenue evidence? Is there paid intent?

The report is built from verifiable local facts (git, gate test files, the
value ledger). Operator-supplied facts (production SHA, verifier status)
are read from the environment and reported as ``unknown`` when absent —
never guessed.
"""

from __future__ import annotations

import os
import subprocess
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from auto_client_acquisition.revenue_assurance_os.root_cause import diagnose
from auto_client_acquisition.value_os.value_ledger import list_events

_REPO_ROOT = Path(__file__).resolve().parents[2]

# The non-negotiable gates and the test-filename substrings that lock each
# one. A gate is "locked" when at least one matching test file exists.
HARD_GATES: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("no_live_send", ("safe_send_gateway_blocking", "live_gates_default_false")),
    ("no_live_charge", ("no_live_charge",)),
    ("no_cold_whatsapp", ("no_cold_whatsapp",)),
    ("no_scraping", ("no_scraping", "no_linkedin_scraper")),
    ("no_fake_proof", ("no_fake_proof",)),
    ("no_guaranteed_claims", ("no_guaranteed_claims",)),
    ("no_linkedin_automation", ("no_linkedin_automation",)),
    ("no_pii_in_logs", ("no_pii_in_logs",)),
    ("no_source_no_answer", ("no_source_no_answer",)),
    ("no_source_passport_no_ai", ("no_source_passport_no_ai",)),
    ("forbidden_actions_doctrine", ("forbidden_actions", "doctrine_guardrails")),
)


@dataclass(frozen=True, slots=True)
class TruthReport:
    generated_at: str
    local_git_sha: str
    prod_git_sha: str
    git_sha_match: str
    verifier_status: str
    health_endpoint: str
    hard_gates: list[dict[str, Any]] = field(default_factory=list)
    revenue_evidence: dict[str, Any] = field(default_factory=dict)
    paid_intent: bool = False
    next_revenue_action: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _local_git_sha() -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],  # noqa: S607
            cwd=_REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        sha = result.stdout.strip()
        return sha or "unknown"
    except Exception:  # noqa: BLE001
        return "unknown"


def _test_file_names() -> list[str]:
    tests_dir = _REPO_ROOT / "tests"
    if not tests_dir.is_dir():
        return []
    return [p.name for p in tests_dir.rglob("test_*.py")]


def _hard_gate_states() -> list[dict[str, Any]]:
    names = _test_file_names()
    states: list[dict[str, Any]] = []
    for gate, patterns in HARD_GATES:
        matches = sorted({n for n in names if any(pat in n for pat in patterns)})
        states.append({"gate": gate, "test_files": matches, "locked": bool(matches)})
    return states


def _revenue_evidence() -> tuple[dict[str, Any], bool]:
    events = list_events(limit=10000)
    verified = sum(1 for e in events if e.tier == "verified")
    confirmed = sum(1 for e in events if e.tier == "client_confirmed")
    bankable = sum(e.amount for e in events if e.tier == "client_confirmed")
    evidence = {
        "value_events": len(events),
        "verified_count": verified,
        "client_confirmed_count": confirmed,
        "bankable_sar": round(bankable, 2),
    }
    return evidence, confirmed > 0


def build_truth_report(funnel_counts: dict[str, int] | None = None) -> TruthReport:
    """Assemble the weekly Truth Report from verifiable facts."""
    local_sha = _local_git_sha()
    prod_sha = os.environ.get("DEALIX_PROD_GIT_SHA", "").strip() or "unknown"
    if prod_sha == "unknown" or local_sha == "unknown":
        sha_match = "unknown"
    else:
        sha_match = "match" if prod_sha == local_sha else "MISMATCH"

    evidence, paid_intent = _revenue_evidence()

    if funnel_counts:
        next_action = diagnose(funnel_counts).recommended_action
    elif not paid_intent:
        next_action = "Close the first paid pilot — no confirmed revenue yet."
    else:
        next_action = "Convert a confirmed pilot into a Revenue Sprint or retainer."

    return TruthReport(
        generated_at=datetime.now(timezone.utc).isoformat(),
        local_git_sha=local_sha,
        prod_git_sha=prod_sha,
        git_sha_match=sha_match,
        verifier_status=os.environ.get("DEALIX_VERIFIER_STATUS", "").strip() or "not_run",
        health_endpoint=os.environ.get("DEALIX_HEALTH_STATUS", "").strip() or "not_checked",
        hard_gates=_hard_gate_states(),
        revenue_evidence=evidence,
        paid_intent=paid_intent,
        next_revenue_action=next_action,
    )


__all__ = [
    "HARD_GATES",
    "TruthReport",
    "build_truth_report",
]
