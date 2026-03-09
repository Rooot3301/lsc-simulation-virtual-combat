"""
Agents - combattants défensifs contre XANA.
"""

from dataclasses import dataclass, field
from enum import Enum
from .entity import Entity, EntityType


class AgentType(Enum):
    """Types d'agents."""
    WARRIOR = "guerrier"
    SCOUT = "éclaireur"
    HACKER = "hackeur"
    SUPPORT = "soutien"


class AgentState(Enum):
    """États d'un agent."""
    IDLE = "inactif"
    MOVING = "en_déplacement"
    FIGHTING = "en_combat"
    HACKING = "piratage"
    RECOVERING = "récupération"
    CORRUPTED = "corrompu"
    DESTROYED = "détruit"


class CorruptionStage(Enum):
    """Stades de corruption d'un agent."""
    CLEAN = "propre"
    EXPOSED = "exposé"
    DESTABILIZED = "déstabilisé"
    INFLUENCED = "influencé"
    PARTIALLY_CORRUPTED = "partiellement_corrompu"
    HEAVILY_CORRUPTED = "lourdement_corrompu"
    LOST = "perdu"


@dataclass
class PsychologicalState:
    """État psychologique d'un agent."""

    fatigue: float = 0.0  # 0.0 à 1.0
    stress: float = 0.0  # 0.0 à 1.0
    morale: float = 1.0  # 0.0 à 1.0
    resistance: float = 1.0  # 0.0 à 1.0
    isolation: float = 0.0  # 0.0 à 1.0
    corruption_exposure: float = 0.0  # 0.0 à 1.0
    trust_with_team: float = 1.0  # 0.0 à 1.0

    def get_overall_stability(self) -> float:
        """Calcule la stabilité globale."""
        stability = (
            (1.0 - self.fatigue) * 0.15 +
            (1.0 - self.stress) * 0.20 +
            self.morale * 0.20 +
            self.resistance * 0.20 +
            (1.0 - self.isolation) * 0.10 +
            (1.0 - self.corruption_exposure) * 0.10 +
            self.trust_with_team * 0.05
        )
        return max(0.0, min(1.0, stability))

    def is_vulnerable_to_corruption(self) -> bool:
        """Détermine si l'agent est vulnérable à la corruption."""
        return (
            self.stress > 0.6 or
            self.isolation > 0.7 or
            self.corruption_exposure > 0.5 or
            self.morale < 0.3 or
            self.fatigue > 0.8
        )


