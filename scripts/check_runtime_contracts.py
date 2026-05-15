#!/usr/bin/env python3
"""Runtime contract smoke checks for core AI platform modules.

This script guards against regression where modules import but required symbols
are missing (or signature behavior drifts) due to partial refactors.
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


@dataclass
class CheckResult:
    name: str
    ok: bool
    details: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _check_api_main_import() -> CheckResult:
    from api.main import app

    route_count = len(getattr(app, "routes", []))
    if route_count <= 0:
        raise RuntimeError("FastAPI app has no routes")
    return CheckResult(
        name="api_main_import",
        ok=True,
        details={"route_count": route_count},
    )


def _check_value_ledger_contract() -> CheckResult:
    from auto_client_acquisition.value_os.value_ledger import (
        ValueDisciplineError,
        add_event,
        clear_for_test,
        list_events,
        summarize,
    )

    with tempfile.TemporaryDirectory() as tmp:
        ledger = os.path.join(tmp, "value-ledger.jsonl")
        os.environ["DEALIX_VALUE_LEDGER_PATH"] = ledger
        clear_for_test()
        try:
            add_event(customer_id="acme", kind="revenue", amount=10.0, tier="estimated")
            add_event(
                customer_id="acme",
                kind="revenue",
                amount=20.0,
                tier="verified",
                source_ref="invoice#1",
            )
            rows = list_events(customer_id="acme")
            summary = summarize(customer_id="acme", period_days=30)
            if len(rows) < 2:
                raise RuntimeError("value ledger list_events did not return expected rows")
            if "verified" not in summary:
                raise RuntimeError("value ledger summarize missing tier key")
            # Discipline guard must reject verified without source_ref.
            try:
                add_event(
                    customer_id="acme",
                    kind="revenue",
                    amount=5.0,
                    tier="verified",
                    source_ref="",
                )
                raise RuntimeError("value discipline guard failed")
            except ValueDisciplineError:
                pass
            return CheckResult(
                name="value_ledger_contract",
                ok=True,
                details={"rows": len(rows), "summary_total_events": summary.get("total_events", 0)},
            )
        finally:
            os.environ.pop("DEALIX_VALUE_LEDGER_PATH", None)


def _check_data_os_contract() -> CheckResult:
    from auto_client_acquisition.data_os.data_quality_score import compute_dq
    from auto_client_acquisition.data_os.import_preview import preview
    from auto_client_acquisition.data_os.source_passport import SourcePassport, validate

    csv_bytes = (
        "company_name,sector,city,contact_email\n"
        "Acme,logistics,Riyadh,ops@acme.sa\n"
    ).encode("utf-8")
    p = preview(csv_bytes)
    passport = SourcePassport(
        source_id="SRC-1",
        source_type="client_upload",
        owner="client",
        allowed_use=frozenset({"internal_analysis", "scoring"}),
        contains_pii=False,
        sensitivity="medium",
        retention_policy="project_duration",
        ai_access_allowed=True,
        external_use_allowed=False,
    )
    pv = validate(passport)
    dq = compute_dq(preview=p, duplicates_found=0, source_passport=passport)
    if not pv.is_valid:
        raise RuntimeError("source passport validation unexpectedly failed")
    if not (0 <= dq.overall <= 100):
        raise RuntimeError("dq score out of range")
    return CheckResult(
        name="data_os_contract",
        ok=True,
        details={"preview_row_count": p.row_count, "dq_overall": dq.overall},
    )


def _check_runtime_decision_contract() -> CheckResult:
    from auto_client_acquisition.governance_os.runtime_decision import decide

    blocked = decide(
        action_type="whatsapp.send_message",
        actor="runtime_contracts",
        risk_score=0.9,
    )
    allowed = decide(
        action_type="run_scoring",
        context={
            "source_passport": object(),
            "contains_pii": False,
            "external_use": False,
        },
    )
    if blocked.decision.value.lower() not in {"escalate", "require_approval"}:
        raise RuntimeError("high-risk action should escalate or require approval")
    if allowed.decision.value.lower() not in {"allow", "allow_with_review"}:
        raise RuntimeError("run_scoring should be allowed for low-risk context")
    if not hasattr(blocked, "approval_required"):
        raise RuntimeError("runtime decision missing approval_required field")
    return CheckResult(
        name="runtime_decision_contract",
        ok=True,
        details={
            "blocked_decision": blocked.decision.value,
            "allowed_decision": allowed.decision.value,
        },
    )


def _check_auditability_contract() -> CheckResult:
    from auto_client_acquisition.auditability_os.audit_event import (
        AuditEventKind,
        clear_for_test,
        list_events,
        record_event,
    )
    from auto_client_acquisition.auditability_os.evidence_chain import build_chain

    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "audit.jsonl")
        os.environ["DEALIX_AUDIT_LOG_PATH"] = path
        clear_for_test()
        try:
            record_event(
                customer_id="acme",
                engagement_id="run_1",
                kind=AuditEventKind.SOURCE_PASSPORT_VALIDATED,
                source_refs=["SRC-1"],
                summary="validated",
            )
            record_event(
                customer_id="acme",
                engagement_id="run_1",
                kind=AuditEventKind.AI_RUN,
                output_refs=["OUT-1"],
                summary="ai run completed",
            )
            chain = build_chain(customer_id="acme", engagement_id="run_1")
            if len(list_events(customer_id="acme")) < 2:
                raise RuntimeError("audit list_events did not return expected rows")
            if chain.node_count < 2:
                raise RuntimeError("evidence chain missing expected nodes")
            return CheckResult(
                name="auditability_contract",
                ok=True,
                details={"node_count": chain.node_count},
            )
        finally:
            os.environ.pop("DEALIX_AUDIT_LOG_PATH", None)


def main() -> int:
    checks = [
        _check_api_main_import,
        _check_value_ledger_contract,
        _check_data_os_contract,
        _check_runtime_decision_contract,
        _check_auditability_contract,
    ]
    results: list[CheckResult] = []
    failures: list[dict[str, Any]] = []

    for fn in checks:
        try:
            results.append(fn())
        except Exception as exc:  # noqa: BLE001
            failures.append({"check": fn.__name__, "error": str(exc)})

    report = {
        "ok": not failures,
        "checks": [r.to_dict() for r in results],
        "failures": failures,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
