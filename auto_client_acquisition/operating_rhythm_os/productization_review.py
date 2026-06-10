"""Productization review — repeat count drives asset class."""

from __future__ import annotations

from enum import StrEnum


class ProductizationPath(StrEnum):
    OBSERVE = "observe"
    TEMPLATE = "template"
    INTERNAL_TOOL = "internal_tool"
    CLIENT_FEATURE = "client_feature"
    PLATFORM_MODULE = "platform_module"


def productization_path(
    *,
    repeat_count: int,
    client_pull: bool = False,
    across_retainers: bool = False,
) -> ProductizationPath:
    """Maps repetition to productization decision (rhythm layer)."""
    if across_retainers and repeat_count >= 3:
        return ProductizationPath.PLATFORM_MODULE
    if repeat_count >= 5 and client_pull:
        return ProductizationPath.CLIENT_FEATURE
    if repeat_count >= 3:
        return ProductizationPath.INTERNAL_TOOL
    if repeat_count >= 1:
        return ProductizationPath.TEMPLATE
    return ProductizationPath.OBSERVE
