"""API Request and Response Models for Drishti."""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from simulator.generator import ScenarioType
from agents.red_team import AttackArchetype

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

class FreezeRequest(BaseModel):
    reason: str = "Suspected Mule Aggregator Ring"

class SignSTRRequest(BaseModel):
    officer_name: str = "Authorized AML Officer"

class DismissRequest(BaseModel):
    analyst_notes: str = "Verified genuine customer transaction"

class RedTeamProbeRequest(BaseModel):
    archetype: AttackArchetype
