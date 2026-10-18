"""Domain Unit Tests for Client Telemetry Proxy, Behavioral Imputation, and Cold-Start Detection."""
import pytest
from backend.engine.telemetry_proxy import default_telemetry_imputer
from backend.engine.cold_start_mule import default_cold_start_scorer
from backend.engine.features import FeaturePipeline
from backend.engine.risk_scorer import TabularRiskScorer, RiskDecision
from simulator.generator import UPISimulator, ScenarioType

def test_telemetry_proxy_imputation():
    """Verify behavioral pacing detects coercion on iOS without phone call permission."""
    sim = UPISimulator()
    tx = sim.generate_scenario(ScenarioType.IOS_RESTRICTED_DIGITAL_ARREST)

    conf, imputed_call, hesitation, liquidation = default_telemetry_imputer.evaluate_telemetry(tx)
    assert conf <= 0.40  # Degraded confidence
    assert hesitation == 1.0
    assert liquidation == 1.0
    assert imputed_call >= 0.60  # Coercion imputed successfully!

def test_trusted_payee_mitigates_false_positives():
    """Verify legitimate hospital payment on active phone call is NOT blocked."""
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
    """Verify fresh student account receiving first large credit is caught."""
    sim = UPISimulator()
    tx = sim.generate_scenario(ScenarioType.FRESH_STUDENT_MULE_COLD_START)

    score, reasons = default_cold_start_scorer.evaluate(tx)
    assert score >= 0.60
    assert any("opened only 3d ago" in r for r in reasons)
    assert any("STUDENT" in r for r in reasons)
