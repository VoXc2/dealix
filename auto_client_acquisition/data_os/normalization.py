"""Normalize inbound tabular fields before scoring / dedupe (deterministic)."""

from __future__ import annotations

from typing import Any

from auto_client_acquisition.data_os.dedupe import (
    normalize_company_name,
    normalize_domain,
    normalize_phone_e164_hint,
)


def _strip_lower(value: object) -> str:
    return str(value or "").strip().lower()


def normalize_account_row_fields(row: dict[str, Any]) -> dict[str, Any]:
    """Return a shallow copy with normalized company/domain/phone and trimmed text fields."""
    out = dict(row)
    cn = str(out.get("company_name") or "").strip()
    if cn:
        out["company_name"] = normalize_company_name(cn)
    for key in ("sector", "city", "source"):
        if key in out and out[key] is not None:
            out[key] = _strip_lower(out[key])
    if "domain" in out:
        dom = out.get("domain")
        out["domain"] = normalize_domain(str(dom) if dom is not None else None)
    if "phone" in out:
        ph = out.get("phone")
        out["phone"] = normalize_phone_e164_hint(str(ph) if ph is not None else None)
    if "notes" in out and out["notes"] is not None:
        out["notes"] = str(out["notes"]).strip()
    return out


__all__ = ["normalize_account_row_fields"]
