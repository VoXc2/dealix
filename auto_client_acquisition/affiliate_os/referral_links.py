"""Affiliate OS — referral / UTM link generation (JSONL-backed).

Code generation mirrors partnership_os/referral_store._generate_code. A link
can only be created for an APPROVED affiliate.
"""

from __future__ import annotations

import hashlib
import json
import os
import secrets
import threading
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from auto_client_acquisition.affiliate_os.affiliate_store import (
    AFFILIATE_OPS_TENANT,
    get_affiliate,
)
from auto_client_acquisition.auditability_os.audit_event import (
    AuditEventKind,
    record_event,
)

_LINKS_PATH_DEFAULT = "var/affiliate-links.jsonl"
_lock = threading.Lock()


def _resolve(env_var: str, default_rel: str) -> Path:
    p = Path(os.environ.get(env_var, default_rel))
    if not p.is_absolute():
        p = Path(__file__).resolve().parent.parent.parent / p
    return p


def _links_path() -> Path:
    return _resolve("DEALIX_AFFILIATE_LINKS_PATH", _LINKS_PATH_DEFAULT)


def _generate_affiliate_code(affiliate_id: str) -> str:
    """AFF-XXXXXXXX where the suffix encodes affiliate_id hash for traceability."""
    seed = (
        hashlib.sha256((affiliate_id + secrets.token_hex(8)).encode("utf-8"))
        .hexdigest()[:8]
        .upper()
    )
    return f"AFF-{seed}"


@dataclass
class AffiliateLink:
    code: str = ""
    affiliate_id: str = ""
    utm_source: str = "affiliate"
    utm_medium: str = "referral"
    utm_campaign: str = ""
    landing_path: str = "/pricing.html"
    is_revoked: bool = False
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _append(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with _lock:
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")


def _read_all(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    out: list[dict[str, Any]] = []
    with _lock:
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    out.append(json.loads(line))
                except Exception:  # noqa: BLE001
                    continue
    return out


def _rewrite(path: Path, items: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with _lock:
        path.write_text(
            "\n".join(json.dumps(i, ensure_ascii=False) for i in items)
            + ("\n" if items else ""),
            encoding="utf-8",
        )


def create_affiliate_link(
    *,
    affiliate_id: str,
    landing_path: str = "/pricing.html",
) -> AffiliateLink:
    """Mint a tracking link. Raises ValueError unless the affiliate exists
    and is approved — a pending or rejected affiliate gets no link."""
    affiliate = get_affiliate(affiliate_id)
    if affiliate is None:
        raise ValueError(f"unknown affiliate: {affiliate_id}")
    if affiliate.status != "approved":
        raise ValueError(
            f"affiliate {affiliate_id} is {affiliate.status}; only approved "
            "affiliates may receive a referral link"
        )
    code = _generate_affiliate_code(affiliate_id)
    link = AffiliateLink(
        code=code,
        affiliate_id=affiliate_id,
        utm_campaign=code,
        landing_path=landing_path,
    )
    _append(_links_path(), link.to_dict())
    record_event(
        customer_id=AFFILIATE_OPS_TENANT,
        kind=AuditEventKind.OUTPUT_DELIVERED,
        actor="affiliate_os",
        decision="affiliate_link_created",
        policy_checked="link_requires_approved_affiliate",
        summary=f"link {code} for affiliate {affiliate_id}",
        source_refs=[affiliate_id],
        output_refs=[code],
    )
    return link


def lookup_link(code: str) -> AffiliateLink | None:
    code = (code or "").strip().upper()
    if not code:
        return None
    for row in _read_all(_links_path()):
        if row.get("code") == code:
            return AffiliateLink(**row)
    return None


def build_tracking_url(link: AffiliateLink, base_url: str = "https://dealix.me") -> str:
    base = base_url.rstrip("/") + link.landing_path
    return (
        f"{base}?utm_source={link.utm_source}"
        f"&utm_medium={link.utm_medium}"
        f"&utm_campaign={link.utm_campaign}"
    )


def list_links(*, affiliate_id: str | None = None) -> list[AffiliateLink]:
    out: list[AffiliateLink] = []
    for row in _read_all(_links_path()):
        if affiliate_id and row.get("affiliate_id") != affiliate_id:
            continue
        out.append(AffiliateLink(**row))
    return out


def revoke_link(code: str) -> bool:
    code = (code or "").strip().upper()
    rows = _read_all(_links_path())
    found = False
    for row in rows:
        if row.get("code") == code:
            row["is_revoked"] = True
            found = True
    if found:
        _rewrite(_links_path(), rows)
    return found


def clear_for_test() -> None:
    path = _links_path()
    if path.exists():
        with _lock:
            path.write_text("", encoding="utf-8")


__all__ = [
    "AffiliateLink",
    "build_tracking_url",
    "clear_for_test",
    "create_affiliate_link",
    "list_links",
    "lookup_link",
    "revoke_link",
]
