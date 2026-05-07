"""Proof Ledger evidence-attachment file storage.

Stores files at:
  data/proof_attachments/{customer_handle}/{event_id}/{filename}

Hard rules:
- 10MB per file cap (rejects above)
- Mime-type allowlist: png, jpg, jpeg, pdf, csv, json, txt
- Filename sanitization (no path traversal)
- Customer-handle scope (no cross-customer reads)
"""
from __future__ import annotations

import os
import re
from typing import Any

_ROOT = os.path.join("data", "proof_attachments")
_MAX_BYTES = 10 * 1024 * 1024  # 10 MB

_ALLOWED_MIME = {
    "image/png": "png",
    "image/jpeg": "jpg",
    "image/jpg": "jpg",
    "application/pdf": "pdf",
    "text/csv": "csv",
    "application/json": "json",
    "text/plain": "txt",
}

_FILENAME_RE = re.compile(r"^[A-Za-z0-9._-]{1,128}$")


def _sanitize_filename(filename: str) -> str:
    base = os.path.basename(filename or "").strip()
    if not _FILENAME_RE.match(base):
        raise ValueError("invalid filename")
    return base


def _customer_dir(customer_handle: str, event_id: str) -> str:
    # Re-use the same handle validator pattern from CustomerHandle
    if not re.match(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$", customer_handle):
        raise ValueError("invalid customer_handle")
    if not re.match(r"^[A-Za-z0-9_-]{1,64}$", event_id):
        raise ValueError("invalid event_id")
    path = os.path.join(_ROOT, customer_handle, event_id)
    os.makedirs(path, exist_ok=True)
    return path


def store_attachment(
    *,
    customer_handle: str,
    event_id: str,
    filename: str,
    mime_type: str,
    data: bytes,
) -> dict[str, Any]:
    """Store one attachment. Returns {'uri', 'bytes', 'sha256_short'}."""
    if mime_type not in _ALLOWED_MIME:
        raise ValueError(f"mime_type not allowed: {mime_type}")
    if len(data) > _MAX_BYTES:
        raise ValueError(f"file too large: {len(data)} > {_MAX_BYTES}")
    if not data:
        raise ValueError("empty file")

    safe_name = _sanitize_filename(filename)
    target_dir = _customer_dir(customer_handle, event_id)
    target_path = os.path.join(target_dir, safe_name)
    with open(target_path, "wb") as f:
        f.write(data)

    import hashlib
    sha = hashlib.sha256(data).hexdigest()[:16]

    return {
        "uri": f"file://{target_path}",
        "bytes": len(data),
        "sha256_short": sha,
        "mime_type": mime_type,
    }


def list_attachments(
    *,
    customer_handle: str,
    event_id: str,
) -> list[dict[str, Any]]:
    target_dir = _customer_dir(customer_handle, event_id)
    out: list[dict[str, Any]] = []
    if not os.path.isdir(target_dir):
        return out
    for name in os.listdir(target_dir):
        full = os.path.join(target_dir, name)
        if os.path.isfile(full):
            out.append({
                "uri": f"file://{full}",
                "filename": name,
                "bytes": os.path.getsize(full),
            })
    return out
