"""Scoring, Simulation, and SSE Streaming API Routes."""
import time
import json
import asyncio
from typing import List
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from backend.schemas.transaction import Transaction
from backend.engine.risk_scorer import RiskDecision
from agents.scam_shield import ScamShieldDecision
from backend.api.schemas import ScoringResponse, ScenarioInjectRequest
from backend.api.deps import (
    feature_pipeline,
    risk_scorer,
    scam_shield,
    copilot,
    simulator,
    metrics_store,
    sse_clients,
    broadcast_event,
    pubsub_service,
    bq_export,
    recent_transactions,
)

router = APIRouter(tags=["Scoring & Simulation"])

@router.post("/api/v1/score", response_model=ScoringResponse)
async def score_transaction(tx: Transaction, language: str = "en"):
    start_total = time.perf_counter()
    metrics_store["total_processed"] += 1

    # 1. Feature Extraction
    features = feature_pipeline.extract_features(tx)

    # 2. Layer 1: Tabular Scorer (<15ms)
    l1_result = risk_scorer.score(features)
    l1_latency = l1_result.latency_ms

    decision_str = "ALLOW"
    intervention_data = None
    policy_citation = None
    mule_data = None
    case_id = None

    friction_tier = "TIER_0_SILENT"
    semantic_cache_hit = False
    tokens_saved = 0
    consortium_ref = None
    cold_start_inds = []
    can_override = True

    # 3. Layer 2: Scam Shield (Grey Zone: 0.35 - 0.75)
    if l1_result.decision == RiskDecision.GREY_ZONE_SCAM_SHIELD:
        metrics_store["gemini_layer2_invocations"] += 1
        scam_decision = await scam_shield.evaluate(tx, features, language=language)
        friction_tier = scam_decision.friction_tier
        semantic_cache_hit = scam_decision.semantic_cache_hit
        tokens_saved = scam_decision.tokens_saved
        consortium_ref = scam_decision.consortium_reference or None
        cold_start_inds = scam_decision.cold_start_indicators
        can_override = (friction_tier != "HARD_BLOCK" and scam_decision.confidence_score <= 0.85)

        if scam_decision.is_scam_detected:
            decision_str = "INTERVENE"
            intervention_data = scam_decision.intervention.model_dump() if scam_decision.intervention else None
            policy_citation = scam_decision.policy_citation
            mule_data = scam_decision.mule_graph_analysis.model_dump() if scam_decision.mule_graph_analysis else None

            # Create case in Layer 3 Investigator Copilot
            case = copilot.create_case(tx, features, l1_result, scam_decision)
            case_id = case.case_id
            copilot.draft_str(case_id)

            metrics_store["total_scams_prevented"] += 1
            metrics_store["loss_prevented_inr"] += tx.amount
            metrics_store["investigator_hours_saved"] += 2.5
        else:
            decision_str = "ALLOW"
            metrics_store["total_allowed"] += 1

    elif l1_result.decision == RiskDecision.HOLD:
        decision_str = "HOLD"
        friction_tier = "HARD_BLOCK"
        can_override = False
        metrics_store["total_scams_prevented"] += 1
        metrics_store["loss_prevented_inr"] += tx.amount
        # Direct hold creates immediate high-priority case
        dummy_scam = ScamShieldDecision(
            is_scam_detected=True,
            scam_typology="CRITICAL_VELOCITY_OR_APK_HOLD",
            confidence_score=0.98,
            reasoning_summary="Layer 1 critical risk score exceeded 0.75 threshold.",
            friction_tier="HARD_BLOCK"
        )
        case = copilot.create_case(tx, features, l1_result, dummy_scam)
        case_id = case.case_id
        copilot.draft_str(case_id)
    else:
        decision_str = "ALLOW"
        metrics_store["total_allowed"] += 1

    total_latency = round((time.perf_counter() - start_total) * 1000, 2)

    response = ScoringResponse(
        transaction_id=tx.id,
        amount=tx.amount,
        sender_vpa=tx.sender_vpa,
        receiver_vpa=tx.receiver_vpa,
        remark=tx.remark,
        risk_score=l1_result.score,
        decision=decision_str,
        layer1_latency_ms=l1_latency,
        total_latency_ms=total_latency,
        intervention=intervention_data,
        policy_citation=policy_citation,
        mule_graph_analysis=mule_data,
        case_id=case_id,
        friction_tier=friction_tier,
        semantic_cache_hit=semantic_cache_hit,
        tokens_saved=tokens_saved,
        consortium_reference=consortium_ref,
        cold_start_indicators=cold_start_inds,
        can_override=can_override,
        telemetry_confidence=features.telemetry_confidence,
        telemetry={
            "is_call_active": tx.device.is_call_active,
            "call_duration_minutes": tx.device.call_duration_minutes,
            "accessibility_service_enabled": tx.device.accessibility_service_enabled,
            "remote_app_active": tx.device.remote_app_active,
            "telemetry_source": tx.device.telemetry_source,
            "telemetry_confidence": features.telemetry_confidence,
            "top_features": [f.model_dump() for f in l1_result.top_contributing_features]
        }
    )

    resp_dict = response.model_dump()

    # Update in-memory ring buffer (idempotent deduplication by transaction_id, max 50 items)
    existing_idx = next((i for i, item in enumerate(recent_transactions) if item.get("transaction_id") == response.transaction_id), None)
    if existing_idx is not None:
        recent_transactions[existing_idx] = resp_dict
    else:
        recent_transactions.insert(0, resp_dict)
        if len(recent_transactions) > 50:
            recent_transactions.pop()

    # Broadcast event to SSE clients
    asyncio.create_task(broadcast_event("TRANSACTION_SCORED", resp_dict))

    # Enterprise event publishing to Google Cloud Pub/Sub & BigQuery streaming
    try:
        pubsub_service.publish_transaction_scored(resp_dict)
        bq_export.export_transaction_risk(resp_dict)
        if decision_str in ("INTERVENE", "HOLD"):
            pubsub_service.publish_fraud_alert({
                "txn_id": tx.id,
                "amount": tx.amount,
                "decision": decision_str,
                "risk_score": l1_result.score,
                "case_id": case_id,
                "friction_tier": friction_tier
            })
    except Exception:
        pass

    return response

@router.get("/api/v1/transactions/recent", response_model=List[ScoringResponse])
async def get_recent_transactions():
    """Retrieve recent transactions from the ring buffer for real-time stream hydration."""
    return recent_transactions

@router.post("/api/v1/simulator/inject", response_model=ScoringResponse)
async def inject_scenario(req: ScenarioInjectRequest):
    tx = simulator.generate_scenario(req.scenario)
    return await score_transaction(tx, language=req.language)

@router.get("/api/v1/stream")
async def sse_stream(request: Request):
    queue = asyncio.Queue()
    sse_clients.append(queue)

    async def event_generator():
        try:
            init_data = json.dumps({"type": "CONNECTED", "data": {"message": "Drishti Real-Time Stream Active"}})
            yield f"data: {init_data}\n\n"
            while True:
                if await request.is_disconnected():
                    break
                data = await queue.get()
                yield f"data: {data}\n\n"
        except asyncio.CancelledError:
            pass
        finally:
            if queue in sse_clients:
                sse_clients.remove(queue)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )
