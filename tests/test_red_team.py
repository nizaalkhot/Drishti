import pytest
from agents.red_team import RedTeamAgent, AttackArchetype

@pytest.mark.asyncio
async def test_red_team_probes_obfuscated_injection():
    agent = RedTeamAgent()
    gap_report = await agent.probe(AttackArchetype.OBFUSCATED_REMARK)
    
    assert gap_report.archetype == AttackArchetype.OBFUSCATED_REMARK
    assert gap_report.simulated_transaction is not None
    assert gap_report.remediation_rule != ""
    assert isinstance(gap_report.evasion_successful, bool)

@pytest.mark.asyncio
async def test_red_team_probes_structured_smurfing():
    agent = RedTeamAgent()
    gap_report = await agent.probe(AttackArchetype.STRUCTURED_SMURFING)
    
    assert gap_report.archetype == AttackArchetype.STRUCTURED_SMURFING
    assert gap_report.simulated_transaction.amount < 50000.0 # Under PAN limit
    assert gap_report.remediation_rule != ""
