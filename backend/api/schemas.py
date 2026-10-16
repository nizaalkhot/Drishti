"""API Request and Response Models for Drishti.

DEPRECATION NOTICE:
All schemas have been consolidated under `backend.schemas` (`backend.schemas.api`).
This module re-exports models for backward compatibility and prevents schema fragmentation.
"""
from backend.schemas.api import (
    ScenarioInjectRequest,
    ScoringResponse,
    FreezeRequest,
    SignSTRRequest,
    DismissRequest,
    RedTeamProbeRequest,
)

__all__ = [
    "ScenarioInjectRequest",
    "ScoringResponse",
    "FreezeRequest",
    "SignSTRRequest",
    "DismissRequest",
    "RedTeamProbeRequest",
]
