import time
import asyncio
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

from backend.schemas.transaction import Transaction, FeatureVector
from backend.security.pii import PIITokenizer, TokenVault
from agents.tools.mule_graph import MuleGraphService, MuleGraphAnalysis
from agents.policy_agent import PolicyAgent, PolicyMatch
from agents.intervention_agent import InterventionAgent, InterventionDialog

class ScamShieldDecision(BaseModel):
    is_scam_detected: bool
    scam_typology: str
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    reasoning_summary: str
    intervention: Optional[InterventionDialog] = None
    policy_citation: str = ""
    mule_graph_analysis: Optional[MuleGraphAnalysis] = None
    masked_remark: str = ""
    latency_ms: float = 0.0
    fallback_applied: bool = False

class ScamShieldOrchestrator:
    """
    Layer 2: Scam Shield Multi-Agent Orchestrator.
    Executes context analysis, graph topology inspection, policy grounding,
    and contextual intervention generation within a strict 3.5s SLA.
    """
    def __init__(
        self,
        mule_graph_service: Optional[MuleGraphService] = None,
        policy_agent: Optional[PolicyAgent] = None,
        intervention_agent: Optional[InterventionAgent] = None,
        tokenizer: Optional[PIITokenizer] = None
    ):
        self.mule_graph = mule_graph_service or MuleGraphService()
        self.policy_agent = policy_agent or PolicyAgent()
        self.intervention_agent = intervention_agent or InterventionAgent()
        self.tokenizer = tokenizer or PIITokenizer()

        # Seed default demonstration mule cluster for known simulated patterns
        self.mule_graph.seed_test_cluster(
            aggregator_id="MULE-AGGREGATOR-RING-1",
            device_id="DEV-SHARED-MULE-PHONE-01",
            victim_senders=["CUST-101", "CUST-102", "CUST-103", "CUST-104", "CUST-105"]
        )

    async def evaluate(
        self,
        tx: Transaction,
        features: FeatureVector,
        language: str = "en"
    ) -> ScamShieldDecision:
        start_time = time.perf_counter()

        # 1. PII Redaction & Tokenization
        masked_remark, vault = self.tokenizer.tokenize(tx.remark)

        # 2. Parallel fan-out: Context Agent + Mule Graph Agent + Policy Agent
        # Execute with a hard 3.5s timeout protection
        try:
            decision = await asyncio.wait_for(
                self._run_agent_pipeline(tx, features, masked_remark, language),
                timeout=3.5
            )
        except asyncio.TimeoutError:
            # Fallback path if budget breached
            latency = (time.perf_counter() - start_time) * 1000
            return ScamShieldDecision(
                is_scam_detected=True, # Safety bias on timeout in grey zone
                scam_typology="TIMEOUT_FALLBACK_HOLD",
                confidence_score=0.60,
                reasoning_summary="Scam Shield SLA timeout breached (>3.5s). Applied safety step-up fallback.",
                latency_ms=round(latency, 2),
                fallback_applied=True
            )

        latency = (time.perf_counter() - start_time) * 1000
        decision.latency_ms = round(latency, 2)
        return decision

    async def _run_agent_pipeline(
        self,
        tx: Transaction,
        features: FeatureVector,
        masked_remark: str,
        language: str
    ) -> ScamShieldDecision:
        # Context Analysis
        is_call_active = tx.device.is_call_active
        call_mins = tx.device.call_duration_minutes
        is_first_payee = tx.is_first_time_payee
        apk_active = tx.device.accessibility_service_enabled or tx.device.remote_app_active
        remark_lower = masked_remark.lower()

        # Determine Typology
        typology = "UNKNOWN"
        confidence = 0.50
        reasoning_points = []

        if apk_active:
            typology = "KYC_APK_TAKEOVER"
            confidence = 0.92
            reasoning_points.append("Device accessibility service or screen-sharing app active during transfer.")
        elif is_call_active and call_mins >= 20.0 and any(kw in remark_lower for kw in ["cbi", "police", "court", "verification", "clearance", "rbi", "bail"]):
            typology = "DIGITAL_ARREST"
            confidence = 0.95
            reasoning_points.append(f"Victim engaged in continuous {call_mins:.0f}-minute phone call with coercive authority keywords.")
            if is_first_payee:
                reasoning_points.append("Large outbound transfer directed to an unverified first-time payee.")
        elif any(kw in remark_lower for kw in ["vip", "crypto", "trading", "profit", "task"]):
            typology = "HIGH_YIELD_INVESTMENT"
            confidence = 0.88
            reasoning_points.append("Narration indicates unauthorized investment/task group manipulation.")
        elif features.amount_to_avg_ratio > 30.0 and is_first_payee:
            typology = "SUSPICIOUS_HIGH_VALUE_FIRST_TIME"
            confidence = 0.72
            reasoning_points.append(f"Amount is {features.amount_to_avg_ratio:.0f}x baseline average sent to first-time beneficiary.")

        # Mule Graph Inspection
        mule_analysis = self.mule_graph.analyze_beneficiary(
            beneficiary_id=tx.receiver_id,
            receiver_vpa=tx.receiver_vpa,
            device_id=tx.device.device_id
        )

        if mule_analysis.mule_risk_score >= 0.60:
            confidence = min(confidence + 0.15, 0.99)
            reasoning_points.append(f"Beneficiary graph: {mule_analysis.summary}")

        is_scam = typology != "UNKNOWN" or confidence >= 0.70

        # Policy Grounding
        policy = self.policy_agent.retrieve_guidelines(typology, tx.remark)
        policy_citation = f"{policy.title} ({policy.circular_ref}): {policy.clause}" if policy else ""

        # Contextual Intervention Dialog
        intervention = None
        if is_scam:
            intervention = self.intervention_agent.generate_intervention(
                typology=typology,
                amount=tx.amount,
                language=language
            )

        return ScamShieldDecision(
            is_scam_detected=is_scam,
            scam_typology=typology,
            confidence_score=confidence,
            reasoning_summary="; ".join(reasoning_points) if reasoning_points else "Baseline behavioral deviation.",
            intervention=intervention,
            policy_citation=policy_citation,
            mule_graph_analysis=mule_analysis,
            masked_remark=masked_remark,
            fallback_applied=False
        )
