"""Evidence export — produces a redacted, audit-ready slice of the ledger."""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from auto_client_acquisition.customer_data_plane.pii_redactor import (
    redact_dict,
)
from auto_client_acquisition.proof_ledger.file_backend import (
    FileProofLedger,
    get_default_ledger,
)


def export_redacted(
    *,
    customer_handle: str | None = None,
    event_type: str | None = None,
    limit: int = 200,
    ledger: FileProofLedger | None = None,
) -> dict[str, Any]:
    """Return a dict ready to share with the founder or legal team.

    PII is redacted at every level. Customer name appears ONLY when
    consent_for_publication=True on the underlying event.
    """
    led = ledger or get_default_ledger()
    events = led.list_events(
        customer_handle=customer_handle,
        event_type=event_type,
        limit=limit,
    )

    redacted_events: list[dict[str, Any]] = []
    for ev in events:
        d = ev.model_dump(mode="json")
        # If consent_for_publication=False, strip the customer_handle
        # and any free-text summaries — only the redacted versions
        # plus event_type / timestamps survive.
        if not ev.consent_for_publication:
            d["customer_handle"] = "<anonymized>"
            d["summary_ar"] = ""
            d["summary_en"] = ""
        d = redact_dict(d)
        redacted_events.append(d)

    return {
        "schema_version": 1,
        "generated_at": datetime.now(UTC).isoformat(),
        "filters": {
            "customer_handle": customer_handle,
            "event_type": event_type,
            "limit": limit,
        },
        "total_returned": len(redacted_events),
        "events": redacted_events,
    }


def export_for_audit(
    *,
    ledger: FileProofLedger | None = None,
) -> dict[str, Any]:
    """SDAIA / DPO-shareable audit pack. All PII redacted unconditionally."""
    led = ledger or get_default_ledger()
    events = led.list_events(limit=10_000)
    units = led.list_units(limit=10_000)

    return redact_dict({
        "schema_version": 1,
        "generated_at": datetime.now(UTC).isoformat(),
        "events_count": len(events),
        "units_count": len(units),
        "events": [ev.model_dump(mode="json") for ev in events],
        "units": [u.model_dump(mode="json") for u in units],
    })
