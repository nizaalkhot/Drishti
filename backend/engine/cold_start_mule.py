"""
Cold-Start Mule Detection Engine (CON 3 Resolution).
Detects freshly recruited first-hop mule accounts before graph topology or fan-in history forms,
leveraging account lifecycle age, KYC profile mismatch, and VPA binding freshness.
"""
from typing import Tuple, List
from backend.schemas.transaction import Transaction

class ColdStartMuleScorer:
    """
    Evaluates pre-transaction beneficiary lifecycle indicators to identify
    clean/student mule recruitment on their very first fraudulent inflow.
    """
    def evaluate(self, tx: Transaction) -> Tuple[float, List[str]]:
        """
        Returns:
            (cold_start_anomaly_score, list_of_risk_indicators)
        """
        score = 0.0
        indicators: List[str] = []
        
        # 1. Account age vs high-value credit
        if tx.receiver_account_age_days <= 30:
            if tx.amount >= 50000.0:
                score += 0.45
                indicators.append(f"Beneficiary account opened only {tx.receiver_account_age_days}d ago receiving large credit (₹{tx.amount:,.0f}).")
            elif tx.amount >= 25000.0:
                score += 0.30
                indicators.append(f"Fresh account ({tx.receiver_account_age_days}d old) receiving significant inbound transfer.")

        # 2. KYC Demographic Profile vs Inflow Amount
        kyc = tx.receiver_kyc_tier.upper()
        if kyc in ["STUDENT", "NO_INCOME", "LOW_TIER"]:
            if tx.amount >= 50000.0:
                score += 0.35
                indicators.append(f"KYC profile anomaly: {kyc} tier account receiving commercial-scale round-sum credit.")
            elif tx.amount >= 20000.0:
                score += 0.20
                indicators.append(f"KYC profile ({kyc}) atypical for transaction scale.")

        # 3. VPA SIM / Device Binding Freshness
        if tx.receiver_vpa_binding_age_hours <= 48.0:
            score += 0.25
            indicators.append(f"Receiver UPI VPA linked to new SIM/device only {tx.receiver_vpa_binding_age_hours:.1f}h ago.")

        final_score = min(round(score, 2), 1.0)
        return final_score, indicators

default_cold_start_scorer = ColdStartMuleScorer()
