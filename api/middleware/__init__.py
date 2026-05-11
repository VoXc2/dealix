"""API middleware modules — Wave 12.6 §33.2.6 hardening + legacy re-exports.

This package contains FastAPI middleware + dependencies that enforce
cross-cutting safety invariants:

- ``tenant_isolation``: resolves tenant_id from JWT/header → injects
  into request.state → all repository calls MUST assert match
  (defense against OWASP API1:2023 BOLA — Broken Object-Level
  Authorization).

- ``bopla_redaction``: Pydantic response-model decorator that filters
  sensitive fields (bank_account, personal_email, phone) by role
  (defense against OWASP API3:2023 BOPLA — Broken Object Property-Level
  Authorization).

- ``legacy_middleware``: pre-Wave-12.6 middleware (RequestID, Security
  Headers, ETag, Rate-Limit, Audit). Re-exported here so `api/main.py`
  imports stay stable: ``from api.middleware import (
      AuditLogMiddleware, ETagMiddleware, ...
  )``.

Article 11: composes existing api/security/ (RBAC + JWT + api_key) —
doesn't duplicate.
"""

from api.middleware.legacy_middleware import (
    AuditLogMiddleware,
    ETagMiddleware,
    RateLimitHeadersMiddleware,
    RequestIDMiddleware,
    SecurityHeadersMiddleware,
)

__all__ = [
    "AuditLogMiddleware",
    "ETagMiddleware",
    "RateLimitHeadersMiddleware",
    "RequestIDMiddleware",
    "SecurityHeadersMiddleware",
]
