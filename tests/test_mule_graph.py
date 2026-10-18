import pytest
from agents.tools.mule_graph import MuleGraphService

def test_mule_graph_identifies_fan_in_and_shared_device():
    graph_service = MuleGraphService()
    
    # Seed known mule cluster
    graph_service.seed_test_cluster(
        aggregator_id="MULE-AGGREGATOR-RING-1",
        device_id="DEV-SHARED-MULE-PHONE-01",
        victim_senders=["CUST-101", "CUST-102", "CUST-103", "CUST-104", "CUST-105"]
    )
    
    analysis = graph_service.analyze_beneficiary(
        beneficiary_id="MULE-AGGREGATOR-RING-1",
        receiver_vpa="central.escrow.mule@paytm",
        device_id="DEV-SHARED-MULE-PHONE-01"
    )
    
    assert analysis.mule_risk_score >= 0.70
    assert analysis.fan_in_count_24h >= 5
    assert len(analysis.shared_device_accounts) >= 1
    assert analysis.rapid_passthrough_detected is True
    assert len(analysis.graph_nodes) > 0
    assert len(analysis.graph_edges) > 0

def test_clean_beneficiary_has_low_mule_score():
    graph_service = MuleGraphService()
    analysis = graph_service.analyze_beneficiary(
        beneficiary_id="BENEF-CLEAN-99",
        receiver_vpa="clean.friend@oksbi",
        device_id="DEV-CLEAN-01"
    )
    assert analysis.mule_risk_score <= 0.15
    assert analysis.fan_in_count_24h <= 1
    assert analysis.rapid_passthrough_detected is False

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
