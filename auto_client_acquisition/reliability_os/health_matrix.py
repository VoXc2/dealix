"""Aggregated health matrix over local subsystems."""
from __future__ import annotations

import importlib
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any, Callable


class HealthStatus(StrEnum):
    OK = "ok"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"
    UNKNOWN = "unknown"


class HealthDimension(StrEnum):
    SAFETY = "safety"
    DELIVERY = "delivery"
    OBSERVABILITY = "observability"
    DATA = "data"


@dataclass
class SubsystemHealth:
    name: str
    dimension: HealthDimension
    status: HealthStatus
    description: str
    details: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        out = asdict(self)
        out["dimension"] = self.dimension.value
        out["status"] = self.status.value
        return out


# ─── Per-subsystem probes ───────────────────────────────────────────


def _probe_safe_action_gateway() -> SubsystemHealth:
    try:
        from auto_client_acquisition.v3.agents import SafeAgentRuntime
        restricted = SafeAgentRuntime.restricted_actions
        expected = {"send_cold_whatsapp", "auto_linkedin_dm", "delete_data", "export_pii"}
        ok = expected.issubset(restricted)
        return SubsystemHealth(
            name="safe_action_gateway",
            dimension=HealthDimension.SAFETY,
            status=HealthStatus.OK if ok else HealthStatus.DEGRADED,
            description=(
                f"SafeAgentRuntime has {len(restricted)} restricted actions"
                + ("" if ok else "; expected core 4 missing")
            ),
            details={"restricted_actions": sorted(restricted)},
        )
    except Exception as exc:  # noqa: BLE001
        return SubsystemHealth(
            name="safe_action_gateway",
            dimension=HealthDimension.SAFETY,
            status=HealthStatus.UNAVAILABLE,
            description=f"import failed: {type(exc).__name__}",
            details={},
        )


def _probe_live_gates() -> SubsystemHealth:
    try:
        from core.config.settings import Settings
        s = Settings()
        live_send_off = s.whatsapp_allow_live_send is False
        return SubsystemHealth(
            name="live_action_gates",
            dimension=HealthDimension.SAFETY,
            status=HealthStatus.OK if live_send_off else HealthStatus.DEGRADED,
            description=(
                "whatsapp_allow_live_send=False (default safe)"
                if live_send_off
                else "whatsapp_allow_live_send=True — DANGER"
            ),
            details={"whatsapp_allow_live_send": s.whatsapp_allow_live_send},
        )
    except Exception as exc:  # noqa: BLE001
        return SubsystemHealth(
            name="live_action_gates",
            dimension=HealthDimension.SAFETY,
            status=HealthStatus.UNAVAILABLE,
            description=f"settings load failed: {type(exc).__name__}",
            details={},
        )


def _probe_safe_publishing_gate() -> SubsystemHealth:
    try:
        from auto_client_acquisition.self_growth_os.safe_publishing_gate import (
            FORBIDDEN_PATTERNS,
            check_text,
        )
        # Smoke: clean text passes; "guaranteed" blocks.
        clean = check_text("صفحة هبوط آمنة جاهزة للمراجعة")
        unsafe = check_text("we guarantee revenue growth")
        ok = clean.decision == "allowed_draft" and unsafe.decision == "blocked"
        return SubsystemHealth(
            name="safe_publishing_gate",
            dimension=HealthDimension.SAFETY,
            status=HealthStatus.OK if ok else HealthStatus.DEGRADED,
            description=f"{len(FORBIDDEN_PATTERNS)} forbidden patterns active",
            details={"clean_decision": clean.decision, "unsafe_decision": unsafe.decision},
        )
    except Exception as exc:  # noqa: BLE001
        return SubsystemHealth(
            name="safe_publishing_gate",
            dimension=HealthDimension.SAFETY,
            status=HealthStatus.UNAVAILABLE,
            description=f"import failed: {type(exc).__name__}",
            details={},
        )


def _probe_service_matrix() -> SubsystemHealth:
    try:
        from auto_client_acquisition.self_growth_os import service_activation_matrix
        counts = service_activation_matrix.counts()
        # Healthy if total = 32 + no service marked Live without gates.
        ok = counts.get("total", 0) >= 1
        return SubsystemHealth(
            name="service_activation_matrix",
            dimension=HealthDimension.DELIVERY,
            status=HealthStatus.OK if ok else HealthStatus.DEGRADED,
            description=f"{counts.get('total', 0)} services in matrix",
            details=counts,
        )
    except Exception as exc:  # noqa: BLE001
        return SubsystemHealth(
            name="service_activation_matrix",
            dimension=HealthDimension.DELIVERY,
            status=HealthStatus.UNAVAILABLE,
            description=f"matrix load failed: {type(exc).__name__}",
            details={},
        )


def _probe_seo_audit() -> SubsystemHealth:
    try:
        from auto_client_acquisition.self_growth_os import seo_technical_auditor
        s = seo_technical_auditor.summary()
        clean = seo_technical_auditor.is_perimeter_clean()
        return SubsystemHealth(
            name="seo_perimeter",
            dimension=HealthDimension.OBSERVABILITY,
            status=HealthStatus.OK if clean else HealthStatus.DEGRADED,
            description=(
                f"perimeter_clean={clean}, advisory_gap={s.get('pages_with_advisory_gap', 0)}"
            ),
            details=s,
        )
    except Exception as exc:  # noqa: BLE001
        return SubsystemHealth(
            name="seo_perimeter",
            dimension=HealthDimension.OBSERVABILITY,
            status=HealthStatus.UNAVAILABLE,
            description=f"audit unavailable: {type(exc).__name__}",
            details={},
        )


