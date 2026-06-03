"""Thread-safe JSON file store for autopilot records."""

from __future__ import annotations

import json
import os
import threading
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from pydantic import TypeAdapter

from dealix.revenue_ops_autopilot.schemas import (
    DiagnosticDeliveryRecord,
    EvidenceEvent,
    FunnelLeadRecord,
    InvoiceDraftRecord,
    OpportunityRecord,
    SupportTicketRecord,
)
from dealix.revenue_ops_autopilot.war_room import normalize_lead

_DEFAULT_PATH_ENV = "DEALIX_REVENUE_AUTOPILOT_STORE"

_LEADS_TA = TypeAdapter(list[FunnelLeadRecord])
_OPPS_TA = TypeAdapter(list[OpportunityRecord])
_TICKETS_TA = TypeAdapter(list[SupportTicketRecord])
_EVID_TA = TypeAdapter(list[EvidenceEvent])
_DIAG_TA = TypeAdapter(list[DiagnosticDeliveryRecord])
_INV_TA = TypeAdapter(list[InvoiceDraftRecord])


def default_store_path() -> Path:
    raw = os.environ.get(_DEFAULT_PATH_ENV, "")
    if raw.strip():
        p = Path(raw)
    else:
        p = Path(__file__).resolve().parents[2] / "var" / "revenue_ops_autopilot.json"
    if not p.is_absolute():
        p = Path(__file__).resolve().parents[2] / p
    return p


def _utcnow_iso() -> str:
    return datetime.now(UTC).isoformat()


