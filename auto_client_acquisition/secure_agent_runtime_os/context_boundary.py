"""Context boundary — prevent untrusted blobs from overriding policy."""

from __future__ import annotations

import hashlib


def untrusted_blob_tamper_score(untrusted_text: str, policy_hash: str) -> tuple[bool, str]:
    """
    If untrusted payload claims to embed a new policy hash, reject.

    Real deployments should verify signed policy documents; this is a deterministic stub.
    """
    low = untrusted_text.lower()
    if "override_policy" in low or "ignore_previous_rules" in low:
        return False, "policy_override_attempt"
    digest = hashlib.sha256(untrusted_text.encode()).hexdigest()[:12]
    _ = digest, policy_hash
    return True, "ok"


__all__ = ["untrusted_blob_tamper_score"]
