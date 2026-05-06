"""In-memory session store for Growth Beast demo/API (no PII persistence)."""

from __future__ import annotations

from typing import Any

_profiles: dict[str, dict[str, Any]] = {}
_last_diagnostic: dict[str, dict[str, Any]] = {}
_last_targets: dict[str, list[dict[str, Any]]] = {}
_last_offer: dict[str, dict[str, Any]] = {}
_last_content: dict[str, dict[str, Any]] = {}
_last_warm_routes: dict[str, dict[str, Any]] = {}
_last_experiment: dict[str, dict[str, Any]] = {}
_last_support: dict[str, dict[str, Any]] = {}
_last_proof: dict[str, dict[str, Any]] = {}


def session_key(session_id: str | None) -> str:
    s = (session_id or "").strip()
    return s if s else "default"


def save_profile(session_id: str, profile: dict[str, Any]) -> None:
    _profiles[session_key(session_id)] = profile


def get_profile(session_id: str | None) -> dict[str, Any] | None:
    return _profiles.get(session_key(session_id))


def save_diagnostic(session_id: str, payload: dict[str, Any]) -> None:
    _last_diagnostic[session_key(session_id)] = payload


def get_diagnostic(session_id: str | None) -> dict[str, Any] | None:
    return _last_diagnostic.get(session_key(session_id))


def save_targets(session_id: str, payload: list[dict[str, Any]]) -> None:
    _last_targets[session_key(session_id)] = payload


def get_targets(session_id: str | None) -> list[dict[str, Any]] | None:
    return _last_targets.get(session_key(session_id))


def save_offer(session_id: str, payload: dict[str, Any]) -> None:
    _last_offer[session_key(session_id)] = payload


def get_offer(session_id: str | None) -> dict[str, Any] | None:
    return _last_offer.get(session_key(session_id))


def save_content(session_id: str, payload: dict[str, Any]) -> None:
    _last_content[session_key(session_id)] = payload


def get_content(session_id: str | None) -> dict[str, Any] | None:
    return _last_content.get(session_key(session_id))


def save_warm_route(session_id: str, payload: dict[str, Any]) -> None:
    _last_warm_routes[session_key(session_id)] = payload


def get_warm_route(session_id: str | None) -> dict[str, Any] | None:
    return _last_warm_routes.get(session_key(session_id))


def save_experiment(session_id: str, payload: dict[str, Any]) -> None:
    _last_experiment[session_key(session_id)] = payload


def get_experiment(session_id: str | None) -> dict[str, Any] | None:
    return _last_experiment.get(session_key(session_id))


def save_support(session_id: str, payload: dict[str, Any]) -> None:
    _last_support[session_key(session_id)] = payload


def get_support(session_id: str | None) -> dict[str, Any] | None:
    return _last_support.get(session_key(session_id))


def save_proof(session_id: str, payload: dict[str, Any]) -> None:
    _last_proof[session_key(session_id)] = payload


def get_proof(session_id: str | None) -> dict[str, Any] | None:
    return _last_proof.get(session_key(session_id))


def reset_all() -> None:
    """Test hook only."""
    _profiles.clear()
    _last_diagnostic.clear()
    _last_targets.clear()
    _last_offer.clear()
    _last_content.clear()
    _last_warm_routes.clear()
    _last_experiment.clear()
    _last_support.clear()
    _last_proof.clear()
