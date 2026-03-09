"""
Boucle de simulation autonome pour CARTHAGE ENGINE v2.0.

Gère l'exécution continue, les contrôles, et la vitesse de simulation.
"""

import time
import threading
from enum import Enum
from typing import Callable, Optional


class SimulationState(Enum):
    """États de la simulation."""
    STOPPED = "stopped"
    RUNNING = "running"
    PAUSED = "paused"


class AutonomousSimulationLoop:
    """
    Boucle de simulation autonome thread-safe.

    Permet:
    - exécution continue
    - pause/reprise
    - arrêt
    - contrôle vitesse
    - callbacks par tick
    """

    def __init__(self, tick_callback: Callable[[], None]):
        """
        Args:
            tick_callback: Fonction appelée à chaque tick
        """
        self.tick_callback = tick_callback
        self.state = SimulationState.STOPPED

        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._pause_event = threading.Event()

        # Vitesse (ticks par seconde)
        self.target_tps = 2.0  # 2 ticks/seconde par défaut
        self.speed_multiplier = 1.0

        # Stats
        self.ticks_executed = 0
        self.actual_tps = 0.0
        self._last_tick_time = 0.0

    def start(self):
        """Démarre la simulation en mode continu."""
        if self.state != SimulationState.STOPPED:
            return

        self.state = SimulationState.RUNNING
        self._stop_event.clear()
        self._pause_event.clear()

        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()

    def pause(self):
        """Met en pause."""
        if self.state == SimulationState.RUNNING:
            self.state = SimulationState.PAUSED
            self._pause_event.set()

    def resume(self):
        """Reprend depuis la pause."""
        if self.state == SimulationState.PAUSED:
            self.state = SimulationState.RUNNING
            self._pause_event.clear()

    def stop(self):
        """Arrête complètement."""
        if self.state == SimulationState.STOPPED:
            return

        self.state = SimulationState.STOPPED
        self._stop_event.set()
        self._pause_event.clear()

        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2.0)

        self._thread = None

    def set_speed(self, multiplier: float):
        """
        Définit le multiplicateur de vitesse.

        Args:
            multiplier: 0.5 = moitié vitesse, 2.0 = double vitesse
        """
        self.speed_multiplier = max(0.1, min(10.0, multiplier))

    def step(self):
        """Exécute un seul tick (mode pas-à-pas)."""
        if self.state == SimulationState.RUNNING:
            return  # Ne pas step si déjà en cours

        self._execute_tick()

    def _run_loop(self):
        """Boucle principale (exécutée dans un thread)."""
        while not self._stop_event.is_set():
            # Attendre si en pause
            if self._pause_event.is_set():
                time.sleep(0.1)
                continue

            # Exécuter le tick
            tick_start = time.time()
            self._execute_tick()
            tick_duration = time.time() - tick_start

            # Calculer le délai pour respecter la vitesse cible
            target_delay = (1.0 / (self.target_tps * self.speed_multiplier))
            sleep_time = max(0.0, target_delay - tick_duration)

            if sleep_time > 0:
                time.sleep(sleep_time)

            # Calculer TPS réel
            if self._last_tick_time > 0:
                elapsed = time.time() - self._last_tick_time
                if elapsed > 0:
                    self.actual_tps = 1.0 / elapsed

            self._last_tick_time = time.time()

    def _execute_tick(self):
        """Exécute un tick unique."""
        try:
            self.tick_callback()
            self.ticks_executed += 1
        except Exception as e:
            print(f"[ERREUR] Tick échoué: {e}")
            import traceback
            traceback.print_exc()

    def get_status(self) -> dict:
        """Retourne le statut actuel."""
        return {
            'state': self.state.value,
            'is_running': self.state == SimulationState.RUNNING,
            'is_paused': self.state == SimulationState.PAUSED,
            'ticks_executed': self.ticks_executed,
            'speed_multiplier': self.speed_multiplier,
            'target_tps': self.target_tps * self.speed_multiplier,
            'actual_tps': self.actual_tps
        }
