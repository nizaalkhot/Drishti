import time
from enum import Enum
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from backend.schemas.transaction import FeatureVector

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

        # Sort by highest contribution
        contributions.sort(key=lambda x: x.contribution, reverse=True)

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
