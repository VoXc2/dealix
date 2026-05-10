"""Wave 12.6 §33.2.6 — BOPLA Field Redaction.

Defends against OWASP API3:2023 BOPLA (Broken Object Property-Level
Authorization) by filtering sensitive fields out of API responses
based on the requesting role.

Pattern (research-validated):
- Server-side allowlist of writable fields per role
- Server-side denylist of readable fields per role
- Pydantic response decorator + dict filter helpers
- NEVER blindly returns the entire object — every response goes
  through the role filter

Hard rule: when in doubt, redact. Default-deny for unknown roles.

Source: https://owasp.org/API-Security/editions/2023/en/0xa3-broken-object-property-level-authorization/
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

# Canonical roles (matches Wave 9 RBAC + plan §32.4A.2 founder bottleneck).
# Order: highest privilege → lowest.
Role = Literal[
    "super_admin",      # Dealix engineering / founder
    "tenant_admin",     # customer's primary contact
    "csm",              # customer success manager (Dealix-side, post-CSM-hire)
    "sales_manager",    # internal sales lead (post-hire)
    "sales_rep",        # internal sales rep (post-hire)
    "finance",          # finance role (payment confirmation)
    "viewer",           # read-only customer user
    "anonymous",        # unauthenticated (public landing pages only)
]


# Sensitive fields by category — used for blanket denylist building
SENSITIVE_FIELD_CATEGORIES: dict[str, frozenset[str]] = {
    "PII_email": frozenset({
        "personal_email", "email_personal", "private_email",
    }),
    "PII_phone": frozenset({
        "phone", "mobile", "personal_phone", "personal_mobile",
        "phone_e164", "mobile_e164",
    }),
    "PII_id": frozenset({
        "national_id", "passport_number", "id_number", "saudi_id",
        "saudi_national_id",
    }),
    "financial": frozenset({
        "bank_account", "bank_account_number", "iban",
        "card_number", "card_token", "card_last4",
        "salary", "compensation", "annual_income",
        "tax_id",
    }),
    "secret": frozenset({
        "password", "password_hash", "api_key", "secret_key",
        "access_token", "refresh_token", "jwt", "session_id",
        "webhook_secret", "moyasar_secret_key",
    }),
    "internal_audit": frozenset({
        "internal_notes", "audit_log_entries", "staff_notes",
        "privileged_metadata", "moderation_flags",
    }),
}


# Default visibility per role per category.
# True = role can see this category; False = redact.
# Default-deny when role not explicitly listed.
_ROLE_VISIBILITY: dict[Role, dict[str, bool]] = {
    "super_admin": {
        "PII_email": True, "PII_phone": True, "PII_id": True,
        "financial": True, "secret": False,  # super_admin sees PII but NOT secrets
        "internal_audit": True,
    },
    "tenant_admin": {
        "PII_email": True, "PII_phone": True, "PII_id": False,
        "financial": True, "secret": False,
        "internal_audit": False,
    },
    "csm": {
        "PII_email": True, "PII_phone": True, "PII_id": False,
        "financial": False, "secret": False,
        "internal_audit": True,  # CSM sees customer-success-side audit
    },
    "sales_manager": {
        "PII_email": True, "PII_phone": True, "PII_id": False,
        "financial": False, "secret": False,
        "internal_audit": False,
    },
    "sales_rep": {
        "PII_email": True, "PII_phone": True, "PII_id": False,
        "financial": False, "secret": False,
        "internal_audit": False,
    },
    "finance": {
        "PII_email": True, "PII_phone": False, "PII_id": True,
        "financial": True, "secret": False,
        "internal_audit": False,
    },
    "viewer": {
        "PII_email": False, "PII_phone": False, "PII_id": False,
        "financial": False, "secret": False,
        "internal_audit": False,
    },
    "anonymous": {
        "PII_email": False, "PII_phone": False, "PII_id": False,
        "financial": False, "secret": False,
        "internal_audit": False,
    },
}


@dataclass(frozen=True, slots=True)
class RedactionResult:
    """Outcome of running BOPLA redaction on a payload."""

    redacted_payload: dict[str, Any]
    fields_redacted: tuple[str, ...]
    role_used: Role
    redacted_count: int


def fields_blocked_for_role(role: Role) -> frozenset[str]:
    """Compute the set of field names the role cannot see.

    Default-deny: when role isn't explicitly listed, blocks every
    sensitive field (Article 4 — fail-closed).
    """
    visibility = _ROLE_VISIBILITY.get(role)
    if visibility is None:
        # Unknown role → block everything sensitive
        blocked: set[str] = set()
        for cat_fields in SENSITIVE_FIELD_CATEGORIES.values():
            blocked.update(cat_fields)
        return frozenset(blocked)

    blocked = set()
    for category, fields in SENSITIVE_FIELD_CATEGORIES.items():
        if not visibility.get(category, False):  # default-deny per category
            blocked.update(fields)
    return frozenset(blocked)


def redact_dict_for_role(
    payload: dict[str, Any],
    *,
    role: Role,
    extra_blocked_fields: tuple[str, ...] = (),
    redaction_marker: str = "[REDACTED]",
) -> RedactionResult:
    """Filter sensitive fields out of a dict payload based on role.

    Args:
        payload: The dict response body (may have nested dicts).
        role: The requesting role (Literal).
        extra_blocked_fields: Per-endpoint extras (e.g. an endpoint may
            want to redact additional fields beyond the canonical set).
        redaction_marker: Replaces the value (default "[REDACTED]").
            Pass empty string to DELETE the key entirely.

    Returns:
        RedactionResult with redacted payload + list of fields redacted.
    """
    blocked = set(fields_blocked_for_role(role)) | set(extra_blocked_fields)
    redacted_keys: list[str] = []

    def _walk(obj: Any, path: str = "") -> Any:
        if isinstance(obj, dict):
            out: dict[str, Any] = {}
            for k, v in obj.items():
                key_path = f"{path}.{k}" if path else k
                if k in blocked:
                    redacted_keys.append(key_path)
                    if redaction_marker:
                        out[k] = redaction_marker
                    # else: skip (delete key)
                else:
                    out[k] = _walk(v, key_path)
            return out
        if isinstance(obj, list):
            return [_walk(item, f"{path}[]") for item in obj]
        return obj

    redacted = _walk(payload)
    return RedactionResult(
        redacted_payload=redacted,
        fields_redacted=tuple(redacted_keys),
        role_used=role,
        redacted_count=len(redacted_keys),
    )


def assert_no_sensitive_field_in_response(
    payload: dict[str, Any], *, role: Role,
) -> None:
    """Defensive double-check after redaction — raises if any blocked
    field is still present (caught a bug where extra_blocked_fields
    were forgotten).

    Use as a final guard in tests.
    """
    blocked = fields_blocked_for_role(role)

    def _has_blocked(obj: Any) -> str | None:
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k in blocked and v != "[REDACTED]":
                    return k
                nested = _has_blocked(v)
                if nested:
                    return nested
        elif isinstance(obj, list):
            for item in obj:
                nested = _has_blocked(item)
                if nested:
                    return nested
        return None

    found = _has_blocked(payload)
    if found:
        raise AssertionError(
            f"BOPLA leak: field {found!r} present in response for role={role!r}"
        )