@dataclass
class Agent(Entity):
    """Représente un agent défensif."""

    agent_type: AgentType = AgentType.WARRIOR
    state: AgentState = AgentState.IDLE
    corruption_stage: CorruptionStage = CorruptionStage.CLEAN
    corruption_level: float = 0.0  # 0.0 à 1.0
    psychological_state: PsychologicalState = field(default_factory=PsychologicalState)

    # Statistiques de combat
    damage: float = 10.0
    defense: float = 5.0
    speed: float = 1.0
    hacking_skill: float = 0.5

    # Expérience
    experience: int = 0
    kills: int = 0
    towers_deactivated: int = 0
    missions_completed: int = 0

    # Combat
    in_combat: bool = False
    target_id: str = None

    def __post_init__(self):
        """Initialisation des statistiques selon le type."""
        super().__post_init__()
        self.entity_type = EntityType.AGENT

        # Ajuster les stats selon le type
        if self.agent_type == AgentType.WARRIOR:
            self.damage = 15.0
            self.defense = 8.0
            self.speed = 0.8
            self.hacking_skill = 0.3
            self.max_health = 120.0
            self.health = 120.0
        elif self.agent_type == AgentType.SCOUT:
            self.damage = 8.0
            self.defense = 4.0
            self.speed = 1.5
            self.hacking_skill = 0.5
            self.max_health = 80.0
            self.health = 80.0
        elif self.agent_type == AgentType.HACKER:
            self.damage = 5.0
            self.defense = 3.0
            self.speed = 1.0
            self.hacking_skill = 1.5
            self.max_health = 70.0
            self.health = 70.0
        elif self.agent_type == AgentType.SUPPORT:
            self.damage = 6.0
            self.defense = 6.0
            self.speed = 1.0
            self.hacking_skill = 0.8
            self.max_health = 100.0
            self.health = 100.0

    def increase_corruption(self, amount: float):
        """Augmente le niveau de corruption."""
        self.corruption_level = min(1.0, self.corruption_level + amount)
        self.psychological_state.corruption_exposure = self.corruption_level

        # Mise à jour du stade de corruption
        if self.corruption_level >= 0.9:
            self.corruption_stage = CorruptionStage.LOST
            self.state = AgentState.CORRUPTED
        elif self.corruption_level >= 0.75:
            self.corruption_stage = CorruptionStage.HEAVILY_CORRUPTED
        elif self.corruption_level >= 0.5:
            self.corruption_stage = CorruptionStage.PARTIALLY_CORRUPTED
        elif self.corruption_level >= 0.35:
            self.corruption_stage = CorruptionStage.INFLUENCED
        elif self.corruption_level >= 0.2:
            self.corruption_stage = CorruptionStage.DESTABILIZED
        elif self.corruption_level >= 0.1:
            self.corruption_stage = CorruptionStage.EXPOSED
        else:
            self.corruption_stage = CorruptionStage.CLEAN

    def decrease_corruption(self, amount: float):
        """Diminue le niveau de corruption."""
        self.corruption_level = max(0.0, self.corruption_level - amount)
        self.psychological_state.corruption_exposure = self.corruption_level

        # Mise à jour du stade
        if self.corruption_level < 0.9 and self.corruption_stage == CorruptionStage.LOST:
            self.corruption_stage = CorruptionStage.HEAVILY_CORRUPTED
            if self.state == AgentState.CORRUPTED:
                self.state = AgentState.RECOVERING

    def increase_stress(self, amount: float):
        """Augmente le stress."""
        self.psychological_state.stress = min(1.0, self.psychological_state.stress + amount)

    def decrease_stress(self, amount: float):
        """Diminue le stress."""
        self.psychological_state.stress = max(0.0, self.psychological_state.stress - amount)

    def increase_fatigue(self, amount: float):
        """Augmente la fatigue."""
        self.psychological_state.fatigue = min(1.0, self.psychological_state.fatigue + amount)

    def rest(self, amount: float):
        """Repose l'agent."""
        self.psychological_state.fatigue = max(0.0, self.psychological_state.fatigue - amount)

    def increase_morale(self, amount: float):
        """Augmente le moral."""
        self.psychological_state.morale = min(1.0, self.psychological_state.morale + amount)

    def decrease_morale(self, amount: float):
        """Diminue le moral."""
        self.psychological_state.morale = max(0.0, self.psychological_state.morale - amount)

    def is_corrupted(self) -> bool:
        """Détermine si l'agent est corrompu."""
        return self.corruption_stage in [
            CorruptionStage.HEAVILY_CORRUPTED,
            CorruptionStage.LOST
        ]

    def is_operational(self) -> bool:
        """Détermine si l'agent est opérationnel."""
        return (
            not self.is_destroyed and
            self.state != AgentState.CORRUPTED and
            self.corruption_stage != CorruptionStage.LOST and
            self.health > 0
        )

    def get_combat_effectiveness(self) -> float:
        """Calcule l'efficacité au combat."""
        base = 1.0
        base -= self.psychological_state.fatigue * 0.3
        base -= self.psychological_state.stress * 0.2
        base -= self.corruption_level * 0.4
        base *= self.psychological_state.morale
        base *= (self.health / self.max_health)
        return max(0.0, base)

    def to_dict(self) -> dict:
        """Convertit l'agent en dictionnaire."""
        base_dict = super().to_dict()
        base_dict.update({
            'agent_type': self.agent_type.value,
            'state': self.state.value,
            'corruption_stage': self.corruption_stage.value,
            'corruption_level': self.corruption_level,
            'damage': self.damage,
            'defense': self.defense,
            'speed': self.speed,
            'hacking_skill': self.hacking_skill,
            'experience': self.experience,
            'kills': self.kills,
            'towers_deactivated': self.towers_deactivated,
            'missions_completed': self.missions_completed,
            'psychological_state': {
                'fatigue': self.psychological_state.fatigue,
                'stress': self.psychological_state.stress,
                'morale': self.psychological_state.morale,
                'resistance': self.psychological_state.resistance,
                'isolation': self.psychological_state.isolation,
                'corruption_exposure': self.psychological_state.corruption_exposure,
                'trust_with_team': self.psychological_state.trust_with_team
            }
        })
        return base_dict
