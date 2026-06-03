"""Retry policy helpers — exponential backoff.

Pure function — no I/O, no sleep, no external clock.
"""
from __future__ import annotations

from auto_client_acquisition.workflow_os_v10.schemas import RetryPolicy


def compute_next_retry(attempt: int, policy: RetryPolicy) -> int:
    """Return the delay in seconds before retry number ``attempt``.

    delay = initial_delay * (backoff_factor ** attempt)

    ``attempt`` is 0-indexed (the first retry is attempt=0).
    Returns 0 if attempt < 0 (no retry yet).
    """
    if attempt < 0:
        return 0
    delay = policy.initial_delay_seconds * (policy.backoff_factor ** attempt)
    return int(delay)


def should_retry(attempt: int, policy: RetryPolicy) -> bool:
    """True iff the step still has retry budget."""
    return attempt < policy.max_retries
