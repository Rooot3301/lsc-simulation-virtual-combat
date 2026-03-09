"""
Doctrine stratégique de XANA - règles de comportement.
"""

from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Any, Callable


class DoctrineRule(Enum):
    """Règles doctrinales de XANA."""
    OPPORTUNISTIC = "opportuniste"
    AGGRESSIVE = "agressif"
    DEFENSIVE = "défensif"
    PATIENT = "patient"
    OVERWHELMING = "écrasant"
    SUBTLE = "subtil"
    ADAPTIVE = "adaptatif"


@dataclass
class XANADoctrine:
    """Doctrine stratégique de XANA."""

    primary_rule: DoctrineRule = DoctrineRule.OPPORTUNISTIC
    secondary_rules: List[DoctrineRule] = None
    aggression_level: float = 0.5  # 0.0 à 1.0
    risk_tolerance: float = 0.5  # 0.0 à 1.0
    patience: float = 0.5  # 0.0 à 1.0

    def __post_init__(self):
        if self.secondary_rules is None:
            self.secondary_rules = []

    def should_activate_tower(self, world_state: Dict[str, Any]) -> bool:
        """Détermine si XANA devrait activer une tour."""
        if self.primary_rule == DoctrineRule.AGGRESSIVE:
            return world_state.get('resources', 0) > 20

        if self.primary_rule == DoctrineRule.PATIENT:
            return world_state.get('resources', 0) > 80

        if self.primary_rule == DoctrineRule.OPPORTUNISTIC:
            # Active si agents éloignés
            return world_state.get('agents_nearby', 0) == 0

        return world_state.get('resources', 0) > 50

    def should_spawn_monsters(self, world_state: Dict[str, Any]) -> bool:
        """Détermine si XANA devrait spawner des monstres."""
        if self.primary_rule == DoctrineRule.OVERWHELMING:
            return True

        if self.primary_rule == DoctrineRule.DEFENSIVE:
            return world_state.get('under_threat', False)

        if self.primary_rule == DoctrineRule.AGGRESSIVE:
            return world_state.get('active_monsters', 0) < 10

        return world_state.get('active_monsters', 0) < 5

    def should_attack_skid(self, world_state: Dict[str, Any]) -> bool:
        """Détermine si XANA devrait attaquer le Skid."""
        if self.primary_rule == DoctrineRule.AGGRESSIVE:
            return world_state.get('skid_detected', False)

        if self.primary_rule == DoctrineRule.OPPORTUNISTIC:
            return (
                world_state.get('skid_detected', False) and
                world_state.get('skid_vulnerable', False)
            )

        if self.primary_rule == DoctrineRule.PATIENT:
            return (
                world_state.get('skid_detected', False) and
                world_state.get('ambush_ready', False)
            )

        return False

    def should_attempt_corruption(self, world_state: Dict[str, Any]) -> bool:
        """Détermine si XANA devrait tenter de corrompre un agent."""
        if self.primary_rule == DoctrineRule.SUBTLE:
            return world_state.get('isolated_agents', 0) > 0

        if self.primary_rule == DoctrineRule.PATIENT:
            return world_state.get('vulnerable_agents', 0) > 0

        return False

    def calculate_action_priority(
        self,
        action_type: str,
        world_state: Dict[str, Any]
    ) -> int:
        """Calcule la priorité d'une action selon la doctrine."""
        priorities = {
            DoctrineRule.AGGRESSIVE: {
                'attack': 10,
                'spawn_monsters': 9,
                'activate_tower': 8,
                'defend': 4
            },
            DoctrineRule.DEFENSIVE: {
                'defend': 10,
                'fortify': 9,
                'activate_tower': 7,
                'attack': 5
            },
            DoctrineRule.OPPORTUNISTIC: {
                'exploit_weakness': 10,
                'activate_tower': 7,
                'attack': 6,
                'defend': 5
            },
            DoctrineRule.PATIENT: {
                'prepare': 10,
                'fortify': 9,
                'wait': 8,
                'attack': 4
            },
            DoctrineRule.SUBTLE: {
                'corrupt': 10,
                'infiltrate': 9,
                'manipulate': 8,
                'attack': 3
            },
            DoctrineRule.OVERWHELMING: {
                'spawn_monsters': 10,
                'mass_attack': 10,
                'activate_tower': 9,
                'corrupt': 4
            }
        }

        doctrine_priorities = priorities.get(self.primary_rule, {})
        return doctrine_priorities.get(action_type, 5)

    def adapt_to_situation(self, world_state: Dict[str, Any]):
        """Adapte la doctrine à la situation."""
        # Si sous pression, devient défensif
        if world_state.get('under_heavy_attack', False):
            self.primary_rule = DoctrineRule.DEFENSIVE
            self.aggression_level = max(0.2, self.aggression_level - 0.2)

        # Si dominant, devient agressif
        elif world_state.get('dominant_position', False):
            self.primary_rule = DoctrineRule.AGGRESSIVE
            self.aggression_level = min(0.9, self.aggression_level + 0.2)

        # Si égalité, devient opportuniste
        elif world_state.get('balanced_situation', True):
            self.primary_rule = DoctrineRule.OPPORTUNISTIC
            self.aggression_level = 0.5

    def get_resource_spending_rate(self) -> float:
        """Retourne le taux de dépense des ressources."""
        if self.primary_rule == DoctrineRule.AGGRESSIVE:
            return 0.8
        elif self.primary_rule == DoctrineRule.OVERWHELMING:
            return 1.0
        elif self.primary_rule == DoctrineRule.DEFENSIVE:
            return 0.4
        elif self.primary_rule == DoctrineRule.PATIENT:
            return 0.2
        else:
            return 0.5
