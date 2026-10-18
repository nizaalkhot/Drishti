"""Domain Unit Tests for I4C / NPCI Cross-Bank Consortium Registry."""
import pytest
from backend.consortium.i4c_registry import default_i4c_registry
from backend.schemas import ScenarioType, AttackArchetype, ScoringResponse

def test_i4c_consortium_cross_bank_match():
    """Verify multi-bank syndicate mule is flagged via salted hash lookup."""
    match = default_i4c_registry.lookup(receiver_vpa="sbi.safety.officer@ybl")
    assert match is not None
    assert match.is_active_block is True
    assert match.reporting_banks_count >= 2
    assert "NCRP" in match.ncrp_reference

def test_canonical_schemas_export_coherence():
    """Verify that backend.schemas exports domain and API contracts without circular imports."""
    assert ScenarioType.DIGITAL_ARREST == "DIGITAL_ARREST"
    assert AttackArchetype.OBFUSCATED_REMARK == "OBFUSCATED_REMARK"
    resp = ScoringResponse(
        transaction_id="TXN-CONS-1",
        amount=500.0,
        sender_vpa="a@b",
        receiver_vpa="c@d",
        remark="consortium test",
        risk_score=0.15,
        decision="ALLOW",
        layer1_latency_ms=1.2,
        total_latency_ms=2.5,
        telemetry={}
    )
    assert resp.transaction_id == "TXN-CONS-1"
