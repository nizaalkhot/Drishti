import pytest
from backend.schemas.transaction import FeatureVector
from backend.engine.risk_scorer import TabularRiskScorer, RiskDecision

def test_legitimate_transaction_is_allowed():
    scorer = TabularRiskScorer()
    features = FeatureVector(
        velocity_1h_count=1,
        velocity_1h_amount=500.0,
        amount_to_avg_ratio=0.5,
        is_first_time_payee=0.0,
        is_call_active=0.0,
        call_duration_minutes=0.0,
        device_changed_recently=0.0,
        malicious_app_flag=0.0,
        high_risk_remark_flag=0.0
    )
    result = scorer.score(features)
    assert result.score < 0.35
    assert result.decision == RiskDecision.ALLOW
    assert result.latency_ms < 15.0

def test_digital_arrest_features_fall_in_grey_zone():
    scorer = TabularRiskScorer()
    features = FeatureVector(
        velocity_1h_count=1,
        velocity_1h_amount=250000.0,
        amount_to_avg_ratio=120.0,
        is_first_time_payee=1.0,
        is_call_active=1.0,
        call_duration_minutes=45.0,
        device_changed_recently=0.0,
        malicious_app_flag=0.0,
        high_risk_remark_flag=1.0
    )
    result = scorer.score(features)
    assert 0.35 <= result.score <= 0.75
    assert result.decision == RiskDecision.GREY_ZONE_SCAM_SHIELD
    assert len(result.top_contributing_features) > 0

def test_critical_risk_is_held():
    scorer = TabularRiskScorer()
    features = FeatureVector(
        velocity_1h_count=8,
        velocity_1h_amount=800000.0,
        amount_to_avg_ratio=400.0,
        is_first_time_payee=1.0,
        is_call_active=1.0,
        call_duration_minutes=65.0,
        device_changed_recently=1.0,
        malicious_app_flag=1.0,
        high_risk_remark_flag=1.0
    )
    result = scorer.score(features)
    assert result.score > 0.75
    assert result.decision == RiskDecision.HOLD

def test_semantic_intervention_cache_sub_millisecond_lookup():
    """Verify intervention copy cache returns in <2ms with zero token cost."""
    from backend.cache.intervention_cache import default_intervention_cache
    hit = default_intervention_cache.lookup("DIGITAL_ARREST", "en")
    assert hit is not None
    dialog, latency = hit
    assert "Digital Arrest" in dialog.headline or "FRAUD ALERT" in dialog.headline
    assert latency < 2

def test_two_tier_fast_fallback_under_5ms():
    """Verify fast fallback provides sub-5ms deterministic friction without LLM latency."""
    from datetime import datetime, timezone
    from backend.schemas import Transaction, DeviceSignals
    from agents.scam_shield import ScamShieldOrchestrator

    orchestrator = ScamShieldOrchestrator()
    tx = Transaction(
        id="TXN-TT-TEST",
        timestamp=datetime.now(timezone.utc),
        sender_id="CUST-TT",
        sender_vpa="sender@upi",
        sender_account="12345",
        receiver_id="MULE-TT",
        receiver_vpa="mule@upi",
        receiver_ifsc="HDFC0001234",
        amount=100000.0,
        remark="Police fine",
        device=DeviceSignals(
            device_id="DEV-TT",
            ip_address="127.0.0.1",
            is_call_active=True,
            call_duration_minutes=40.0
        )
    )
    features = FeatureVector(is_call_active=1.0)
    decision = orchestrator.generate_fast_fallback_decision(tx, features)
    assert decision.is_scam_detected is True
    assert decision.fallback_applied is True
    assert decision.latency_ms <= 5.0
