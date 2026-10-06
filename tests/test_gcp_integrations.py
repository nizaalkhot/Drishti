"""
Unit & Integration Tests for Google Cloud Enterprise Integrations.
Validates Document AI, Pub/Sub, BigQuery Export, Database Persistence (Cloud SQL / AlloyDB),
and Vertex AI Search / Model Predictor dual-mode operation.
"""
import pytest
from datetime import datetime, timezone
from fastapi.testclient import TestClient

from backend.main import app
from backend.integrations.document_ai import DocumentAIService, default_document_ai
from backend.integrations.pubsub import DrishtiPubSubService, default_pubsub_service
from backend.integrations.bigquery_export import BigQueryExportService, default_bq_export
from backend.engine.risk_scorer import VertexAIModelPredictor, TabularRiskScorer
from backend.schemas.transaction import FeatureVector
from backend.database.db import init_db
from backend.database.repository import CaseRepository, ConsentRepository, AuditLogRepository
from agents.tools.doc_parser import analyze_case_document
from agents.tools.mule_graph import default_mule_service, query_mule_graph

client = TestClient(app)

@pytest.mark.asyncio
async def test_database_persistence_and_audit():
    """Validates database schema creation and async CRUD across all repository models."""
    await init_db()

    # 1. Save and retrieve Case Dossier
    case = await CaseRepository.save_case(
        case_id="TEST-CASE-GCP-01",
        transaction_id="TXN-GCP-999",
        sender_vpa="victim@okhdfc",
        receiver_vpa="mule@fakecbi",
        amount=150000.0,
        risk_score=0.92,
        decision="INTERVENE",
        scam_typology="DIGITAL_ARREST",
        transaction_json={"id": "TXN-GCP-999", "amount": 150000.0},
        features_json={"is_call_active": 1.0},
        risk_result_json={"score": 0.92},
        scam_decision_json={"typology": "DIGITAL_ARREST"}
    )
    assert case.case_id == "TEST-CASE-GCP-01"

    fetched_case = await CaseRepository.get_case("TEST-CASE-GCP-01")
    assert fetched_case is not None
    assert fetched_case.amount == 150000.0
    assert fetched_case.status == "PENDING_REVIEW"

    # 2. Update Case status
    await CaseRepository.update_status("TEST-CASE-GCP-01", "STR_FILED")
    updated = await CaseRepository.get_case("TEST-CASE-GCP-01")
    assert updated.status == "STR_FILED"

    # 3. Save Consent Receipt
    receipt = await ConsentRepository.save_receipt(
        receipt_id="REC-TEST-01",
        transaction_id="TXN-GCP-999",
        customer_id="CUST-888",
        status="ACCEPTED_OVERRIDE",
        scam_score=0.45,
        reason="Customer certified no coercion",
        chain_hash="sha256-hash-sample",
        can_proceed=True,
        raw_request_json={"customer_id": "CUST-888"}
    )
    assert receipt.receipt_id == "REC-TEST-01"

    recent_receipts = await ConsentRepository.list_recent(5)
    assert any(r.receipt_id == "REC-TEST-01" for r in recent_receipts)

    # 4. Record Audit Log
    log = await AuditLogRepository.record_audit(
        action="VERIFIED",
        case_id="TXN-GCP-999",
        actor="TEST_RUNNER",
        details_json={"note": "passed"}
    )
    assert log.id is not None

def test_document_ai_forensics():
    """Validates Document AI scam heuristic and forged court notice detection."""
    doc_service = DocumentAIService()

    # Forged document
    fake_doc = """
    SUPREME COURT OF INDIA - DIGITAL ARREST WARRANT
    Case Crime No: CBI/2026/CYBER-ARREST-901
    Accused is ordered to transfer ₹2,50,000 to RBI Clearance Safe Account
    Failure to comply within 2 hours will lead to immediate custody.
    Contact: cbi-officer@gmail.com
    """
    res = doc_service.analyze_document(fake_doc)
    assert res.is_forgery_suspected is True
    assert "court" in res.detected_document_type.lower() or "police" in res.detected_document_type.lower()
    assert len(res.forgery_indicators) >= 2
    assert res.confidence_score >= 0.85

    # Genuine document
    genuine_doc = """
    Invoice No: INV-2026-00452
    Apollo Pharmacy Ltd
    Medicines and medical diagnostics supply
    Total Amount: INR 4,200.00
    Authorized Signatory
    """
    res_gen = doc_service.analyze_document(genuine_doc)
    assert res_gen.is_forgery_suspected is False

    # Function tool integration
    tool_out = analyze_case_document(fake_doc)
    assert "COURT_WARRANT" in tool_out or "POLICE_NOTICE" in tool_out

