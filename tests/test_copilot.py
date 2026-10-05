import pytest
from datetime import datetime, timezone
from backend.schemas.transaction import Transaction, DeviceSignals
from backend.engine.features import FeaturePipeline
from backend.engine.risk_scorer import TabularRiskScorer
from agents.scam_shield import ScamShieldOrchestrator
from agents.copilot import InvestigatorCopilot, CaseStatus

@pytest.mark.asyncio
async def test_investigator_copilot_case_workflow():
    copilot = InvestigatorCopilot()
    orchestrator = ScamShieldOrchestrator()
    pipeline = FeaturePipeline()
    scorer = TabularRiskScorer()

    tx = Transaction(
        id="TXN-COPILOT-01",
        timestamp=datetime.now(timezone.utc),
        sender_id="CUST-MEERA",
        sender_vpa="meera.d@oksbi",
        sender_account="998877665544",
        receiver_id="MULE-AGGREGATOR-RING-1",
        receiver_vpa="central.escrow.mule@paytm",
        receiver_ifsc="PYTM0123456",
        amount=350000.0,
        remark="CBI legal clearance deposit",
        device=DeviceSignals(
            device_id="DEV-SHARED-MULE-PHONE-01",
            ip_address="14.139.12.5",
            is_call_active=True,
            call_duration_minutes=42.0,
            accessibility_service_enabled=False,
            remote_app_active=False
        ),
        is_first_time_payee=True,
        customer_avg_tx_amount=2000.0
    )

    features = pipeline.extract_features(tx)
    risk_score = scorer.score(features)
    scam_decision = await orchestrator.evaluate(tx, features)

    # 1. Create Case
    case = copilot.create_case(tx, features, risk_score, scam_decision)
    assert case.status == CaseStatus.PENDING_REVIEW
    assert case.transaction.amount == 350000.0

    # 2. Draft STR using Draft-Critic-Revise loop
    str_report = copilot.draft_str(case.case_id)
    assert str_report.critic_score >= 0.85
    assert len(str_report.verified_evidence_citations) > 0
    assert "cbi" in str_report.grounds_of_suspicion.lower()

    # 3. Action: Freeze Account
    freeze_record = copilot.freeze_account(case.case_id, reason="Mule Aggregator Ring confirmed")
    assert freeze_record["status"] == "ACCOUNT_FROZEN"
    assert copilot.get_case(case.case_id).status == CaseStatus.ACCOUNT_FROZEN

    # 4. Action: Sign & Approve STR
    signed = copilot.sign_and_export_str(case.case_id, officer_name="Compliance Officer Sharma")
    assert signed["human_sign_off_status"] == "APPROVED"
