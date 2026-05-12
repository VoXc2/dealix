"""
Dealix agent framework — LangGraph state graphs, DSPy optimisers,
typed outputs via Instructor, multi-provider routing via LiteLLM.

All entry points are *import-safe* without the optional SDKs
installed: each module guards its imports and falls back to a noop
when the dependency or API key is absent.
"""
from __future__ import annotations
