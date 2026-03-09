"""
Journal de simulation - enregistre tous les événements.
"""

from typing import List
from ..core.events import Event, EventManager


class Journal:
    """Journal de simulation."""

    def __init__(self, event_manager: EventManager):
        self.event_manager = event_manager
        self.logs: List[str] = []

    def log(self, message: str, severity: str = "INFO"):
        """Enregistre un message."""
        log_entry = f"[{severity}] {message}"
        self.logs.append(log_entry)
        print(log_entry)

    def log_event(self, event: Event):
        """Enregistre un événement."""
        self.log(str(event), event.severity)

    def get_recent_logs(self, count: int = 20) -> List[str]:
        """Retourne les N derniers logs."""
        return self.logs[-count:]

    def clear(self):
        """Efface tous les logs."""
        self.logs.clear()
