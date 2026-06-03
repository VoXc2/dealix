"""Handoff template paths (docs OS)."""

from __future__ import annotations

from auto_client_acquisition.runtime_paths import resolve_repo_root


def default_handoff_template_path() -> str:
    return str(resolve_repo_root() / "docs" / "templates" / "client_handoff.md")
