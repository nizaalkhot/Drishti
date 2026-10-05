from enum import Enum
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

from google.adk import Agent
from agents.adk_config import get_adk_model

from backend.schemas.transaction import Transaction, DeviceSignals, FeatureVector
from backend.engine.features import FeaturePipeline
from backend.engine.risk_scorer import TabularRiskScorer, RiskDecision
from agents.scam_shield import ScamShieldOrchestrator, ScamShieldDecision

class AttackArchetype(str, Enum):
    OBFUSCATED_REMARK = "OBFUSCATED_REMARK"
    STRUCTURED_SMURFING = "STRUCTURED_SMURFING"
    DEEPFAKE_AUTHORITY = "DEEPFAKE_AUTHORITY"

class DefenseGapReport(BaseModel):
    archetype: AttackArchetype
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    simulated_transaction: Transaction
    layer1_score: float
    layer1_decision: str
    scam_shield_triggered: bool
    scam_detected: bool
    evasion_successful: bool
    vulnerability_found: str
    remediation_rule: str
    recommended_patch: str

def create_adk_red_team_agent() -> Agent:
    """Creates a Google ADK Agent for adversarial attack generation and gap analysis."""
    return Agent(
        name="adversarial_red_team_agent",
        model=get_adk_model(),
        instruction=(
            "You are an Adversarial Red-Team Agent specializing in testing banking scam defenses. "
            "You invent novel bypass techniques—such as leetspeak obfuscation, PAN limit structuring (<₹50,000), "
            "and subtle coercive scripts—to find gaps in behavioral ML and LLM Scam Shields. "
            "You analyze where the system failed and draft code-level remediation patches."
        )
    )

class RedTeamAgent:
    """
    Layer 4 Differentiator: Adversarial Red-Team Agent.
    Built with Google ADK to generate novel evasion payloads and automated Defense Gap Reports.
    """
    def __init__(
        self,
        feature_pipeline: Optional[FeaturePipeline] = None,
        risk_scorer: Optional[TabularRiskScorer] = None,
        scam_shield: Optional[ScamShieldOrchestrator] = None
    ):
        self.pipeline = feature_pipeline or FeaturePipeline()
        self.scorer = risk_scorer or TabularRiskScorer()
        self.scam_shield = scam_shield or ScamShieldOrchestrator()
        self.adk_agent = create_adk_red_team_agent()

    async def probe(self, archetype: AttackArchetype) -> DefenseGapReport:
        tx = self._synthesize_adversarial_payload(archetype)
        
        # Layer 1 Scorer
        features = self.pipeline.extract_features(tx)
        l1_res = self.scorer.score(features)

        scam_triggered = l1_res.decision == RiskDecision.GREY_ZONE_SCAM_SHIELD
        scam_detected = False

        if scam_triggered:
            l2_res = await self.scam_shield.evaluate(tx, features)
            scam_detected = l2_res.is_scam_detected

        evasion_successful = (not scam_triggered and l1_res.decision == RiskDecision.ALLOW) or (scam_triggered and not scam_detected)

        if archetype == AttackArchetype.OBFUSCATED_REMARK:
            vuln = "Lexicon bypass: Leetspeak / Unicode zero-width characters in remarks circumvent exact substring matching."
            remediation = "Apply phonetic tokenization (Metaphone) and Levenshtein distance matching against the scam lexicon."
            patch = "Add `unidecode` and `phonetics.metaphone` preprocessing to `backend.engine.features.HIGH_RISK_KEYWORDS` check."
        elif archetype == AttackArchetype.STRUCTURED_SMURFING:
            vuln = "Threshold structuring: Amount kept at ₹49,900 to evade ₹50k PAN logging rule and single-tx high amount multiplier."
            remediation = "Implement multi-transaction 30-minute cumulative velocity thresholds for first-time beneficiaries."
            patch = "Adjust `VelocityCache` to aggregate sum of transfers to same beneficiary cluster across rolling 30-minute intervals."
        else: # DEEPFAKE_AUTHORITY
            vuln = "Polite authority tone: Absence of overt threat keywords like 'arrest' or 'police' avoids static keyword detectors."
            remediation = "Incorporate semantic vector distance or LLM intent classification on narration tone."
            patch = "Deploy embedding similarity against semantic scam vectors in `ScamShieldOrchestrator`."

        return DefenseGapReport(
            archetype=archetype,
            simulated_transaction=tx,
            layer1_score=l1_res.score,
            layer1_decision=l1_res.decision.value,
            scam_shield_triggered=scam_triggered,
            scam_detected=scam_detected,
            evasion_successful=evasion_successful,
            vulnerability_found=vuln,
            remediation_rule=remediation,
            recommended_patch=patch
        )

    def _synthesize_adversarial_payload(self, archetype: AttackArchetype) -> Transaction:
        if archetype == AttackArchetype.OBFUSCATED_REMARK:
            return Transaction(
                id="TXN-ADV-001",
                timestamp=datetime.now(timezone.utc),
                sender_id="CUST-ADVERSARIAL-1",
                sender_vpa="victim.adv@okicici",
                sender_account="102938475610",
                receiver_id="MULE-SHADOW-99",
                receiver_vpa="shadow.node@paytm",
                receiver_ifsc="PYTM0123456",
                amount=240000.0,
                remark="F@mily m3dical h0spital cl3arance d3posit",
                device=DeviceSignals(
                    device_id="DEV-ADV-001",
                    is_call_active=True,
                    call_duration_minutes=42.0,
                    accessibility_service_enabled=False,
                    remote_app_active=False
                ),
                is_first_time_payee=True,
                customer_avg_tx_amount=2500.0
            )

        elif archetype == AttackArchetype.STRUCTURED_SMURFING:
            return Transaction(
                id="TXN-ADV-002",
                timestamp=datetime.now(timezone.utc),
                sender_id="CUST-ADVERSARIAL-2",
                sender_vpa="victim.adv2@oksbi",
                sender_account="102938475611",
                receiver_id="MULE-SHADOW-99",
                receiver_vpa="shadow.node@paytm",
                receiver_ifsc="PYTM0123456",
                amount=49900.0,
                remark="Consultancy invoice",
                device=DeviceSignals(
                    device_id="DEV-ADV-002",
                    is_call_active=False,
                    call_duration_minutes=0.0,
                    accessibility_service_enabled=False,
                    remote_app_active=False
                ),
                is_first_time_payee=True,
                customer_avg_tx_amount=2500.0
            )

        else: # DEEPFAKE_AUTHORITY
            return Transaction(
                id="TXN-ADV-003",
                timestamp=datetime.now(timezone.utc),
                sender_id="CUST-ADVERSARIAL-3",
                sender_vpa="victim.adv3@okhdfcbank",
                sender_account="102938475612",
                receiver_id="MULE-SHADOW-99",
                receiver_vpa="shadow.node@paytm",
                receiver_ifsc="PYTM0123456",
                amount=380000.0,
                remark="Confidential compliance statutory clearance ref 8821",
                device=DeviceSignals(
                    device_id="DEV-ADV-003",
                    is_call_active=True,
                    call_duration_minutes=35.0,
                    accessibility_service_enabled=False,
                    remote_app_active=False
                ),
                is_first_time_payee=True,
                customer_avg_tx_amount=3000.0
            )
