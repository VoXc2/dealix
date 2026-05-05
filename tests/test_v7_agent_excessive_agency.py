"""v7 Phase 8 hardening — no agent in the v7 workforce may execute
externally without explicit human approval.

Four perimeter assertions, all gated on the v7 ``ai_workforce``
module. Until ai_workforce ships, every test in this file
``pytest.skip``s cleanly so collection passes.

  1. Every agent in ``AGENT_REGISTRY`` either has
     ``requires_approval=True`` OR carries an autonomy_level in
     ``{"observe_only", "analyze_only"}``.
  2. No agent has ``default_action_mode`` containing the substring
     ``"live"``.
  3. ``apply_policy`` from workforce_policy refuses to elevate any
     agent to live execution.
  4. ``ComplianceGuardAgent`` ALWAYS appears last in
     ``route_for_goal(...)`` for any goal.
"""
from __future__ import annotations

import importlib
import importlib.util

import pytest


def _ai_workforce_available() -> bool:
    return importlib.util.find_spec("auto_client_acquisition.ai_workforce") is not None


def _import_first(*candidates: tuple[str, str]):
    """Try import paths in order; return the first attribute that loads."""
    for module_name, attr in candidates:
        try:
            mod = importlib.import_module(module_name)
        except ImportError:
            continue
        if hasattr(mod, attr):
            return getattr(mod, attr)
    return None


_OBSERVE_LEVELS = {"observe_only", "analyze_only"}


def _registry():
    return _import_first(
        ("auto_client_acquisition.ai_workforce", "AGENT_REGISTRY"),
        ("auto_client_acquisition.ai_workforce.agents", "AGENT_REGISTRY"),
        ("auto_client_acquisition.ai_workforce.agent_registry", "AGENT_REGISTRY"),
        ("auto_client_acquisition.ai_workforce.workforce_policy", "AGENT_REGISTRY"),
    )


def test_all_workforce_agents_require_approval_unless_observe_only():
    if not _ai_workforce_available():
        pytest.skip("auto_client_acquisition.ai_workforce not yet shipped")
    registry = _registry()
    if registry is None:
        pytest.skip("ai_workforce shipped but AGENT_REGISTRY not found")

    offenders: list[str] = []
    for name, agent in registry.items() if isinstance(registry, dict) else []:
        autonomy = str(getattr(agent, "autonomy_level", "") or "")
        requires_approval = bool(getattr(agent, "requires_approval", False))
        if autonomy in _OBSERVE_LEVELS:
            continue
        if not requires_approval:
            offenders.append(
                f"{name}: autonomy_level={autonomy!r}, "
                f"requires_approval={requires_approval}"
            )
    assert not offenders, (
        "Every workforce agent must either be observe/analyze-only OR "
        "require approval:\n" + "\n".join(offenders)
    )


def test_no_workforce_agent_has_live_default_action_mode():
    if not _ai_workforce_available():
        pytest.skip("auto_client_acquisition.ai_workforce not yet shipped")
    registry = _registry()
    if registry is None:
        pytest.skip("ai_workforce shipped but AGENT_REGISTRY not found")

    offenders: list[str] = []
    for name, agent in registry.items() if isinstance(registry, dict) else []:
        mode = str(getattr(agent, "default_action_mode", "") or "")
        if "live" in mode.lower():
            offenders.append(f"{name}: default_action_mode={mode!r}")
    assert not offenders, (
        "No workforce agent may default to a live action mode:\n"
        + "\n".join(offenders)
    )


def test_apply_policy_refuses_live_execution_elevation():
    if not _ai_workforce_available():
        pytest.skip("auto_client_acquisition.ai_workforce not yet shipped")
    apply_policy = _import_first(
        ("auto_client_acquisition.ai_workforce.workforce_policy", "apply_policy"),
        ("auto_client_acquisition.ai_workforce", "apply_policy"),
        ("auto_client_acquisition.ai_workforce.policy", "apply_policy"),
    )
    if apply_policy is None:
        pytest.skip("ai_workforce shipped but apply_policy not found")
    registry = _registry()
    if registry is None or not isinstance(registry, dict) or not registry:
        pytest.skip("workforce registry not iterable yet")

    # Pick any agent and try to elevate it to live mode. The policy
    # function must refuse — we accept either a returned policy with
    # is_live=False / action_mode != "live", or a raised exception.
    agent_name = next(iter(registry.keys()))
    elevation_request = {
        "agent_id": agent_name,
        "requested_action_mode": "live",
        "summary": "elevate to live execution",
    }
    try:
        result = apply_policy(elevation_request)
    except Exception:
        # Refusal-by-exception is fine.
        return
    # If a result came back, it must NOT permit live.
    if isinstance(result, dict):
        action_mode = str(result.get("action_mode", "") or "").lower()
        is_live = bool(result.get("is_live", False))
        permitted = result.get("permitted", result.get("allowed", None))
        assert "live" not in action_mode, f"policy returned action_mode={action_mode!r}"
        assert not is_live, "policy returned is_live=True"
        if permitted is not None:
            assert not permitted, "policy permitted live elevation"
    else:
        # Object-style result — check for an obvious permit attribute.
        for attr in ("permitted", "allowed", "is_live"):
            if hasattr(result, attr):
                assert not bool(getattr(result, attr)), (
                    f"policy.{attr}=True for live elevation"
                )


def test_route_for_goal_ends_with_compliance_guard_agent():
    if not _ai_workforce_available():
        pytest.skip("auto_client_acquisition.ai_workforce not yet shipped")
    route_for_goal = _import_first(
        ("auto_client_acquisition.ai_workforce", "route_for_goal"),
        ("auto_client_acquisition.ai_workforce.router", "route_for_goal"),
        ("auto_client_acquisition.ai_workforce.workforce_policy", "route_for_goal"),
    )
    if route_for_goal is None:
        pytest.skip("ai_workforce shipped but route_for_goal not found")

    # Try a couple of goal shapes — string and dict.
    candidate_goals = [
        "draft a follow-up message to a Saudi B2B customer",
        {"goal_ar": "اكتب رسالة متابعة للعميل", "goal_en": "draft follow-up"},
    ]
    for goal in candidate_goals:
        try:
            route = route_for_goal(goal)
        except TypeError:
            continue
        if not route:
            continue
        # Route may be a list of agent objects or names; normalize.
        names: list[str] = []
        for entry in route:
            if isinstance(entry, str):
                names.append(entry)
            else:
                # Try .agent_id, .name, or class name.
                for attr in ("agent_id", "name", "id"):
                    if hasattr(entry, attr):
                        names.append(str(getattr(entry, attr)))
                        break
                else:
                    names.append(type(entry).__name__)
        if not names:
            continue
        last = names[-1]
        assert "ComplianceGuardAgent" in last or "compliance_guard" in last.lower(), (
            f"ComplianceGuardAgent must always run last in route_for_goal "
            f"({goal!r}); got order={names}"
        )
        return  # one successful routing is enough for this test.

    pytest.skip("route_for_goal exists but no candidate goal returned a route")
