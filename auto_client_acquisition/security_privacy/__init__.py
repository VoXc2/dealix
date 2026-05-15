"""Security & Privacy v5 — code-level helpers.

Policy lives in markdown (PRIVACY_PDPL_READINESS.md, trust-center.html
on the site). This module exposes the policy as **code** that other
modules can call inline:

  - ``scan_text_for_secrets`` — regex over a string for sk_live_,
    GitHub PATs, AWS keys, etc.
  - ``redact_log_entry`` — wraps the existing pii_redactor for log
    middleware.
  - ``data_minimization_for(object_type)`` — returns the typed
    contract of which fields are PII-flagged per object type.
"""
from auto_client_acquisition.security_privacy.data_minimization import (
    DataMinimizationContract,
    data_minimization_for,
    list_known_object_types,
)
from auto_client_acquisition.security_privacy.log_redaction import (
    redact_log_entry,
)
from auto_client_acquisition.security_privacy.secret_scan_policy import (
    SECRET_PATTERNS,
    SecretFinding,
    scan_text_for_secrets,
)

__all__ = [
    "SECRET_PATTERNS",
    "DataMinimizationContract",
    "SecretFinding",
    "data_minimization_for",
    "list_known_object_types",
    "redact_log_entry",
    "scan_text_for_secrets",
]
