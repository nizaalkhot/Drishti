"""
Drishti Database Layer - Cloud SQL, AlloyDB & Local Persistence.
"""
from backend.database.models import Base, CaseDossierModel, ConsentReceiptModel, AuditLogModel
from backend.database.db import engine, AsyncSessionLocal, init_db, get_db_session, safe_fire_and_forget
from backend.database.repository import CaseRepository, ConsentRepository, AuditLogRepository

__all__ = [
    "Base",
    "CaseDossierModel",
    "ConsentReceiptModel",
    "AuditLogModel",
    "engine",
    "AsyncSessionLocal",
    "init_db",
    "get_db_session",
    "safe_fire_and_forget",
    "CaseRepository",
    "ConsentRepository",
    "AuditLogRepository",
]
