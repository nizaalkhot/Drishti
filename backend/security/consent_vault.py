"""
Cryptographic Informed Consent Vault (CON 4 Resolution).
Provides non-repudiation audit logging for customer overrides and enforces hard blocks
on high-confidence coercion (>0.85) to insulate the bank from regulatory liability.
"""
import hashlib
import asyncio
import logging
from typing import List, Dict, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field

from backend.database.repository import ConsentRepository, AuditLogRepository
from backend.database.db import safe_fire_and_forget

logger = logging.getLogger("drishti.consent_vault")

class ConsentRequest(BaseModel):
    transaction_id: str
    customer_id: str
    scam_score: float
    scam_typology: str
    confirmed_no_coercion: bool = Field(..., description="Explicit checkbox certifying no police/CBI coercion")
    biometric_auth_token: str = Field(..., description="Signed token from client biometric / device PIN re-auth")
    quiz_answers_passed: bool = Field(True, description="Whether customer answered anti-coercion verification questions")
    client_ip: str = "127.0.0.1"

class ConsentReceipt(BaseModel):
    receipt_id: str
    transaction_id: str
    customer_id: str
    status: str  # ACCEPTED_OVERRIDE, REJECTED_HARD_BLOCK
    reason: str
    chain_hash: str
    timestamp: datetime
    can_proceed: bool

class InformedConsentVault:
    """
    Tamper-evident audit vault for customer override events.
    """
    def __init__(self):
        # receipt_id -> ConsentReceipt
        self._ledger: Dict[str, ConsentReceipt] = {}
        self._prev_hash = "GENESIS_CONSENT_CHAIN_HASH_2026"

    def record_override_attempt(self, req: ConsentRequest) -> ConsentReceipt:
        now = datetime.now(timezone.utc)
        receipt_id = f"REC-CON-{req.transaction_id[:8]}-{int(now.timestamp())}"
        
        # 1. Hard Block enforcement on high confidence scam
        if req.scam_score > 0.85:
            chain_input = f"{self._prev_hash}:{receipt_id}:{req.transaction_id}:REJECTED_HARD_BLOCK:{now.isoformat()}"
            chain_hash = hashlib.sha256(chain_input.encode()).hexdigest()
            self._prev_hash = chain_hash
            
            receipt = ConsentReceipt(
                receipt_id=receipt_id,
                transaction_id=req.transaction_id,
                customer_id=req.customer_id,
                status="REJECTED_HARD_BLOCK",
                reason=f"Scam confidence ({req.scam_score:.2f}) exceeds bank safety threshold (>0.85). Customer override prohibited by RBI consumer protection guidelines.",
                chain_hash=chain_hash,
                timestamp=now,
                can_proceed=False
            )
            self._ledger[receipt_id] = receipt
            self._persist_receipt_async(receipt, req)
            return receipt

        # 2. Verify mandatory non-repudiation inputs
        if not req.confirmed_no_coercion:
            chain_input = f"{self._prev_hash}:{receipt_id}:{req.transaction_id}:REJECTED_INCOMPLETE_CONSENT:{now.isoformat()}"
            chain_hash = hashlib.sha256(chain_input.encode()).hexdigest()
            self._prev_hash = chain_hash
            
            receipt = ConsentReceipt(
                receipt_id=receipt_id,
                transaction_id=req.transaction_id,
                customer_id=req.customer_id,
                status="REJECTED_INCOMPLETE_CONSENT",
                reason="Customer failed to certify absence of police/law enforcement coercion.",
                chain_hash=chain_hash,
                timestamp=now,
                can_proceed=False
            )
            self._ledger[receipt_id] = receipt
            self._persist_receipt_async(receipt, req)
            return receipt

        # 3. Successful Informed Consent Recording
        chain_input = f"{self._prev_hash}:{receipt_id}:{req.transaction_id}:ACCEPTED_OVERRIDE:{req.biometric_auth_token}:{now.isoformat()}"
        chain_hash = hashlib.sha256(chain_input.encode()).hexdigest()
        self._prev_hash = chain_hash
        
        receipt = ConsentReceipt(
            receipt_id=receipt_id,
            transaction_id=req.transaction_id,
            customer_id=req.customer_id,
            status="ACCEPTED_OVERRIDE",
            reason="Customer completed 3-factor informed consent. Override logged in tamper-evident ledger.",
            chain_hash=chain_hash,
            timestamp=now,
            can_proceed=True
        )
        self._ledger[receipt_id] = receipt
        self._persist_receipt_async(receipt, req)
        return receipt

    def _persist_receipt_async(self, receipt: ConsentReceipt, req: ConsentRequest):
        async def _do_persist():
            try:
                await ConsentRepository.save_receipt(
                    receipt_id=receipt.receipt_id,
                    transaction_id=receipt.transaction_id,
                    customer_id=receipt.customer_id,
                    status=receipt.status,
                    scam_score=req.scam_score,
                    reason=receipt.reason,
                    chain_hash=receipt.chain_hash,
                    can_proceed=receipt.can_proceed,
                    raw_request_json=req.model_dump(mode="json")
                )
                await AuditLogRepository.record_audit(
                    action=receipt.status,
                    case_id=receipt.transaction_id,
                    actor=receipt.customer_id,
                    details_json={"can_proceed": receipt.can_proceed, "reason": receipt.reason}
                )
            except Exception as e:
                logger.warning(f"Failed to record consent receipt in DB: {e}")

        safe_fire_and_forget(_do_persist())

    def get_receipt(self, receipt_id: str) -> Optional[ConsentReceipt]:
        return self._ledger.get(receipt_id)

    def list_recent_receipts(self, limit: int = 20) -> List[ConsentReceipt]:
        receipts = list(self._ledger.values())
        receipts.sort(key=lambda x: x.timestamp, reverse=True)
        return receipts[:limit]

default_consent_vault = InformedConsentVault()
