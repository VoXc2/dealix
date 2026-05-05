"""HMAC-SHA256 signing for Proof Pack metadata.

Thin, dependency-free interface: a Proof Pack assembled by
``self_growth_os.proof_snippet_engine.render_pack`` can carry an
HMAC-SHA256 signature over its canonical JSON metadata so the
recipient can later verify the pack hasn't been tampered with.

This is an interface placeholder for the v6 Proof Pack standard.
The actual secret rotation / key management lives outside this
module — callers pass the secret in. When ``secret`` is ``None``
the signer returns the literal string ``"UNSIGNED"`` so that
test fixtures and local development never accidentally publish
a signature derived from an empty key.

Pure stdlib: ``hashlib`` + ``hmac`` + ``json``.
"""
from __future__ import annotations

import hashlib
import hmac
import json
from typing import Any


UNSIGNED = "UNSIGNED"


def _canonical_json(payload: dict[str, Any]) -> bytes:
    """Serialize ``payload`` deterministically (sorted keys, no whitespace).

    Two callers signing the same dict on different machines must
    produce the same bytes. ``ensure_ascii=False`` keeps Arabic
    characters intact; the bytes are encoded as UTF-8.
    """
    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        default=str,
    ).encode("utf-8")


def sign_pack_metadata(payload: dict[str, Any], secret: str | None = None) -> str:
    """Return a hex HMAC-SHA256 over the canonical JSON of ``payload``.

    - When ``secret`` is ``None`` (or empty), returns the literal
      string ``"UNSIGNED"`` — never a digest of the empty key.
    - Otherwise returns a 64-character lowercase hex digest that is
      stable across processes for the same ``(payload, secret)`` pair.
    """
    if not secret:
        return UNSIGNED
    key = secret.encode("utf-8")
    msg = _canonical_json(payload)
    return hmac.new(key, msg, hashlib.sha256).hexdigest()


__all__ = ["sign_pack_metadata", "UNSIGNED"]
