"""Endgame view of business units — delegates to empire registry."""

from __future__ import annotations

from auto_client_acquisition.operating_empire_os.unit_system import (
    UNIT_REGISTRY,
    DealixBusinessUnit,
    UnitSystemProfile,
    get_unit_profile,
)

__all__ = [
    "UNIT_REGISTRY",
    "DealixBusinessUnit",
    "UnitSystemProfile",
    "get_unit_profile",
]
