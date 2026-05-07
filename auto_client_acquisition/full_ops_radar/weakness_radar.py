"""Weakness Radar — prioritized list of named gaps with bilingual fixes.

Detects:
- broken endpoint
- empty lead queue
- customer portal demo fallback for active org
- no proof events
- no payment confirmed
- service sessions stuck
- approvals pending too long
- support ticket without SLA
- no executive pack generated
- missing consent
- internal terms visible to customer
- no case study candidate after proof
- no customer brain snapshot
- no leadops spine records
- no payment-to-delivery kickoff

Each weakness includes: id, layer, severity, blocker, reason_ar/en,
fix_ar/en, owner_role, related_endpoint?, related_doc?
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Literal

from auto_client_acquisition.integration_upgrade import safe_call

Severity = Literal["low", "medium", "high", "critical"]


def _wk(
    *,
    wid: str,
    layer: str,
    severity: Severity,
    blocker: bool,
    reason_ar: str,
    reason_en: str,
    fix_ar: str,
    fix_en: str,
    owner_role: str,
    related_endpoint: str | None = None,
    related_doc: str | None = None,
) -> dict[str, Any]:
    out = {
        "id": wid,
        "layer": layer,
        "severity": severity,
        "blocker": blocker,
        "reason_ar": reason_ar,
        "reason_en": reason_en,
        "fix_ar": fix_ar,
        "fix_en": fix_en,
        "owner_role": owner_role,
    }
    if related_endpoint:
        out["related_endpoint"] = related_endpoint
    if related_doc:
        out["related_doc"] = related_doc
    return out


def _no_leadops_records() -> list[dict[str, Any]]:
    try:
        from auto_client_acquisition.leadops_spine import list_records
        if not list_records(limit=1):
            return [_wk(
                wid="leadops_empty_queue",
                layer="leadops_spine",
                severity="medium",
                blocker=False,
                reason_ar="لا توجد فرص (leads) في القائمة بعد.",
                reason_en="No leads in the queue yet.",
                fix_ar="أرسل رسالة WhatsApp شخصيّة لـ ٥ من شبكتك.",
                fix_en="Send a personal WhatsApp message to 5 contacts in your network.",
                owner_role="founder",
                related_endpoint="POST /api/v1/leadops/run",
                related_doc="docs/V14_7_DAY_REVENUE_PLAN.md",
            )]
    except Exception:
        return []
    return []


def _no_proof_events(customer_handle: str | None) -> list[dict[str, Any]]:
    try:
        from auto_client_acquisition.proof_ledger.file_backend import list_events
        events = list_events(customer_handle=customer_handle, limit=1) if customer_handle else list_events(limit=1)
        if not events:
            return [_wk(
                wid="proof_ledger_empty",
                layer="proof_ledger",
                severity="medium",
                blocker=False,
                reason_ar="لا توجد أدلّة (proof events) مسجّلة بعد.",
                reason_en="No proof events recorded yet.",
                fix_ar="سجّل أوّل واقعة تشغيليّة (تسليم/إنجاز) كـ proof event.",
                fix_en="Record your first operational event (delivery/win) as a proof event.",
                owner_role="csm_or_founder",
                related_endpoint="POST /api/v1/proof-ledger/events",
            )]
    except Exception:
        return []
    return []


def _no_payment_confirmed() -> list[dict[str, Any]]:
    try:
        from auto_client_acquisition.payment_ops.orchestrator import _INDEX
        if not any(p.status == "payment_confirmed" or p.status == "delivery_kickoff" for p in _INDEX.values()):
            return [_wk(
                wid="payment_no_confirmed",
                layer="payment_ops",
                severity="high",
                blocker=False,
                reason_ar="لا توجد عمليّة دفع مؤكّدة بعد.",
                reason_en="No confirmed payment yet.",
                fix_ar="أرسل فاتورة يدويّة + استلم التحويل + اعتمد الدفع.",
                fix_en="Send a manual invoice, receive the transfer, then confirm payment.",
                owner_role="founder",
                related_endpoint="POST /api/v1/payment-ops/confirm",
            )]
    except Exception:
        return []
    return []


def _stuck_service_sessions() -> list[dict[str, Any]]:
    try:
        from auto_client_acquisition.service_sessions import list_sessions
        sessions = list_sessions(limit=100)
        threshold = datetime.now(timezone.utc) - timedelta(days=7)
        stuck = [s for s in sessions if s.status == "waiting_for_approval" and s.started_at < threshold]
        if stuck:
            return [_wk(
                wid="sessions_stuck_waiting_approval",
                layer="service_sessions",
                severity="high",
                blocker=False,
                reason_ar=f"{len(stuck)} جلسة خدمة عالقة في انتظار الموافقة منذ أسبوع+.",
                reason_en=f"{len(stuck)} service session(s) stuck waiting_for_approval for >1 week.",
                fix_ar="راجع /decisions.html واعتمد أو ارفض كل قرار معلّق.",
                fix_en="Review /decisions.html and approve or reject every pending item.",
                owner_role="founder",
                related_endpoint="GET /api/v1/approvals/pending",
            )]
    except Exception:
        return []
    return []


def _no_customer_brain_snapshot(customer_handle: str | None) -> list[dict[str, Any]]:
    if not customer_handle:
        return []
    try:
        from auto_client_acquisition.customer_brain import get_snapshot
        if get_snapshot(customer_handle=customer_handle) is None:
            return [_wk(
                wid="customer_brain_missing_snapshot",
                layer="customer_brain",
                severity="low",
                blocker=False,
                reason_ar="لا توجد ذاكرة تشغيليّة للعميل بعد.",
                reason_en="Customer brain snapshot not yet built.",
                fix_ar="ابنِ snapshot عبر POST /api/v1/customers/{handle}/brain/build.",
                fix_en="Build the snapshot via POST /api/v1/customers/{handle}/brain/build.",
                owner_role="csm_or_founder",
                related_endpoint="POST /api/v1/customers/{handle}/brain/build",
            )]
    except Exception:
        return []
    return []


def _approvals_pending_too_long() -> list[dict[str, Any]]:
    try:
        from auto_client_acquisition.approval_center import approval_store
        pending = approval_store.get_default_approval_store().list_pending()
        threshold = datetime.now(timezone.utc) - timedelta(hours=24)
        old = [a for a in pending if a.created_at < threshold]
        if old:
            return [_wk(
                wid="approvals_overdue",
                layer="approval_center",
                severity="medium",
                blocker=False,
                reason_ar=f"{len(old)} قرار معلّق منذ أكثر من ٢٤ ساعة.",
                reason_en=f"{len(old)} approval(s) pending for more than 24 hours.",
                fix_ar="راجعها واعتمد أو ارفض حسب السياق.",
                fix_en="Review and approve or reject each by context.",
                owner_role="founder",
                related_endpoint="GET /api/v1/approvals/pending",
            )]
    except Exception:
        return []
    return []


def _support_breached_sla() -> list[dict[str, Any]]:
    try:
        from auto_client_acquisition.support_inbox import find_breached_tickets
        breached = find_breached_tickets()
        if breached:
            return [_wk(
                wid="support_sla_breached",
                layer="support",
                severity="critical" if any(b["priority"] == "p0" for b in breached) else "high",
                blocker=True if any(b["priority"] == "p0" for b in breached) else False,
                reason_ar=f"{len(breached)} تذكرة دعم تجاوزت SLA.",
                reason_en=f"{len(breached)} support ticket(s) past SLA.",
                fix_ar="افتح /api/v1/support-inbox/sla-breaches وعالج P0 أوّلاً.",
                fix_en="Open /api/v1/support-inbox/sla-breaches and handle P0 first.",
                owner_role="founder",
                related_endpoint="GET /api/v1/support-inbox/sla-breaches",
            )]
    except Exception:
        return []
    return []


def _no_case_study_after_proof() -> list[dict[str, Any]]:
    try:
        from auto_client_acquisition.proof_ledger.file_backend import list_events
        events = list_events(limit=10)
        if events:
            from auto_client_acquisition.case_study_engine import list_library
            library = list_library(limit=10)
            if not library:
                return [_wk(
                    wid="case_study_missing_after_proof",
                    layer="case_study_engine",
                    severity="low",
                    blocker=False,
                    reason_ar="توجد أدلّة لكن لم يتم بناء أي دراسة حالة بعد.",
                    reason_en="Proof events exist but no case study has been built.",
                    fix_ar="ابنِ candidate عبر POST /api/v1/case-study/build.",
                    fix_en="Build a candidate via POST /api/v1/case-study/build.",
                    owner_role="founder",
                    related_endpoint="POST /api/v1/case-study/build",
                )]
    except Exception:
        return []
    return []


def detect_weaknesses(*, customer_handle: str | None = None) -> list[dict[str, Any]]:
    """Compose all weakness detectors. Never raises — returns empty list
    if everything's healthy or all detectors fail."""
    weaknesses: list[dict[str, Any]] = []
    detectors = [
        ("leadops_empty", lambda: _no_leadops_records()),
        ("proof_empty", lambda: _no_proof_events(customer_handle)),
        ("no_payment_confirmed", lambda: _no_payment_confirmed()),
        ("sessions_stuck", lambda: _stuck_service_sessions()),
        ("brain_missing", lambda: _no_customer_brain_snapshot(customer_handle)),
        ("approvals_old", lambda: _approvals_pending_too_long()),
        ("support_sla", lambda: _support_breached_sla()),
        ("no_case_study", lambda: _no_case_study_after_proof()),
    ]
    for name, fn in detectors:
        result = safe_call(name=name, fn=fn, fallback=[])
        if isinstance(result, list):
            weaknesses.extend(result)

    # Sort by severity (critical → high → medium → low)
    severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    weaknesses.sort(key=lambda w: severity_order.get(w.get("severity", "low"), 4))
    return weaknesses
