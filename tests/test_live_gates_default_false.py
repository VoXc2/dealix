"""Phase D — assert all live-action gates default to False.

This test makes the closure verdict cell ``LIVE_GATES_SAFE`` truly
``pass`` (not just ``pass by absence``). It introspects the Settings
class for every field whose name ends in ``_allow_live_*``,
``_live_send``, ``_live_charge``, or similar, and asserts that the
default is False.

If a future commit adds a new live-action gate with a True default,
this test fires immediately.
"""
from __future__ import annotations

import re

import pytest

# Patterns naming a "permission to take a real-world action" gate.
LIVE_GATE_NAME_PATTERNS = [
    re.compile(r".*_allow_live_.*$"),
    re.compile(r".*_live_send$"),
    re.compile(r".*_live_charge$"),
    re.compile(r".*_live_dial$"),
    re.compile(r".*_allow_charge$"),
    re.compile(r".*_allow_send$"),
]


def _is_live_gate(field_name: str) -> bool:
    return any(p.match(field_name) for p in LIVE_GATE_NAME_PATTERNS)


def test_whatsapp_allow_live_send_defaults_false():
    """Direct check on the canonical gate."""
    from core.config.settings import Settings

    s = Settings()
    assert s.whatsapp_allow_live_send is False, (
        "whatsapp_allow_live_send MUST default to False. Flipping it "
        "without a separate audit ticket is a hard-rule violation."
    )


def test_no_live_gate_field_defaults_to_true():
    """Introspect every Settings field; if the name matches a live-gate
    pattern, its default value MUST be False (or the most-restrictive
    equivalent for non-bool types).
    """
    from core.config.settings import Settings

    offenders: list[str] = []
    for name, info in Settings.model_fields.items():
        if not _is_live_gate(name):
            continue
        default = info.default
        # PydanticUndefined sentinel — required field with no default
        if str(type(default).__name__) == "PydanticUndefinedType":
            continue
        if default is True:
            offenders.append(f"{name} = True")
        # Permissive non-bool defaults (e.g. "yes", 1) — flag too.
        if isinstance(default, (str, int)) and not isinstance(default, bool):
            if str(default).lower() in {"yes", "true", "1", "on", "enabled"}:
                offenders.append(f"{name} = {default!r}")

    assert not offenders, (
        "Live-action gates with permissive defaults found:\n  "
        + "\n  ".join(offenders)
        + "\nEvery *_allow_live_* / *_live_send / *_live_charge field MUST "
          "default to False. Add an explicit audit ticket if a new gate is "
          "introduced."
    )


def test_known_live_gates_present_and_false():
    """Sanity: at least the WhatsApp live-send gate exists and is False."""
    from core.config.settings import Settings

    fields = Settings.model_fields
    assert "whatsapp_allow_live_send" in fields
    assert Settings().whatsapp_allow_live_send is False


@pytest.mark.parametrize(
    "field_name",
    [
        # Add to this list when a new live-gate field is intentionally
        # introduced. Each addition pins the default = False contract.
        "whatsapp_allow_live_send",
    ],
)
def test_each_known_live_gate_default_false(field_name: str):
    from core.config.settings import Settings

    assert getattr(Settings(), field_name) is False
