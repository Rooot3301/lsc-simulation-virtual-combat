"""
Classe de base pour toutes les entités du monde virtuel.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional
import uuid


class EntityType(Enum):
    """Types d'entités."""
    AGENT = "agent"
    MONSTER = "monstre"
    TOWER = "tour"
    SKID = "skid"
    XANA = "xana"


@dataclass
class Entity:
    """Classe de base pour toutes les entités."""

    id: str
    name: str
    sector: str
    entity_type: EntityType = EntityType.AGENT
    health: float = 100.0
    max_health: float = 100.0
    position_x: float = 0.0
    position_y: float = 0.0
    is_active: bool = True
    is_destroyed: bool = False

    def __post_init__(self):
        """Génère un ID si nécessaire."""
        if not self.id:
            self.id = f"{self.entity_type.value}_{uuid.uuid4().hex[:8]}"

    def take_damage(self, amount: float) -> bool:
        """Inflige des dégâts à l'entité."""
        if self.is_destroyed:
            return False

        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.is_destroyed = True
            self.is_active = False
            return True
        return False

    def heal(self, amount: float):
        """Soigne l'entité."""
        if not self.is_destroyed:
            self.health = min(self.max_health, self.health + amount)

    def get_health_percentage(self) -> float:
        """Retourne le pourcentage de santé."""
        return (self.health / self.max_health) * 100 if self.max_health > 0 else 0

    def move_to(self, x: float, y: float):
        """Déplace l'entité."""
        self.position_x = x
        self.position_y = y

    def change_sector(self, new_sector: str):
        """Change le secteur de l'entité."""
        self.sector = new_sector

    def to_dict(self) -> dict:
        """Convertit l'entité en dictionnaire."""
        return {
            'id': self.id,
            'name': self.name,
            'entity_type': self.entity_type.value,
            'sector': self.sector,
            'health': self.health,
            'max_health': self.max_health,
            'position_x': self.position_x,
            'position_y': self.position_y,
            'is_active': self.is_active,
            'is_destroyed': self.is_destroyed
        }
