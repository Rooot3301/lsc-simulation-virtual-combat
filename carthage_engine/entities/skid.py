"""
Skid - véhicule stratégique de navigation.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
from .entity import Entity, EntityType


class SkidMode(Enum):
    """Modes de fonctionnement du Skid."""
    IDLE = "repos"
    NAVIGATION = "navigation"
    COMBAT = "combat"
    SCANNING = "scan"
    RETREAT = "repli"
    EMERGENCY = "urgence"
    INFILTRATION = "infiltration"  # v2.0
    SILENCE = "silence"  # v2.0


class SkidMission(Enum):
    """Types de missions du Skid."""
    NONE = "aucune"
    EXPLORATION = "exploration"
    TRANSPORT = "transport"
    RECONNAISSANCE = "reconnaissance"
    INTERCEPT = "interception"
    EXTRACTION = "extraction"
    SUPPORT = "support"  # v2.0
    REPLI = "repli"  # v2.0


@dataclass
class Skid(Entity):
    """Représente le Skid - véhicule stratégique."""

    mode: SkidMode = SkidMode.IDLE
    mission: SkidMission = SkidMission.NONE

    # Caractéristiques techniques
    hull_integrity: float = 100.0
    max_hull_integrity: float = 100.0
    energy: float = 100.0
    max_energy: float = 100.0
    speed: float = 2.0
    scan_range: float = 10.0

    # Navigation
    current_node: str = "N-SEC5-GATE"
    destination_node: str = None
    route: List[str] = field(default_factory=list)
    route_progress: int = 0

    # Passagers
    passengers: List[str] = field(default_factory=list)
    max_passengers: int = 4

    # Risques
    danger_level: float = 0.0
    under_attack: bool = False
    enemies_detected: int = 0

    # v2.0 - Systèmes avancés
    signature: float = 0.8  # Signature de détection (0.0-1.0)
    navigation_mode: str = "normal"  # normal, stealth, aggressive
    autonomous: bool = False  # Mode autonome
    module_status: dict = field(default_factory=lambda: {
        'shields': 100.0,
        'engines': 100.0,
        'sensors': 100.0,
        'weapons': 100.0
    })

    def __post_init__(self):
        """Initialisation du Skid."""
        super().__post_init__()
        self.entity_type = EntityType.SKID
        self.max_health = 200.0
        self.health = 200.0

    def set_mission(self, mission: SkidMission, destination: str = None):
        """Définit une mission."""
        self.mission = mission
        if destination:
            self.destination_node = destination
        self.mode = SkidMode.NAVIGATION

    def set_route(self, route: List[str]):
        """Définit un itinéraire."""
        self.route = route
        self.route_progress = 0
        if route:
            self.destination_node = route[-1]

    def advance_route(self):
        """Avance sur l'itinéraire."""
        if self.route and self.route_progress < len(self.route) - 1:
            self.route_progress += 1
            self.current_node = self.route[self.route_progress]
            self.consume_energy(5.0)

    def board_passenger(self, agent_id: str) -> bool:
        """Embarque un passager."""
        if len(self.passengers) < self.max_passengers:
            if agent_id not in self.passengers:
                self.passengers.append(agent_id)
                return True
        return False

    def disembark_passenger(self, agent_id: str) -> bool:
        """Débarque un passager."""
        if agent_id in self.passengers:
            self.passengers.remove(agent_id)
            return True
        return False

    def disembark_all(self):
        """Débarque tous les passagers."""
        self.passengers.clear()

    def consume_energy(self, amount: float):
        """Consomme de l'énergie."""
        self.energy = max(0.0, self.energy - amount)
        if self.energy == 0.0:
            self.mode = SkidMode.EMERGENCY

    def recharge_energy(self, amount: float):
        """Recharge l'énergie."""
        self.energy = min(self.max_energy, self.energy + amount)
        if self.mode == SkidMode.EMERGENCY and self.energy > 20.0:
            self.mode = SkidMode.IDLE

    def damage_hull(self, amount: float):
        """Endommage la coque."""
        self.hull_integrity = max(0.0, self.hull_integrity - amount)
        self.health = self.hull_integrity

        if self.hull_integrity < 30.0:
            self.mode = SkidMode.RETREAT
        elif self.hull_integrity < 50.0:
            self.mode = SkidMode.EMERGENCY

        if self.hull_integrity == 0.0:
            self.is_destroyed = True
            self.is_active = False

    def repair_hull(self, amount: float):
        """Répare la coque."""
        self.hull_integrity = min(self.max_hull_integrity, self.hull_integrity + amount)
        self.health = self.hull_integrity

    def scan_area(self) -> dict:
        """Scanne la zone autour du Skid."""
        self.mode = SkidMode.SCANNING
        self.consume_energy(10.0)

        return {
            'current_node': self.current_node,
            'scan_range': self.scan_range,
            'danger_level': self.danger_level,
            'enemies_detected': self.enemies_detected
        }

    def engage_combat(self):
        """Passe en mode combat."""
        self.mode = SkidMode.COMBAT
        self.under_attack = True

    def retreat(self):
        """Ordonne le repli."""
        self.mode = SkidMode.RETREAT
        self.mission = SkidMission.NONE

    def evaluate_risk(self, corridor_danger: float, enemy_count: int) -> float:
        """Évalue le risque actuel."""
        risk = corridor_danger * 0.5
        risk += (enemy_count / 10.0) * 0.3
        risk += (1.0 - self.hull_integrity / self.max_hull_integrity) * 0.2

        self.danger_level = min(1.0, risk)
        self.enemies_detected = enemy_count

        return self.danger_level

    def is_operational(self) -> bool:
        """Détermine si le Skid est opérationnel."""
        return (
            not self.is_destroyed and
            self.hull_integrity > 0 and
            self.energy > 0 and
            self.mode != SkidMode.EMERGENCY
        )

    def get_status_summary(self) -> str:
        """Retourne un résumé du statut."""
        return (
            f"Mode: {self.mode.value} | "
            f"Mission: {self.mission.value} | "
            f"Coque: {self.hull_integrity:.0f}% | "
            f"Énergie: {self.energy:.0f}% | "
            f"Position: {self.current_node} | "
            f"Passagers: {len(self.passengers)}/{self.max_passengers}"
        )

    def to_dict(self) -> dict:
        """Convertit le Skid en dictionnaire."""
        base_dict = super().to_dict()
        base_dict.update({
            'mode': self.mode.value,
            'mission': self.mission.value,
            'hull_integrity': self.hull_integrity,
            'max_hull_integrity': self.max_hull_integrity,
            'energy': self.energy,
            'max_energy': self.max_energy,
            'speed': self.speed,
            'scan_range': self.scan_range,
            'current_node': self.current_node,
            'destination_node': self.destination_node,
            'route': self.route,
            'route_progress': self.route_progress,
            'passengers': self.passengers,
            'max_passengers': self.max_passengers,
            'danger_level': self.danger_level,
            'under_attack': self.under_attack,
            'enemies_detected': self.enemies_detected
        })
        return base_dict
