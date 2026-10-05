import pytest
from datetime import datetime, timezone
from backend.schemas.transaction import Transaction, DeviceSignals
from backend.engine.telemetry_proxy import default_telemetry_imputer
from backend.engine.payee_memory import default_payee_memory, FrictionTier
from backend.engine.cold_start_mule import default_cold_start_scorer
from backend.consortium.i4c_registry import default_i4c_registry
from backend.cache.semantic_cache import default_semantic_cache
from backend.security.consent_vault import default_consent_vault, ConsentRequest
from backend.engine.features import FeaturePipeline
from backend.engine.risk_scorer import TabularRiskScorer, RiskDecision
from simulator.generator import UPISimulator, ScenarioType

def test_telemetry_proxy_imputation():
    """CON 1: Verify behavioral pacing detects coercion on iOS without phone call permission."""
    sim = UPISimulator()
    tx = sim.generate_scenario(ScenarioType.IOS_RESTRICTED_DIGITAL_ARREST)
    
    conf, imputed_call, hesitation, liquidation = default_telemetry_imputer.evaluate_telemetry(tx)
    assert conf <= 0.40  # Degraded confidence
    assert hesitation == 1.0
    assert liquidation == 1.0
    assert imputed_call >= 0.60  # Coercion imputed successfully!

def test_trusted_payee_mitigates_false_positives():
    """CON 2: Verify legitimate hospital payment on active phone call is NOT blocked."""
    sim = UPISimulator()
    tx = sim.generate_scenario(ScenarioType.LEGITIMATE_HOSPITAL_EMERGENCY)
    
    pipeline = FeaturePipeline()
    features = pipeline.extract_features(tx)
    assert features.trusted_payee_score >= 0.70
    
    scorer = TabularRiskScorer()
    res = scorer.score(features)
    # Must be allowed without intrusive blocking!
    assert res.decision == RiskDecision.ALLOW
    assert res.score < 0.35

def test_cold_start_fresh_student_mule():
    """CON 3: Verify fresh student account receiving first large credit is caught."""
    sim = UPISimulator()
    tx = sim.generate_scenario(ScenarioType.FRESH_STUDENT_MULE_COLD_START)
    
    score, reasons = default_cold_start_scorer.evaluate(tx)
    assert score >= 0.60
    assert any("opened only 3d ago" in r for r in reasons)
    assert any("STUDENT" in r for r in reasons)

def test_i4c_consortium_cross_bank_match():
    """CON 5: Verify multi-bank syndicate mule is flagged via salted hash lookup."""
    match = default_i4c_registry.lookup(receiver_vpa="sbi.safety.officer@ybl")
    assert match is not None
    assert match.is_active_block is True
    assert match.reporting_banks_count >= 2
    assert "NCRP" in match.ncrp_reference

def test_semantic_cache_zero_token_intervention():
    """CON 6: Verify repeated scam narrative hits cache in <2ms with zero token cost."""
    cached_dialog, latency_ms = default_semantic_cache.lookup("DIGITAL_ARREST", "en")
    assert cached_dialog is not None
    assert latency_ms <= 2
    assert "URGENT FRAUD ALERT" in cached_dialog.headline
    
    metrics = default_semantic_cache.get_metrics()
    assert metrics["total_hits"] >= 1
    assert metrics["total_tokens_saved"] >= 450

def test_informed_consent_hard_block_on_high_confidence():
    """CON 4: Verify scam score > 0.85 enforces HARD BLOCK and rejects customer override."""
    req = ConsentRequest(
        transaction_id="tx_high_coercion_99",
        customer_id="cust_victim_01",
        scam_score=0.94,
        scam_typology="DIGITAL_ARREST",
        confirmed_no_coercion=True,
        biometric_auth_token="BIOMETRIC_TOKEN_OK"
    )
    receipt = default_consent_vault.record_override_attempt(req)
    assert receipt.can_proceed is False
    assert receipt.status == "REJECTED_HARD_BLOCK"
    assert "exceeds bank safety threshold" in receipt.reason

def test_informed_consent_permits_override_on_medium_confidence():
    """CON 4: Verify customer override is logged in tamper-evident ledger when score <= 0.85."""
    req = ConsentRequest(
        transaction_id="tx_medium_risk_50",
        customer_id="cust_user_44",
        scam_score=0.72,
        scam_typology="SUSPICIOUS_HIGH_VALUE_FIRST_TIME",
        confirmed_no_coercion=True,
        biometric_auth_token="BIOMETRIC_TOKEN_OK"
    )
    receipt = default_consent_vault.record_override_attempt(req)
    assert receipt.can_proceed is True
    assert receipt.status == "ACCEPTED_OVERRIDE"
    assert receipt.chain_hash is not None
