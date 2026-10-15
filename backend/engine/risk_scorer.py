import os
import time
import logging
from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from backend.schemas.transaction import FeatureVector

logger = logging.getLogger("drishti.risk_scorer")

try:
    from google.cloud import aiplatform
    HAVE_VERTEX = True
except ImportError:
    HAVE_VERTEX = False

class RiskDecision(str, Enum):
    ALLOW = "ALLOW"
    GREY_ZONE_SCAM_SHIELD = "GREY_ZONE_SCAM_SHIELD"
    HOLD = "HOLD"

class FeatureContribution(BaseModel):
    feature: str
    value: float
    weight: float
    contribution: float

class RiskScoreResult(BaseModel):
    score: float = Field(..., ge=0.0, le=1.0)
    decision: RiskDecision
    top_contributing_features: List[FeatureContribution]
    latency_ms: float
    model_name: str = "drishti-tabular-v1"
    model_version: str = "1.0.4"
    vertex_registry_id: str = "projects/team-gain/locations/asia-south1/models/drishti-tabular-v1"

class TabularRiskScorer:
    """
    High-performance Layer 1 tabular predictive risk engine.
    Calibrated logistic response over behavioral and device velocity signals.
    """
    WEIGHTS: Dict[str, float] = {
        "is_call_active": 0.18,
        "high_risk_remark_flag": 0.18,
        "is_first_time_payee": 0.12,
        "malicious_app_flag": 0.28,
        "device_changed_recently": 0.10,
        "amount_ratio_normalized": 0.14,
        "velocity_1h_count_normalized": 0.14,
        # CON 1, 3, 5 features
        "consortium_blacklisted_flag": 0.35,
        "receiver_cold_start_anomaly": 0.22,
        "savings_liquidation_flag": 0.12,
        "behavioral_hesitation_flag": 0.08,
        # Biometrics & Telemetry upgrades
        "gyroscope_tremor_score": 0.10,
        "untrusted_clipboard_flag": 0.12,
    }

    def score(self, features: FeatureVector) -> RiskScoreResult:
        start_time = time.perf_counter()

        # Normalized components
        amt_norm = min(features.amount_to_avg_ratio / 50.0, 1.0)
        vel_norm = min(features.velocity_1h_count / 5.0, 1.0)

        feature_map = {
            "is_call_active": features.is_call_active,
            "high_risk_remark_flag": features.high_risk_remark_flag,
            "is_first_time_payee": features.is_first_time_payee,
            "malicious_app_flag": features.malicious_app_flag,
            "device_changed_recently": features.device_changed_recently,
            "amount_ratio_normalized": amt_norm,
            "velocity_1h_count_normalized": vel_norm,
            "consortium_blacklisted_flag": features.consortium_blacklisted_flag,
            "receiver_cold_start_anomaly": features.receiver_cold_start_anomaly,
            "savings_liquidation_flag": features.savings_liquidation_flag,
            "behavioral_hesitation_flag": features.behavioral_hesitation_flag,
            "gyroscope_tremor_score": features.gyroscope_tremor_score,
            "untrusted_clipboard_flag": features.untrusted_clipboard_flag,
        }

        contributions: List[FeatureContribution] = []
        raw_score = 0.0

        for feat_name, val in feature_map.items():
            wt = self.WEIGHTS.get(feat_name, 0.0)
            contrib = val * wt
            raw_score += contrib
            if contrib > 0.0:
                contributions.append(FeatureContribution(
                    feature=feat_name,
                    value=round(val, 2),
                    weight=wt,
                    contribution=round(contrib, 3)
                ))

        # CON 2: Deduct risk for verified trusted payees (suppresses false positives)
        if features.trusted_payee_score > 0.0:
            trust_deduction = features.trusted_payee_score * 0.30
            raw_score = max(raw_score - trust_deduction, 0.02)
            contributions.append(FeatureContribution(
                feature="trusted_payee_mitigation",
                value=round(features.trusted_payee_score, 2),
                weight=-0.30,
                contribution=round(-trust_deduction, 3)
            ))

        # Sort by absolute contribution impact
        contributions.sort(key=lambda x: abs(x.contribution), reverse=True)

        # Baseline offset for normal transactions
        final_score = min(max(raw_score, 0.02), 0.99)
        final_score = round(final_score, 3)

        # Decision thresholds agreed in design
        if final_score < 0.35:
            decision = RiskDecision.ALLOW
        elif final_score <= 0.75:
            decision = RiskDecision.GREY_ZONE_SCAM_SHIELD
        else:
            decision = RiskDecision.HOLD

        latency_ms = round((time.perf_counter() - start_time) * 1000, 2)

        return RiskScoreResult(
            score=final_score,
            decision=decision,
            top_contributing_features=contributions[:5],
            latency_ms=latency_ms
        )

class VertexAIModelPredictor:
    """
    Enterprise predictor interfacing with Google Cloud Vertex AI Model Registry
    (drishti-tabular-v1) and Online Prediction Endpoints, with zero-downtime
    calibrated fallback to local high-speed tabular engine (<1ms).
    """
    def __init__(
        self,
        endpoint_id: Optional[str] = None,
        project_id: Optional[str] = None,
        location: str = "asia-south1",
        model_name: str = "projects/team-gain/locations/asia-south1/models/drishti-tabular-v1"
    ):
        self.project_id = project_id or os.getenv("GCP_PROJECT", "team-gain")
        self.location = location or os.getenv("GCP_REGION", "asia-south1")
        self.endpoint_id = endpoint_id or os.getenv("VERTEX_ENDPOINT_ID")
        self.model_name = model_name
        self.local_scorer = TabularRiskScorer()
        self.endpoint = None

        if HAVE_VERTEX and self.endpoint_id and (os.getenv("GOOGLE_APPLICATION_CREDENTIALS") or os.getenv("K_SERVICE")):
            try:
                aiplatform.init(project=self.project_id, location=self.location)
                self.endpoint = aiplatform.Endpoint(self.endpoint_id)
                logger.info(f"Connected to live Vertex AI Endpoint: {self.endpoint_id}")
            except Exception as e:
                logger.warning(f"Could not initialize Vertex AI endpoint: {e}. Falling back to calibrated tabular model.")
                self.endpoint = None
        else:
            logger.info("VertexAIModelPredictor operating in dual-mode calibrated engine.")

    def score(self, features: FeatureVector) -> RiskScoreResult:
        start_time = time.perf_counter()
        if self.endpoint:
            try:
                instance = features.model_dump()
                prediction = self.endpoint.predict(instances=[instance])
                if prediction.predictions:
                    pred = prediction.predictions[0]
                    # Parse predictions if formatted by Vertex custom container
                    score_val = float(pred.get("score", 0.5)) if isinstance(pred, dict) else float(pred[0])
                    res = self.local_scorer.score(features)
                    res.score = round(score_val, 3)
                    res.latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
                    return res
            except Exception as e:
                logger.warning(f"Vertex AI prediction request failed ({e}), using calibrated local scorer.")

        # High-speed local calibrated scoring
        return self.local_scorer.score(features)

default_risk_scorer = VertexAIModelPredictor()