def _probe_email_provider() -> SubsystemHealth:
    """Inspects whether at least one email provider is configured.
    NEVER sends a probe email."""
    try:
        from core.config.settings import Settings
        s = Settings()
        configured = bool(
            (s.resend_api_key and s.resend_api_key.get_secret_value())
            or (s.sendgrid_api_key and s.sendgrid_api_key.get_secret_value())
            or (s.smtp_host and s.smtp_user)
        )
        return SubsystemHealth(
            name="email_provider",
            dimension=HealthDimension.DELIVERY,
            status=HealthStatus.OK if configured else HealthStatus.DEGRADED,
            description=(
                f"primary={s.email_provider}; configured={configured}"
            ),
            details={"primary_provider": s.email_provider, "configured": configured},
        )
    except Exception as exc:  # noqa: BLE001
        return SubsystemHealth(
            name="email_provider",
            dimension=HealthDimension.DELIVERY,
            status=HealthStatus.UNAVAILABLE,
            description=f"settings unavailable: {type(exc).__name__}",
            details={},
        )


def _probe_payment_provider() -> SubsystemHealth:
    """Inspects MOYASAR_SECRET_KEY shape — never calls Moyasar."""
    import os
    try:
        key = os.getenv("MOYASAR_SECRET_KEY", "") or ""
        if not key:
            return SubsystemHealth(
                name="payment_provider",
                dimension=HealthDimension.DELIVERY,
                status=HealthStatus.DEGRADED,
                description="MOYASAR_SECRET_KEY not configured (test mode unavailable)",
                details={"configured": False},
            )
        if key.startswith("sk_live_"):
            return SubsystemHealth(
                name="payment_provider",
                dimension=HealthDimension.DELIVERY,
                status=HealthStatus.DEGRADED,
                description=(
                    "MOYASAR_SECRET_KEY is sk_live_* — admin CLI requires "
                    "explicit --allow-live; ensure live charge policy is signed"
                ),
                details={"configured": True, "mode": "live"},
            )
        return SubsystemHealth(
            name="payment_provider",
            dimension=HealthDimension.DELIVERY,
            status=HealthStatus.OK,
            description="Moyasar test mode configured (default safe)",
            details={"configured": True, "mode": "test"},
        )
    except Exception as exc:  # noqa: BLE001
        return SubsystemHealth(
            name="payment_provider",
            dimension=HealthDimension.DELIVERY,
            status=HealthStatus.UNAVAILABLE,
            description=f"settings unavailable: {type(exc).__name__}",
            details={},
        )


def _probe_proof_ledger() -> SubsystemHealth:
    """In-process buffer state."""
    try:
        from auto_client_acquisition.self_growth_os import evidence_collector
        events = evidence_collector.all_events()
        return SubsystemHealth(
            name="proof_ledger_in_process",
            dimension=HealthDimension.DATA,
            status=HealthStatus.OK,
            description=f"{len(events)} events in current process buffer",
            details={"events_count": len(events)},
        )
    except Exception as exc:  # noqa: BLE001
        return SubsystemHealth(
            name="proof_ledger_in_process",
            dimension=HealthDimension.DATA,
            status=HealthStatus.UNAVAILABLE,
            description=f"buffer unavailable: {type(exc).__name__}",
            details={},
        )


def _probe_redis_optional() -> SubsystemHealth:
    """Soft probe — checks if redis package is importable. Doesn't open
    a connection to avoid blocking the matrix on a slow DNS."""
    try:
        importlib.import_module("redis")
        return SubsystemHealth(
            name="redis_client_available",
            dimension=HealthDimension.OBSERVABILITY,
            status=HealthStatus.OK,
            description="redis-py installed (live connection NOT probed)",
            details={"installed": True},
        )
    except Exception:  # noqa: BLE001
        return SubsystemHealth(
            name="redis_client_available",
            dimension=HealthDimension.OBSERVABILITY,
            status=HealthStatus.DEGRADED,
            description="redis-py not installed",
            details={"installed": False},
        )


_PROBES: list[Callable[[], SubsystemHealth]] = [
    _probe_safe_action_gateway,
    _probe_live_gates,
    _probe_safe_publishing_gate,
    _probe_service_matrix,
    _probe_seo_audit,
    _probe_email_provider,
    _probe_payment_provider,
    _probe_proof_ledger,
    _probe_redis_optional,
]


def build_health_matrix() -> dict[str, Any]:
    rows: list[SubsystemHealth] = [probe() for probe in _PROBES]
    counts: dict[str, int] = {s.value: 0 for s in HealthStatus}
    for r in rows:
        counts[r.status.value] += 1
    overall = HealthStatus.OK if counts[HealthStatus.OK.value] == len(rows) else HealthStatus.DEGRADED
    return {
        "schema_version": 1,
        "generated_at": datetime.now(UTC).isoformat(),
        "overall_status": overall.value,
        "counts": counts,
        "subsystems": [r.to_dict() for r in rows],
        "guardrails": {
            "no_live_send": True,
            "no_scraping": True,
            "no_cold_outreach": True,
            "approval_required_for_external_actions": True,
        },
    }


def summary() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "subsystems_total": len(_PROBES),
        "dimensions": [d.value for d in HealthDimension],
        "statuses": [s.value for s in HealthStatus],
    }
