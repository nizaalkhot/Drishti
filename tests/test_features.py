from datetime import datetime, timezone
import pytest
from backend.schemas.transaction import Transaction, DeviceSignals
from backend.engine.features import FeaturePipeline, VelocityCache

def test_feature_pipeline_calculates_correct_flags():
    cache = VelocityCache()
    pipeline = FeaturePipeline(cache=cache)

    tx = Transaction(
        id="TXN-TEST-001",
        timestamp=datetime.now(timezone.utc),
        sender_id="CUST-1001",
        sender_vpa="user1@okicici",
        sender_account="112233445566",
        receiver_id="BENEF-9999",
        receiver_vpa="suspect@paytm",
        receiver_ifsc="PYTM0123456",
        amount=250000.0,
        remark="RBI verification bond for court case",
        device=DeviceSignals(
            device_id="DEV-NEW-888",
            ip_address="192.168.1.10",
            is_call_active=True,
            call_duration_minutes=48.5,
            accessibility_service_enabled=False,
            remote_app_active=False
        ),
        is_first_time_payee=True,
        customer_avg_tx_amount=1500.0
    )

    features = pipeline.extract_features(tx)
    
    assert features.is_first_time_payee == 1.0
    assert features.is_call_active == 1.0
    assert features.call_duration_minutes == 48.5
    assert features.high_risk_remark_flag == 1.0
    assert features.amount_to_avg_ratio > 100.0
    assert features.velocity_1h_count == 1
    assert features.velocity_1h_amount == 250000.0
