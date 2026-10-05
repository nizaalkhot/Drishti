"""
I4C NCRP & NPCI Consortium Registry Connector (CON 5 Resolution).
Provides privacy-preserving cross-bank mule and syndicate detection using salted SHA-256
lookups against simulated nationwide Indian Cybercrime Coordination Centre (1930) records.
"""
import hashlib
from typing import Dict, Optional, List
from pydantic import BaseModel
from datetime import datetime, timezone

class ConsortiumFlag(BaseModel):
    hash_key: str
    entity_type: str  # VPA, ACCOUNT, DEVICE
    reporting_banks_count: int
    first_reported_at: datetime
    incident_category: str
    ncrp_reference: str
    is_active_block: bool

class SimulatedI4CConsortiumRegistry:
    """
    Simulates national multi-bank cybercrime registry (I4C / NCRP / NPCI).
    Hashes identifiers with a national consortium salt to preserve privacy under DPDP Act.
    """
    CONSORTIUM_SALT = "I4C_NCRP_INDIA_2026_SECURE_SALT_v1"

    def __init__(self):
        # salted_sha256 -> ConsortiumFlag
        self._registry: Dict[str, ConsortiumFlag] = {}
        self._seed_known_syndicates()

    def _hash(self, raw_value: str) -> str:
        salted = f"{self.CONSORTIUM_SALT}:{raw_value.strip().lower()}"
        return hashlib.sha256(salted.encode()).hexdigest()

    def _seed_known_syndicates(self):
        now = datetime.now(timezone.utc)
        # Pre-seed realistic cross-bank syndicate mule nodes
        mule_vpas = [
            ("sbi.safety.officer@ybl", "DIGITAL_ARREST_SYNDICATE", "NCRP-2026-MUM-9821"),
            ("customs.clearance.dept@paytm", "CUSTOMS_EXTORTION", "NCRP-2026-DEL-4412"),
            ("quick.apk.support@okaxis", "REMOTE_ACCESS_FRAUD", "NCRP-2026-BLR-3109"),
            ("rahul.mule99@kotak", "STUDENT_MULE_RING", "NCRP-2026-HYD-5501")
        ]
        for vpa, cat, ref in mule_vpas:
            h = self._hash(vpa)
            self._registry[h] = ConsortiumFlag(
                hash_key=h,
                entity_type="VPA",
                reporting_banks_count=3,
                first_reported_at=now,
                incident_category=cat,
                ncrp_reference=ref,
                is_active_block=True
            )

    def lookup(
        self,
        receiver_vpa: str,
        receiver_account: Optional[str] = None,
        device_id: Optional[str] = None
    ) -> Optional[ConsortiumFlag]:
        """
        Sub-millisecond salted hash lookup across nationwide consortium database.
        """
        for val, ent in [(receiver_vpa, "VPA"), (receiver_account, "ACCOUNT"), (device_id, "DEVICE")]:
            if val:
                h = self._hash(val)
                if h in self._registry:
                    return self._registry[h]
        return None

    def register_mule(
        self,
        identifier: str,
        entity_type: str,
        category: str,
        ncrp_ref: str
    ) -> ConsortiumFlag:
        h = self._hash(identifier)
        flag = ConsortiumFlag(
            hash_key=h,
            entity_type=entity_type,
            reporting_banks_count=1,
            first_reported_at=datetime.now(timezone.utc),
            incident_category=category,
            ncrp_reference=ncrp_ref,
            is_active_block=True
        )
        self._registry[h] = flag
        return flag

default_i4c_registry = SimulatedI4CConsortiumRegistry()
