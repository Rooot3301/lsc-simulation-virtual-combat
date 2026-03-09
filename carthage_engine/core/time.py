"""
Gestion du temps de simulation.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class SimulationTime:
    """
    Représente le temps dans la simulation.
    Chaque tick représente une unité de temps virtuel.
    """

    current_tick: int = 0
    start_time: datetime = None
    tick_duration_seconds: float = 1.0

    def __post_init__(self):
        if self.start_time is None:
            self.start_time = datetime.now()

    def advance(self, ticks: int = 1):
        """Avance le temps de simulation."""
        self.current_tick += ticks

    def get_elapsed_time(self) -> timedelta:
        """Retourne le temps écoulé depuis le début."""
        return timedelta(seconds=self.current_tick * self.tick_duration_seconds)

    def get_timestamp(self) -> str:
        """Retourne un timestamp formaté."""
        elapsed = self.get_elapsed_time()
        hours, remainder = divmod(elapsed.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"T+{hours:02d}:{minutes:02d}:{seconds:02d}"

    def reset(self):
        """Réinitialise le temps."""
        self.current_tick = 0
        self.start_time = datetime.now()
