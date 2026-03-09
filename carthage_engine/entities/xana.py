"""
XANA - intelligence artificielle hostile principale.
"""

from dataclasses import dataclass, field
from typing import List, Dict
from .entity import Entity, EntityType
from carthage_engine.systems.resources import ResourcePool


@dataclass
class XANAEntity(Entity):
    """Représente XANA - l'IA hostile principale."""

    # Puissance et influence
    power_level: float = 1.0
    influence: float = 0.5
    global_corruption: float = 0.0

    # Ressources
    resources: int = 100
    active_towers: int = 0
    active_monsters: int = 0

    # Stratégie
    current_goal: str = None
    active_plans: List[str] = field(default_factory=list)
    completed_objectives: int = 0
    failed_objectives: int = 0

    # Adaptation
    adaptation_level: float = 1.0
    threat_awareness: float = 0.5
    learning_rate: float = 0.1

    # v2.0 - Ressources avancées
    resource_pools: Dict[str, ResourcePool] = field(default_factory=dict)

    # v2.0 - Plans stratégiques (objets complets)
    active_strategic_plans: List = field(default_factory=list)

    def __post_init__(self):
        """Initialisation de XANA."""
        super().__post_init__()
        self.entity_type = EntityType.XANA
        self.max_health = 1000.0
        self.health = 1000.0
        self.is_destroyed = False

        # v2.0 - Initialiser les pools de ressources si vide
        if not self.resource_pools:
            from carthage_engine.systems.resources import ResourceSystem
            self.resource_pools = ResourceSystem.create_xana_resources(self.power_level)

    def increase_power(self, amount: float):
        """Augmente la puissance de XANA."""
        self.power_level = min(10.0, self.power_level + amount)

    def decrease_power(self, amount: float):
        """Diminue la puissance de XANA."""
        self.power_level = max(0.1, self.power_level - amount)

    def increase_influence(self, amount: float):
        """Augmente l'influence de XANA."""
        self.influence = min(1.0, self.influence + amount)

    def decrease_influence(self, amount: float):
        """Diminue l'influence de XANA."""
        self.influence = max(0.0, self.influence - amount)

    def gain_resources(self, amount: int):
        """Gagne des ressources."""
        self.resources += amount

    def spend_resources(self, amount: int) -> bool:
        """Dépense des ressources."""
        if self.resources >= amount:
            self.resources -= amount
            return True
        return False

    def update_tower_count(self, count: int):
        """Met à jour le nombre de tours actives."""
        self.active_towers = count

    def update_monster_count(self, count: int):
        """Met à jour le nombre de monstres actifs."""
        self.active_monsters = count

    def set_goal(self, goal: str):
        """Définit l'objectif actuel."""
        self.current_goal = goal

    def add_active_plan(self, plan_id: str):
        """Ajoute un plan actif."""
        if plan_id not in self.active_plans:
            self.active_plans.append(plan_id)

    def remove_active_plan(self, plan_id: str):
        """Retire un plan actif."""
        if plan_id in self.active_plans:
            self.active_plans.remove(plan_id)

    def complete_objective(self):
        """Marque un objectif comme complété."""
        self.completed_objectives += 1
        self.increase_power(0.1)
        self.gain_resources(50)

    def fail_objective(self):
        """Marque un objectif comme échoué."""
        self.failed_objectives += 1
        self.decrease_power(0.05)

    def adapt(self):
        """XANA s'adapte à la situation."""
        self.adaptation_level = min(3.0, self.adaptation_level + self.learning_rate)
        self.threat_awareness = min(1.0, self.threat_awareness + 0.05)

    def get_strategic_capacity(self) -> float:
        """Calcule la capacité stratégique de XANA."""
        capacity = self.power_level * 0.4
        capacity += self.influence * 0.3
        capacity += (self.active_towers / 10.0) * 0.2
        capacity += (self.adaptation_level / 3.0) * 0.1
        return min(10.0, capacity)

    def get_success_rate(self) -> float:
        """Calcule le taux de réussite."""
        total = self.completed_objectives + self.failed_objectives
        if total == 0:
            return 0.5
        return self.completed_objectives / total

    def is_dominant(self) -> bool:
        """Détermine si XANA est en position dominante."""
        return (
            self.power_level > 5.0 and
            self.influence > 0.7 and
            self.active_towers > 5
        )

    def to_dict(self) -> dict:
        """Convertit XANA en dictionnaire."""
        base_dict = super().to_dict()
        base_dict.update({
            'power_level': self.power_level,
            'influence': self.influence,
            'global_corruption': self.global_corruption,
            'resources': self.resources,
            'active_towers': self.active_towers,
            'active_monsters': self.active_monsters,
            'current_goal': self.current_goal,
            'active_plans': self.active_plans,
            'completed_objectives': self.completed_objectives,
            'failed_objectives': self.failed_objectives,
            'adaptation_level': self.adaptation_level,
            'threat_awareness': self.threat_awareness
        })
        return base_dict
