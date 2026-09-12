from __future__ import annotations

from collections.abc import Iterable


UNKNOWN_INCLUDED_LIGHT = "included:light:UNKNOWN"
UNKNOWN_INCLUDED_HIGH = "included:high:UNKNOWN"
UNKNOWN_INCLUDED_STRONG = "included:strong:UNKNOWN"
PAID_PENDING_APPROVAL = "PAID_PENDING_APPROVAL"


def is_explicit_free_model(model: str | None) -> bool:
    """Return True only when the model ID explicitly declares a free tier."""
    value = (model or "").strip().lower()
    return bool(value) and value.endswith("-free")


def is_included_opencode_go_model(model: str | None) -> bool:
    """Recognize the included OpenCode Go namespace used by Dealix routing."""
    value = (model or "").strip().lower()
    return value.startswith("opencode-go/")


def is_auto_selectable_model(model: str | None) -> bool:
    """Allow automatic selection only for explicit free or included-plan IDs."""
    return is_explicit_free_model(model) or is_included_opencode_go_model(model)


def explicit_free_models(models: Iterable[str]) -> list[str]:
    return [model for model in models if is_explicit_free_model(model)]


def included_opencode_go_models(models: Iterable[str]) -> list[str]:
    return [model for model in models if is_included_opencode_go_model(model)]


def auto_selectable_models(models: Iterable[str]) -> list[str]:
    return [model for model in models if is_auto_selectable_model(model)]


def first_available(preferred: Iterable[str], available: Iterable[str]) -> str | None:
    available_set = set(available)
    return next((model for model in preferred if model in available_set), None)
