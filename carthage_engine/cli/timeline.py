"""
Timeline - visualisation de l'historique.
"""

from typing import List
from ..core.events import Event, EventManager


class Timeline:
    """Gère la timeline des événements."""

    def __init__(self, event_manager: EventManager):
        self.event_manager = event_manager

    def show_recent(self, count: int = 10):
        """Affiche les événements récents."""
        events = self.event_manager.get_recent_events(count)
        print(f"\n=== {count} DERNIERS ÉVÉNEMENTS ===\n")
        for event in events:
            print(f"  {event}")

    def show_since_tick(self, tick: int):
        """Affiche les événements depuis un tick."""
        events = self.event_manager.get_events_since_tick(tick)
        print(f"\n=== ÉVÉNEMENTS DEPUIS TICK {tick} ===\n")
        for event in events:
            print(f"  {event}")