def test_pubsub_service():
    """Validates Pub/Sub message publishing and subscriber dispatch."""
    pubsub = DrishtiPubSubService()
    received_events = []

    def subscriber(msg):
        received_events.append(msg)

    pubsub.subscribe("drishti-transaction-events", subscriber)

    # Publish transaction event
    event_data = {"txn_id": "TXN-TEST-PS", "amount": 50000.0, "decision": "ALLOW"}
    msg_id = pubsub.publish_transaction_scored(event_data)
    assert msg_id is not None
    assert len(received_events) == 1
    assert received_events[0]["txn_id"] == "TXN-TEST-PS"

    # Publish fraud alert
    alert_id = pubsub.publish_fraud_alert({"txn_id": "TXN-ALERT-01", "risk_score": 0.95})
    assert alert_id is not None

    # Publish STR filing
    str_id = pubsub.publish_str_filing({"case_id": "CASE-STR-01", "amount": 200000.0})
    assert str_id is not None

def test_bigquery_export_journal():
    """Validates BigQuery streaming export and local audit journal."""
    bq = BigQueryExportService()

    success_txn = bq.export_transaction_risk({"txn_id": "TXN-BQ-01", "score": 0.77})
    assert success_txn is True

    success_str = bq.export_filed_dossier({"case_id": "CASE-BQ-01", "officer": "AML Lead"})
    assert success_str is True

    txns = bq.get_local_transactions()
    assert any(t.get("txn_id") == "TXN-BQ-01" for t in txns)

    dossiers = bq.get_local_dossiers()
    assert any(d.get("case_id") == "CASE-BQ-01" for d in dossiers)

def test_vertex_ai_predictor():
    """Validates VertexAIModelPredictor with high-speed calibrated response."""
    predictor = VertexAIModelPredictor()

    features_high = FeatureVector(
        is_call_active=1.0,
        high_risk_remark_flag=1.0,
        malicious_app_flag=1.0,
        consortium_blacklisted_flag=1.0
    )
    result_high = predictor.score(features_high)
    assert result_high.score >= 0.75
    assert result_high.decision.value == "HOLD"
    assert result_high.latency_ms < 50.0

    features_low = FeatureVector(
        trusted_payee_score=0.9
    )
    result_low = predictor.score(features_low)
    assert result_low.score < 0.35
    assert result_low.decision.value == "ALLOW"

def test_mule_graph_analytics():
    """Validates BigQuery topological mule ring graph traversal tool."""
    mule_res = default_mule_service.analyze_beneficiary("MULE-AGGREGATOR-RING-1", device_id="DEV-SHARED-MULE-PHONE-01")
    assert mule_res.mule_risk_score >= 0.60
    assert mule_res.fan_in_count_24h >= 3
    assert len(mule_res.graph_nodes) > 0

    tool_text = query_mule_graph("MULE-AGGREGATOR-RING-1", device_id="DEV-SHARED-MULE-PHONE-01")
    assert "Mule Risk Score" in tool_text

def test_case_document_ai_api_endpoint():
    """Validates the POST /api/v1/cases/{case_id}/analyze-document route."""
    # First inject a scenario to create a case
    inject_res = client.post("/api/v1/simulator/inject", json={
        "scenario": "DIGITAL_ARREST",
        "language": "en"
    })
    assert inject_res.status_code == 200
    case_id = inject_res.json()["case_id"]
    assert case_id is not None

    # Analyze suspicious document for this case
    doc_payload = {
        "document_text": "SUPREME COURT OF INDIA ARREST NOTICE. Transfer funds immediately to CBI Safe Account.",
        "mime_type": "text/plain",
        "document_name": "cbi_arrest_order.txt"
    }
    doc_res = client.post(f"/api/v1/cases/{case_id}/analyze-document", json=doc_payload)
    assert doc_res.status_code == 200
    doc_data = doc_res.json()
    assert doc_data["is_forgery_suspected"] is True
    assert doc_data["confidence_score"] >= 0.85
    assert len(doc_data["forgery_indicators"]) > 0
