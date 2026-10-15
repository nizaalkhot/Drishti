"""
Tests for Drishti 2.0 Institutional Upgrade Features:
- Behavioral Biometrics & Telco Telemetry (Tremor & Clipboard)
- Autonomous Closed-Loop Immune System (Auto-patching & Cache Hot-Reload)
- Deep Multi-Hop Mule Ring Analytics
- FIU-IND FINnet 2.0 XML Generation
- ISO 20022 camt.056 Payment Cancellation Recall
"""
import pytest
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from fastapi.testclient import TestClient

from backend.main import app
from backend.schemas.transaction import Transaction, DeviceSignals
from backend.engine.features import FeaturePipeline
from backend.engine.risk_scorer import TabularRiskScorer
from agents.red_team import RedTeamAgent, AttackArchetype
from agents.tools.mule_graph import MuleGraphService
from backend.compliance.finnet_generator import generate_finnet2_xml
from backend.compliance.iso20022 import generate_camt056_recall
from backend.cache.semantic_cache import default_semantic_cache

client = TestClient(app)

def test_biometrics_feature_extraction_and_scoring():
    """Verify that tremor biometrics and untrusted clipboard sources are extracted and scored."""
    pipeline = FeaturePipeline()
    scorer = TabularRiskScorer()

    tx = Transaction(
        id="TX-BIO-01",
        sender_id="CUST-BIO-1",
        sender_vpa="victim.tremor@okaxis",
        sender_account="1234567890",
        receiver_id="MULE-BIO-1",
        receiver_vpa="mule.bio@paytm",
        receiver_ifsc="PYTM0123456",
        amount=150000.0,
        remark="CBI safe verification holding",
        device=DeviceSignals(
            device_id="DEV-BIO-01",
            is_call_active=True,
            call_duration_minutes=30.0,
            gyroscope_tremor_score=0.88,
            clipboard_source_app="telegram"
        ),
        is_first_time_payee=True
    )

    features = pipeline.extract_features(tx)
    assert features.gyroscope_tremor_score == 0.88
    assert features.untrusted_clipboard_flag == 1.0

    res = scorer.score(features)
    assert res.score >= 0.50
    contributing_feats = [f.feature for f in res.top_contributing_features]
    assert any("tremor" in f or "clipboard" in f or "remark" in f for f in contributing_feats)

def test_closed_loop_immune_patch_synthesis():
    """Verify that Red Team generates and injects an immune patch into Semantic Cache."""
    red_team = RedTeamAgent()
    patch = red_team.synthesize_immune_patch(AttackArchetype.OBFUSCATED_REMARK)

    assert patch.status == "IMMUNIZED"
    assert "OBFUSCATED_LEETSPEAK_REMARK:en" in patch.semantic_clusters_seeded
    assert len(patch.audit_hash) == 64  # SHA-256

    # Verify cache now serves the synthesized cluster in <2ms with 0 tokens
    cached_dialog, latency = default_semantic_cache.lookup("OBFUSCATED_LEETSPEAK_REMARK", "en")
    assert cached_dialog is not None
    assert "Obfuscated" in cached_dialog.headline
    assert latency <= 2

def test_multi_hop_mule_ring_analysis():
    """Verify that MuleGraphService resolves multi-hop depth and smurfing properties."""
    mule_service = MuleGraphService()
    mule_service.seed_test_cluster("MULE-ROOT-01", "DEV-SHARED-X", ["VICTIM-A", "VICTIM-B", "VICTIM-C"])
    analysis = mule_service.analyze_beneficiary("MULE-ROOT-01", device_id="DEV-SHARED-X")

    assert analysis.fan_in_count_24h == 3
    assert analysis.rapid_passthrough_detected is True
    assert analysis.max_hop_depth >= 3
    assert analysis.smurfing_splits_count >= 1
    assert len(analysis.terminal_sinks) >= 1

