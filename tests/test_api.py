import pytest
from httpx import AsyncClient, ASGITransport
from backend.main import app

@pytest.mark.asyncio
async def test_health_check():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/v1/health")
        assert response.status_code == 200
        assert response.json()["status"] == "HEALTHY"

@pytest.mark.asyncio
async def test_simulate_digital_arrest_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        payload = {"scenario": "DIGITAL_ARREST"}
        response = await ac.post("/api/v1/simulator/inject", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["decision"] == "INTERVENE"
        assert data["intervention"] is not None
        assert data["case_id"] is not None

@pytest.mark.asyncio
async def test_simulate_legitimate_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        payload = {"scenario": "LEGITIMATE"}
        response = await ac.post("/api/v1/simulator/inject", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["decision"] == "ALLOW"
        assert data["intervention"] is None

@pytest.mark.asyncio
async def test_case_actions_and_roi():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # First inject a scam to create a case
        inj_resp = await ac.post("/api/v1/simulator/inject", json={"scenario": "DIGITAL_ARREST"})
        case_id = inj_resp.json()["case_id"]
        assert case_id is not None

        # Freeze account
        freeze_resp = await ac.post(f"/api/v1/cases/{case_id}/freeze", json={"reason": "Mule cluster confirmed"})
        assert freeze_resp.status_code == 200
        assert freeze_resp.json()["status"] == "ACCOUNT_FROZEN"

        # Export STR
        str_resp = await ac.post(f"/api/v1/cases/{case_id}/export-str", json={"officer_name": "Compliance Head Desai"})
        assert str_resp.status_code == 200
        assert "APPROVED" in str_resp.json()["human_sign_off_status"]

        # ROI Metrics
        roi_resp = await ac.get("/api/v1/metrics/roi")
        assert roi_resp.status_code == 200
        assert roi_resp.json()["loss_prevented_inr"] > 0
