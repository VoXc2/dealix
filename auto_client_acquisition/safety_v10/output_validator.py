"""Output validator — checks rendered text for forbidden tokens.

Returns a dict describing whether the text is safe to publish (e.g. on
the landing page) or safe to send (e.g. in a customer-facing email).
By default ``safe_to_send`` is ALWAYS False — the platform requires
human approval before any external send.
"""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.safety_v10.policies import policy_engine_check


def validate_output(text: str, schema: dict[str, Any] | None = None) -> dict[str, Any]:
    """Validate ``text`` against the canonical perimeter regex.

    Parameters
    ----------
    text:
        Rendered text to validate (Arabic, English, or mixed).
    schema:
        Optional schema dict — currently unused but reserved for future
        structured-output validation.

    Returns
    -------
    dict with keys:
      - ``ok``: True iff no forbidden token was matched.
      - ``blocked_reasons``: list of reasons (one per match).
      - ``safe_to_publish``: True iff ``ok``.
      - ``safe_to_send``: ALWAYS False — external send requires human
        approval per platform policy. The validator never sets this
        True, regardless of input.
    """
    if not isinstance(text, str):
        text = str(text or "")

    result = policy_engine_check(text)
    blocked = result.actual_action == "block"
    blocked_reasons = [result.reason] if blocked else []

    return {
        "ok": not blocked,
        "blocked_reasons": blocked_reasons,
        "safe_to_publish": not blocked,
        # External send always requires human approval; this validator
        # alone is NOT sufficient authority to send. Default False.
        "safe_to_send": False,
        "schema_provided": schema is not None,
    }
