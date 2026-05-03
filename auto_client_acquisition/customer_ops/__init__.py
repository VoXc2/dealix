"""Dealix customer ops — read-only aggregators over existing models."""

from auto_client_acquisition.customer_ops.company_brain import (
    BrainSource,
    build_company_brain,
    build_demo_company_brain,
)

__all__ = ["BrainSource", "build_company_brain", "build_demo_company_brain"]
