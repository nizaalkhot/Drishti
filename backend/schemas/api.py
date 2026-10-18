"""API Request and Response Data Transfer Models for Drishti.

Consolidated under backend/schemas/ to prevent schema fragmentation and circular imports.
"""
from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class ScenarioType(str, Enum):
    DIGITAL_ARREST = "DIGITAL_ARREST"
    KYC_APK_TAKEOVER = "KYC_APK_TAKEOVER"
    MULE_AGGREGATOR_FAN_IN = "MULE_AGGREGATOR_FAN_IN"
    HIGH_YIELD_INVESTMENT = "HIGH_YIELD_INVESTMENT"
    LEGITIMATE = "LEGITIMATE"
    # Emerging & Boundary Test Scenarios
    LEGITIMATE_HOSPITAL_EMERGENCY = "LEGITIMATE_HOSPITAL_EMERGENCY"
    IOS_RESTRICTED_DIGITAL_ARREST = "IOS_RESTRICTED_DIGITAL_ARREST"
    FRESH_STUDENT_MULE_COLD_START = "FRESH_STUDENT_MULE_COLD_START"
    I4C_CONSORTIUM_SYNDICATE = "I4C_CONSORTIUM_SYNDICATE"
    OVERRIDE_ATTEMPT_HIGH_COERCION = "OVERRIDE_ATTEMPT_HIGH_COERCION"

class AttackArchetype(str, Enum):
    OBFUSCATED_REMARK = "OBFUSCATED_REMARK"
    STRUCTURED_SMURFING = "STRUCTURED_SMURFING"
    DEEPFAKE_AUTHORITY = "DEEPFAKE_AUTHORITY"

class ScenarioInjectRequest(BaseModel):
    scenario: ScenarioType
    language: str = "en"

class ScoringResponse(BaseModel):
    transaction_id: str
    amount: float
    sender_vpa: str
    receiver_vpa: str
    remark: str
    risk_score: float
    decision: str  # ALLOW | INTERVENE | HOLD
    layer1_latency_ms: float
    total_latency_ms: float
    intervention: Optional[Dict[str, Any]] = None
    policy_citation: Optional[str] = None
    mule_graph_analysis: Optional[Dict[str, Any]] = None
    case_id: Optional[str] = None
    telemetry: Dict[str, Any]
    friction_tier: str = "TIER_0_SILENT"
    semantic_cache_hit: bool = False
    tokens_saved: int = 0
    consortium_reference: Optional[str] = None
    cold_start_indicators: List[str] = Field(default_factory=list)
    can_override: bool = True
    telemetry_confidence: float = 1.0
    is_synthetic: bool = False

class FreezeRequest(BaseModel):
    reason: str = "Suspected Mule Aggregator Ring"

class SignSTRRequest(BaseModel):
    officer_name: str = "Authorized AML Officer"

class DismissRequest(BaseModel):
    analyst_notes: str = "Verified genuine customer transaction"

class RedTeamProbeRequest(BaseModel):
    archetype: AttackArchetype
