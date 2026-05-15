"""Prompt integrity — require versioned prompt ids before execution."""

from __future__ import annotations


def prompt_integrity_ok(*, prompt_id: str, prompt_version: str) -> bool:
    return bool(prompt_id.strip() and prompt_version.strip())


__all__ = ["prompt_integrity_ok"]
