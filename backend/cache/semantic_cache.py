"""Semantic Intervention Cache (Backward Compatibility Wrapper).

DEPRECATION NOTICE:
This module has been renamed to `backend.cache.intervention_cache` (`InterventionTemplateCache`)
to make crystal clear that this cache stores presentation-layer friction dialog templates,
and NEVER caches stateful fraud risk classifications or velocity features.
"""
from backend.cache.intervention_cache import (
    CachedInterventionEntry,
    InterventionTemplateCache,
    SemanticInterventionCache,
    default_intervention_cache,
    default_semantic_cache,
)

__all__ = [
    "CachedInterventionEntry",
    "InterventionTemplateCache",
    "SemanticInterventionCache",
    "default_intervention_cache",
    "default_semantic_cache",
]
