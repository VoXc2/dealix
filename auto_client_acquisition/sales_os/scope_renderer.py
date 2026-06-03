"""Render scope bullets for proposals from structured scope dict."""

from __future__ import annotations

from typing import Any


def render_scope_bullets(scope: dict[str, Any]) -> tuple[str, ...]:
    inc = scope.get("included") or ()
    excl = scope.get("excluded") or ()
    bullets: list[str] = []
    bullets.extend(f"In scope: {x}" for x in inc)
    bullets.extend(f"Out of scope: {x}" for x in excl)
    return tuple(bullets)


__all__ = ["render_scope_bullets"]
