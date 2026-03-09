"""
Système d'économie de ressources - v2.0.

Gère les coûts et contraintes pour XANA et les agents.
"""

from dataclasses import dataclass
from typing import Dict, Optional
from enum import Enum


class ResourceType(Enum):
    """Types de ressources."""
    # XANA
    POWER = "power"
    BANDWIDTH = "bandwidth"
    CORRUPTION_PRESSURE = "corruption_pressure"
    OPERATIONAL_RESERVE = "operational_reserve"

    # Agents
    ENERGY = "energy"
    STAMINA = "stamina"
    SUPPORT_AVAILABILITY = "support_availability"


@dataclass
class ResourcePool:
    """Pool de ressources."""
    max_capacity: float
    current: float
    regeneration_rate: float = 0.0
    consumption_rate: float = 0.0

    def consume(self, amount: float) -> bool:
        """
        Consomme une quantité de ressource.

        Returns:
            True si suffisamment de ressources
        """
        if self.current >= amount:
            self.current -= amount
            return True
        return False

    def add(self, amount: float):
        """Ajoute des ressources."""
        self.current = min(self.max_capacity, self.current + amount)

    def regenerate(self, dt: float = 1.0):
        """Régénère les ressources."""
        regen = self.regeneration_rate * dt
        self.add(regen)

    def get_percentage(self) -> float:
        """Retourne le % de ressources."""
        return (self.current / self.max_capacity) if self.max_capacity > 0 else 0.0

    def is_depleted(self) -> bool:
        """Les ressources sont-elles épuisées?"""
        return self.current <= 0.0

    def is_low(self, threshold: float = 0.25) -> bool:
        """Les ressources sont-elles basses?"""
        return self.get_percentage() < threshold


class ResourceSystem:
    """Système gérant les ressources."""

    # Coûts des opérations XANA
    XANA_OPERATION_COSTS = {
        'activate_tower': {'power': 15, 'bandwidth': 10},
        'deploy_monster': {'power': 8, 'operational_reserve': 5},
        'corruption_attempt': {'corruption_pressure': 20, 'power': 5},
        'network_attack': {'bandwidth': 25, 'power': 10},
        'create_plan': {'operational_reserve': 10},
        'maintain_tower': {'power': 2},  # Par tick
        'maintain_monster': {'power': 1},  # Par tick
        'spread_corruption': {'corruption_pressure': 10, 'power': 3}
    }

    # Coûts des actions agents
    AGENT_ACTION_COSTS = {
        'combat': {'energy': 10, 'stamina': 15},
        'deactivate_tower': {'energy': 20, 'stamina': 10},
        'travel': {'energy': 5, 'stamina': 5},
        'scan_sector': {'energy': 3},
        'support_ally': {'support_availability': 10, 'energy': 5},
        'rest': {'energy': -10},  # Négatif = récupération
        'strategic_move': {'energy': 8, 'stamina': 8}
    }

    @staticmethod
    def can_afford_xana_operation(
        resources: Dict[str, ResourcePool],
        operation: str
    ) -> bool:
        """
        XANA peut-il effectuer une opération?

        Args:
            resources: Pools de ressources XANA
            operation: Nom de l'opération

        Returns:
            True si suffisamment de ressources
        """
        costs = ResourceSystem.XANA_OPERATION_COSTS.get(operation, {})

        for resource_type, cost in costs.items():
            pool = resources.get(resource_type)
            if not pool or pool.current < cost:
                return False

        return True

    @staticmethod
    def consume_xana_operation(
        resources: Dict[str, ResourcePool],
        operation: str
    ) -> bool:
        """
        Consomme les ressources pour une opération XANA.

        Returns:
            True si opération effectuée
        """
        if not ResourceSystem.can_afford_xana_operation(resources, operation):
            return False

        costs = ResourceSystem.XANA_OPERATION_COSTS.get(operation, {})

        for resource_type, cost in costs.items():
            pool = resources.get(resource_type)
            if pool:
                pool.consume(cost)

        return True

    @staticmethod
    def can_afford_agent_action(
        resources: Dict[str, ResourcePool],
        action: str
    ) -> bool:
        """
        Un agent peut-il effectuer une action?

        Args:
            resources: Pools de ressources de l'agent
            action: Nom de l'action

        Returns:
            True si suffisamment de ressources
        """
        costs = ResourceSystem.AGENT_ACTION_COSTS.get(action, {})

        for resource_type, cost in costs.items():
            if cost < 0:  # Récupération
                continue

            pool = resources.get(resource_type)
            if not pool or pool.current < cost:
                return False

        return True

    @staticmethod
    def consume_agent_action(
        resources: Dict[str, ResourcePool],
        action: str
    ) -> bool:
        """
        Consomme les ressources pour une action agent.

        Returns:
            True si action effectuée
        """
        if not ResourceSystem.can_afford_agent_action(resources, action):
            return False

        costs = ResourceSystem.AGENT_ACTION_COSTS.get(action, {})

        for resource_type, cost in costs.items():
            pool = resources.get(resource_type)
            if pool:
                if cost < 0:  # Récupération
                    pool.add(abs(cost))
                else:
                    pool.consume(cost)

        return True

    @staticmethod
    def create_xana_resources(power_level: float = 1.0) -> Dict[str, ResourcePool]:
        """
        Crée les pools de ressources XANA.

        Args:
            power_level: Niveau de puissance XANA (multiplie les capacités)

        Returns:
            Dict de ResourcePools
        """
        base_capacity = 100.0 * power_level

        return {
            'power': ResourcePool(
                max_capacity=base_capacity,
                current=base_capacity * 0.8,
                regeneration_rate=2.0 * power_level
            ),
            'bandwidth': ResourcePool(
                max_capacity=base_capacity * 0.8,
                current=base_capacity * 0.6,
                regeneration_rate=1.5 * power_level
            ),
            'corruption_pressure': ResourcePool(
                max_capacity=base_capacity * 1.5,
                current=base_capacity,
                regeneration_rate=3.0 * power_level
            ),
            'operational_reserve': ResourcePool(
                max_capacity=base_capacity * 0.6,
                current=base_capacity * 0.5,
                regeneration_rate=1.0 * power_level
            )
        }

    @staticmethod
    def create_agent_resources() -> Dict[str, ResourcePool]:
        """
        Crée les pools de ressources d'un agent.

        Returns:
            Dict de ResourcePools
        """
        return {
            'energy': ResourcePool(
                max_capacity=100.0,
                current=100.0,
                regeneration_rate=2.0
            ),
            'stamina': ResourcePool(
                max_capacity=100.0,
                current=100.0,
                regeneration_rate=1.5
            ),
            'support_availability': ResourcePool(
                max_capacity=50.0,
                current=50.0,
                regeneration_rate=1.0
            )
        }

    @staticmethod
    def regenerate_all_pools(resources: Dict[str, ResourcePool], dt: float = 1.0):
        """
        Régénère tous les pools de ressources.

        Args:
            resources: Dict de pools
            dt: Delta temps
        """
        for pool in resources.values():
            pool.regenerate(dt)

    @staticmethod
    def get_resource_status(resources: Dict[str, ResourcePool]) -> Dict[str, float]:
        """
        Retourne le statut de toutes les ressources.

        Returns:
            Dict {resource_type: percentage}
        """
        return {
            name: pool.get_percentage()
            for name, pool in resources.items()
        }
