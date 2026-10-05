import pytest
from simulator.generator import UPISimulator, ScenarioType

def test_simulator_generates_digital_arrest_scenario():
    sim = UPISimulator()
    tx = sim.generate_scenario(ScenarioType.DIGITAL_ARREST)
    
    assert tx.device.is_call_active is True
    assert tx.device.call_duration_minutes >= 30.0
    assert tx.is_first_time_payee is True
    assert tx.amount >= 50000.0
    assert any(term in tx.remark.lower() for term in ["cbi", "police", "court", "verification", "clearance", "rbi"])

def test_simulator_generates_legitimate_scenario():
    sim = UPISimulator()
    tx = sim.generate_scenario(ScenarioType.LEGITIMATE)
    
    assert tx.device.is_call_active is False
    assert tx.device.accessibility_service_enabled is False
    assert tx.amount <= 30000.0
