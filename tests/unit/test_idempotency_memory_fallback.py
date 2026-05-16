"""Unit tests — IdempotencyStore process-local fallback.

When Redis is not configured, IdempotencyStore must still detect duplicates
via its in-memory fallback so retries do not double-process.
"""

from __future__ import annotations

import time

from dealix.reliability.idempotency import IdempotencyStore


def test_claim_first_call_owns_key() -> None:
    """First claim on a fresh key returns True (caller owns it)."""
    store = IdempotencyStore(prefix="test-idem-1:", redis_client=None)
    assert store.claim("evt-001") is True


def test_claim_second_call_is_duplicate() -> None:
    """Replaying the same key returns False (duplicate)."""
    store = IdempotencyStore(prefix="test-idem-2:", redis_client=None)
    assert store.claim("evt-001") is True
    assert store.claim("evt-001") is False


def test_seen_reflects_mark() -> None:
    """seen() is False before mark, True after."""
    store = IdempotencyStore(prefix="test-idem-3:", redis_client=None)
    assert store.seen("evt-002") is False
    assert store.mark("evt-002") is True
    assert store.seen("evt-002") is True


def test_mark_expires_after_ttl() -> None:
    """An expired mark no longer counts as seen / blocks re-claim."""
    store = IdempotencyStore(prefix="test-idem-4:", redis_client=None)
    assert store.mark("evt-003", ttl_seconds=1) is True
    time.sleep(1.1)
    assert store.seen("evt-003") is False
    assert store.claim("evt-003", ttl_seconds=1) is True
