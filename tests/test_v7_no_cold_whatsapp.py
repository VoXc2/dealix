"""v7 Phase 8 hardening — cold WhatsApp must remain platform-blocked.

Three perimeter assertions:

  1. ``v3.compliance_os.assess_contactability`` returns BLOCKED for
     a cold WhatsApp contact (no opt-in, no prior relationship).
  2. Repo-wide check: no ``*.py`` file under ``auto_client_acquisition/``
     contains the literal string ``send_cold_whatsapp`` outside of the
     blocked-action lists / forbidden-tools registries that *exist
     specifically* to enumerate the forbidden surface.
  3. If the v7 ``ai_workforce`` module ships, the SaudiCopyAgent's
     ``forbidden_tools`` list must include ``cold_whatsapp``.
"""
from __future__ import annotations

import importlib.util
import re
from pathlib import Path

import pytest

from auto_client_acquisition.v3.compliance_os import (
    ContactPolicyInput,
    Contactability,
    assess_contactability,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
PKG_ROOT = REPO_ROOT / "auto_client_acquisition"

# Files inside the package that legitimately enumerate
# ``send_cold_whatsapp`` because they are the registries / policies that
# explicitly block it. These are the *source of truth* for the ban —
# the ban itself depends on the literal token appearing here.
_REGISTRY_FILES_ALLOWED = {
    # SafeAgentRuntime.restricted_actions
    PKG_ROOT / "v3" / "agents.py",
    # health-matrix expected restricted-actions set
    PKG_ROOT / "reliability_os" / "health_matrix.py",
    # vertical playbook blocked_actions / forbidden_channels
    PKG_ROOT / "vertical_playbooks" / "catalog.py",
    # role-brief blocked_actions
    PKG_ROOT / "role_command_os" / "role_briefs.py",
    # gtm_os experiment blocked-channel list
    PKG_ROOT / "gtm_os" / "message_experiment.py",
    # business gtm_plan "avoid" list
    PKG_ROOT / "business" / "gtm_plan.py",
    # company_brain risk profile compares against blocked-actions list
    PKG_ROOT / "company_brain_v6" / "risk_profile.py",
    # company_brain blocked-actions schema enum
    PKG_ROOT / "company_brain_v6" / "schemas.py",
    # the compliance OS itself (the canonical block lives here)
    PKG_ROOT / "v3" / "compliance_os.py",
}


def test_assess_contactability_blocks_cold_whatsapp():
    """A cold WhatsApp contact (no opt-in, no prior relationship) MUST
    return ``Contactability.BLOCKED``."""
    cold = ContactPolicyInput(
        channel="whatsapp",
        has_opt_in=False,
        has_prior_relationship=False,
    )
    result = assess_contactability(cold)
    assert result["status"] == Contactability.BLOCKED.value
    assert result["score"] == 0
    assert any("cold whatsapp" in r.lower() for r in result["reasons"]), (
        f"expected at least one reason mentioning cold whatsapp, got {result['reasons']!r}"
    )


def test_assess_contactability_blocks_explicit_is_cold_whatsapp_flag():
    """The explicit ``is_cold_whatsapp=True`` flag also triggers BLOCKED
    — defense in depth so a non-WA channel labelled cold-WA is still
    blocked."""
    cold_flag = ContactPolicyInput(
        channel="email",
        is_cold_whatsapp=True,
        includes_unsubscribe=True,
    )
    result = assess_contactability(cold_flag)
    assert result["status"] == Contactability.BLOCKED.value


def test_no_send_cold_whatsapp_outside_registry_files():
    """``send_cold_whatsapp`` must appear ONLY inside the allowlisted
    block-list / registry files. Any *new* code path that introduces
    the literal token outside those files is a regression."""
    token = "send_cold_whatsapp"
    pattern = re.compile(re.escape(token))
    violations: list[str] = []
    for py_file in PKG_ROOT.rglob("*.py"):
        if py_file in _REGISTRY_FILES_ALLOWED:
            continue
        try:
            text = py_file.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if pattern.search(text):
            violations.append(str(py_file.relative_to(REPO_ROOT)))
    assert not violations, (
        "send_cold_whatsapp leaked outside the allowed registry/blocklist files:\n"
        + "\n".join(sorted(violations))
        + "\nIf you intentionally added it to a new registry, extend "
        "_REGISTRY_FILES_ALLOWED in this test."
    )


def test_saudi_copy_agent_forbids_cold_whatsapp_when_ai_workforce_ships():
    """When the v7 ai_workforce module lands, SaudiCopyAgent.forbidden_tools
    MUST list ``cold_whatsapp``. Skip cleanly until the module exists."""
    if importlib.util.find_spec("auto_client_acquisition.ai_workforce") is None:
        pytest.skip("auto_client_acquisition.ai_workforce not yet shipped")

    # Module exists — now we can import. Try a few likely import paths.
    saudi_copy_agent = None
    candidate_paths = [
        ("auto_client_acquisition.ai_workforce", "SaudiCopyAgent"),
        ("auto_client_acquisition.ai_workforce.agents", "SaudiCopyAgent"),
        ("auto_client_acquisition.ai_workforce.saudi_copy_agent", "SaudiCopyAgent"),
    ]
    for module_name, attr in candidate_paths:
        try:
            mod = importlib.import_module(module_name)
        except ImportError:
            continue
        if hasattr(mod, attr):
            saudi_copy_agent = getattr(mod, attr)
            break

    if saudi_copy_agent is None:
        pytest.skip(
            "ai_workforce module exists but SaudiCopyAgent not located via "
            "expected import paths"
        )

    forbidden = getattr(saudi_copy_agent, "forbidden_tools", None)
    # Some agent classes may store the list on an instance — try both.
    if forbidden is None and callable(saudi_copy_agent):
        try:
            forbidden = getattr(saudi_copy_agent(), "forbidden_tools", None)
        except Exception:
            forbidden = None

    assert forbidden is not None, (
        "SaudiCopyAgent must expose a forbidden_tools attribute"
    )
    forbidden_str = [str(t) for t in forbidden]
    assert any("cold_whatsapp" in t for t in forbidden_str), (
        f"SaudiCopyAgent.forbidden_tools must include cold_whatsapp, got {forbidden_str!r}"
    )
