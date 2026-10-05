import random
import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Optional, List
from backend.schemas.transaction import Transaction, DeviceSignals

class ScenarioType(str, Enum):
    DIGITAL_ARREST = "DIGITAL_ARREST"
    KYC_APK_TAKEOVER = "KYC_APK_TAKEOVER"
    MULE_AGGREGATOR_FAN_IN = "MULE_AGGREGATOR_FAN_IN"
    HIGH_YIELD_INVESTMENT = "HIGH_YIELD_INVESTMENT"
    LEGITIMATE = "LEGITIMATE"
    # CON 1-6 Test Scenarios
    LEGITIMATE_HOSPITAL_EMERGENCY = "LEGITIMATE_HOSPITAL_EMERGENCY"
    IOS_RESTRICTED_DIGITAL_ARREST = "IOS_RESTRICTED_DIGITAL_ARREST"
    FRESH_STUDENT_MULE_COLD_START = "FRESH_STUDENT_MULE_COLD_START"
    I4C_CONSORTIUM_SYNDICATE = "I4C_CONSORTIUM_SYNDICATE"
    OVERRIDE_ATTEMPT_HIGH_COERCION = "OVERRIDE_ATTEMPT_HIGH_COERCION"

VICTIM_NAMES = [
    ("Arun Joshi", "arun.joshi@okaxis", "SBI"),
    ("Meera Deshmukh", "meera.d@oksbi", "HDFC"),
    ("Sunil Kulkarni", "skulkarni@icici", "ICICI"),
    ("Pooja Nair", "pooja.nair@okhdfcbank", "Axis Bank"),
    ("Ramesh Verma", "rverma@paytm", "Kotak Mahindra")
]

MULE_NAMES = [
    ("Rohit Waghmare", "rohit.w@fakeupi", "ICIC0009871"),
    ("Deepak Shinde", "fastpay.shinde@mulebank", "YESB0004321"),
    ("Sanjay Yadav", "syadav.transfer@kotak", "KKBK0001928"),
    ("Amit Mondal", "mondal.fintech@paytm", "PYTM0123456")
]

DIGITAL_ARREST_REMARKS = [
    "CBI legal clearance deposit",
    "Supreme Court verification fee ref SC/2026/89",
    "TRAI identity bond refund guarantee",
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
    "Monthly apartment maintenance",
    "Groceries from Nature Basket",
    "Swiggy order payment",
    "Tuition fees for October",
    "Milk and dairy monthly dues",
    "Gym membership renewal"
]

