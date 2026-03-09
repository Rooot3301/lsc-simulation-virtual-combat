"""
Tests pour le module core.
"""

import sys
sys.path.insert(0, '..')

from core.time import SimulationTime
from core.events import Event, EventType, EventManager
from core.scheduler import Scheduler, Priority


def test_simulation_time():
    """Test du système de temps."""
    time = SimulationTime()
    assert time.current_tick == 0

    time.advance(5)
    assert time.current_tick == 5

    timestamp = time.get_timestamp()
    assert "T+" in timestamp


def test_event_manager():
    """Test du gestionnaire d'événements."""
    manager = EventManager()

    event = Event(
        type=EventType.SIMULATION_START,
        tick=0,
        timestamp="T+00:00:00",
        message="Test",
        severity="INFO"
    )

    manager.emit(event)
    assert len(manager.events) == 1

    recent = manager.get_recent_events(1)
    assert len(recent) == 1


def test_scheduler():
    """Test de l'ordonnanceur."""
    scheduler = Scheduler()

    executed = []

    def task1():
        executed.append("task1")

    def task2():
        executed.append("task2")

    scheduler.add_task("task1", task1, Priority.HIGH)
    scheduler.add_task("task2", task2, Priority.LOW)

    scheduler.execute_all()

    assert "task1" in executed
    assert "task2" in executed


if __name__ == "__main__":
    test_simulation_time()
    print("✓ test_simulation_time passed")

    test_event_manager()
    print("✓ test_event_manager passed")

    test_scheduler()
    print("✓ test_scheduler passed")

    print("\n✓ Tous les tests core réussis !")
