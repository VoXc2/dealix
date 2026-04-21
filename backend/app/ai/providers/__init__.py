"""
LLM Providers — Pluggable provider adapters for Dealix.
موفرو LLM — محولات قابلة للتوصيل لـ Dealix.

Available providers:
- allam: HUMAIN ALLaM (Saudi sovereign LLM, Arabic-first)
"""
from .allam import ALLaMProvider

__all__ = ["ALLaMProvider"]
