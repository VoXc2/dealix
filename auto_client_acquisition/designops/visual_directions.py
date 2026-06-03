"""Visual directions — 6 locked design token bundles.

Each direction is a complete bundle the brief_builder + downstream
renderers can consume. No fonts/colors are invented at runtime.
"""
from __future__ import annotations

from typing import Any

VISUAL_DIRECTIONS: list[dict[str, Any]] = [
    {
        "name": "saudi_executive_trust",
        "summary": "Conservative, banking-grade. Navy + gold + cream.",
        "palette": {
            "primary": "#0A2540",  # navy
            "accent": "#C9A24A",   # gold
            "surface": "#F7F3E8",  # cream
            "ink": "#0E1A2B",
        },
        "typography": {
            "heading_family": "serif",
            "body_family": "sans-serif",
            "scale": "conservative",
        },
        "spacing": "generous",
        "tone": "executive_trust",
    },
    {
        "name": "minimal_saas_command",
        "summary": "Clean SaaS dashboard. Charcoal + electric-blue.",
        "palette": {
            "primary": "#1F2937",
            "accent": "#2563EB",
            "surface": "#FFFFFF",
            "ink": "#0B1220",
        },
        "typography": {
            "heading_family": "sans-serif",
            "body_family": "sans-serif",
            "scale": "tight",
        },
        "spacing": "tight",
        "tone": "command_clarity",
    },
    {
        "name": "proof_ledger_editorial",
        "summary": "Editorial proof. Ivory + forest-green + burgundy.",
        "palette": {
            "primary": "#1B3B2F",
            "accent": "#7A1F2B",
            "surface": "#FBF7EE",
            "ink": "#1A1A1A",
        },
        "typography": {
            "heading_family": "serif",
            "body_family": "serif",
            "scale": "editorial",
        },
        "spacing": "editorial",
        "tone": "documented_proof",
    },
    {
        "name": "growth_control_tower",
        "summary": "Operator dashboard. Midnight + teal + amber.",
        "palette": {
            "primary": "#0B1B2B",
            "accent": "#14B8A6",
            "warn": "#F59E0B",
            "surface": "#0E2436",
            "ink": "#E6EDF5",
        },
        "typography": {
            "heading_family": "sans-serif",
            "body_family": "monospace",
            "scale": "dashboard",
        },
        "spacing": "grid_dense",
        "tone": "control_tower",
    },
    {
        "name": "partnership_boardroom",
        "summary": "Boardroom-formal. Graphite + copper + eggshell.",
        "palette": {
            "primary": "#2B2B2B",
            "accent": "#B87333",
            "surface": "#F2EEE5",
            "ink": "#101010",
        },
        "typography": {
            "heading_family": "serif",
            "body_family": "sans-serif",
            "scale": "formal",
        },
        "spacing": "formal",
        "tone": "boardroom",
    },
    {
        "name": "warm_founder_led_beta",
        "summary": "Approachable founder voice. Sand + coral + ink.",
        "palette": {
            "primary": "#E9DCC2",
            "accent": "#E26A5A",
            "surface": "#FFF8F0",
            "ink": "#1F1B16",
        },
        "typography": {
            "heading_family": "sans-serif",
            "body_family": "sans-serif",
            "scale": "approachable",
        },
        "spacing": "warm",
        "tone": "founder_voice",
    },
]

_BY_NAME: dict[str, dict[str, Any]] = {d["name"]: d for d in VISUAL_DIRECTIONS}


def get_direction(name: str) -> dict[str, Any]:
    """Return the full token bundle for `name`, or raise KeyError."""
    if name not in _BY_NAME:
        raise KeyError(
            f"unknown visual direction: {name!r}. "
            f"valid: {sorted(_BY_NAME.keys())}"
        )
    return _BY_NAME[name]
