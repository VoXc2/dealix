"""API middleware modules — Wave 12.6 §33.2.6 hardening + http_stack + enterprise security.

This package contains FastAPI middleware + dependencies that enforce
cross-cutting safety invariants:

- ``http_stack``: request ID, security headers, PDPL audit logging, ETag,
  rate-limit headers (shared HTTP layer used by ``api.main``).

- ``tenant_isolation``: resolves tenant_id from JWT/header → injects
  into request.state → all repository calls MUST assert match
  (defense against OWASP API1:2023 BOLA — Broken Object-Level
  Authorization).

- ``bopla_redaction``: Pydantic response-model decorator that filters
  sensitive fields (bank_account, personal_email, phone) by role
  (defense against OWASP API3:2023 BOPLA — Broken Object Property-Level
  Authorization).

- ``ip_allowlist``: Enterprise IP allowlisting middleware for network-level
  access control per tenant.

- ``privileged_audit``: Immutable audit trail for all super admin and
  tenant admin privileged operations (PDPL Art. 18, NCA ECC-11).

Re-exports all middleware classes so ``api/main.py`` imports stay stable.
"""

from api.middleware.http_stack import (
    AuditLogMiddleware,
    ETagMiddleware,
    RateLimitHeadersMiddleware,
    RequestIDMiddleware,
    SecurityHeadersMiddleware,
)
from api.middleware.ip_allowlist import IPAllowlistMiddleware
from api.middleware.privileged_audit import PrivilegedAuditMiddleware

__all__ = [
    "AuditLogMiddleware",
    "ETagMiddleware",
    "IPAllowlistMiddleware",
    "PrivilegedAuditMiddleware",
    "RateLimitHeadersMiddleware",
    "RequestIDMiddleware",
    "SecurityHeadersMiddleware",
]
