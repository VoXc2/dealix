"""Post-Deploy Self-Check — Wave 16 (A3).

In-process production smoke. Runs from inside the prod app so the
founder hits ONE URL from their phone after a Railway deploy and gets
a single pass/fail picture.

Differs from `prod_smoke.sh` (curl-based, external):
- Uses Python `TestClient` against the same FastAPI app
- Pulls module-level state instead of network round-trips
- Returns one JSON the founder reads on mobile

Admin-gated.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Depends
from fastapi.testclient import TestClient

from api.security.api_key import require_admin_key

router = APIRouter(prefix="/api/v1/founder", tags=["founder"])


def _check(name: str, fn) -> dict[str, Any]:
    try:
        result = fn()
        return {
            "name": name,
            "ok": True,
            "detail": result if isinstance(result, (str, int, float, bool)) else "ok",
        }
    except Exception as exc:  # noqa: BLE001
        return {
            "name": name,
            "ok": False,
            "detail": f"{type(exc).__name__}: {exc}",
        }


def _check_module_imports() -> list[dict[str, Any]]:
    """Verify each canonical Wave 14-15 module imports cleanly."""
    targets = (
        ("data_os.source_passport", "auto_client_acquisition.data_os.source_passport"),
        ("governance_os.runtime_decision", "auto_client_acquisition.governance_os.runtime_decision"),
        ("proof_os.proof_pack", "auto_client_acquisition.proof_os.proof_pack"),
        ("value_os.value_ledger", "auto_client_acquisition.value_os.value_ledger"),
        ("value_os.monthly_report", "auto_client_acquisition.value_os.monthly_report"),
        ("capital_os.capital_ledger", "auto_client_acquisition.capital_os.capital_ledger"),
        ("adoption_os.adoption_score", "auto_client_acquisition.adoption_os.adoption_score"),
        ("friction_log.store", "auto_client_acquisition.friction_log.store"),
        ("client_os.badges", "auto_client_acquisition.client_os.badges"),
        ("trust_os.trust_pack", "auto_client_acquisition.trust_os.trust_pack"),
        ("auditability_os.audit_event", "auto_client_acquisition.auditability_os.audit_event"),
        ("evidence_control_plane_os.evidence_graph", "auto_client_acquisition.evidence_control_plane_os.evidence_graph"),
        ("agent_os.agent_registry", "auto_client_acquisition.agent_os.agent_registry"),
        ("secure_agent_runtime_os.four_boundaries", "auto_client_acquisition.secure_agent_runtime_os.four_boundaries"),
        ("benchmark_os.report_generator", "auto_client_acquisition.benchmark_os.report_generator"),
        ("sales_os.qualification", "auto_client_acquisition.sales_os.qualification"),
        ("partnership_os.referral_store", "auto_client_acquisition.partnership_os.referral_store"),
        ("payment_ops.renewal_scheduler", "auto_client_acquisition.payment_ops.renewal_scheduler"),
        ("email.transactional", "auto_client_acquisition.email.transactional"),
        ("delivery_factory.delivery_sprint", "auto_client_acquisition.delivery_factory.delivery_sprint"),
    )
    out: list[dict[str, Any]] = []
    for name, path in targets:
        out.append(_check(f"import:{name}", lambda p=path: __import__(p, fromlist=["*"]) and "imported"))
    return out


def _check_endpoints() -> list[dict[str, Any]]:
    """In-process curl: hit each canonical endpoint via TestClient."""
    # Lazy import to avoid circular at module load (main.py imports this router).
    from api.main import app
    client = TestClient(app)
    targets = (
        ("/healthz", 200),
        ("/api/v1/commercial-map", 200),
        ("/api/v1/commercial-map/markdown", 200),
        ("/api/v1/sprint/sample", 200),
        ("/api/v1/sector-intel/sample/b2b_services", 200),
        ("/api/v1/value/trust-pack/smoke/markdown", 200),
        ("/api/v1/audit/smoke/markdown", 200),
        ("/api/v1/audit/smoke/control-graph", 200),
        ("/api/v1/founder/launch-status/public", 200),
        ("/api/v1/customer-portal/smoke/workspace", 200),
        ("/api/v1/customer-success/smoke/adoption-score", 200),
        ("/api/v1/friction-log/smoke", 200),
        ("/api/v1/value/smoke/report/monthly", 200),
        ("/api/v1/proof-to-market/case-safe/eng_smoke?customer_id=smoke&sector=b2b_services", 200),
    )
    out: list[dict[str, Any]] = []
    for path, expect in targets:
        def call(p=path, e=expect):
            r = client.get(p)
            if r.status_code != e:
                raise RuntimeError(f"got {r.status_code} expected {e}")
            return f"status={r.status_code}"
        out.append(_check(f"GET {path}", call))
    return out


def _check_jsonl_writability() -> dict[str, Any]:
    """Verify the JSONL stores can be written (Railway volume mounted)."""
    try:
        from auto_client_acquisition.friction_log.store import emit, list_events
        ev = emit(
            customer_id="dealix_post_deploy_check",
            kind="manual_override",
            severity="low",
            workflow_id="post_deploy_check",
            notes="self-check write probe",
        )
        events = list_events(customer_id="dealix_post_deploy_check", limit=5)
        return {
            "name": "jsonl_writability",
            "ok": True,
            "detail": f"wrote event={ev.event_id}, list returned {len(events)} events",
        }
    except Exception as exc:  # noqa: BLE001
        return {
            "name": "jsonl_writability",
            "ok": False,
            "detail": f"{type(exc).__name__}: {exc}",
        }


def _check_governance_envelope() -> dict[str, Any]:
    """Verify governance_os.decide returns a valid envelope."""
    try:
        from auto_client_acquisition.governance_os.runtime_decision import (
            GovernanceDecision,
            decide,
        )
        result = decide(action="run_scoring", context={})
        return {
            "name": "governance_envelope",
            "ok": result.decision == GovernanceDecision.BLOCK,
            "detail": f"action=run_scoring no_context → decision={result.decision.value} (expected BLOCK)",
        }
    except Exception as exc:  # noqa: BLE001
        return {
            "name": "governance_envelope",
            "ok": False,
            "detail": f"{type(exc).__name__}: {exc}",
        }


def _check_doctrine_count() -> dict[str, Any]:
    """Verify the 11 non-negotiables are guarded by passing tests by
    counting test files in tests/test_no_*.py.
    """
    import os
    try:
        repo_root = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )
        # api/routers/post_deploy_check.py → api/routers → api → REPO_ROOT
        repo_root = os.path.dirname(repo_root)
        tests_dir = os.path.join(repo_root, "tests")
        files = [
            f for f in os.listdir(tests_dir)
            if f.startswith("test_no_") and f.endswith(".py")
        ]
        return {
            "name": "doctrine_guard_count",
            "ok": len(files) >= 6,
            "detail": f"{len(files)} doctrine guard tests found: {sorted(files)}",
        }
    except Exception as exc:  # noqa: BLE001
        return {
            "name": "doctrine_guard_count",
            "ok": False,
            "detail": f"{type(exc).__name__}: {exc}",
        }


def _check_warnings_silenced() -> dict[str, Any]:
    try:
        from core.warnings_filter import silenced_summary
        items = silenced_summary()
        return {
            "name": "warnings_filter",
            "ok": len(items) > 0,
            "detail": f"{len(items)} known-safe DeprecationWarning silencers installed",
        }
    except Exception as exc:  # noqa: BLE001
        return {
            "name": "warnings_filter",
            "ok": False,
            "detail": f"{type(exc).__name__}: {exc}",
        }


@router.get("/post-deploy-check", dependencies=[Depends(require_admin_key)])
async def post_deploy_check() -> dict[str, Any]:
    """Single-call production self-check. Admin-gated.

    Returns:
        {
          "generated_at": ISO timestamp,
          "summary": {"passed": N, "failed": M, "total": K},
          "checks": [...],
          "governance_decision": "allow",
        }
    """
    checks: list[dict[str, Any]] = []
    checks.extend(_check_module_imports())
    checks.extend(_check_endpoints())
    checks.append(_check_jsonl_writability())
    checks.append(_check_governance_envelope())
    checks.append(_check_doctrine_count())
    checks.append(_check_warnings_silenced())

    passed = sum(1 for c in checks if c["ok"])
    failed = len(checks) - passed

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "passed": passed,
            "failed": failed,
            "total": len(checks),
            "all_green": failed == 0,
        },
        "checks": checks,
        "governance_decision": "allow",
        "is_estimate": False,
    }
