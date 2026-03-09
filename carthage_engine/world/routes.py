"""
Gestion des routes et déplacements dans le monde.
"""

from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum


class RouteType(Enum):
    """Types de routes."""
    DIRECT = "directe"
    SAFE = "sécurisée"
    FAST = "rapide"
    STEALTH = "furtive"


@dataclass
class Route:
    """Représente une route entre deux points."""

    start: str
    end: str
    waypoints: List[str] = field(default_factory=list)
    route_type: RouteType = RouteType.DIRECT
    distance: int = 1
    danger_level: float = 0.0
    is_available: bool = True

    def get_total_distance(self) -> int:
        """Retourne la distance totale."""
        return self.distance + len(self.waypoints)


class RouteManager:
    """Gère les routes du monde."""

    def __init__(self):
        self.routes: List[Route] = []

    def add_route(self, route: Route):
        """Ajoute une route."""
        self.routes.append(route)

    def find_routes(self, start: str, end: str) -> List[Route]:
        """Trouve toutes les routes entre deux points."""
        return [r for r in self.routes if r.start == start and r.end == end and r.is_available]

    def find_safest_route(self, start: str, end: str) -> Optional[Route]:
        """Trouve la route la plus sûre."""
        routes = self.find_routes(start, end)
        if not routes:
            return None
        return min(routes, key=lambda r: r.danger_level)

    def find_fastest_route(self, start: str, end: str) -> Optional[Route]:
        """Trouve la route la plus rapide."""
        routes = self.find_routes(start, end)
        if not routes:
            return None
        return min(routes, key=lambda r: r.get_total_distance())

    def update_route_danger(self, start: str, end: str, danger: float):
        """Met à jour le niveau de danger d'une route."""
        for route in self.routes:
            if route.start == start and route.end == end:
                route.danger_level = danger

    def block_route(self, start: str, end: str):
        """Bloque une route."""
        for route in self.routes:
            if route.start == start and route.end == end:
                route.is_available = False

    def unblock_route(self, start: str, end: str):
        """Débloque une route."""
        for route in self.routes:
            if route.start == start and route.end == end:
                route.is_available = True
