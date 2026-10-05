import pytest
from datetime import datetime, timezone
from backend.schemas.transaction import Transaction, DeviceSignals, FeatureVector
from backend.engine.features import FeaturePipeline
from agents.scam_shield import ScamShieldOrchestrator

@pytest.mark.asyncio
async def test_scam_shield_intercepts_digital_arrest():
    orchestrator = ScamShieldOrchestrator()
    
    tx = Transaction(
        id="TXN-SCAM-001",
        timestamp=datetime.now(timezone.utc),
        sender_id="CUST-ARUN-JOSHI",
        sender_vpa="arun.joshi@okaxis",
        sender_account="112233445566",
        receiver_id="MULE-AGGREGATOR-RING-1",
        receiver_vpa="central.escrow.mule@paytm",
        receiver_ifsc="PYTM0123456",
        amount=480000.0,
        remark="CBI legal clearance security deposit",
        device=DeviceSignals(
            device_id="DEV-SHARED-MULE-PHONE-01",
            ip_address="14.139.12.5",
            is_call_active=True,
            call_duration_minutes=52.0,
            accessibility_service_enabled=False,
            remote_app_active=False
        ),
        is_first_time_payee=True,
        customer_avg_tx_amount=2500.0
    )

    pipeline = FeaturePipeline()
    features = pipeline.extract_features(tx)

    decision = await orchestrator.evaluate(tx, features)

    assert decision.is_scam_detected is True
    assert decision.scam_typology == "DIGITAL_ARREST"
    assert decision.intervention is not None
    assert decision.intervention.headline != ""
    assert "safe account" in decision.intervention.body.lower() or "cbi" in decision.intervention.body.lower() or "police" in decision.intervention.body.lower()
    assert decision.latency_ms <= 3500.0 # Under 3.5s budget
    assert decision.policy_citation != ""
