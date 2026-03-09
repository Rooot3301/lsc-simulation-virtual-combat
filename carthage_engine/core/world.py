"""
Monde virtuel - contient tous les secteurs, entités et état global.
"""

from typing import Dict, List, Optional
from ..entities import Agent, Monster, Tower, Skid, XANAEntity
from ..world import Sector, create_default_sectors, Network


class World:
    """Représente le monde virtuel complet."""

    def __init__(self):
        # Secteurs
        self.sectors: Dict[str, Sector] = create_default_sectors()

        # Entités
        self.agents: Dict[str, Agent] = {}
        self.monsters: Dict[str, Monster] = {}
        self.towers: Dict[str, Tower] = {}
        self.skid: Optional[Skid] = None
        self.xana: Optional[XANAEntity] = None

        # Réseau
        self.network = Network()

        # État global
        self.global_corruption: float = 0.0

    def add_agent(self, agent: Agent):
        """Ajoute un agent au monde."""
        self.agents[agent.id] = agent
        if agent.sector in self.sectors:
            self.sectors[agent.sector].add_entity(agent.id)

    def add_monster(self, monster: Monster):
        """Ajoute un monstre au monde."""
        self.monsters[monster.id] = monster
        if monster.sector in self.sectors:
            self.sectors[monster.sector].add_entity(monster.id)

    def add_tower(self, tower: Tower):
        """Ajoute une tour au monde."""
        self.towers[tower.id] = tower
        if tower.sector in self.sectors:
            self.sectors[tower.sector].add_tower(tower.id)

    def set_skid(self, skid: Skid):
        """Définit le Skid."""
        self.skid = skid

    def set_xana(self, xana: XANAEntity):
        """Définit XANA."""
        self.xana = xana

    def remove_agent(self, agent_id: str):
        """Retire un agent du monde."""
        if agent_id in self.agents:
            agent = self.agents[agent_id]
            if agent.sector in self.sectors:
                self.sectors[agent.sector].remove_entity(agent_id)
            del self.agents[agent_id]

    def remove_monster(self, monster_id: str):
        """Retire un monstre du monde."""
        if monster_id in self.monsters:
            monster = self.monsters[monster_id]
            if monster.sector in self.sectors:
                self.sectors[monster.sector].remove_entity(monster_id)
            del self.monsters[monster_id]

    def get_agents_in_sector(self, sector_name: str) -> List[Agent]:
        """Retourne tous les agents dans un secteur."""
        return [a for a in self.agents.values() if a.sector == sector_name and not a.is_destroyed]

    def get_monsters_in_sector(self, sector_name: str) -> List[Monster]:
        """Retourne tous les monstres dans un secteur."""
        return [m for m in self.monsters.values() if m.sector == sector_name and not m.is_destroyed]

    def get_towers_in_sector(self, sector_name: str) -> List[Tower]:
        """Retourne toutes les tours dans un secteur."""
        return [t for t in self.towers.values() if t.sector == sector_name]

    def get_active_towers(self) -> List[Tower]:
        """Retourne toutes les tours actives."""
        from ..entities.tower import TowerState
        return [t for t in self.towers.values()
                if t.state in [TowerState.ACTIVE, TowerState.CORRUPTED]]

    def update_global_corruption(self):
        """Met à jour le niveau de corruption globale."""
        if not self.sectors:
            self.global_corruption = 0.0
            return

        total_corruption = sum(s.corruption_level for s in self.sectors.values())
        self.global_corruption = total_corruption / len(self.sectors)

        # Met à jour XANA
        if self.xana:
            self.xana.global_corruption = self.global_corruption

    def get_operational_agents_count(self) -> int:
        """Compte les agents opérationnels."""
        return sum(1 for a in self.agents.values() if a.is_operational())

    def get_active_monsters_count(self) -> int:
        """Compte les monstres actifs."""
        return sum(1 for m in self.monsters.values() if not m.is_destroyed)

    def to_dict(self) -> dict:
        """Convertit le monde en dictionnaire."""
        return {
            'sectors': {name: sector.to_dict() for name, sector in self.sectors.items()},
            'agents': {aid: agent.to_dict() for aid, agent in self.agents.items()},
            'monsters': {mid: monster.to_dict() for mid, monster in self.monsters.items()},
            'towers': {tid: tower.to_dict() for tid, tower in self.towers.items()},
            'skid': self.skid.to_dict() if self.skid else None,
            'xana': self.xana.to_dict() if self.xana else None,
            'global_corruption': self.global_corruption
        }
