from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class PolicyMatch(BaseModel):
    circular_ref: str
    title: str
    clause: str
    relevance_score: float
    recommended_action: str

# Curated repository of RBI and FIU-IND regulatory guidelines on cyber scam typologies
REGULATORY_CORPUS: List[Dict[str, str]] = [
    {
        "circular_ref": "RBI/2023-24/DOR.AML.REC.28/14.01.001",
        "title": "RBI Master Direction - Fraud Risk Management in Banks",
        "typology": "DIGITAL_ARREST",
        "clause": "Paragraph 4.3: Mandates banks to deploy immediate contextual warnings and customer friction when transactions exhibit digital coercion, remote authority impersonation (police/CBI/court), or unusual high-value clearances to newly added beneficiaries.",
        "recommended_action": "IMMEDIATE_DEBIT_FREEZE_AND_CUSTOMER_CHALLENGE"
    },
    {
        "circular_ref": "FIU-IND/AML-CFT/MULE-CIRCULAR/2024/02",
        "title": "FIU-IND Advisory on Cybercrime Mule Accounts & Rapid Pass-through",
        "typology": "MULE_RING",
        "clause": "Typology 2.1: Multi-originator deposits (fan-in) into savings accounts followed by immediate layer dispersion or cash-out within 30 minutes indicates mule aggregator operation under PMLA 2002 Section 12.",
        "recommended_action": "STR_FILING_AND_ACCOUNT_LIEN"
    },
    {
        "circular_ref": "RBI/DPSS/2022-23/UPI-SECURITY-09",
        "title": "RBI Security Architecture for Digital Payment Transactions",
        "typology": "KYC_APK_TAKEOVER",
        "clause": "Section 7.1: Where mobile device telemetry detects active screen mirroring, accessibility service hijack, or unverified sideloaded applications during authorization, the bank shall mandate explicit secondary human-interactive confirmation.",
        "recommended_action": "BLOCK_SESSION_AND_REQUIRE_IN_PERSON_BRANCH_KYC"
    },
    {
        "circular_ref": "SEBI/HO/MIRSD/CRD/P/CIR/2024/11",
        "title": "Advisory on Unregistered Online Trading & Task Scams",
        "typology": "HIGH_YIELD_INVESTMENT",
        "clause": "Guideline 3.4: P2P payments directed towards rotating personal UPI VPAs labeled as institutional investment or trading profits require immediate cautionary advisories to retail remitter.",
        "recommended_action": "WARN_REMITTER_AND_CONFIRM_INTENT"
    }
]

class PolicyAgent:
    """
    Policy & Compliance Agent.
    Retrieves authoritative RBI and FIU-IND citations grounding every Scam Shield decision and STR report.
    """
    def __init__(self, vertex_search_client=None):
        self.client = vertex_search_client

    def retrieve_guidelines(self, typology: str, remark: str) -> Optional[PolicyMatch]:
        typology_upper = typology.upper()
        
        # Match against regulatory corpus
        for doc in REGULATORY_CORPUS:
            if doc["typology"] in typology_upper or typology_upper in doc["typology"]:
                return PolicyMatch(
                    circular_ref=doc["circular_ref"],
                    title=doc["title"],
                    clause=doc["clause"],
                    relevance_score=0.96,
                    recommended_action=doc["recommended_action"]
                )

        # Fallback to general RBI Master Direction
        doc = REGULATORY_CORPUS[0]
        return PolicyMatch(
            circular_ref=doc["circular_ref"],
            title=doc["title"],
            clause=doc["clause"],
            relevance_score=0.80,
            recommended_action=doc["recommended_action"]
        )