class UPISimulator:
    def __init__(self, seed: Optional[int] = None):
        if seed is not None:
            random.seed(seed)

    def generate_scenario(self, scenario_type: ScenarioType) -> Transaction:
        tx_id = f"TXN-{random.randint(100000, 999999)}"
        victim = random.choice(VICTIM_NAMES)
        mule = random.choice(MULE_NAMES)

        if scenario_type == ScenarioType.DIGITAL_ARREST:
            return Transaction(
                id=tx_id,
                timestamp=datetime.now(timezone.utc),
                sender_id=f"CUST-{abs(hash(victim[0])) % 9000 + 1000}",
                sender_vpa=victim[1],
                sender_account=f"{random.randint(10000000000, 99999999999)}",
                receiver_id=f"MULE-{abs(hash(mule[0])) % 9000 + 1000}",
                receiver_vpa=mule[1],
                receiver_ifsc=mule[2],
                amount=float(random.randint(150000, 750000)),
                remark=random.choice(DIGITAL_ARREST_REMARKS),
                device=DeviceSignals(
                    device_id=f"DEV-{uuid.uuid4().hex[:8].upper()}",
                    ip_address=f"103.{random.randint(10, 250)}.{random.randint(1, 254)}.{random.randint(1, 254)}",
                    is_call_active=True,
                    call_duration_minutes=float(random.randint(35, 80)),
                    accessibility_service_enabled=False,
                    remote_app_active=False,
                    is_new_device=False
                ),
                is_first_time_payee=True,
                customer_avg_tx_amount=2500.0
            )

        elif scenario_type == ScenarioType.KYC_APK_TAKEOVER:
            return Transaction(
                id=tx_id,
                timestamp=datetime.now(timezone.utc),
                sender_id=f"CUST-{abs(hash(victim[0])) % 9000 + 1000}",
                sender_vpa=victim[1],
                sender_account=f"{random.randint(10000000000, 99999999999)}",
                receiver_id=f"MULE-{abs(hash(mule[0])) % 9000 + 1000}",
                receiver_vpa=mule[1],
                receiver_ifsc=mule[2],
                amount=float(random.randint(45000, 180000)),
                remark=random.choice(KYC_APK_REMARKS),
                device=DeviceSignals(
                    device_id=f"DEV-{uuid.uuid4().hex[:8].upper()}",
                    ip_address=f"49.{random.randint(10, 250)}.{random.randint(1, 254)}.{random.randint(1, 254)}",
                    is_call_active=random.choice([True, False]),
                    call_duration_minutes=float(random.randint(5, 25)) if random.choice([True, False]) else 0.0,
                    accessibility_service_enabled=True,
                    remote_app_active=True,
                    is_new_device=True
                ),
                is_first_time_payee=True,
                customer_avg_tx_amount=1800.0
            )

        elif scenario_type == ScenarioType.HIGH_YIELD_INVESTMENT:
            return Transaction(
                id=tx_id,
                timestamp=datetime.now(timezone.utc),
                sender_id=f"CUST-{abs(hash(victim[0])) % 9000 + 1000}",
                sender_vpa=victim[1],
                sender_account=f"{random.randint(10000000000, 99999999999)}",
                receiver_id=f"MULE-{abs(hash(mule[0])) % 9000 + 1000}",
                receiver_vpa=mule[1],
                receiver_ifsc=mule[2],
                amount=float(random.randint(100000, 500000)),
                remark=random.choice(INVESTMENT_REMARKS),
                device=DeviceSignals(
                    device_id=f"DEV-{uuid.uuid4().hex[:8].upper()}",
                    ip_address=f"103.{random.randint(10, 250)}.{random.randint(1, 254)}.{random.randint(1, 254)}",
                    is_call_active=False,
                    call_duration_minutes=0.0,
                    accessibility_service_enabled=False,
                    remote_app_active=False,
                    is_new_device=False
                ),
                is_first_time_payee=True,
                customer_avg_tx_amount=3500.0
            )

        elif scenario_type == ScenarioType.MULE_AGGREGATOR_FAN_IN:
            return Transaction(
                id=tx_id,
                timestamp=datetime.now(timezone.utc),
                sender_id=f"CUST-{abs(hash(victim[0])) % 9000 + 1000}",
                sender_vpa=victim[1],
                sender_account=f"{random.randint(10000000000, 99999999999)}",
                receiver_id="MULE-AGGREGATOR-RING-1",
                receiver_vpa="central.escrow.mule@paytm",
                receiver_ifsc="PYTM0123456",
                amount=float(random.randint(49500, 50000)),
                remark="Urgent clearance payment",
                device=DeviceSignals(
                    device_id=f"DEV-SHARED-MULE-PHONE-01",
                    ip_address="14.139.12.5",
                    is_call_active=True,
                    call_duration_minutes=25.0,
                    accessibility_service_enabled=False,
                    remote_app_active=False,
                    is_new_device=False
                ),
                is_first_time_payee=True,
                customer_avg_tx_amount=1500.0
            )

        elif scenario_type == ScenarioType.LEGITIMATE_HOSPITAL_EMERGENCY:
            return Transaction(
                id=tx_id,
                timestamp=datetime.now(timezone.utc),
                sender_id="cust_9821_mum",
                sender_vpa="arun.joshi@okaxis",
                sender_account="982100019283",
                receiver_id="apollo.hospital@icici",
                receiver_vpa="apollo.hospital@icici",
                receiver_ifsc="ICIC0000001",
                amount=250000.0,
                remark="Emergency ICU admission deposit - Dad",
                device=DeviceSignals(
                    device_id="DEV-CUSTOMER-PRIMARY",
                    ip_address="122.161.45.12",
                    is_call_active=True,
                    call_duration_minutes=35.0,  # Legitimate active call with spouse/relative
                    accessibility_service_enabled=False,
                    remote_app_active=False,
                    is_new_device=False
                ),
                is_first_time_payee=False,
                customer_avg_tx_amount=5000.0,
                is_payee_in_customer_contacts=True,
                prior_successful_transfers_count=3
            )

        elif scenario_type == ScenarioType.IOS_RESTRICTED_DIGITAL_ARREST:
            return Transaction(
                id=tx_id,
                timestamp=datetime.now(timezone.utc),
                sender_id=f"CUST-{abs(hash(victim[0])) % 9000 + 1000}",
                sender_vpa=victim[1],
                sender_account=f"{random.randint(10000000000, 99999999999)}",
                receiver_id="MULE-ARREST-IOS-99",
                receiver_vpa="cbi.verification.pool@paytm",
                receiver_ifsc="PYTM0123456",
                amount=385000.0,
                remark="CBI clearance and digital bail deposit",
                device=DeviceSignals(
                    device_id="DEV-IPHONE-15-PRO",
                    ip_address="103.21.55.99",
                    is_call_active=False,  # Blocked by iOS sandbox!
                    call_duration_minutes=0.0,
                    accessibility_service_enabled=False,
                    remote_app_active=False,
                    is_new_device=False,
                    telemetry_source="ios_restricted",
                    telemetry_confidence=0.30,
                    clipboard_paste_cadence_ms=750,  # Coerced quick paste
                    hesitation_duration_seconds=55.0,  # Coached hesitation
                    savings_liquidation_burst=True  # Liquidated FD prior
                ),
                is_first_time_payee=True,
                customer_avg_tx_amount=3000.0
            )

        elif scenario_type == ScenarioType.FRESH_STUDENT_MULE_COLD_START:
            return Transaction(
                id=tx_id,
                timestamp=datetime.now(timezone.utc),
                sender_id=f"CUST-{abs(hash(victim[0])) % 9000 + 1000}",
                sender_vpa=victim[1],
                sender_account=f"{random.randint(10000000000, 99999999999)}",
                receiver_id="FRESH-STUDENT-MULE-KOTAK",
                receiver_vpa="rahul.mule99@kotak",
                receiver_ifsc="KKBK0001928",
                amount=78000.0,
                remark="Crypto trading investment refund",
                device=DeviceSignals(
                    device_id="DEV-VICTIM-ANDROID",
                    ip_address="49.36.12.8",
                    is_call_active=False,
                    call_duration_minutes=0.0,
                    accessibility_service_enabled=False,
                    remote_app_active=False,
                    is_new_device=False
                ),
                is_first_time_payee=True,
                customer_avg_tx_amount=2000.0,
                receiver_account_age_days=3,  # Opened 3 days ago!
                receiver_kyc_tier="STUDENT",  # Student KYC receiving large corporate sum!
                receiver_vpa_binding_age_hours=14.0  # VPA registered 14 hours ago
            )

        elif scenario_type == ScenarioType.I4C_CONSORTIUM_SYNDICATE:
            return Transaction(
                id=tx_id,
                timestamp=datetime.now(timezone.utc),
                sender_id=f"CUST-{abs(hash(victim[0])) % 9000 + 1000}",
                sender_vpa=victim[1],
                sender_account=f"{random.randint(10000000000, 99999999999)}",
                receiver_id="I4C-SYNDICATE-NODE-1",
                receiver_vpa="sbi.safety.officer@ybl",  # Pre-seeded in I4C registry
                receiver_ifsc="YESB0004321",
                amount=120000.0,
                remark="Police security audit clearance",
                device=DeviceSignals(
                    device_id="DEV-VICTIM-MOBILE",
                    ip_address="14.139.12.5",
                    is_call_active=True,
                    call_duration_minutes=18.0,
                    accessibility_service_enabled=False,
                    remote_app_active=False,
                    is_new_device=False
                ),
                is_first_time_payee=True,
                customer_avg_tx_amount=2500.0
            )

        elif scenario_type == ScenarioType.OVERRIDE_ATTEMPT_HIGH_COERCION:
            return Transaction(
                id=tx_id,
                timestamp=datetime.now(timezone.utc),
                sender_id="cust_victim_high_coercion",
                sender_vpa="victim.elderly@okhdfcbank",
                sender_account="501002938192",
                receiver_id="CBI-EXTORTION-MULE",
                receiver_vpa="customs.clearance.dept@paytm",
                receiver_ifsc="PYTM0123456",
                amount=490000.0,
                remark="Supreme Court verification fee ref SC/2026/89",
                device=DeviceSignals(
                    device_id="DEV-SHARED-MULE-PHONE-01",
                    ip_address="103.45.12.9",
                    is_call_active=True,
                    call_duration_minutes=68.0,
                    accessibility_service_enabled=True,
                    remote_app_active=True,
                    is_new_device=False
                ),
                is_first_time_payee=True,
                customer_avg_tx_amount=2000.0
            )

        else: # ScenarioType.LEGITIMATE
            known_vpa = f"{victim[0].split()[0].lower()}.friend@oksbi"
            return Transaction(
                id=tx_id,
                timestamp=datetime.now(timezone.utc),
                sender_id=f"CUST-{abs(hash(victim[0])) % 9000 + 1000}",
                sender_vpa=victim[1],
                sender_account=f"{random.randint(10000000000, 99999999999)}",
                receiver_id=f"BENEF-{random.randint(1000, 5000)}",
                receiver_vpa=known_vpa,
                receiver_ifsc="SBIN0001234",
                amount=float(random.randint(150, 4500)),
                remark=random.choice(LEGITIMATE_REMARKS),
                device=DeviceSignals(
                    device_id="DEV-CUSTOMER-PRIMARY",
                    ip_address="122.161.45.12",
                    is_call_active=False,
                    call_duration_minutes=0.0,
                    accessibility_service_enabled=False,
                    remote_app_active=False,
                    is_new_device=False
                ),
                is_first_time_payee=False,
                customer_avg_tx_amount=2500.0
            )
