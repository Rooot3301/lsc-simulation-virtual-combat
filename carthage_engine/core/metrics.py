"""
Système de métriques complètes pour CARTHAGE ENGINE v2.0.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any
from datetime import datetime


@dataclass
class SimulationMetrics:
    """Métriques globales de la simulation."""

    # Métriques temps
    current_tick: int = 0
    simulation_time: float = 0.0
    start_time: datetime = field(default_factory=datetime.now)

    # Statut simulation
    is_running: bool = False
    is_paused: bool = False
    simulation_speed: float = 1.0

    # Métriques monde
    global_threat: float = 0.0
    global_corruption: float = 0.0
    global_stability: float = 1.0

    # Secteurs
    sectors_stable: int = 0
    sectors_contested: int = 0
    sectors_corrupted: int = 0
    sectors_dominated: int = 0

    # Tours
    active_towers: int = 0
    corrupted_towers: int = 0
    deactivated_towers: int = 0

    # XANA
    xana_power_level: float = 0.0
    xana_influence: float = 0.0
    xana_resources: int = 0
    xana_active_doctrine: str = "INCONNU"
    xana_current_goal: str = "AUCUN"
    xana_plan_phase: str = "AUCUNE"
    xana_active_plans: int = 0

    # Monstres
    active_monsters: int = 0
    destroyed_monsters: int = 0
    deployed_monsters_total: int = 0

    # Agents
    active_agents: int = 0
    incapacitated_agents: int = 0
    corrupted_agents: int = 0
    average_agent_health: float = 100.0
    average_agent_morale: float = 1.0
    average_agent_stress: float = 0.0
    average_agent_fatigue: float = 0.0
    average_agent_corruption: float = 0.0

    # Skid
    skid_hull_integrity: float = 100.0
    skid_energy: float = 100.0
    skid_mode: str = "REPOS"
    skid_danger_level: float = 0.0
    skid_passengers: int = 0

    # Événements
    total_events: int = 0
    critical_events: int = 0
    alert_events: int = 0
    event_rate: float = 0.0  # événements par tick

    # Opérations
    successful_deactivations: int = 0
    failed_deactivations: int = 0
    successful_missions: int = 0
    failed_missions: int = 0

    # Corruption
    corruption_attempts: int = 0
    successful_corruptions: int = 0
    corruption_resistance: int = 0

    # Combat
    combat_engagements: int = 0
    agent_victories: int = 0
    agent_defeats: int = 0

    # Réseau
    network_stability: float = 1.0
    active_routes: int = 0
    corrupted_routes: int = 0

    def to_dict(self) -> Dict[str, Any]:
        """Convertit en dictionnaire."""
        return {
            'tick': self.current_tick,
            'time': self.simulation_time,
            'running': self.is_running,
            'paused': self.is_paused,
            'speed': self.simulation_speed,
            'threat': self.global_threat,
            'corruption': self.global_corruption,
            'stability': self.global_stability,
            'xana': {
                'power': self.xana_power_level,
                'influence': self.xana_influence,
                'resources': self.xana_resources,
                'doctrine': self.xana_active_doctrine,
                'goal': self.xana_current_goal,
                'plans': self.xana_active_plans
            },
            'agents': {
                'active': self.active_agents,
                'health': self.average_agent_health,
                'morale': self.average_agent_morale,
                'stress': self.average_agent_stress,
                'fatigue': self.average_agent_fatigue,
                'corruption': self.average_agent_corruption
            },
            'sectors': {
                'stable': self.sectors_stable,
                'contested': self.sectors_contested,
                'corrupted': self.sectors_corrupted,
                'dominated': self.sectors_dominated
            }
        }

    def summary(self) -> str:
        """Résumé textuel français."""
        lines = [
            f"Tick {self.current_tick} | Menace: {self.global_threat:.0%} | Corruption: {self.global_corruption:.0%}",
            f"XANA: {self.xana_active_doctrine} | Puissance: {self.xana_power_level:.1f} | Plans: {self.xana_active_plans}",
            f"Agents: {self.active_agents}/{self.active_agents + self.incapacitated_agents} | Moral: {self.average_agent_morale:.0%}",
            f"Secteurs: {self.sectors_stable} stables, {self.sectors_contested} contestés, {self.sectors_corrupted} corrompus"
        ]
        return '\n'.join(lines)


class MetricsTracker:
    """Suivi et calcul des métriques."""

    def __init__(self):
        self.current = SimulationMetrics()
        self.history: List[SimulationMetrics] = []
        self.history_max_size = 1000

    def snapshot(self):
        """Prend un snapshot des métriques actuelles."""
        import copy
        snapshot = copy.deepcopy(self.current)
        self.history.append(snapshot)

        # Limite la taille de l'historique
        if len(self.history) > self.history_max_size:
            self.history = self.history[-self.history_max_size:]

    def update_from_world(self, world: Any, xana_ai: Any = None):
        """Met à jour les métriques depuis l'état du monde."""

        # Monde
        self.current.global_corruption = world.global_corruption
        self.current.global_threat = world.global_threat

        # Secteurs
        stable = contested = corrupted = dominated = 0
        for sector in world.sectors.values():
            if sector.is_dominated_by_xana():
                dominated += 1
                corrupted += 1
            elif not sector.is_safe():
                contested += 1
            else:
                stable += 1

        self.current.sectors_stable = stable
        self.current.sectors_contested = contested
        self.current.sectors_corrupted = corrupted
        self.current.sectors_dominated = dominated

        # Tours
        active = 0
        for tower in world.towers.values():
            if tower.is_active:
                active += 1
        self.current.active_towers = active

        # XANA
        if world.xana:
            self.current.xana_power_level = world.xana.power_level
            self.current.xana_influence = world.xana.influence
            self.current.xana_resources = world.xana.resources
            self.current.xana_active_plans = len(world.xana.active_plans)

            if xana_ai and xana_ai.doctrine:
                self.current.xana_active_doctrine = xana_ai.doctrine.primary_rule.value.upper()

        # Agents
        agents = list(world.agents.values())
        self.current.active_agents = len([a for a in agents if a.is_operational()])
        self.current.incapacitated_agents = len([a for a in agents if not a.is_operational()])

        if agents:
            self.current.average_agent_health = sum(a.health / a.max_health for a in agents) / len(agents) * 100
            self.current.average_agent_corruption = sum(a.corruption_level for a in agents) / len(agents)

            if hasattr(agents[0], 'psychological_state'):
                self.current.average_agent_stress = sum(a.psychological_state.stress for a in agents) / len(agents)
                self.current.average_agent_fatigue = sum(a.psychological_state.fatigue for a in agents) / len(agents)
                self.current.average_agent_morale = sum(1.0 - a.psychological_state.stress for a in agents) / len(agents)

        # Skid
        if world.skid:
            self.current.skid_hull_integrity = world.skid.hull_integrity
            self.current.skid_energy = world.skid.energy
            self.current.skid_mode = world.skid.mode.value
            self.current.skid_danger_level = world.skid.danger_level
            self.current.skid_passengers = len(world.skid.passengers)

        # Monstres
        self.current.active_monsters = len([m for m in world.monsters.values() if not m.is_destroyed])
        self.current.destroyed_monsters = len([m for m in world.monsters.values() if m.is_destroyed])

    def get_history_range(self, start_tick: int, end_tick: int) -> List[SimulationMetrics]:
        """Récupère l'historique sur une plage de ticks."""
        return [m for m in self.history if start_tick <= m.current_tick <= end_tick]

    def get_last_n(self, n: int) -> List[SimulationMetrics]:
        """Récupère les N dernières métriques."""
        return self.history[-n:] if len(self.history) >= n else self.history

    def calculate_trends(self, window: int = 10) -> Dict[str, float]:
        """Calcule les tendances sur une fenêtre."""
        if len(self.history) < 2:
            return {}

        recent = self.get_last_n(window)
        if len(recent) < 2:
            return {}

        trends = {}
        trends['corruption_trend'] = recent[-1].global_corruption - recent[0].global_corruption
        trends['threat_trend'] = recent[-1].global_threat - recent[0].global_threat
        trends['xana_power_trend'] = recent[-1].xana_power_level - recent[0].xana_power_level
        trends['morale_trend'] = recent[-1].average_agent_morale - recent[0].average_agent_morale

        return trends
