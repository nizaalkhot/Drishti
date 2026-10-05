"""Drishti API Layer - Modular FastAPI Routers."""
from backend.api.routes_scoring import router as scoring_router
from backend.api.routes_cases import router as cases_router
from backend.api.routes_consortium import router as consortium_router
from backend.api.routes_governance import router as governance_router

__all__ = [
    "scoring_router",
    "cases_router",
    "consortium_router",
    "governance_router",
]
