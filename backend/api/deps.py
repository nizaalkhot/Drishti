"""Shared Singletons and Dependencies for Drishti API."""
import time
import json
import asyncio
from typing import Dict, Any, List

from backend.engine.features import FeaturePipeline, VelocityCache
from backend.engine.risk_scorer import default_risk_scorer, TabularRiskScorer, VertexAIModelPredictor
from agents.scam_shield import ScamShieldOrchestrator
from agents.copilot import InvestigatorCopilot
from agents.red_team import RedTeamAgent
from simulator.generator import UPISimulator
from backend.integrations.pubsub import default_pubsub_service
from backend.integrations.bigquery_export import default_bq_export
from backend.integrations.document_ai import default_document_ai

# Service Singletons
velocity_cache = VelocityCache()
feature_pipeline = FeaturePipeline(cache=velocity_cache)
risk_scorer = default_risk_scorer
scam_shield = ScamShieldOrchestrator()
copilot = InvestigatorCopilot()
red_team = RedTeamAgent(feature_pipeline, risk_scorer, scam_shield)
simulator = UPISimulator()
pubsub_service = default_pubsub_service
bq_export = default_bq_export
document_ai = default_document_ai

# SSE Event Subscribers
sse_clients: List[asyncio.Queue] = []

async def broadcast_event(event_type: str, data: Dict[str, Any]):
    """Broadcast real-time JSON events to active SSE client queues."""
    dead_queues = []
    payload = json.dumps({"type": event_type, "data": data, "timestamp": time.time()}, default=str)
    for q in sse_clients:
        try:
            await q.put(payload)
        except Exception:
            dead_queues.append(q)
    for dq in dead_queues:
        if dq in sse_clients:
            sse_clients.remove(dq)

# Executive Metrics Store
metrics_store: Dict[str, Any] = {
    "total_processed": 0,
    "total_allowed": 0,
    "total_scams_prevented": 0,
    "loss_prevented_inr": 0.0,
    "investigator_hours_saved": 0.0,
    "gemini_layer2_invocations": 0
}
