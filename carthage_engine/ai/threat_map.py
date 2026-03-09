"""
Carte des menaces - évaluation tactique du terrain.
"""

from dataclasses import dataclass, field
from typing import Dict, List
from enum import Enum


class ThreatLevel(Enum):
    """Niveaux de menace."""
    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class ThreatZone:
    """Zone de menace."""

    location: str
    threat_level: ThreatLevel = ThreatLevel.NONE
    threat_score: float = 0.0
    enemy_count: int = 0
    enemy_strength: float = 0.0
    strategic_value: float = 0.0

    def update_threat_level(self):
        """Met à jour le niveau de menace."""
        if self.threat_score >= 8.0:
            self.threat_level = ThreatLevel.CRITICAL
        elif self.threat_score >= 6.0:
            self.threat_level = ThreatLevel.HIGH
        elif self.threat_score >= 3.0:
            self.threat_level = ThreatLevel.MEDIUM
        elif self.threat_score >= 1.0:
            self.threat_level = ThreatLevel.LOW
        else:
            self.threat_level = ThreatLevel.NONE


class ThreatMap:
    """Carte globale des menaces."""

    def __init__(self):
        self.zones: Dict[str, ThreatZone] = {}

    def register_zone(self, location: str):
        """Enregistre une nouvelle zone."""
        if location not in self.zones:
            self.zones[location] = ThreatZone(location=location)

    def update_zone_threat(
        self,
        location: str,
        enemy_count: int,
        enemy_strength: float,
        strategic_value: float
    ):
        """Met à jour la menace d'une zone."""
        if location not in self.zones:
            self.register_zone(location)

        zone = self.zones[location]
        zone.enemy_count = enemy_count
        zone.enemy_strength = enemy_strength
        zone.strategic_value = strategic_value

        # Calcule le score de menace
        zone.threat_score = (
            enemy_count * 0.3 +
            enemy_strength * 0.5 +
            strategic_value * 0.2
        )

        zone.update_threat_level()

    def get_highest_threat_zone(self) -> ThreatZone:
        """Retourne la zone la plus menacée."""
        if not self.zones:
            return None
        return max(self.zones.values(), key=lambda z: z.threat_score)

    def get_zones_by_threat_level(self, level: ThreatLevel) -> List[ThreatZone]:
        """Retourne toutes les zones d'un niveau de menace donné."""
        return [z for z in self.zones.values() if z.threat_level == level]

    def get_critical_zones(self) -> List[ThreatZone]:
        """Retourne toutes les zones critiques."""
        return self.get_zones_by_threat_level(ThreatLevel.CRITICAL)

    def get_safe_zones(self) -> List[ThreatZone]:
        """Retourne toutes les zones sûres."""
        return [z for z in self.zones.values()
                if z.threat_level in [ThreatLevel.NONE, ThreatLevel.LOW]]

    def get_total_threat_score(self) -> float:
        """Calcule le score de menace total."""
        return sum(z.threat_score for z in self.zones.values())

    def clear_zone(self, location: str):
        """Efface les menaces d'une zone."""
        if location in self.zones:
            zone = self.zones[location]
            zone.enemy_count = 0
            zone.enemy_strength = 0.0
            zone.threat_score = 0.0
            zone.update_threat_level()

    def is_zone_safe(self, location: str) -> bool:
        """Détermine si une zone est sûre."""
        if location not in self.zones:
            return True
        return self.zones[location].threat_level in [ThreatLevel.NONE, ThreatLevel.LOW]

    def get_zone(self, location: str) -> ThreatZone:
        """Récupère une zone."""
        if location not in self.zones:
            self.register_zone(location)
        return self.zones[location]
