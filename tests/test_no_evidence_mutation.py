"""Non-negotiable guard: the Evidence Ledger is append-only.

No HTTP route under /api/v1/evidence may mutate the ledger, and the
EvidenceLedger class itself must expose no update/delete path.
"""

from __future__ import annotations

from auto_client_acquisition.evidence_control_plane_os.event_store import (
    EvidenceLedger,
)


def test_evidence_ledger_class_is_append_only():
    for forbidden in ("update", "delete", "remove", "edit", "patch"):
        assert not hasattr(EvidenceLedger, forbidden), (
            f"EvidenceLedger must not expose a '{forbidden}' method — "
            "the evidence ledger is append-only"
        )


def test_evidence_routes_are_read_only():
    from api.main import app

    write_methods = {"POST", "PUT", "PATCH", "DELETE"}
    for route in app.routes:
        path = getattr(route, "path", "")
        if not path.startswith("/api/v1/evidence"):
            continue
        methods = getattr(route, "methods", set()) or set()
        offending = methods & write_methods
        assert not offending, (
            f"evidence route {path} exposes write methods {offending} — "
            "evidence may only be written via record_evidence_event()"
        )
