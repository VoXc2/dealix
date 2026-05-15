"""safe_call — execute a callable; on any exception, return degraded.

Used as the universal "try this; if it fails, mark degraded" wrapper.
Never raises. Never leaks stacktrace to caller.
"""
from __future__ import annotations

from collections.abc import Callable
from typing import Any

from auto_client_acquisition.integration_upgrade.degraded import degraded_section


def safe_call(
    *,
    name: str,
    fn: Callable[[], Any],
    fallback: Any = None,
    reason_ar_template: str = "{name} غير متاح حاليًا.",
    reason_en_template: str = "{name} is currently unavailable.",
) -> Any:
    """Run fn() and return its result; on exception return fallback or
    a degraded_section dict.

    NEVER raises. NEVER includes stacktrace in the returned object.
    """
    try:
        return fn()
    except BaseException as exc:
        # Defensive: never leak exception type/message to caller
        if fallback is not None:
            return fallback
        # Use the exception type name only (no message, no traceback)
        # to give engineers a hint without leaking secrets
        exc_type = type(exc).__name__
        return degraded_section(
            section=name,
            reason_ar=reason_ar_template.format(name=name),
            reason_en=reason_en_template.format(name=name),
            next_fix_ar=f"تحقّق من توفّر الوحدة ({exc_type}).",
            next_fix_en=f"Check module availability ({exc_type}).",
            severity="medium",
        )
