"""
Définition des secteurs du monde virtuel.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict


class SectorType(Enum):
    """Types de secteurs."""
    FOREST = "Forêt"
    DESERT = "Désert"
    ICE = "Banquise"
    MOUNTAIN = "Montagne"
    SECTOR5 = "Secteur5"
    DIGITAL_SEA = "Mer Numérique"
    NETWORK = "Réseau"


@dataclass
class Sector:
    """Représente un secteur du monde virtuel."""

    name: str
    sector_type: SectorType
    corruption_level: float = 0.0  # 0.0 à 1.0
    tower_ids: List[str] = field(default_factory=list)
    entity_ids: List[str] = field(default_factory=list)
    connected_sectors: List[str] = field(default_factory=list)
    threat_score: float = 0.0
    is_accessible: bool = True

    # Caractéristiques du secteur
    difficulty: float = 1.0
    spawn_rate: float = 1.0
    corruption_resistance: float = 1.0

    def add_tower(self, tower_id: str):
        """Ajoute une tour au secteur."""
        if tower_id not in self.tower_ids:
            self.tower_ids.append(tower_id)

    def remove_tower(self, tower_id: str):
        """Retire une tour du secteur."""
        if tower_id in self.tower_ids:
            self.tower_ids.remove(tower_id)

    def add_entity(self, entity_id: str):
        """Ajoute une entité au secteur."""
        if entity_id not in self.entity_ids:
            self.entity_ids.append(entity_id)

    def remove_entity(self, entity_id: str):
        """Retire une entité du secteur."""
        if entity_id in self.entity_ids:
            self.entity_ids.remove(entity_id)

    def increase_corruption(self, amount: float):
        """Augmente le niveau de corruption."""
        self.corruption_level = min(1.0, self.corruption_level + amount)
        self._update_threat_score()

    def decrease_corruption(self, amount: float):
        """Diminue le niveau de corruption."""
        self.corruption_level = max(0.0, self.corruption_level - amount)
        self._update_threat_score()

    def _update_threat_score(self):
        """Met à jour le score de menace."""
        base_threat = self.corruption_level * 10
        tower_threat = len(self.tower_ids) * 2
        entity_threat = len(self.entity_ids) * 0.5
        self.threat_score = base_threat + tower_threat + entity_threat

    def get_active_tower_count(self, towers: Dict) -> int:
        """Compte le nombre de tours actives dans le secteur."""
        count = 0
        for tower_id in self.tower_ids:
            if tower_id in towers and towers[tower_id].is_active:
                count += 1
        return count

    def is_dominated_by_xana(self) -> bool:
        """Détermine si le secteur est dominé par XANA."""
        return self.corruption_level > 0.7

    def is_safe(self) -> bool:
        """Détermine si le secteur est sûr."""
        return self.corruption_level < 0.2 and self.threat_score < 5.0

    def to_dict(self) -> dict:
        """Convertit en dictionnaire."""
        return {
            'name': self.name,
            'sector_type': self.sector_type.value,
            'corruption_level': self.corruption_level,
            'tower_ids': self.tower_ids,
            'entity_ids': self.entity_ids,
            'connected_sectors': self.connected_sectors,
            'threat_score': self.threat_score,
            'is_accessible': self.is_accessible,
            'difficulty': self.difficulty,
            'spawn_rate': self.spawn_rate,
            'corruption_resistance': self.corruption_resistance
        }


def create_default_sectors() -> Dict[str, Sector]:
    """Crée les secteurs par défaut du monde."""
    sectors = {}

    # Secteur Forêt
    sectors['forest'] = Sector(
        name='Forêt',
        sector_type=SectorType.FOREST,
        connected_sectors=['desert', 'ice', 'sector5'],
        difficulty=1.0,
        corruption_resistance=0.9
    )

    # Secteur Désert
    sectors['desert'] = Sector(
        name='Désert',
        sector_type=SectorType.DESERT,
        connected_sectors=['forest', 'mountain', 'sector5'],
        difficulty=1.2,
        corruption_resistance=0.85
    )

    # Secteur Banquise
    sectors['ice'] = Sector(
        name='Banquise',
        sector_type=SectorType.ICE,
        connected_sectors=['forest', 'mountain', 'sector5'],
        difficulty=1.3,
        corruption_resistance=0.8
    )

    # Secteur Montagne
    sectors['mountain'] = Sector(
        name='Montagne',
        sector_type=SectorType.MOUNTAIN,
        connected_sectors=['desert', 'ice', 'sector5'],
        difficulty=1.5,
        corruption_resistance=0.75
    )

    # Secteur 5
    sectors['sector5'] = Sector(
        name='Secteur 5',
        sector_type=SectorType.SECTOR5,
        connected_sectors=['forest', 'desert', 'ice', 'mountain', 'network'],
        difficulty=2.0,
        corruption_resistance=0.6
    )

    # Mer Numérique
    sectors['digital_sea'] = Sector(
        name='Mer Numérique',
        sector_type=SectorType.DIGITAL_SEA,
        connected_sectors=['network'],
        difficulty=2.5,
        corruption_resistance=0.5
    )

    # Réseau
    sectors['network'] = Sector(
        name='Réseau',
        sector_type=SectorType.NETWORK,
        connected_sectors=['sector5', 'digital_sea'],
        difficulty=3.0,
        corruption_resistance=0.4
    )

    return sectors
