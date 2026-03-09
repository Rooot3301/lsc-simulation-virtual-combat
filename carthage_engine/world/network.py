"""
Système de réseau et corridors pour la navigation du Skid.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional


class CorridorState(Enum):
    """États possibles d'un corridor."""
    CLEAR = "dégagé"
    CORRUPTED = "corrompu"
    BLOCKED = "bloqué"
    PATROLLED = "patrouillé"


@dataclass
class NetworkNode:
    """Représente un nœud dans le réseau."""

    id: str
    name: str
    sector: str
    corruption_level: float = 0.0
    is_strategic: bool = False
    connected_corridors: List[str] = field(default_factory=list)

    def is_safe(self) -> bool:
        """Détermine si le nœud est sûr."""
        return self.corruption_level < 0.3


@dataclass
class NetworkCorridor:
    """Représente un corridor entre deux nœuds."""

    id: str
    node_a: str
    node_b: str
    state: CorridorState = CorridorState.CLEAR
    corruption_level: float = 0.0
    length: int = 1
    patrol_count: int = 0

    def is_passable(self) -> bool:
        """Détermine si le corridor est franchissable."""
        return self.state != CorridorState.BLOCKED

    def get_danger_level(self) -> float:
        """Calcule le niveau de danger du corridor."""
        danger = self.corruption_level
        if self.state == CorridorState.CORRUPTED:
            danger += 0.3
        if self.state == CorridorState.PATROLLED:
            danger += 0.5
        if self.state == CorridorState.BLOCKED:
            danger = 1.0
        return min(1.0, danger)


class Network:
    """Gère le réseau de navigation."""

    def __init__(self):
        self.nodes: Dict[str, NetworkNode] = {}
        self.corridors: Dict[str, NetworkCorridor] = {}
        self._initialize_default_network()

    def _initialize_default_network(self):
        """Initialise le réseau par défaut."""
        # Nœuds principaux
        self.nodes['N-SEC5-GATE'] = NetworkNode(
            id='N-SEC5-GATE',
            name='Portail Secteur 5',
            sector='sector5',
            is_strategic=True
        )

        self.nodes['N-DIGITAL-GATE'] = NetworkNode(
            id='N-DIGITAL-GATE',
            name='Portail Mer Numérique',
            sector='digital_sea',
            is_strategic=True
        )

        self.nodes['N-HUB-1'] = NetworkNode(
            id='N-HUB-1',
            name='Hub Principal',
            sector='network',
            is_strategic=True
        )

        self.nodes['N-HUB-2'] = NetworkNode(
            id='N-HUB-2',
            name='Hub Secondaire',
            sector='network'
        )

        self.nodes['N-RELAY-1'] = NetworkNode(
            id='N-RELAY-1',
            name='Relais 1',
            sector='network'
        )

        self.nodes['N-RELAY-2'] = NetworkNode(
            id='N-RELAY-2',
            name='Relais 2',
            sector='network'
        )

        # Corridors
        self.corridors['C-1'] = NetworkCorridor(
            id='C-1',
            node_a='N-SEC5-GATE',
            node_b='N-HUB-1',
            length=3
        )

        self.corridors['C-2'] = NetworkCorridor(
            id='C-2',
            node_a='N-HUB-1',
            node_b='N-HUB-2',
            length=2
        )

        self.corridors['C-3'] = NetworkCorridor(
            id='C-3',
            node_a='N-HUB-1',
            node_b='N-RELAY-1',
            length=2
        )

        self.corridors['C-4'] = NetworkCorridor(
            id='C-4',
            node_a='N-HUB-2',
            node_b='N-RELAY-2',
            length=2
        )

        self.corridors['C-5'] = NetworkCorridor(
            id='C-5',
            node_a='N-RELAY-1',
            node_b='N-DIGITAL-GATE',
            length=4
        )

        self.corridors['C-6'] = NetworkCorridor(
            id='C-6',
            node_a='N-RELAY-2',
            node_b='N-DIGITAL-GATE',
            length=4
        )

        # Connexions
        self.nodes['N-SEC5-GATE'].connected_corridors = ['C-1']
        self.nodes['N-HUB-1'].connected_corridors = ['C-1', 'C-2', 'C-3']
        self.nodes['N-HUB-2'].connected_corridors = ['C-2', 'C-4']
        self.nodes['N-RELAY-1'].connected_corridors = ['C-3', 'C-5']
        self.nodes['N-RELAY-2'].connected_corridors = ['C-4', 'C-6']
        self.nodes['N-DIGITAL-GATE'].connected_corridors = ['C-5', 'C-6']

    def find_path(self, start_node: str, end_node: str) -> Optional[List[str]]:
        """Trouve un chemin entre deux nœuds (algorithme simple BFS)."""
        if start_node not in self.nodes or end_node not in self.nodes:
            return None

        visited = set()
        queue = [(start_node, [start_node])]

        while queue:
            current, path = queue.pop(0)

            if current == end_node:
                return path

            if current in visited:
                continue

            visited.add(current)

            # Explorer les corridors connectés
            for corridor_id in self.nodes[current].connected_corridors:
                corridor = self.corridors[corridor_id]
                if not corridor.is_passable():
                    continue

                # Trouver le nœud suivant
                next_node = corridor.node_b if corridor.node_a == current else corridor.node_a

                if next_node not in visited:
                    queue.append((next_node, path + [next_node]))

        return None

    def get_corridor_between_nodes(self, node_a: str, node_b: str) -> Optional[NetworkCorridor]:
        """Trouve le corridor entre deux nœuds."""
        for corridor in self.corridors.values():
            if (corridor.node_a == node_a and corridor.node_b == node_b) or \
               (corridor.node_a == node_b and corridor.node_b == node_a):
                return corridor
        return None

    def increase_corridor_corruption(self, corridor_id: str, amount: float):
        """Augmente la corruption d'un corridor."""
        if corridor_id in self.corridors:
            corridor = self.corridors[corridor_id]
            corridor.corruption_level = min(1.0, corridor.corruption_level + amount)

            if corridor.corruption_level > 0.7:
                corridor.state = CorridorState.CORRUPTED

    def block_corridor(self, corridor_id: str):
        """Bloque un corridor."""
        if corridor_id in self.corridors:
            self.corridors[corridor_id].state = CorridorState.BLOCKED

    def clear_corridor(self, corridor_id: str):
        """Débloque un corridor."""
        if corridor_id in self.corridors:
            self.corridors[corridor_id].state = CorridorState.CLEAR
            self.corridors[corridor_id].corruption_level = 0.0

    def get_strategic_nodes(self) -> List[NetworkNode]:
        """Retourne les nœuds stratégiques."""
        return [node for node in self.nodes.values() if node.is_strategic]

    def get_network_integrity(self) -> float:
        """Calcule l'intégrité globale du réseau."""
        if not self.corridors:
            return 1.0

        total_corruption = sum(c.corruption_level for c in self.corridors.values())
        blocked_count = sum(1 for c in self.corridors.values() if c.state == CorridorState.BLOCKED)

        integrity = 1.0 - (total_corruption / len(self.corridors))
        integrity -= (blocked_count / len(self.corridors)) * 0.5

        return max(0.0, integrity)
