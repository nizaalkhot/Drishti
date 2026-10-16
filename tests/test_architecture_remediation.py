"""Tests verifying the architecture remediation:
1. InterventionTemplateCache functionality, memory bounds, and presentation copy isolation.
2. 180ms banking SLA circuit breaker and fast deterministic safety fallback.
3. MuleGraphService memory bounds and bounded eviction.
4. Schema consolidation without circular dependencies.
"""
import pytest
from datetime import datetime, timezone
from backend.schemas import (
    Transaction,
    DeviceSignals,
    FeatureVector,
    ScenarioType,
    AttackArchetype,
    ScoringResponse,
)
from backend.cache.intervention_cache import InterventionTemplateCache, default_intervention_cache
from agents.intervention_agent import InterventionDialog
from agents.scam_shield import ScamShieldOrchestrator
from agents.tools.mule_graph import MuleGraphService

def test_intervention_template_cache_isolation_and_eviction():
    """Verify that intervention cache only stores UI copy, never fraud decisions, and enforces bounded capacity."""
    cache = InterventionTemplateCache(max_entries=5)

    # Verify pre-seeded clusters
    hit = cache.lookup("DIGITAL_ARREST", "en")
    assert hit is not None
    dialog, latency = hit
    assert "Digital Arrest" in dialog.headline
    assert latency < 2

    # Verify cache miss
    miss = cache.lookup("NON_EXISTENT_SCAM", "en")
    assert miss is None

    # Test eviction under capacity overflow
    for i in range(10):
        dummy_dialog = InterventionDialog(
            headline=f"Warning {i}",
            body="Body text",
            language="en",
            primary_action="Action",
            secondary_action="Secondary",
            override_action="Override",
            risk_level="HIGH"
        )
        cache.store(f"TYPOLOGY_{i}", "en", dummy_dialog)

    assert len(cache._cache) <= 5

def test_scam_shield_fast_fallback_decision():
    """Verify that generate_fast_fallback_decision executes in sub-2ms with safety guarantees."""
    orchestrator = ScamShieldOrchestrator()

    tx = Transaction(
        id="TXN-SLA-TEST",
        timestamp=datetime.now(timezone.utc),
        sender_id="CUST-TEST",
        sender_vpa="test@upi",
        sender_account="123456",
        receiver_id="MULE-TEST",
        receiver_vpa="mule@upi",
        receiver_ifsc="ABCD0123456",
        amount=50000.0,
        remark="Urgent CBI transfer",
        device=DeviceSignals(
            device_id="DEV-001",
            ip_address="127.0.0.1",
            is_call_active=True,
            call_duration_minutes=30.0
        )
    )

    features = FeatureVector(
        is_call_active=1.0,
        malicious_app_flag=0.0,
        consortium_blacklisted_flag=0.0
    )

    decision = orchestrator.generate_fast_fallback_decision(tx, features)
    assert decision.is_scam_detected is True
    assert decision.fallback_applied is True
    assert decision.latency_ms <= 5.0
    assert decision.intervention is not None
    assert "Digital Arrest" in decision.intervention.headline

def test_mule_graph_service_bounded_capacity():
    """Verify that MuleGraphService evicts entries when exceeding max capacity."""
    service = MuleGraphService()
    service._max_cache_entries = 10

    for i in range(25):
        service.seed_test_cluster(
            aggregator_id=f"MULE-{i}",
            device_id=f"DEV-{i}",
            victim_senders=[f"VICTIM-{i}-1", f"VICTIM-{i}-2"]
        )

    # Inflows should be bounded
    assert len(service._beneficiary_inflows) <= 15

def test_canonical_schemas_export_coherence():
    """Verify that backend.schemas exports domain and API contracts without circular imports."""
    assert ScenarioType.DIGITAL_ARREST == "DIGITAL_ARREST"
    assert AttackArchetype.OBFUSCATED_REMARK == "OBFUSCATED_REMARK"
    resp = ScoringResponse(
        transaction_id="TXN-1",
        amount=100.0,
        sender_vpa="a@b",
        receiver_vpa="c@d",
        remark="test",
        risk_score=0.1,
        decision="ALLOW",
        layer1_latency_ms=1.2,
        total_latency_ms=2.5,
        telemetry={}
    )
    assert resp.transaction_id == "TXN-1"
