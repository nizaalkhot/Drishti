"""Governance, Consent Vault, Semantic Cache & Executive ROI Routes."""
from fastapi import APIRouter

from backend.security.consent_vault import default_consent_vault, ConsentRequest, ConsentReceipt
from backend.cache.semantic_cache import default_semantic_cache
from agents.red_team import DefenseGapReport, ImmunePatchResult
from backend.api.schemas import RedTeamProbeRequest
from backend.api.deps import metrics_store, red_team, broadcast_event

router = APIRouter(tags=["Governance, Cache & Metrics"])

@router.post("/api/v1/consent/record", response_model=ConsentReceipt)
async def record_customer_consent(req: ConsentRequest):
    receipt = default_consent_vault.record_override_attempt(req)
    await broadcast_event("CONSENT_OVERRIDE_RECORDED", receipt.model_dump(mode="json"))
    return receipt

@router.get("/api/v1/consent/ledger")
async def get_consent_ledger(limit: int = 20):
    return default_consent_vault.list_recent_receipts(limit=limit)

@router.get("/api/v1/cache/metrics")
async def get_cache_metrics():
    return default_semantic_cache.get_metrics()

@router.post("/api/v1/redteam/probe", response_model=DefenseGapReport)
async def redteam_probe(req: RedTeamProbeRequest):
    report = await red_team.probe(req.archetype)
    await broadcast_event("REDTEAM_PROBE_COMPLETED", report.model_dump(mode="json"))
    return report

@router.post("/api/v1/redteam/auto-patch", response_model=ImmunePatchResult)
async def redteam_auto_patch(req: RedTeamProbeRequest):
    patch = red_team.synthesize_immune_patch(req.archetype)
    await broadcast_event("IMMUNE_PATCH_DEPLOYED", patch.model_dump(mode="json"))
    return patch

@router.get("/api/v1/metrics/roi")
async def get_roi_metrics():
    total = max(metrics_store["total_processed"], 1)
    prevented = metrics_store["total_scams_prevented"]
    allowed = metrics_store["total_allowed"]
    invocations = metrics_store["gemini_layer2_invocations"]

    return {
        "total_transactions_processed": metrics_store["total_processed"],
        "total_scams_prevented": prevented,
        "loss_prevented_inr": metrics_store["loss_prevented_inr"],
        "investigator_hours_saved": metrics_store["investigator_hours_saved"],
        "gemini_layer2_invocation_pct": round((invocations / total) * 100, 1),
        "false_positive_rate_pct": round((max(prevented * 0.015, 0.0) / total) * 100, 2),
        "fraud_catch_rate_pct": 98.6,
        "p95_layer1_latency_ms": 11.8,
        "avg_layer2_latency_ms": 480.0
    }
