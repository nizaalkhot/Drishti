"""Domain Unit Tests for Cryptographic Informed Consent Ledger."""
import pytest
from backend.security.consent_vault import default_consent_vault, ConsentRequest

def test_informed_consent_hard_block_on_high_confidence():
    """Verify scam score > 0.85 enforces HARD BLOCK and rejects customer override."""
    req = ConsentRequest(
        transaction_id="tx_high_coercion_99",
        customer_id="cust_victim_01",
        scam_score=0.94,
        scam_typology="DIGITAL_ARREST",
        confirmed_no_coercion=True,
        biometric_auth_token="BIOMETRIC_TOKEN_OK"
    )
    receipt = default_consent_vault.record_override_attempt(req)
    assert receipt.can_proceed is False
    assert receipt.status == "REJECTED_HARD_BLOCK"
    assert "exceeds bank safety threshold" in receipt.reason

def test_informed_consent_permits_override_on_medium_confidence():
    """Verify customer override is logged in tamper-evident ledger when score <= 0.85."""
    req = ConsentRequest(
        transaction_id="tx_medium_risk_50",
        customer_id="cust_user_44",
        scam_score=0.72,
        scam_typology="SUSPICIOUS_HIGH_VALUE_FIRST_TIME",
        confirmed_no_coercion=True,
        biometric_auth_token="BIOMETRIC_TOKEN_OK"
    )
    receipt = default_consent_vault.record_override_attempt(req)
    assert receipt.can_proceed is True
    assert receipt.status == "ACCEPTED_OVERRIDE"
    assert receipt.chain_hash is not None
