"""
Système d'événements pour la simulation.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List
from datetime import datetime


class EventType(Enum):
    """Types d'événements dans la simulation."""

    # Système
    SIMULATION_START = "simulation_start"
    SIMULATION_PAUSE = "simulation_pause"
    SIMULATION_STOP = "simulation_stop"
    TICK = "tick"

    # XANA
    XANA_GOAL_SET = "xana_goal_set"
    XANA_PLAN_CREATED = "xana_plan_created"
    XANA_PLAN_EXECUTED = "xana_plan_executed"
    XANA_ADAPTATION = "xana_adaptation"

    # Tours
    TOWER_ACTIVATED = "tower_activated"
    TOWER_DEACTIVATED = "tower_deactivated"
    TOWER_CONTESTED = "tower_contested"
    TOWER_CORRUPTED = "tower_corrupted"

    # Entités
    MONSTER_SPAWNED = "monster_spawned"
    MONSTER_DESTROYED = "monster_destroyed"
    AGENT_SPAWNED = "agent_spawned"
    AGENT_DESTROYED = "agent_destroyed"
    AGENT_MOVED = "agent_moved"

    # Combat
    COMBAT_START = "combat_start"
    COMBAT_END = "combat_end"
    DAMAGE_DEALT = "damage_dealt"

    # Corruption
    CORRUPTION_SPREAD = "corruption_spread"
    CORRUPTION_INCREASED = "corruption_increased"
    AGENT_CORRUPTED = "agent_corrupted"
    AGENT_RECOVERED = "agent_recovered"

    # Psychologie
    STRESS_INCREASED = "stress_increased"
    MORALE_CHANGED = "morale_changed"
    FATIGUE_INCREASED = "fatigue_increased"

    # Skid
    SKID_MOVED = "skid_moved"
    SKID_DAMAGED = "skid_damaged"
    SKID_MISSION_START = "skid_mission_start"
    SKID_MISSION_END = "skid_mission_end"

    # Réseau
    NETWORK_CORRUPTED = "network_corrupted"
    CORRIDOR_BLOCKED = "corridor_blocked"

    # Secteurs
    SECTOR_DOMINATED = "sector_dominated"
    SECTOR_LIBERATED = "sector_liberated"


@dataclass
class Event:
    """Représente un événement dans la simulation."""

    type: EventType
    tick: int
    timestamp: str
    data: Dict[str, Any] = field(default_factory=dict)
    message: str = ""
    severity: str = "INFO"  # INFO, ALERTE, CRITIQUE, DEBUG

    def __str__(self) -> str:
        return f"[{self.severity}] {self.timestamp} - {self.message}"


class EventManager:
    """Gère les événements de la simulation."""

    def __init__(self):
        self.events: List[Event] = []
        self.listeners: Dict[EventType, List[callable]] = {}

    def emit(self, event: Event):
        """Émet un événement."""
        self.events.append(event)

        # Notifier les listeners
        if event.type in self.listeners:
            for listener in self.listeners[event.type]:
                listener(event)

    def subscribe(self, event_type: EventType, callback: callable):
        """S'abonne à un type d'événement."""
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(callback)

    def get_recent_events(self, count: int = 10) -> List[Event]:
        """Retourne les N derniers événements."""
        return self.events[-count:]

    def get_events_by_type(self, event_type: EventType) -> List[Event]:
        """Retourne tous les événements d'un type donné."""
        return [e for e in self.events if e.type == event_type]

    def get_events_since_tick(self, tick: int) -> List[Event]:
        """Retourne tous les événements depuis un tick donné."""
        return [e for e in self.events if e.tick >= tick]

    def clear(self):
        """Efface tous les événements."""
        self.events.clear()
