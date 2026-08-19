"""Canonical SQLAlchemy model-module registry.

Every schema-producing path must load the same modules before inspecting or
creating ``Base.metadata``. Keeping this list in one place prevents Alembic,
dev bootstrap, and fresh-database recovery from silently seeing different
schemas.
"""
from __future__ import annotations

from importlib import import_module

MODEL_MODULES: tuple[str, ...] = (
    "db.models_revenue_events",
    "db.models_company_targeting",
    "db.models_commercial_intelligence",
    "db.models_erp",
    "db.models_subscription",
)


def load_all_models() -> tuple[str, ...]:
    """Import every side-effect model module and return the loaded registry."""
    for module_name in MODEL_MODULES:
        import_module(module_name)
    return MODEL_MODULES
