"""Eval report for the lead_qualification workflow.

Evaluates the declarative checks in ``evals/lead_qualification_eval.yaml``
against a live ``WorkflowRun`` checkpoint. An eval failure does not crash
the run — it downgrades the run's governance decision to ALLOW_WITH_REVIEW
so a human reviews before the result is trusted.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from auto_client_acquisition.compliance_trust_os.approval_engine import GovernanceDecision
from auto_client_acquisition.sales_os.lead_qualification.sales_agent import DRAFT_LABEL

_EVAL_PATH = Path(__file__).resolve().parents[3] / "evals" / "lead_qualification_eval.yaml"


def load_eval_spec() -> dict[str, Any]:
    """Load the declarative eval spec from the evals/ directory."""
    with _EVAL_PATH.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _check_governance_present(checkpoint: dict[str, Any]) -> tuple[bool, str]:
    results = checkpoint.get("step_results", [])
    if not results:
        return False, "no step results recorded"
    missing = [r["step_id"] for r in results if not r.get("governance_decision")]
    if missing:
        return False, f"steps missing governance_decision: {missing}"
    return True, f"{len(results)} step results carry a governance_decision"


def _check_draft_labeled(checkpoint: dict[str, Any]) -> tuple[bool, str]:
    draft = checkpoint.get("draft", "")
    if not draft:
        return False, "no draft produced"
    if draft.startswith(DRAFT_LABEL):
        return True, "draft begins with the draft label"
    return False, "draft is not labeled as a draft"


def _check_no_forbidden_language(checkpoint: dict[str, Any]) -> tuple[bool, str]:
    risk = checkpoint.get("risk", {})
    if not risk:
        return False, "risk check did not run"
    if risk.get("decision") == str(GovernanceDecision.BLOCK):
        return False, f"risk check blocked: {risk.get('policy_issues')}"
    issues = risk.get("policy_issues", []) + risk.get("claim_issues", [])
    if issues:
        return False, f"governance issues raised: {issues}"
    return True, "no forbidden language detected"


def _check_approval_gated(checkpoint: dict[str, Any]) -> tuple[bool, str]:
    approval_id = checkpoint.get("approval_id", "")
    if approval_id:
        return True, f"approval request created: {approval_id}"
    return False, "no approval request was created"


def _check_score_justified(checkpoint: dict[str, Any]) -> tuple[bool, str]:
    reasons = checkpoint.get("qualification", {}).get("reasons", [])
    if reasons:
        return True, f"verdict backed by reasons: {reasons}"
    return False, "qualification verdict has no documented reason"


_CHECKS = {
    "governance_present": _check_governance_present,
    "draft_labeled": _check_draft_labeled,
    "no_forbidden_language": _check_no_forbidden_language,
    "approval_gated": _check_approval_gated,
    "score_justified": _check_score_justified,
}


def build_eval_report(run: Any) -> dict[str, Any]:
    """Evaluate the eval spec against ``run.checkpoint``."""
    spec = load_eval_spec()
    checkpoint = run.checkpoint
    results: list[dict[str, Any]] = []
    for check in spec.get("checks", []):
        check_id = check["id"]
        fn = _CHECKS.get(check_id)
        if fn is None:
            results.append({"id": check_id, "passed": False, "detail": "unknown check"})
            continue
        passed, detail = fn(checkpoint)
        results.append({"id": check_id, "passed": passed, "detail": detail})
    return {
        "eval_id": spec.get("eval_id", "lead_qualification"),
        "version": spec.get("version", 1),
        "checks": results,
        "overall_pass": all(r["passed"] for r in results),
    }


__all__ = ["build_eval_report", "load_eval_spec"]
