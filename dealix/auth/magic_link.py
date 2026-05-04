"""
Magic-link tokens — passwordless auth for partners.

Token structure:
    base64url( payload_json ) + "." + base64url( hmac_sha256(payload_json, secret) )

Payload:
    {
      "sub": "partner_id",       # subject
      "email": "...@agency.sa",  # contact email
      "kind": "magic" | "session",
      "iat": 1714760000,         # issued at (epoch seconds)
      "exp": 1714763600,         # expires at (epoch seconds)
      "nonce": "hex8",           # one-time-use guard for magic kind
    }

`magic` tokens: 15 minutes, single-use (one-time consume on /verify).
`session` tokens: 7 days, repeatable use until expiry.

Pure functions — no I/O. Side effects (sending email, setting cookies)
live in the auth router.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import secrets
import time
from dataclasses import dataclass
from typing import Literal

from core.config.settings import get_settings

MAGIC_TTL_SECONDS = 15 * 60        # 15 minutes
SESSION_TTL_SECONDS = 7 * 24 * 3600  # 7 days


def _secret_bytes() -> bytes:
    """Return the HMAC key derived from app_secret_key."""
    s = get_settings()
    raw = s.app_secret_key.get_secret_value() if s.app_secret_key else "change-me"
    # Derive a stable 32-byte key from whatever the operator set.
    return hashlib.sha256(raw.encode("utf-8")).digest()


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64url_decode(s: str) -> bytes:
    pad = "=" * (-len(s) % 4)
    return base64.urlsafe_b64decode(s + pad)


@dataclass(frozen=True)
class MagicLinkPayload:
    sub: str
    email: str
    kind: Literal["magic", "session"]
    iat: int
    exp: int
    nonce: str

    def to_dict(self) -> dict:
        return {
            "sub": self.sub,
            "email": self.email,
            "kind": self.kind,
            "iat": self.iat,
            "exp": self.exp,
            "nonce": self.nonce,
        }

    @property
    def is_expired(self) -> bool:
        return time.time() > self.exp


def issue(
    *,
    partner_id: str,
    email: str,
    kind: Literal["magic", "session"] = "magic",
    ttl_seconds: int | None = None,
    now: int | None = None,
) -> str:
    """Issue a signed token. Returns the encoded token string."""
    if not partner_id or not email:
        raise ValueError("partner_id and email are required")
    if kind not in ("magic", "session"):
        raise ValueError(f"kind must be 'magic' or 'session', got {kind!r}")
    issued = int(now if now is not None else time.time())
    if ttl_seconds is None:
        ttl_seconds = MAGIC_TTL_SECONDS if kind == "magic" else SESSION_TTL_SECONDS
    payload = {
        "sub": partner_id,
        "email": email.lower().strip(),
        "kind": kind,
        "iat": issued,
        "exp": issued + int(ttl_seconds),
        "nonce": secrets.token_hex(8),
    }
    body = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    sig = hmac.new(_secret_bytes(), body, hashlib.sha256).digest()
    return _b64url_encode(body) + "." + _b64url_encode(sig)


def verify(token: str) -> MagicLinkPayload:
    """Decode + verify a token. Raises ValueError on any failure."""
    if not token or "." not in token:
        raise ValueError("malformed_token")
    body_b64, sig_b64 = token.rsplit(".", 1)
    try:
        body = _b64url_decode(body_b64)
        sig = _b64url_decode(sig_b64)
    except Exception as exc:
        raise ValueError("malformed_token") from exc
    expected = hmac.new(_secret_bytes(), body, hashlib.sha256).digest()
    if not hmac.compare_digest(sig, expected):
        raise ValueError("bad_signature")
    try:
        data = json.loads(body)
    except Exception as exc:
        raise ValueError("malformed_payload") from exc
    payload = MagicLinkPayload(
        sub=str(data.get("sub") or ""),
        email=str(data.get("email") or ""),
        kind=str(data.get("kind") or "magic"),  # type: ignore[arg-type]
        iat=int(data.get("iat") or 0),
        exp=int(data.get("exp") or 0),
        nonce=str(data.get("nonce") or ""),
    )
    if not payload.sub or not payload.email:
        raise ValueError("incomplete_payload")
    if payload.is_expired:
        raise ValueError("expired_token")
    return payload
