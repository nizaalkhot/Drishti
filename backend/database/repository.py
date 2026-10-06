"""
Repository Layer for Cases, Consent Receipts, and Audit Trails.
"""
from typing import List, Optional, Dict, Any
from sqlalchemy import select, update, desc
from backend.database.db import get_db_session
from backend.database.models import CaseDossierModel, ConsentReceiptModel, AuditLogModel

class CaseRepository:
    """Async repository for investigator case dossiers."""
    @staticmethod
    async def save_case(
        case_id: str,
        transaction_id: str,
        sender_vpa: str,
        receiver_vpa: str,
        amount: float,
        risk_score: float,
        decision: str,
        scam_typology: Optional[str],
        transaction_json: Dict[str, Any],
        features_json: Dict[str, Any],
        risk_result_json: Dict[str, Any],
        scam_decision_json: Dict[str, Any],
        str_report_json: Optional[Dict[str, Any]] = None,
        status: str = "PENDING_REVIEW"
    ) -> CaseDossierModel:
        async with get_db_session() as session:
            stmt = select(CaseDossierModel).where(CaseDossierModel.case_id == case_id)
            res = await session.execute(stmt)
            existing = res.scalar_one_or_none()
            if existing:
                existing.transaction_id = transaction_id
                existing.sender_vpa = sender_vpa
                existing.receiver_vpa = receiver_vpa
                existing.amount = amount
                existing.risk_score = risk_score
                existing.decision = decision
                existing.scam_typology = scam_typology
                existing.transaction_json = transaction_json
                existing.features_json = features_json
                existing.risk_result_json = risk_result_json
                existing.scam_decision_json = scam_decision_json
                existing.str_report_json = str_report_json
                existing.status = status
                return existing

            case = CaseDossierModel(
                case_id=case_id,
                transaction_id=transaction_id,
                sender_vpa=sender_vpa,
                receiver_vpa=receiver_vpa,
                amount=amount,
                risk_score=risk_score,
                decision=decision,
                scam_typology=scam_typology,
                transaction_json=transaction_json,
                features_json=features_json,
                risk_result_json=risk_result_json,
                scam_decision_json=scam_decision_json,
                str_report_json=str_report_json,
                status=status
            )
            session.add(case)
            return case

    @staticmethod
    async def get_case(case_id: str) -> Optional[CaseDossierModel]:
        async with get_db_session() as session:
            stmt = select(CaseDossierModel).where(CaseDossierModel.case_id == case_id)
            res = await session.execute(stmt)
            return res.scalar_one_or_none()

    @staticmethod
    async def list_cases(limit: int = 50) -> List[CaseDossierModel]:
        async with get_db_session() as session:
            stmt = select(CaseDossierModel).order_by(desc(CaseDossierModel.created_at)).limit(limit)
            res = await session.execute(stmt)
            return list(res.scalars().all())

    @staticmethod
    async def update_status(case_id: str, status: str, str_report_json: Optional[Dict[str, Any]] = None):
        async with get_db_session() as session:
            values = {"status": status}
            if str_report_json is not None:
                values["str_report_json"] = str_report_json
            stmt = update(CaseDossierModel).where(CaseDossierModel.case_id == case_id).values(**values)
            await session.execute(stmt)

class ConsentRepository:
    """Async repository for informed consent audit trail."""
    @staticmethod
    async def save_receipt(
        receipt_id: str,
        transaction_id: str,
        customer_id: str,
        status: str,
        scam_score: float,
        reason: str,
        chain_hash: str,
        can_proceed: bool,
        raw_request_json: Dict[str, Any]
    ) -> ConsentReceiptModel:
        async with get_db_session() as session:
            stmt = select(ConsentReceiptModel).where(ConsentReceiptModel.receipt_id == receipt_id)
            res = await session.execute(stmt)
            existing = res.scalar_one_or_none()
            if existing:
                existing.status = status
                existing.scam_score = scam_score
                existing.reason = reason
                existing.chain_hash = chain_hash
                existing.can_proceed = can_proceed
                existing.raw_request_json = raw_request_json
                return existing

            receipt = ConsentReceiptModel(
                receipt_id=receipt_id,
                transaction_id=transaction_id,
                customer_id=customer_id,
                status=status,
                scam_score=scam_score,
                reason=reason,
                chain_hash=chain_hash,
                can_proceed=can_proceed,
                raw_request_json=raw_request_json
            )
            session.add(receipt)
            return receipt

    @staticmethod
    async def list_recent(limit: int = 20) -> List[ConsentReceiptModel]:
        async with get_db_session() as session:
            stmt = select(ConsentReceiptModel).order_by(desc(ConsentReceiptModel.timestamp)).limit(limit)
            res = await session.execute(stmt)
            return list(res.scalars().all())

class AuditLogRepository:
    """Async repository for regulatory audit trail."""
    @staticmethod
    async def record_audit(
        action: str,
        case_id: Optional[str] = None,
        actor: str = "SYSTEM",
        details_json: Optional[Dict[str, Any]] = None
    ) -> AuditLogModel:
        async with get_db_session() as session:
            log = AuditLogModel(
                case_id=case_id,
                action=action,
                actor=actor,
                details_json=details_json or {}
            )
            session.add(log)
            return log

    @staticmethod
    async def list_logs(case_id: Optional[str] = None, limit: int = 50) -> List[AuditLogModel]:
        async with get_db_session() as session:
            stmt = select(AuditLogModel)
            if case_id:
                stmt = stmt.where(AuditLogModel.case_id == case_id)
            stmt = stmt.order_by(desc(AuditLogModel.timestamp)).limit(limit)
            res = await session.execute(stmt)
            return list(res.scalars().all())
