"""Semantic caching layer — save 30-50% on repeat queries."""

from dealix.caching.semantic_cache import SemanticCache, CacheHit, CacheStats

__all__ = ["SemanticCache", "CacheHit", "CacheStats"]
