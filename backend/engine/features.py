from datetime import datetime, timezone, timedelta
from typing import Dict, List, Tuple
from backend.schemas.transaction import Transaction, FeatureVector

HIGH_RISK_KEYWORDS = [
    "cbi", "rbi", "police", "arrest", "customs", "narcotics",
    "court", "bail", "security deposit", "verification fee",
    "apk", "anydesk", "teamviewer", "rustdesk", "kyc update",
    "electricity bill", "sim block", "vip share", "trading profit",
    "crypto", "lottery", "task reward"
]

class VelocityCache:
    """Sliding-window velocity tracking for sender accounts."""
    def __init__(self):
        # sender_id -> list of (timestamp, amount)
        self._history: Dict[str, List[Tuple[datetime, float]]] = {}

    def record(self, sender_id: str, timestamp: datetime, amount: float):
        if sender_id not in self._history:
            self._history[sender_id] = []
        self._history[sender_id].append((timestamp, amount))

    def get_velocity(self, sender_id: str, current_time: datetime) -> Tuple[int, float, int]:
        """Returns (velocity_1h_count, velocity_1h_amount, velocity_24h_count)"""
        records = self._history.get(sender_id, [])
        one_hour_ago = current_time - timedelta(hours=1)
        one_day_ago = current_time - timedelta(days=1)

        v1_count = 0
        v1_amount = 0.0
        v24_count = 0

        for ts, amt in records:
            if ts >= one_hour_ago:
                v1_count += 1
                v1_amount += amt
            if ts >= one_day_ago:
                v24_count += 1

        return v1_count, v1_amount, v24_count


from backend.engine.telemetry_proxy import default_telemetry_imputer, TelemetryProxyImputer
from backend.engine.payee_memory import default_payee_memory, TrustedPayeeMemory
from backend.engine.cold_start_mule import default_cold_start_scorer, ColdStartMuleScorer
from backend.consortium.i4c_registry import default_i4c_registry, SimulatedI4CConsortiumRegistry

class FeaturePipeline:
    def __init__(
        self,
        cache: VelocityCache = None,
        telemetry_imputer: TelemetryProxyImputer = None,
        payee_memory: TrustedPayeeMemory = None,
        cold_start_scorer: ColdStartMuleScorer = None,
        consortium_registry: SimulatedI4CConsortiumRegistry = None
    ):
        self.cache = cache or VelocityCache()
        self.telemetry_imputer = telemetry_imputer or default_telemetry_imputer
        self.payee_memory = payee_memory or default_payee_memory
        self.cold_start_scorer = cold_start_scorer or default_cold_start_scorer
        self.consortium_registry = consortium_registry or default_i4c_registry

    def extract_features(self, tx: Transaction) -> FeatureVector:
        # Record into velocity cache
        self.cache.record(tx.sender_id, tx.timestamp, tx.amount)
        v1_count, v1_amount, v24_count = self.cache.get_velocity(tx.sender_id, tx.timestamp)

        # Baseline amount ratio
        avg_amt = max(tx.customer_avg_tx_amount, 100.0)
        ratio = round(tx.amount / avg_amt, 2)

        # High risk remark detection
        remark_lower = tx.remark.lower()
        has_high_risk_keyword = 1.0 if any(kw in remark_lower for kw in HIGH_RISK_KEYWORDS) else 0.0

        # Malicious APK / screen sharing
        malicious_app = 1.0 if (tx.device.accessibility_service_enabled or tx.device.remote_app_active) else 0.0

        # CON 1: Telemetry degradation & behavioral proxy
        conf, imputed_call_proxy, hesitation_flag, liquidation_flag = self.telemetry_imputer.evaluate_telemetry(tx)
        effective_call_signal = 1.0 if tx.device.is_call_active else imputed_call_proxy

        # CON 2: Trusted Payee Memory
        trust_score, _ = self.payee_memory.evaluate_payee_trust(tx)

        # CON 3: Cold-start mule detection
        cold_start_score, _ = self.cold_start_scorer.evaluate(tx)

        # CON 5: I4C / NPCI Consortium Registry
        consortium_flag = self.consortium_registry.lookup(
            receiver_vpa=tx.receiver_vpa,
            receiver_account=tx.receiver_id,
            device_id=tx.device.device_id
        )
        is_consortium_blacklisted = 1.0 if consortium_flag and consortium_flag.is_active_block else 0.0

        return FeatureVector(
            velocity_1h_count=v1_count,
            velocity_1h_amount=v1_amount,
            velocity_24h_count=v24_count,
            amount_to_avg_ratio=ratio,
            is_first_time_payee=1.0 if tx.is_first_time_payee else 0.0,
            is_call_active=effective_call_signal,
            call_duration_minutes=tx.device.call_duration_minutes,
            device_changed_recently=1.0 if tx.device.is_new_device else 0.0,
            malicious_app_flag=malicious_app,
            high_risk_remark_flag=has_high_risk_keyword,
            telemetry_confidence=conf,
            behavioral_hesitation_flag=hesitation_flag,
            savings_liquidation_flag=liquidation_flag,
            receiver_cold_start_anomaly=cold_start_score,
            trusted_payee_score=trust_score,
            consortium_blacklisted_flag=is_consortium_blacklisted
        )
