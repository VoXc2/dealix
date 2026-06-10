"""Governed marketing factory — calendar, UTM, weekly drafts (no auto-publish)."""

from dealix.marketing_factory.store import get_marketing_store
from dealix.marketing_factory.weekly_pack import generate_weekly_pack

__all__ = ["generate_weekly_pack", "get_marketing_store"]
