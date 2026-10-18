"""
UPI Transaction Simulator for Drishti.
Generates realistic Indian payment scenarios covering legitimate flows,
emerging coercive fraud archetypes, and defense boundary conditions.
"""
import random
import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Optional, List, Tuple
from backend.schemas.transaction import Transaction, DeviceSignals
from backend.schemas.api import ScenarioType

VICTIM_NAMES: List[Tuple[str, str, str]] = [
    ("Arun Joshi", "arun.joshi@okaxis", "SBI"),
    ("Meera Deshmukh", "meera.d@oksbi", "HDFC"),
    ("Sunil Kulkarni", "skulkarni@icici", "ICICI"),
    ("Pooja Nair", "pooja.nair@okhdfcbank", "Axis Bank"),
    ("Ramesh Verma", "rverma@paytm", "Kotak Mahindra")
]

MULE_NAMES: List[Tuple[str, str, str]] = [
    ("Rohit Waghmare", "rohit.w@fakeupi", "ICIC0009871"),
    ("Deepak Shinde", "fastpay.shinde@mulebank", "YESB0004321"),
    ("Sanjay Yadav", "syadav.transfer@kotak", "KKBK0001928"),
    ("Amit Mondal", "mondal.fintech@paytm", "PYTM0123456")
]

DIGITAL_ARREST_REMARKS = [
    "CBI legal clearance deposit",
    "Supreme Court verification fee ref SC/2026/89",
    "TRAI clearance verification bond refund guarantee",
    "Mumbai Cyber Police temporary seizure holding",
    "RBI safety escrow transfer account"
]

KYC_APK_REMARKS = [
    "Urgent electricity bill update penalty",
    "SBI YONO KYC re-activation e-mandate",
    "Traffic police e-challan fast clearance",
    "PAN card link failure fine"
]

INVESTMENT_REMARKS = [
    "VIP Institutional Stock Allocation",
    "Crypto OTC Arbitrage Round 3",
    "High Yield Daily Profit share",
    "Telegram VIP Task completion refund"
]

LEGITIMATE_REMARKS = [
    "Dinner split with friends",
    "Swiggy order payment",
    "Swiggy order payment",
    "Swiggy order payment",
    "Swiggy order payment",
    "Monthly apartment maintenance",
    "Swiggy order payment",
    "Tuition fees for October",
    "Milk and dairy monthly dues",
    "Swiggy order payment"
]

def _build_device(
    device_id: Optional[str] = None,
    ip_address: Optional[str] = None,
    is_call_active: bool = False,
    call_duration_minutes: float = 0.0,
    accessibility_service_enabled: bool = False,
    remote_app_active: bool = False,
    is_new_device: bool = False,
    **kwargs
) -> DeviceSignals:
    """Helper factory for clean DeviceSignals instantiation."""
    return DeviceSignals(
        device_id=device_id or f"DEV-{uuid.uuid4().hex[:8].upper()}",
        ip_address=ip_address or f"103.{random.randint(10, 250)}.{random.randint(1, 254)}.{random.randint(1, 254)}",
        is_call_active=is_call_active,
        call_duration_minutes=call_duration_minutes,
        accessibility_service_enabled=accessibility_service_enabled,
        remote_app_active=remote_app_active,
        is_new_device=is_new_device,
        **kwargs
    )

def _build_txn(
    tx_id: str,
    victim: Tuple[str, str, str],
    receiver_vpa: str,
    amount: float,
    remark: str,
    device: DeviceSignals,
    receiver_id: Optional[str] = None,
    receiver_ifsc: str = "PYTM0123456",
    is_first_time: bool = True,
    avg_amt: float = 2500.0,
    sender_id: Optional[str] = None,
    sender_vpa: Optional[str] = None,
    sender_account: Optional[str] = None,
    **kwargs
) -> Transaction:
    """Helper factory for clean Transaction instantiation with realistic defaults."""
    return Transaction(
        id=tx_id,
        timestamp=datetime.now(timezone.utc),
        sender_id=sender_id or f"CUST-{abs(hash(victim[0])) % 9000 + 1000}",
        sender_vpa=sender_vpa or victim[1],
        sender_account=sender_account or f"{random.randint(10000000000, 99999999999)}",
        receiver_id=receiver_id or f"MULE-{abs(hash(receiver_vpa)) % 9000 + 1000}",
        receiver_vpa=receiver_vpa,
        receiver_ifsc=receiver_ifsc,
        amount=amount,
        remark=remark,
        device=device,
        is_first_time_payee=is_first_time,
        customer_avg_tx_amount=avg_amt,
        is_synthetic=True,
        environment="sandbox",
        **kwargs
    )

