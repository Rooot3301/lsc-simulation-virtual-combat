"""
Tours - points stratégiques contrôlés par XANA.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List
from .entity import Entity, EntityType


class TowerState(Enum):
    """États d'une tour."""
    INACTIVE = "inactive"
    ACTIVE = "active"
    CONTESTED = "contestée"
    CORRUPTED = "corrompue"
    DEACTIVATED = "désactivée"


@dataclass
class Tower(Entity):
    """Représente une tour contrôlée par XANA."""

    state: TowerState = TowerState.INACTIVE
    activation_level: float = 0.0  # 0.0 à 1.0
    corruption_radius: float = 5.0
    corruption_strength: float = 0.1
    defense_rating: float = 10.0

    # Défense
    defending_monsters: List[str] = field(default_factory=list)
    is_guarded: bool = False

    # Activité
    ticks_active: int = 0
    times_activated: int = 0
    times_deactivated: int = 0

    def __post_init__(self):
        """Initialisation de la tour."""
        super().__post_init__()
        self.entity_type = EntityType.TOWER
        self.max_health = 100.0
        self.health = 100.0

    def activate(self):
        """Active la tour."""
        if self.state == TowerState.INACTIVE or self.state == TowerState.DEACTIVATED:
            self.state = TowerState.ACTIVE
            self.activation_level = 1.0
            self.times_activated += 1

    def deactivate(self):
        """Désactive la tour."""
        if self.state == TowerState.ACTIVE or self.state == TowerState.CORRUPTED:
            self.state = TowerState.DEACTIVATED
            self.activation_level = 0.0
            self.times_deactivated += 1
            self.defending_monsters.clear()

    def contest(self):
        """Marque la tour comme contestée."""
        if self.state == TowerState.ACTIVE:
            self.state = TowerState.CONTESTED

    def corrupt(self):
        """Corrompt complètement la tour."""
        self.state = TowerState.CORRUPTED
        self.activation_level = 1.0
        self.corruption_strength *= 1.5

    def add_defender(self, monster_id: str):
        """Ajoute un monstre défenseur."""
        if monster_id not in self.defending_monsters:
            self.defending_monsters.append(monster_id)
            self.is_guarded = True

    def remove_defender(self, monster_id: str):
        """Retire un monstre défenseur."""
        if monster_id in self.defending_monsters:
            self.defending_monsters.remove(monster_id)
            if not self.defending_monsters:
                self.is_guarded = False

    def update(self):
        """Met à jour l'état de la tour."""
        if self.state == TowerState.ACTIVE:
            self.ticks_active += 1

    def get_corruption_output(self) -> float:
        """Calcule la corruption émise par la tour."""
        if self.state in [TowerState.ACTIVE, TowerState.CORRUPTED]:
            multiplier = 1.5 if self.state == TowerState.CORRUPTED else 1.0
            return self.corruption_strength * self.activation_level * multiplier
        return 0.0

    def is_vulnerable(self) -> bool:
        """Détermine si la tour est vulnérable."""
        return not self.is_guarded or len(self.defending_monsters) < 2

    def get_strategic_value(self) -> float:
        """Calcule la valeur stratégique de la tour."""
        value = 10.0
        if self.state == TowerState.ACTIVE:
            value += 5.0
        if self.state == TowerState.CORRUPTED:
            value += 10.0
        value += len(self.defending_monsters) * 2.0
        value += self.ticks_active * 0.1
        return value

    def to_dict(self) -> dict:
        """Convertit la tour en dictionnaire."""
        base_dict = super().to_dict()
        base_dict.update({
            'state': self.state.value,
            'activation_level': self.activation_level,
            'corruption_radius': self.corruption_radius,
            'corruption_strength': self.corruption_strength,
            'defense_rating': self.defense_rating,
            'defending_monsters': self.defending_monsters,
            'is_guarded': self.is_guarded,
            'ticks_active': self.ticks_active,
            'times_activated': self.times_activated,
            'times_deactivated': self.times_deactivated
        })
        return base_dict
