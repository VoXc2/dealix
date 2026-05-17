"""Affiliate OS — approved-asset registry.

Affiliate-submitted promotional copy must clear THREE governance gates before
it becomes an approved asset:

1. ``audit_claim_safety`` — the governance_os forbidden-claim/term scan.
2. ``runtime_decision.decide`` — regex guaranteed-outcome detection (handles
   negation: "we do not guarantee ..." is not flagged).
3. the ``affiliate_rules.yaml`` ``forbidden_claims`` substring list.

If any gate flags a forbidden claim, the asset is BLOCKED and no approved
asset is produced. These are shallow backstops — human review of every asset
remains mandatory; the governance verdict is advisory, not a substitute.
"""

from __future__ import annotations

import json
import os
import threading
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.affiliate_os.affiliate_store import AFFILIATE_OPS_TENANT
from auto_client_acquisition.affiliate_os.rules_loader import (
    disclosure_text,
    forbidden_claims,
)
from auto_client_acquisition.auditability_os.audit_event import (
    AuditEventKind,
    record_event,
)
from auto_client_acquisition.compliance_trust_os.approval_engine import (
    GovernanceDecision,
)
from auto_client_acquisition.governance_os import runtime_decision
from auto_client_acquisition.governance_os.claim_safety import audit_claim_safety

_ASSETS_PATH_DEFAULT = "var/affiliate-assets.jsonl"
_lock = threading.Lock()


def _resolve(env_var: str, default_rel: str) -> Path:
    p = Path(os.environ.get(env_var, default_rel))
    if not p.is_absolute():
        p = Path(__file__).resolve().parent.parent.parent / p
    return p


def _assets_path() -> Path:
    return _resolve("DEALIX_AFFILIATE_ASSETS_PATH", _ASSETS_PATH_DEFAULT)


class AssetSubmission(BaseModel):
    model_config = ConfigDict(extra="forbid")

    asset_id: str = Field(min_length=1, max_length=64)
    affiliate_id: str = Field(min_length=1, max_length=64)
    copy_text: str = Field(min_length=1, max_length=4000)
    locale: Literal["en", "ar"] = "en"


class ApprovedAsset(BaseModel):
    model_config = ConfigDict(extra="forbid")

    asset_id: str
    affiliate_id: str
    copy_text: str
    disclosure_text: str
    locale: str
    governance_decision: str
    approved_at: str


@dataclass(frozen=True, slots=True)
class AssetReviewResult:
    decision: GovernanceDecision
    issues: tuple[str, ...]
    approved_asset: ApprovedAsset | None


def _append(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with _lock:
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")


def _read_all(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    out: list[dict[str, Any]] = []
    with _lock:
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    out.append(json.loads(line))
                except Exception:  # noqa: BLE001
                    continue
    return out


def _forbidden_claim_hits(text: str) -> list[str]:
    low = text.lower()
    return [f"forbidden_claim:{c}" for c in forbidden_claims() if c and c in low]


def review_asset_copy(submission: AssetSubmission) -> AssetReviewResult:
    """Run affiliate copy through the three governance gates."""
    text = submission.copy_text
    claim = audit_claim_safety(text)
    rt = runtime_decision.decide(context={"text": text})
    rule_hits = _forbidden_claim_hits(text)

    issues: tuple[str, ...] = tuple(
        dict.fromkeys((*claim.issues, *rule_hits))
    )
    guarantee_blocked = str(rt.decision) == "block"

    if claim.suggested_decision == GovernanceDecision.BLOCK or guarantee_blocked or rule_hits:
        decision = GovernanceDecision.BLOCK
        if guarantee_blocked and "guaranteed_outcome_claim" not in issues:
            issues = (*issues, "guaranteed_outcome_claim")
        approved: ApprovedAsset | None = None
    elif issues:
        decision = GovernanceDecision.DRAFT_ONLY
        approved = None
    else:
        decision = GovernanceDecision.ALLOW
        approved = ApprovedAsset(
            asset_id=submission.asset_id,
            affiliate_id=submission.affiliate_id,
            copy_text=text,
            disclosure_text=disclosure_text(submission.locale),
            locale=submission.locale,
            governance_decision=decision.value,
            approved_at=datetime.now(UTC).isoformat(),
        )

    record_event(
        customer_id=AFFILIATE_OPS_TENANT,
        kind=AuditEventKind.GOVERNANCE_DECISION,
        actor="affiliate_os",
        decision=decision.value,
        policy_checked="affiliate_asset_claim_safety",
        summary=f"asset {submission.asset_id}: {', '.join(issues) or 'clean'}",
        source_refs=[submission.affiliate_id, submission.asset_id],
    )

    if approved is not None:
        _append(_assets_path(), approved.model_dump())

    return AssetReviewResult(decision=decision, issues=issues, approved_asset=approved)


def list_approved_assets(*, affiliate_id: str | None = None) -> list[ApprovedAsset]:
    out: list[ApprovedAsset] = []
    for row in _read_all(_assets_path()):
        if affiliate_id and row.get("affiliate_id") != affiliate_id:
            continue
        out.append(ApprovedAsset(**row))
    return out


def get_disclosure_text(locale: str = "en") -> str:
    return disclosure_text(locale)


def clear_for_test() -> None:
    path = _assets_path()
    if path.exists():
        with _lock:
            path.write_text("", encoding="utf-8")


__all__ = [
    "ApprovedAsset",
    "AssetReviewResult",
    "AssetSubmission",
    "clear_for_test",
    "get_disclosure_text",
    "list_approved_assets",
    "review_asset_copy",
]