def test_finnet2_xml_generation():
    """Verify that FIU-IND FINnet 2.0 XML conforms to schema standards."""
    sample_dossier = {
        "case_id": "DRISHTI-CASE-TEST-01",
        "scam_typology": "DIGITAL_ARREST_COERCION",
        "risk_score": 0.95,
        "account_frozen": True,
        "transaction": {
            "id": "TXN-FINNET-01",
            "amount": 480000.0,
            "sender_vpa": "victim@oksbi",
            "receiver_vpa": "mule.escrow@paytm",
            "receiver_ifsc": "PYTM0123456",
            "remark": "Supreme Court legal fee"
        },
        "draft_str": "Severe digital arrest coercion under active voice call."
    }

    xml_str = generate_finnet2_xml(sample_dossier, officer_name="Shri A. K. Sharma")
    assert "<?xml" in xml_str
    assert "FIU_IND_STR_Batch" in xml_str

    root = ET.fromstring(xml_str)
    assert root.attrib["version"] == "2.0"
    ns = {"fiu": "http://fiuindia.gov.in/finnet2.0/str"}
    header = root.find("fiu:ReportingEntityHeader", ns)
    assert header is not None
    assert header.find("fiu:PrincipalOfficerName", ns).text == "Shri A. K. Sharma"

    report = root.find("fiu:SuspiciousTransactionReport", ns)
    assert report is not None
    assert report.find("fiu:AccountLienFrozen", ns).text == "TRUE"
    assert report.find("fiu:DigitalSignatureBlock", ns) is not None

def test_iso20022_camt056_recall_generation():
    """Verify that ISO 20022 camt.056 cancellation request is correctly formed."""
    sample_dossier = {
        "case_id": "DRISHTI-CASE-TEST-02",
        "transaction": {
            "id": "TXN-ISO-99",
            "amount": 350000.0,
            "receiver_vpa": "mule.iso@paytm",
            "receiver_ifsc": "PYTM0123456"
        }
    }

    res = generate_camt056_recall(sample_dossier, reason_code="FRAD")
    assert res["standard"] == "ISO 20022 camt.056.001.08"
    assert res["reason_code"] == "FRAD"
    assert res["clawback_amount_inr"] == 350000.0
    assert "urn:iso:std:iso:20022:tech:xsd:camt.056.001.08" in res["raw_iso20022_xml"]

def test_api_auto_patch_endpoint():
    """Verify the /api/v1/redteam/auto-patch REST endpoint."""
    resp = client.post("/api/v1/redteam/auto-patch", json={"archetype": "STRUCTURED_SMURFING"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "IMMUNIZED"
    assert "STRUCTURED_THRESHOLD_SMURFING:en" in data["semantic_clusters_seeded"]

@pytest.mark.asyncio
async def test_api_finnet_and_recall_endpoints():
    """Verify the /finnet-xml and /dispatch-recall case endpoints."""
    from httpx import AsyncClient, ASGITransport
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # 1. Inject a scam scenario to create an active case
        inj_resp = await ac.post("/api/v1/simulator/inject", json={"scenario": "DIGITAL_ARREST"})
        assert inj_resp.status_code == 200
        case_id = inj_resp.json()["case_id"]
        assert case_id is not None

        # 2. Test FINnet 2.0 XML export
        xml_resp = await ac.get(f"/api/v1/cases/{case_id}/finnet-xml")
        assert xml_resp.status_code == 200
        assert "application/xml" in xml_resp.headers["content-type"]
        assert "FIU_IND_STR_Batch" in xml_resp.text

        # 3. Test ISO 20022 Interbank Recall
        recall_resp = await ac.post(f"/api/v1/cases/{case_id}/dispatch-recall")
        assert recall_resp.status_code == 200
        data = recall_resp.json()
        assert data["standard"] == "ISO 20022 camt.056.001.08"
        assert data["status"] == "DISPATCHED_TO_RECEIVING_INSTITUTION"
