"""
Tests pour le système de corruption.
"""

import sys
sys.path.insert(0, '..')

from entities.agent import Agent, AgentType, CorruptionStage


def test_agent_corruption():
    """Test de la corruption d'un agent."""
    agent = Agent(
        id="test_agent",
        name="Test",
        sector="forest",
        agent_type=AgentType.WARRIOR
    )

    assert agent.corruption_level == 0.0
    assert agent.corruption_stage == CorruptionStage.CLEAN

    # Augmente la corruption
    agent.increase_corruption(0.3)
    assert agent.corruption_level == 0.3
    assert agent.corruption_stage == CorruptionStage.INFLUENCED

    # Augmente encore
    agent.increase_corruption(0.5)
    assert agent.corruption_level == 0.8
    assert agent.corruption_stage == CorruptionStage.HEAVILY_CORRUPTED

    # Diminue
    agent.decrease_corruption(0.3)
    assert agent.corruption_level == 0.5


def test_agent_psychology():
    """Test de la psychologie de l'agent."""
    agent = Agent(
        id="test_agent",
        name="Test",
        sector="forest",
        agent_type=AgentType.SCOUT
    )

    # Test stress
    agent.increase_stress(0.4)
    assert agent.psychological_state.stress == 0.4

    # Test fatigue
    agent.increase_fatigue(0.3)
    assert agent.psychological_state.fatigue == 0.3

    # Test morale
    agent.decrease_morale(0.2)
    assert agent.psychological_state.morale == 0.8

    # Test vulnérabilité
    agent.increase_stress(0.5)
    assert agent.psychological_state.is_vulnerable_to_corruption()


if __name__ == "__main__":
    test_agent_corruption()
    print("✓ test_agent_corruption passed")

    test_agent_psychology()
    print("✓ test_agent_psychology passed")

    print("\n✓ Tous les tests corruption réussis !")