def _new(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


class AutopilotJSONStore:
    def __init__(self, path: Path | None = None) -> None:
        self._path = path or default_store_path()
        self._lock = threading.Lock()

    def _read_raw(self) -> dict[str, Any]:
        if not self._path.exists():
            return {
                "version": 1,
                "generated_at": _utcnow_iso(),
                "leads": [],
                "opportunities": [],
                "support_tickets": [],
                "evidence_events": [],
                "diagnostics": [],
                "invoice_drafts": [],
            }
        try:
            return json.loads(self._path.read_text(encoding="utf-8"))
        except Exception:
            return {
                "version": 1,
                "generated_at": _utcnow_iso(),
                "leads": [],
                "opportunities": [],
                "support_tickets": [],
                "evidence_events": [],
                "diagnostics": [],
                "invoice_drafts": [],
                "corrupted_previous": True,
            }

    def _write_atomic(self, data: dict[str, Any]) -> None:
        import shutil
        import time

        self._path.parent.mkdir(parents=True, exist_ok=True)
        data["generated_at"] = _utcnow_iso()
        payload = json.dumps(data, ensure_ascii=False, indent=2, default=str)
        tmp = self._path.with_suffix(".tmp")
        last_err: OSError | None = None
        for attempt in range(5):
            try:
                tmp.write_text(payload, encoding="utf-8")
                tmp.replace(self._path)
                return
            except OSError as exc:
                last_err = exc
                if tmp.is_file():
                    try:
                        shutil.copyfile(tmp, self._path)
                        tmp.unlink(missing_ok=True)
                        return
                    except OSError:
                        pass
                if attempt < 4:
                    time.sleep(0.08 * (attempt + 1))
                    continue
        try:
            self._path.write_text(payload, encoding="utf-8")
            tmp.unlink(missing_ok=True)
            return
        except OSError:
            if last_err:
                raise last_err
            raise

    def _mutate(self, fn: Any) -> Any:
        with self._lock:
            blob = self._read_raw()
            out = fn(blob)
            self._write_atomic(blob)
            return out

    def list_leads(self, limit: int = 500) -> list[FunnelLeadRecord]:
        blob = self._read_raw()
        leads = [normalize_lead(L) for L in _LEADS_TA.validate_python(blob.get("leads") or [])]
        leads.sort(key=lambda x: x.created_at, reverse=True)
        return leads[:limit]

    def get_lead(self, lead_id: str) -> FunnelLeadRecord | None:
        for L in self.list_leads(limit=5000):
            if L.id == lead_id:
                return L
        return None

    def upsert_lead(self, lead: FunnelLeadRecord) -> FunnelLeadRecord:
        def _fn(blob: dict[str, Any]) -> FunnelLeadRecord:
            leads_raw = blob.get("leads") or []
            leads = _LEADS_TA.validate_python(leads_raw)
            rest = [x for x in leads if x.id != lead.id]
            rest.append(lead)
            blob["leads"] = [x.model_dump(mode="json") for x in rest]
            return lead

        return self._mutate(_fn)

    def append_evidence(self, event: EvidenceEvent) -> EvidenceEvent:
        def _fn(blob: dict[str, Any]) -> EvidenceEvent:
            evs = blob.get("evidence_events") or []
            evs.append(event.model_dump(mode="json"))
            blob["evidence_events"] = evs
            return event

        return self._mutate(_fn)

    def list_evidence(self, *, limit: int = 100) -> list[EvidenceEvent]:
        blob = self._read_raw()
        evs = _EVID_TA.validate_python(blob.get("evidence_events") or [])
        evs.sort(key=lambda x: x.created_at, reverse=True)
        return evs[:limit]

    def append_ticket(self, ticket: SupportTicketRecord) -> SupportTicketRecord:
        def _fn(blob: dict[str, Any]) -> SupportTicketRecord:
            tix = blob.get("support_tickets") or []
            tix.append(ticket.model_dump(mode="json"))
            blob["support_tickets"] = tix
            return ticket

        return self._mutate(_fn)

    def list_tickets(self, *, limit: int = 100) -> list[SupportTicketRecord]:
        blob = self._read_raw()
        out = _TICKETS_TA.validate_python(blob.get("support_tickets") or [])
        out.sort(key=lambda x: x.created_at, reverse=True)
        return out[:limit]

    def upsert_ticket(self, ticket: SupportTicketRecord) -> SupportTicketRecord:
        def _fn(blob: dict[str, Any]) -> SupportTicketRecord:
            tix = _TICKETS_TA.validate_python(blob.get("support_tickets") or [])
            rest = [x for x in tix if x.id != ticket.id]
            rest.append(ticket)
            blob["support_tickets"] = [x.model_dump(mode="json") for x in rest]
            return ticket

        return self._mutate(_fn)

    def pipeline_counts(self) -> dict[str, int]:
        blob = self._read_raw()
        leads = _LEADS_TA.validate_python(blob.get("leads") or [])
        counts: dict[str, int] = {}
        for key in (
            "new_lead",
            "qualified_A",
            "qualified_B",
            "nurture",
            "partner_candidate",
            "meeting_booked",
            "meeting_done",
            "scope_requested",
            "scope_sent",
            "invoice_sent",
            "invoice_paid",
            "delivery_started",
            "proof_pack_sent",
            "sprint_candidate",
            "retainer_candidate",
            "closed_lost",
        ):
            counts[key] = sum(1 for L in leads if L.stage == key)
        return counts

    def append_invoice_draft(self, inv: InvoiceDraftRecord) -> InvoiceDraftRecord:
        def _fn(blob: dict[str, Any]) -> InvoiceDraftRecord:
            rows = blob.get("invoice_drafts") or []
            rows.append(inv.model_dump(mode="json"))
            blob["invoice_drafts"] = rows
            return inv

        return self._mutate(_fn)

    def append_diagnostic(self, rec: DiagnosticDeliveryRecord) -> DiagnosticDeliveryRecord:
        def _fn(blob: dict[str, Any]) -> DiagnosticDeliveryRecord:
            rows = blob.get("diagnostics") or []
            rows.append(rec.model_dump(mode="json"))
            blob["diagnostics"] = rows
            return rec

        return self._mutate(_fn)

    def get_diagnostic(self, diag_id: str) -> DiagnosticDeliveryRecord | None:
        blob = self._read_raw()
        rows = _DIAG_TA.validate_python(blob.get("diagnostics") or [])
        for r in reversed(rows):
            if r.id == diag_id:
                return r
        return None


_BACKEND_ENV = "DEALIX_AUTOPILOT_STORE_BACKEND"

_default_store_singleton: AutopilotJSONStore | Any | None = None
_singleton_lock = threading.Lock()


def _build_autopilot_store() -> AutopilotJSONStore | Any:
    backend = os.environ.get(_BACKEND_ENV, "json").strip().lower()
    if backend == "postgres":
        from dealix.revenue_ops_autopilot.postgres_store import (
            AutopilotPostgresStore,
            sync_database_url_from_env,
        )

        url = sync_database_url_from_env()
        if url:
            try:
                return AutopilotPostgresStore(database_url=url, create_tables=True)
            except Exception:
                pass
    return AutopilotJSONStore()


def get_autopilot_store() -> AutopilotJSONStore | Any:
    global _default_store_singleton
    if _default_store_singleton is None:
        with _singleton_lock:
            if _default_store_singleton is None:
                _default_store_singleton = _build_autopilot_store()
    return _default_store_singleton


def clear_autopilot_store_singleton_for_tests() -> None:
    """Reset lazy singleton so factory/env tests get a fresh backend."""
    global _default_store_singleton
    with _singleton_lock:
        _default_store_singleton = None


def reset_autopilot_store_for_tests(path: Path | None = None) -> AutopilotJSONStore:
    """Test helper — isolated store."""
    global _default_store_singleton
    st = AutopilotJSONStore(path=path)
    _default_store_singleton = st
    return st


def uid(prefix: str) -> str:
    return _new(prefix)
