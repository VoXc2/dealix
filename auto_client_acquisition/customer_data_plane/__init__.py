"""Customer Data & Consent Plane v5 — in-memory consent registry +
contactability gate + PII redactor.

In-memory storage now; the public API stays the same when the
Postgres consent_table ships later. Defaults are PDPL-safe: unknown
consent → no outbound; opt-out → blocked across all channels.
"""
from auto_client_acquisition.customer_data_plane.schemas import (
    ChannelKind,
    ConsentRecord,
    ConsentSource,
    ConsentStatus,
    ContactabilityVerdict,
)
from auto_client_acquisition.customer_data_plane.consent_registry import (
    ConsentRegistry,
    get_default_registry,
)
from auto_client_acquisition.customer_data_plane.contactability import (
    contactability_check,
)
from auto_client_acquisition.customer_data_plane.pii_redactor import (
    redact_email,
    redact_phone,
    redact_text,
)

__all__ = [
    "ChannelKind",
    "ConsentRecord",
    "ConsentSource",
    "ConsentStatus",
    "ContactabilityVerdict",
    "ConsentRegistry",
    "get_default_registry",
    "contactability_check",
    "redact_email",
    "redact_phone",
    "redact_text",
]
