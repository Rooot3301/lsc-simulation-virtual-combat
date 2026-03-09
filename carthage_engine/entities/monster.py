"""
Monstres - créatures de XANA.
"""

from dataclasses import dataclass
from enum import Enum
from .entity import Entity, EntityType


class MonsterType(Enum):
    """Types de monstres."""
    KANKRELAT = "kankrelat"
    BLOK = "blok"
    HORNET = "hornet"
    MEGATANK = "megatank"
    KRABE = "krabe"
    MANTA = "manta"
    TARANTULA = "tarantula"


class MonsterBehavior(Enum):
    """Comportements des monstres."""
    IDLE = "inactif"
    PATROL = "patrouille"
    GUARD = "garde"
    ATTACK = "attaque"
    PURSUE = "poursuite"
    RETREAT = "repli"


@dataclass
class Monster(Entity):
    """Représente un monstre de XANA."""

    monster_type: MonsterType = MonsterType.KANKRELAT
    behavior: MonsterBehavior = MonsterBehavior.PATROL
    damage: float = 5.0
    defense: float = 2.0
    speed: float = 1.0
    attack_range: float = 1.0
    detection_range: float = 5.0

    # Combat
    target_id: str = None
    in_combat: bool = False

    # Affectation
    assigned_tower: str = None
    patrol_route: list = None

    def __post_init__(self):
        """Initialisation des statistiques selon le type."""
        super().__post_init__()
        self.entity_type = EntityType.MONSTER

        # Statistiques selon le type de monstre
        if self.monster_type == MonsterType.KANKRELAT:
            self.max_health = 30.0
            self.health = 30.0
            self.damage = 5.0
            self.defense = 2.0
            self.speed = 1.2
            self.attack_range = 1.0
            self.detection_range = 4.0

        elif self.monster_type == MonsterType.BLOK:
            self.max_health = 50.0
            self.health = 50.0
            self.damage = 8.0
            self.defense = 5.0
            self.speed = 0.8
            self.attack_range = 3.0
            self.detection_range = 6.0

        elif self.monster_type == MonsterType.HORNET:
            self.max_health = 40.0
            self.health = 40.0
            self.damage = 10.0
            self.defense = 3.0
            self.speed = 1.5
            self.attack_range = 1.5
            self.detection_range = 7.0

        elif self.monster_type == MonsterType.MEGATANK:
            self.max_health = 150.0
            self.health = 150.0
            self.damage = 20.0
            self.defense = 15.0
            self.speed = 0.5
            self.attack_range = 5.0
            self.detection_range = 8.0

        elif self.monster_type == MonsterType.KRABE:
            self.max_health = 80.0
            self.health = 80.0
            self.damage = 12.0
            self.defense = 8.0
            self.speed = 0.9
            self.attack_range = 2.0
            self.detection_range = 5.0

        elif self.monster_type == MonsterType.MANTA:
            self.max_health = 100.0
            self.health = 100.0
            self.damage = 15.0
            self.defense = 10.0
            self.speed = 1.3
            self.attack_range = 4.0
            self.detection_range = 9.0

        elif self.monster_type == MonsterType.TARANTULA:
            self.max_health = 60.0
            self.health = 60.0
            self.damage = 14.0
            self.defense = 6.0
            self.speed = 1.1
            self.attack_range = 6.0
            self.detection_range = 10.0

    def assign_to_tower(self, tower_id: str):
        """Affecte le monstre à la défense d'une tour."""
        self.assigned_tower = tower_id
        self.behavior = MonsterBehavior.GUARD

    def set_patrol(self, route: list):
        """Définit une route de patrouille."""
        self.patrol_route = route
        self.behavior = MonsterBehavior.PATROL

    def engage_target(self, target_id: str):
        """Engage un combat avec une cible."""
        self.target_id = target_id
        self.behavior = MonsterBehavior.ATTACK
        self.in_combat = True

    def pursue_target(self, target_id: str):
        """Poursuit une cible."""
        self.target_id = target_id
        self.behavior = MonsterBehavior.PURSUE

    def retreat(self):
        """Ordonne au monstre de battre en retraite."""
        self.behavior = MonsterBehavior.RETREAT
        self.in_combat = False
        self.target_id = None

    def is_aggressive(self) -> bool:
        """Détermine si le monstre est agressif."""
        return self.behavior in [MonsterBehavior.ATTACK, MonsterBehavior.PURSUE]

    def get_threat_level(self) -> float:
        """Calcule le niveau de menace du monstre."""
        threat = (self.damage * 0.4 + self.defense * 0.2 + self.health * 0.3 + self.speed * 0.1)
        return threat / 10.0

    def to_dict(self) -> dict:
        """Convertit le monstre en dictionnaire."""
        base_dict = super().to_dict()
        base_dict.update({
            'monster_type': self.monster_type.value,
            'behavior': self.behavior.value,
            'damage': self.damage,
            'defense': self.defense,
            'speed': self.speed,
            'attack_range': self.attack_range,
            'detection_range': self.detection_range,
            'target_id': self.target_id,
            'in_combat': self.in_combat,
            'assigned_tower': self.assigned_tower
        })
        return base_dict
