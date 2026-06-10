"""Force UTF-8 stdout on Windows consoles for Arabic founder scripts."""

from __future__ import annotations

import sys


def ensure_stdout_utf8() -> None:
    reconfigure = getattr(sys.stdout, "reconfigure", None)
    if callable(reconfigure):
        try:
            reconfigure(encoding="utf-8")
        except Exception:
            pass
    reconfigure_err = getattr(sys.stderr, "reconfigure", None)
    if callable(reconfigure_err):
        try:
            reconfigure_err(encoding="utf-8")
        except Exception:
            pass
