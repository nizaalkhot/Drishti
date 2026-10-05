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


class FeaturePipeline:
    def __init__(self, cache: VelocityCache = None):
        self.cache = cache or VelocityCache()

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

        return FeatureVector(
            velocity_1h_count=v1_count,
            velocity_1h_amount=v1_amount,
            velocity_24h_count=v24_count,
            amount_to_avg_ratio=ratio,
            is_first_time_payee=1.0 if tx.is_first_time_payee else 0.0,
            is_call_active=1.0 if tx.device.is_call_active else 0.0,
            call_duration_minutes=tx.device.call_duration_minutes,
            device_changed_recently=1.0 if tx.device.is_new_device else 0.0,
            malicious_app_flag=malicious_app,
            high_risk_remark_flag=has_high_risk_keyword
        )
