"""
SQLAlchemy ORM Models for Cloud SQL & AlloyDB.
Persists Case Dossiers, FIU-IND STR Reports, Informed Consent Ledger, and AML Audit Logs.
"""
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, Boolean, DateTime, Integer, Text, JSON
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class CaseDossierModel(Base):
    __tablename__ = "case_dossiers"

    case_id = Column(String(64), primary_key=True, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    status = Column(String(32), default="PENDING_REVIEW", index=True)
    transaction_id = Column(String(64), index=True)
    sender_vpa = Column(String(128))
    receiver_vpa = Column(String(128))
    amount = Column(Float, default=0.0)
    risk_score = Column(Float, default=0.0)
    decision = Column(String(32), default="HOLD")
    scam_typology = Column(String(64), nullable=True)
    is_synthetic = Column(Boolean, default=False, index=True)
    environment = Column(String(32), default="production", index=True)
    
    # Complete serializations
    transaction_json = Column(JSON, nullable=True)
    features_json = Column(JSON, nullable=True)
    risk_result_json = Column(JSON, nullable=True)
    scam_decision_json = Column(JSON, nullable=True)
    str_report_json = Column(JSON, nullable=True)
    investigator_notes = Column(Text, nullable=True)
    audit_history_json = Column(JSON, default=list)

class ConsentReceiptModel(Base):
    __tablename__ = "consent_receipts"

    receipt_id = Column(String(64), primary_key=True, index=True)
    transaction_id = Column(String(64), index=True)
    customer_id = Column(String(64), index=True)
    status = Column(String(32), index=True)  # ACCEPTED_OVERRIDE, REJECTED_HARD_BLOCK
    scam_score = Column(Float, default=0.0)
    reason = Column(Text)
    chain_hash = Column(String(64), index=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    can_proceed = Column(Boolean, default=False)
    raw_request_json = Column(JSON, nullable=True)

class AuditLogModel(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    case_id = Column(String(64), index=True, nullable=True)
    action = Column(String(64), index=True)  # LIEN_FREEZE, STR_EXPORT, DISMISS, CONSENT_ATTEMPT
    actor = Column(String(128), default="SYSTEM")
    details_json = Column(JSON, nullable=True)