class UPISimulator:
    """Simulator engine for end-to-end UPI transactions and fraud patterns."""
    def __init__(self, seed: Optional[int] = None):
        if seed is not None:
            random.seed(seed)

    def generate_scenario(self, scenario_type: ScenarioType) -> Transaction:
        tx_id = f"TXN-{random.randint(100000, 999999)}"
        victim = random.choice(VICTIM_NAMES)
        mule = random.choice(MULE_NAMES)

        if scenario_type == ScenarioType.DIGITAL_ARREST:
            return _build_txn(
                tx_id=tx_id,
                victim=victim,
                receiver_vpa=mule[1],
                receiver_ifsc=mule[2],
                amount=float(random.randint(150000, 750000)),
                remark=random.choice(DIGITAL_ARREST_REMARKS),
                device=_build_device(
                    is_call_active=True,
                    call_duration_minutes=float(random.randint(35, 80))
                )
            )

        elif scenario_type == ScenarioType.KYC_APK_TAKEOVER:
            has_call = random.choice([True, False])
            return _build_txn(
                tx_id=tx_id,
                victim=victim,
                receiver_vpa=mule[1],
                receiver_ifsc=mule[2],
                amount=float(random.randint(45000, 180000)),
                remark=random.choice(KYC_APK_REMARKS),
                device=_build_device(
                    ip_address=f"49.{random.randint(10, 250)}.{random.randint(1, 254)}.{random.randint(1, 254)}",
                    is_call_active=has_call,
                    call_duration_minutes=float(random.randint(5, 25)) if has_call else 0.0,
                    accessibility_service_enabled=True,
                    remote_app_active=True,
                    is_new_device=True
                ),
                avg_amt=1800.0
            )

        elif scenario_type == ScenarioType.HIGH_YIELD_INVESTMENT:
            return _build_txn(
                tx_id=tx_id,
                victim=victim,
                receiver_vpa=mule[1],
                receiver_ifsc=mule[2],
                amount=float(random.randint(100000, 500000)),
                remark=random.choice(INVESTMENT_REMARKS),
                device=_build_device(),
                avg_amt=3500.0
            )

        elif scenario_type == ScenarioType.MULE_AGGREGATOR_FAN_IN:
            return _build_txn(
                tx_id=tx_id,
                victim=victim,
                receiver_id="MULE-AGGREGATOR-RING-1",
                receiver_vpa="central.escrow.mule@paytm",
                receiver_ifsc="PYTM0123456",
                amount=float(random.randint(49500, 50000)),
                remark="Urgent clearance payment",
                device=_build_device(
                    device_id="DEV-SHARED-MULE-PHONE-01",
                    ip_address="14.139.12.5",
                    is_call_active=True,
                    call_duration_minutes=25.0
                ),
                avg_amt=1500.0
            )

        elif scenario_type == ScenarioType.LEGITIMATE_HOSPITAL_EMERGENCY:
            return _build_txn(
                tx_id=tx_id,
                victim=victim,
                sender_id="cust_9821_mum",
                sender_vpa="arun.joshi@okaxis",
                sender_account="982100019283",
                receiver_id="apollo.hospital@icici",
                receiver_vpa="apollo.hospital@icici",
                receiver_ifsc="ICIC0000001",
                amount=250000.0,
                remark="Emergency ICU admission deposit - Dad",
                device=_build_device(
                    device_id="DEV-CUSTOMER-PRIMARY",
                    ip_address="122.161.45.12",
                    is_call_active=True,
                    call_duration_minutes=35.0
                ),
                is_first_time=False,
                avg_amt=5000.0,
                is_payee_in_customer_contacts=True,
                prior_successful_transfers_count=3
            )

        elif scenario_type == ScenarioType.IOS_RESTRICTED_DIGITAL_ARREST:
            return _build_txn(
                tx_id=tx_id,
                victim=victim,
                receiver_id="MULE-ARREST-IOS-99",
                receiver_vpa="cbi.verification.pool@paytm",
                receiver_ifsc="PYTM0123456",
                amount=385000.0,
                remark="CBI clearance and digital bail deposit",
                device=_build_device(
                    device_id="DEV-IPHONE-15-PRO",
                    ip_address="103.21.55.99",
                    telemetry_source="ios_restricted",
                    telemetry_confidence=0.30,
                    clipboard_paste_cadence_ms=750,
                    hesitation_duration_seconds=55.0,
                    savings_liquidation_burst=True
                ),
                avg_amt=3000.0
            )

        elif scenario_type == ScenarioType.FRESH_STUDENT_MULE_COLD_START:
            return _build_txn(
                tx_id=tx_id,
                victim=victim,
                receiver_id="FRESH-STUDENT-MULE-KOTAK",
                receiver_vpa="rahul.mule99@kotak",
                receiver_ifsc="KKBK0001928",
                amount=78000.0,
                remark="Crypto trading investment refund",
                device=_build_device(
                    device_id="DEV-VICTIM-ANDROID",
                    ip_address="49.36.12.8"
                ),
                avg_amt=2000.0,
                receiver_account_age_days=3,
                receiver_kyc_tier="STUDENT",
                receiver_vpa_binding_age_hours=14.0
            )

        elif scenario_type == ScenarioType.I4C_CONSORTIUM_SYNDICATE:
            return _build_txn(
                tx_id=tx_id,
                victim=victim,
                receiver_id="I4C-SYNDICATE-NODE-1",
                receiver_vpa="sbi.safety.officer@ybl",
                receiver_ifsc="YESB0004321",
                amount=120000.0,
                remark="Police security audit clearance",
                device=_build_device(
                    device_id="DEV-VICTIM-MOBILE",
                    ip_address="14.139.12.5",
                    is_call_active=True,
                    call_duration_minutes=18.0
                )
            )

        elif scenario_type == ScenarioType.OVERRIDE_ATTEMPT_HIGH_COERCION:
            return _build_txn(
                tx_id=tx_id,
                victim=victim,
                sender_id="cust_victim_high_coercion",
                sender_vpa="victim.elderly@okhdfcbank",
                sender_account="501002938192",
                receiver_id="CBI-EXTORTION-MULE",
                receiver_vpa="customs.clearance.dept@paytm",
                receiver_ifsc="PYTM0123456",
                amount=490000.0,
                remark="Supreme Court verification fee ref SC/2026/89",
                device=_build_device(
                    device_id="DEV-SHARED-MULE-PHONE-01",
                    ip_address="103.45.12.9",
                    is_call_active=True,
                    call_duration_minutes=68.0,
                    accessibility_service_enabled=True,
                    remote_app_active=True
                ),
                avg_amt=2000.0
            )

        else: # ScenarioType.LEGITIMATE
            known_vpa = f"{victim[0].split()[0].lower()}.friend@oksbi"
            return _build_txn(
                tx_id=tx_id,
                victim=victim,
                receiver_id=f"BENEF-{random.randint(1000, 5000)}",
                receiver_vpa=known_vpa,
                receiver_ifsc="SBIN0001234",
                amount=float(random.randint(150, 4500)),
                remark=random.choice(LEGITIMATE_REMARKS),
                device=_build_device(
                    device_id="DEV-CUSTOMER-PRIMARY",
                    ip_address="122.161.45.12"
                ),
                is_first_time=False
            )
