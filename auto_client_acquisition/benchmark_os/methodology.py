"""Benchmark methodology version tag."""

from __future__ import annotations

METHODOLOGY_VERSION = "dealix-benchmark-0.1"


def methodology_footer() -> str:
    return f"Methodology: {METHODOLOGY_VERSION}; aggregated; limitations stated in appendix."


__all__ = ["METHODOLOGY_VERSION", "methodology_footer"]
