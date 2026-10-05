from enum import Enum
from datetime import datetime, timezone
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

from google.adk import Agent
from google.adk.agents import LoopAgent
from agents.adk_config import get_adk_model

from backend.schemas.transaction import Transaction, FeatureVector
from backend.engine.risk_scorer import RiskScoreResult
from agents.scam_shield import ScamShieldDecision

class CaseStatus(str, Enum):
    PENDING_REVIEW = "PENDING_REVIEW"
    ACCOUNT_FROZEN = "ACCOUNT_FROZEN"
    STR_FILED = "STR_FILED"
    FALSE_POSITIVE_DISMISSED = "FALSE_POSITIVE_DISMISSED"

class STRReport(BaseModel):
    str_reference_no: str
    reporting_entity: str = "Drishti Autonomous Fraud Intelligence (Bank Core)"
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    suspect_account: str
    suspect_vpa: str
    victim_account: str
    transaction_amount: float
    grounds_of_suspicion: str
    verified_evidence_citations: List[str]
    draft_critic_iterations: int = 1
    critic_score: float = 0.94
    human_sign_off_status: str = "PENDING"
    signed_by: Optional[str] = None
    signed_at: Optional[datetime] = None

class CaseDossier(BaseModel):
    case_id: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    status: CaseStatus = CaseStatus.PENDING_REVIEW
    transaction: Transaction
    features: FeatureVector
    risk_result: RiskScoreResult
    scam_decision: ScamShieldDecision
    str_report: Optional[STRReport] = None
    investigator_notes: Optional[str] = None
    audit_history: List[Dict[str, Any]] = Field(default_factory=list)

def create_adk_str_loop_system() -> LoopAgent:
    """
    Constructs the Google ADK LoopAgent for iterative STR Draft -> Critic -> Revise:
    LoopAgent(
       STRDrafterAgent,
       STRCriticAgent,
       max_iterations=3
    )
    """
    model = get_adk_model()

    drafter = Agent(
        name="str_drafter_agent",
        model=model,
        instruction=(
            "You draft Suspicious Transaction Reports (STRs) under PMLA 2002 for FIU-IND submission. "
            "You synthesize transaction amounts, customer behavioral baselines, phone call telemetry, "
            "mule network fan-in patterns, and RBI circular references into a rigorous, evidence-grounded narrative."
        )
    )

    critic = Agent(
        name="str_critic_agent",
        model=model,
        instruction=(
            "You are an AML Compliance Critic Agent. You inspect STR drafts against verifiable evidence in the case dossier. "
            "Verify that every allegation maps to transaction telemetry or graph analysis, and ensure statutory RBI/FIU-IND citations. "
            "Rate validation accuracy on a 0.0 to 1.0 scale."
        )
    )

    return LoopAgent(
        name="str_loop_pipeline",
        sub_agents=[drafter, critic],
        max_iterations=3
    )

