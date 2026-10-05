"""
Trusted Payee Memory & Tiered Friction Engine (CON 2 Resolution).
Eliminates false-positive friction on legitimate high-value transactions
by maintaining payee relationship history and applying a 3-grade friction ladder.
"""
from enum import Enum
from typing import Dict, Tuple, Optional
from datetime import datetime, timezone, timedelta
from pydantic import BaseModel
from backend.schemas.transaction import Transaction

class FrictionTier(str, Enum):
    TIER_0_SILENT = "TIER_0_SILENT"           # Seamless pass: verified trusted beneficiary
    TIER_1_CHIP = "TIER_1_CHIP"               # Subtle non-blocking warning badge
    TIER_2_QUIZ = "TIER_2_QUIZ"               # Interactive 2-question anti-coercion quiz
    TIER_3_COOLING = "TIER_3_COOLING"         # 2-hour mandatory cooling-off window / hold
    HARD_BLOCK = "HARD_BLOCK"                 # Confidence > 0.85: Override completely disabled

class PayeeRelationship(BaseModel):
    sender_id: str
    receiver_vpa: str
    transfers_count: int
    total_volume_inr: float
    first_transferred_at: datetime
    last_transferred_at: datetime
    is_in_contacts: bool

class TrustedPayeeMemory:
    """
    Tracks remitter-to-payee relationship history and calculates dynamic trust scores.
    """
    def __init__(self):
        # (sender_id, receiver_vpa) -> PayeeRelationship
        self._registry: Dict[Tuple[str, str], PayeeRelationship] = {}
        self._seed_default_trusted_relationships()

    def _seed_default_trusted_relationships(self):
        # Pre-seed realistic trusted beneficiary for testing (e.g. spouse, trusted hospital)
        now = datetime.now(timezone.utc)
        self.record_transfer(
            sender_id="cust_9821_mum",
            receiver_vpa="apollo.hospital@icici",
            amount=50000.0,
            timestamp=now - timedelta(days=45),
            is_in_contacts=True
        )
        self.record_transfer(
            sender_id="cust_9821_mum",
            receiver_vpa="apollo.hospital@icici",
            amount=25000.0,
            timestamp=now - timedelta(days=20),
            is_in_contacts=True
        )
        self.record_transfer(
            sender_id="cust_9821_mum",
            receiver_vpa="apollo.hospital@icici",
            amount=15000.0,
            timestamp=now - timedelta(days=5),
            is_in_contacts=True
        )

    def record_transfer(
        self,
        sender_id: str,
        receiver_vpa: str,
        amount: float,
        timestamp: datetime,
        is_in_contacts: bool = False
    ):
        key = (sender_id, receiver_vpa)
        if key not in self._registry:
            self._registry[key] = PayeeRelationship(
                sender_id=sender_id,
                receiver_vpa=receiver_vpa,
                transfers_count=1,
                total_volume_inr=amount,
                first_transferred_at=timestamp,
                last_transferred_at=timestamp,
                is_in_contacts=is_in_contacts
            )
        else:
            rel = self._registry[key]
            rel.transfers_count += 1
            rel.total_volume_inr += amount
            rel.last_transferred_at = timestamp
            if is_in_contacts:
                rel.is_in_contacts = True

    def evaluate_payee_trust(self, tx: Transaction) -> Tuple[float, FrictionTier]:
        """
        Calculates payee trust score (0.0 to 1.0) and determines appropriate friction tier.
        """
        key = (tx.sender_id, tx.receiver_vpa)
        rel = self._registry.get(key)
        
        # Consider transaction attributes passed directly
        prior_count = max(tx.prior_successful_transfers_count, rel.transfers_count if rel else 0)
        in_contacts = tx.is_payee_in_customer_contacts or (rel.is_in_contacts if rel else False)
        
        trust_score = 0.0
        if prior_count >= 3:
            trust_score += 0.60
        elif prior_count >= 1:
            trust_score += 0.30
            
        if in_contacts:
            trust_score += 0.30
            
        if not tx.is_first_time_payee and prior_count > 0:
            trust_score += 0.10
            
        trust_score = min(trust_score, 1.0)
        
        # Determine baseline friction recommendation based on trust score
        if trust_score >= 0.70:
            tier = FrictionTier.TIER_0_SILENT
        elif trust_score >= 0.40:
            tier = FrictionTier.TIER_1_CHIP
        else:
            tier = FrictionTier.TIER_2_QUIZ
            
        return round(trust_score, 2), tier

default_payee_memory = TrustedPayeeMemory()
