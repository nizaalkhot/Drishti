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