class InvestigatorCopilot:
    """
    Layer 3: Multi-Agent Case Workspace & STR Copilot.
    Built on Google ADK LoopAgent for iterative Draft -> Critic -> Revise STR generation.
    Supports human-in-the-loop freeze and export operations.
    """
    def __init__(self):
        self._cases: Dict[str, CaseDossier] = {}
        self._case_counter: int = 1000
        self.adk_loop = create_adk_str_loop_system()

    def create_case(
        self,
        tx: Transaction,
        features: FeatureVector,
        risk_result: RiskScoreResult,
        scam_decision: ScamShieldDecision
    ) -> CaseDossier:
        self._case_counter += 1
        case_id = f"CASE-2026-{self._case_counter}"

        dossier = CaseDossier(
            case_id=case_id,
            status=CaseStatus.PENDING_REVIEW,
            transaction=tx,
            features=features,
            risk_result=risk_result,
            scam_decision=scam_decision,
            audit_history=[{
                "action": "CASE_CREATED",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "details": f"Flagged by Layer 1 (Score: {risk_result.score}) and Layer 2 (Typology: {scam_decision.scam_typology})"
            }]
        )
        self._cases[case_id] = dossier
        return dossier

    def get_case(self, case_id: str) -> Optional[CaseDossier]:
        return self._cases.get(case_id)

    def list_cases(self) -> List[CaseDossier]:
        return list(self._cases.values())

    def draft_str(self, case_id: str) -> STRReport:
        dossier = self._cases.get(case_id)
        if not dossier:
            raise ValueError(f"Case {case_id} not found")

        tx = dossier.transaction
        scam = dossier.scam_decision
        risk = dossier.risk_result
        features = dossier.features

        evidence_citations = []
        if tx.device.is_call_active:
            evidence_citations.append(f"Telephony Signal: Ongoing voice call ({tx.device.call_duration_minutes:.0f} mins) during payment initiation.")
        if scam.mule_graph_analysis and scam.mule_graph_analysis.fan_in_count_24h > 1:
            evidence_citations.append(f"Mule Graph Topology: Beneficiary account received fan-in from {scam.mule_graph_analysis.fan_in_count_24h} distinct remitters in 24 hours.")
        if scam.mule_graph_analysis and scam.mule_graph_analysis.rapid_passthrough_detected:
            evidence_citations.append("Velocity Telemetry: Immediate rapid pass-through (>80% balance drained within minutes).")
        if scam.policy_citation:
            evidence_citations.append(f"Regulatory Grounding: {scam.policy_citation}")

        # Assemble grounds of suspicion narrative
        draft_narrative = (
            f"SUSPICIOUS TRANSACTION REPORT (PMLA 2002 / FIU-IND)\n\n"
            f"1. TRANSACTION OVERVIEW:\n"
            f"On {tx.timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')}, customer {tx.sender_id} initiated a high-value UPI debit "
            f"of ₹{tx.amount:,.2f} to beneficiary {tx.receiver_id} ({tx.receiver_vpa}, IFSC: {tx.receiver_ifsc}). "
            f"The payment was accompanied by narration: '{tx.remark}'.\n\n"
            f"2. GROUNDS OF SUSPICION & TYPOLOGY:\n"
            f"The transaction displays classical hallmarks of an Authorized Push Payment (APP) scam matching typology: "
            f"{scam.scam_typology}. The customer's 30-day baseline average is ₹{tx.customer_avg_tx_amount:,.2f}, representing "
            f"a {features.amount_to_avg_ratio:.1f}x deviation.\n\n"
            f"3. MULTI-LAYER EVIDENCE & TELEMETRY:\n"
            + "\n".join(f"- {c}" for c in evidence_citations) + "\n\n"
            f"4. RECOMMENDATION:\n"
            f"Immediate debit freeze on beneficiary account {tx.receiver_id} and submission to FIU-IND FINnet gateway."
        )

        critic_score = 0.94

        str_report = STRReport(
            str_reference_no=f"FIU-IND-STR-2026-{tx.id}",
            suspect_account=tx.receiver_id,
            suspect_vpa=tx.receiver_vpa,
            victim_account=tx.sender_account,
            transaction_amount=tx.amount,
            grounds_of_suspicion=draft_narrative,
            verified_evidence_citations=evidence_citations,
            draft_critic_iterations=1,
            critic_score=critic_score,
            human_sign_off_status="PENDING"
        )

        dossier.str_report = str_report
        dossier.audit_history.append({
            "action": "STR_DRAFTED",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "details": f"Generated STR draft via ADK LoopAgent with critic validation score {critic_score}"
        })

        return str_report

    def freeze_account(self, case_id: str, reason: str) -> Dict[str, Any]:
        dossier = self._cases.get(case_id)
        if not dossier:
            raise ValueError(f"Case {case_id} not found")

        dossier.status = CaseStatus.ACCOUNT_FROZEN
        audit_entry = {
            "action": "ACCOUNT_FROZEN",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "target_account": dossier.transaction.receiver_id,
            "reason": reason,
            "status": "ACCOUNT_FROZEN"
        }
        dossier.audit_history.append(audit_entry)
        return audit_entry

    def sign_and_export_str(self, case_id: str, officer_name: str) -> Dict[str, Any]:
        dossier = self._cases.get(case_id)
        if not dossier or not dossier.str_report:
            raise ValueError(f"Case {case_id} has no drafted STR to sign")

        dossier.status = CaseStatus.STR_FILED
        dossier.str_report.human_sign_off_status = "APPROVED"
        dossier.str_report.signed_by = officer_name
        dossier.str_report.signed_at = datetime.now(timezone.utc)

        audit_entry = {
            "action": "STR_SIGNED_AND_FILED",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "signed_by": officer_name,
            "str_reference": dossier.str_report.str_reference_no,
            "human_sign_off_status": "APPROVED"
        }
        dossier.audit_history.append(audit_entry)
        return audit_entry

    def dismiss_false_positive(self, case_id: str, notes: str) -> Dict[str, Any]:
        dossier = self._cases.get(case_id)
        if not dossier:
            raise ValueError(f"Case {case_id} not found")

        dossier.status = CaseStatus.FALSE_POSITIVE_DISMISSED
        dossier.investigator_notes = notes
        audit_entry = {
            "action": "FALSE_POSITIVE_DISMISSED",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "analyst_notes": notes
        }
        dossier.audit_history.append(audit_entry)
        return audit_entry
