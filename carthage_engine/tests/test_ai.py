"""
Tests pour l'IA de XANA.
"""

import sys
sys.path.insert(0, '..')

from ai.xana_memory import XANAMemory, MemoryType
from ai.xana_planner import XANAPlanner, StrategicGoal
from ai.threat_map import ThreatMap


def test_xana_memory():
    """Test de la mémoire de XANA."""
    memory = XANAMemory(max_size=100)

    memory.add_memory(
        memory_type=MemoryType.OBSERVATION,
        tick=1,
        timestamp="T+00:00:01",
        data={'test': 'data'},
        importance=0.5,
        tags=['test']
    )

    assert memory.get_memory_count() == 1

    observations = memory.get_memories_by_type(MemoryType.OBSERVATION)
    assert len(observations) == 1


def test_xana_planner():
    """Test du planificateur de XANA."""
    planner = XANAPlanner()

    plan = planner.create_plan(
        goal=StrategicGoal.DOMINATE_SECTOR,
        target_sector='forest',
        tick=0,
        world_state={}
    )

    assert plan is not None
    assert plan.goal == StrategicGoal.DOMINATE_SECTOR
    assert len(plan.actions) > 0


def test_threat_map():
    """Test de la carte des menaces."""
    threat_map = ThreatMap()

    threat_map.register_zone('forest')
    threat_map.update_zone_threat('forest', 3, 5.0, 3.0)

    zone = threat_map.get_zone('forest')
    assert zone.enemy_count == 3
    assert zone.threat_score > 0


if __name__ == "__main__":
    test_xana_memory()
    print("✓ test_xana_memory passed")

    test_xana_planner()
    print("✓ test_xana_planner passed")

    test_threat_map()
    print("✓ test_threat_map passed")

    print("\n✓ Tous les tests AI réussis !")
