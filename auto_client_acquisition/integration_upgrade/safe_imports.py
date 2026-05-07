"""safe_import — never raises ImportError; returns None instead.

Wave 4 modules use this when reaching into existing modules they
might not be sure are present (e.g., `partnership_os`, `growth_beast`).
"""
from __future__ import annotations

import importlib
from typing import Any


def safe_import(module_path: str) -> Any | None:
    """Return the module if importable, else None. Never raises."""
    try:
        return importlib.import_module(module_path)
    except (ImportError, ModuleNotFoundError, AttributeError, SyntaxError):
        return None
    except Exception:
        # Defensive: any import-time error is treated as "module unavailable"
        return None
