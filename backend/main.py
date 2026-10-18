"""
Drishti: Agentic Scam & Fraud Intelligence Engine
Main Application Entrypoint.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from simulator.generator import ScenarioType
from backend.api.deps import (
    simulator,
    feature_pipeline,
    risk_scorer,
    scam_shield,
    copilot,
    metrics_store,
)
from backend.api import (
    scoring_router,
    cases_router,
    consortium_router,
    governance_router,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Pre-seed default scenarios on startup for immediate live demo state."""
    normal_tx = simulator.generate_scenario(ScenarioType.LEGITIMATE)
    feat_norm = feature_pipeline.extract_features(normal_tx)
    risk_scorer.score(feat_norm)
    metrics_store["total_processed"] += 1
    metrics_store["total_allowed"] += 1

    scam_tx = simulator.generate_scenario(ScenarioType.DIGITAL_ARREST)
    feat_scam = feature_pipeline.extract_features(scam_tx)
    risk_scam = risk_scorer.score(feat_scam)
    scam_dec = await scam_shield.evaluate(scam_tx, feat_scam)
    case = copilot.create_case(scam_tx, feat_scam, risk_scam, scam_dec)
    copilot.draft_str(case.case_id)
    metrics_store["total_processed"] += 1
    metrics_store["total_scams_prevented"] += 1
    metrics_store["loss_prevented_inr"] += scam_tx.amount
    metrics_store["investigator_hours_saved"] += 2.5
    metrics_store["gemini_layer2_invocations"] += 1
    yield

app = FastAPI(
    title="Drishti: Agentic Scam & Fraud Intelligence",
    version="1.0.0",
    description="APP Fraud Prevention & Autonomous Investigator Copilot",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Modular API Routers
app.include_router(scoring_router)
app.include_router(cases_router)
app.include_router(consortium_router)
app.include_router(governance_router)

@app.get("/api/v1/health")
@app.get("/health")
async def health_check():
    """Service health and environment metadata."""
    return {
        "status": "HEALTHY",
        "service": "drishti-core",
        "gcp_project": "team-gain",
        "region": "asia-south1",
        "version": "1.0.0"
    }

import os
from fastapi import HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Serve built frontend Single Page App if present (e.g. in container or built dist)
DIST_DIR = os.getenv("DRISHTI_STATIC_DIR", os.path.join(os.path.dirname(os.path.dirname(__file__)), "web", "dist"))

if os.path.exists(DIST_DIR):
    assets_dir = os.path.join(DIST_DIR, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="static-assets")

    @app.get("/{full_path:path}", include_in_schema=False)
    async def serve_spa(full_path: str):
        if full_path.startswith(("api/", "health", "docs", "redoc", "openapi.json")):
            raise HTTPException(status_code=404, detail="Not Found")
        target_file = os.path.join(DIST_DIR, full_path)
        if full_path and os.path.isfile(target_file):
            return FileResponse(target_file)
        index_file = os.path.join(DIST_DIR, "index.html")
        if os.path.exists(index_file):
            return FileResponse(index_file)
        raise HTTPException(status_code=404, detail="Frontend index.html not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
