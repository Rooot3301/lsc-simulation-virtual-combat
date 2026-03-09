"""
Moteur principal de la simulation Carthage Engine.
"""

from typing import Dict, Any
from .world import World
from .scheduler import Scheduler, Priority
from .events import EventManager, Event, EventType
from .time import SimulationTime
from ..ai import XANACore
from ..entities import XANAEntity, Skid, Agent, Monster, Tower, AgentType, MonsterType
from ..entities.tower import TowerState
import random


class CarthageEngine:
    """Moteur principal de simulation."""

    def __init__(self):
        self.world = World()
        self.scheduler = Scheduler()
        self.event_manager = EventManager()
        self.time = SimulationTime()
        self.xana_ai = XANACore()

        self.is_running = False
        self.is_paused = False

        # Initialisation
        self._initialize_world()
        self._setup_scheduler()

    def _initialize_world(self):
        """Initialise le monde avec les entités par défaut."""
        # XANA
        xana = XANAEntity(
            id="XANA",
            name="XANA",
            sector="network",
            health=1000.0
        )
        self.world.set_xana(xana)

        # Skid
        skid = Skid(
            id="SKID-01",
            name="Le Skid",
            sector="network"
        )
        self.world.set_skid(skid)

        # Agents
        agents_data = [
            ("Yumi", AgentType.WARRIOR, "forest"),
            ("Odd", AgentType.SCOUT, "desert"),
            ("Ulrich", AgentType.WARRIOR, "ice"),
            ("Aelita", AgentType.HACKER, "sector5")
        ]

        for name, agent_type, sector in agents_data:
            agent = Agent(
                id=f"agent_{name.lower()}",
                name=name,
                sector=sector,
                agent_type=agent_type
            )
            self.world.add_agent(agent)

        # Tours
        tower_positions = [
            ("T-FOREST-01", "forest"),
            ("T-FOREST-02", "forest"),
            ("T-DESERT-01", "desert"),
            ("T-ICE-01", "ice"),
            ("T-ICE-02", "ice"),
            ("T-MOUNTAIN-01", "mountain"),
            ("T-SEC5-01", "sector5"),
            ("T-SEC5-02", "sector5")
        ]

        for tower_id, sector in tower_positions:
            tower = Tower(
                id=tower_id,
                name=tower_id,
                sector=sector
            )
            self.world.add_tower(tower)

    def _setup_scheduler(self):
        """Configure l'ordonnanceur des tâches."""
        self.scheduler.add_task(
            "update_xana_ai",
            self._update_xana_ai,
            Priority.CRITICAL
        )
        self.scheduler.add_task(
            "update_towers",
            self._update_towers,
            Priority.HIGH
        )
        self.scheduler.add_task(
            "update_corruption",
            self._update_corruption,
            Priority.HIGH
        )
        self.scheduler.add_task(
            "update_psychology",
            self._update_psychology,
            Priority.NORMAL
        )
        self.scheduler.add_task(
            "update_world_state",
            self._update_world_state,
            Priority.LOW
        )

    def start(self):
        """Démarre la simulation."""
        self.is_running = True
        self.is_paused = False

        event = Event(
            type=EventType.SIMULATION_START,
            tick=self.time.current_tick,
            timestamp=self.time.get_timestamp(),
            message="Simulation Carthage Engine démarrée.",
            severity="INFO"
        )
        self.event_manager.emit(event)

    def pause(self):
        """Met la simulation en pause."""
        self.is_paused = True

        event = Event(
            type=EventType.SIMULATION_PAUSE,
            tick=self.time.current_tick,
            timestamp=self.time.get_timestamp(),
            message="Simulation mise en pause.",
            severity="INFO"
        )
        self.event_manager.emit(event)

    def resume(self):
        """Reprend la simulation."""
        self.is_paused = False

    def stop(self):
        """Arrête la simulation."""
        self.is_running = False

        event = Event(
            type=EventType.SIMULATION_STOP,
            tick=self.time.current_tick,
            timestamp=self.time.get_timestamp(),
            message="Simulation arrêtée.",
            severity="INFO"
        )
        self.event_manager.emit(event)

    def tick(self, count: int = 1):
        """Exécute N ticks de simulation."""
        for _ in range(count):
            if not self.is_running or self.is_paused:
                break

            self._execute_tick()

    def _execute_tick(self):
        """Exécute un tick de simulation."""
        # Avance le temps
        self.time.advance()

        # Événement de tick
        event = Event(
            type=EventType.TICK,
            tick=self.time.current_tick,
            timestamp=self.time.get_timestamp(),
            message=f"Tick {self.time.current_tick}",
            severity="DEBUG"
        )
        self.event_manager.emit(event)

        # Exécute toutes les tâches
        self.scheduler.execute_all()

    def _update_xana_ai(self):
        """Met à jour l'IA de XANA."""
        world_state = self._get_world_state()

        # Perception
        self.xana_ai.perceive(
            world_state,
            self.time.current_tick,
            self.time.get_timestamp()
        )

        # Décision
        plan = self.xana_ai.decide(
            world_state,
            self.time.current_tick,
            self.time.get_timestamp()
        )

        if plan:
            event = Event(
                type=EventType.XANA_GOAL_SET,
                tick=self.time.current_tick,
                timestamp=self.time.get_timestamp(),
                message=f"XANA sélectionne l'objectif : {plan.goal.value}",
                severity="STRATEGIE",
                data={'goal': plan.goal.value, 'target': plan.target_sector}
            )
            self.event_manager.emit(event)

            # Exécute la première action
            self._execute_xana_action(plan)

    def _execute_xana_action(self, plan):
        """Exécute une action du plan de XANA."""
        action = plan.get_next_action()
        if not action:
            return

        # Vérifie si XANA a les ressources
        xana = self.world.xana
        if not xana or xana.resources < 20:
            return

        # Exécute selon le type d'action
        if action.action_type == "activate_tower":
            self._xana_activate_tower(action.target)
            xana.spend_resources(30)

        elif action.action_type == "spawn_monsters":
            monster_type = action.parameters.get('type', 'kankrelat')
            count = action.parameters.get('count', 1)
            self._xana_spawn_monsters(action.target, monster_type, count)
            xana.spend_resources(20 * count)

        elif action.action_type == "spread_corruption":
            intensity = action.parameters.get('intensity', 0.1)
            self._xana_spread_corruption(action.target, intensity)
            xana.spend_resources(15)

        # Marque l'action comme complétée
        plan.complete_action(action, self.time.current_tick)

    def _xana_activate_tower(self, sector_name: str):
        """XANA active une tour."""
        towers = self.world.get_towers_in_sector(sector_name)
        inactive_towers = [t for t in towers if t.state == TowerState.INACTIVE]

        if inactive_towers:
            tower = inactive_towers[0]
            tower.activate()

            event = Event(
                type=EventType.TOWER_ACTIVATED,
                tick=self.time.current_tick,
                timestamp=self.time.get_timestamp(),
                message=f"Activation de la tour {tower.name} dans le secteur {sector_name} détectée.",
                severity="ALERTE",
                data={'tower_id': tower.id, 'sector': sector_name}
            )
            self.event_manager.emit(event)

    def _xana_spawn_monsters(self, sector_name: str, monster_type_str: str, count: int):
        """XANA spawne des monstres."""
        from ..entities import MonsterType

        type_map = {
            'kankrelat': MonsterType.KANKRELAT,
            'blok': MonsterType.BLOK,
            'hornet': MonsterType.HORNET,
            'megatank': MonsterType.MEGATANK
        }

        monster_type = type_map.get(monster_type_str, MonsterType.KANKRELAT)

        for i in range(count):
            monster = Monster(
                id=f"monster_{monster_type.value}_{self.time.current_tick}_{i}",
                name=f"{monster_type.value.capitalize()} {i+1}",
                sector=sector_name,
                monster_type=monster_type
            )
            self.world.add_monster(monster)

        event = Event(
            type=EventType.MONSTER_SPAWNED,
            tick=self.time.current_tick,
            timestamp=self.time.get_timestamp(),
            message=f"XANA déploie {count} {monster_type_str}(s) dans le secteur {sector_name}.",
            severity="ALERTE",
            data={'monster_type': monster_type_str, 'count': count, 'sector': sector_name}
        )
        self.event_manager.emit(event)

    def _xana_spread_corruption(self, sector_name: str, intensity: float):
        """XANA propage la corruption."""
        if sector_name in self.world.sectors:
            sector = self.world.sectors[sector_name]
            sector.increase_corruption(intensity)

            event = Event(
                type=EventType.CORRUPTION_SPREAD,
                tick=self.time.current_tick,
                timestamp=self.time.get_timestamp(),
                message=f"Corruption propagée dans le secteur {sector_name}. Niveau: {sector.corruption_level:.2f}",
                severity="CORRUPTION",
                data={'sector': sector_name, 'corruption_level': sector.corruption_level}
            )
            self.event_manager.emit(event)

    def _update_towers(self):
        """Met à jour les tours."""
        for tower in self.world.towers.values():
            tower.update()

            # Corruption passive
            if tower.state in [TowerState.ACTIVE, TowerState.CORRUPTED]:
                corruption_output = tower.get_corruption_output()
                if corruption_output > 0:
                    sector = self.world.sectors.get(tower.sector)
                    if sector:
                        sector.increase_corruption(corruption_output * 0.01)

    def _update_corruption(self):
        """Met à jour la corruption globale."""
        self.world.update_global_corruption()

        # Corruption des agents
        for agent in self.world.agents.values():
            if agent.is_destroyed:
                continue

            sector = self.world.sectors.get(agent.sector)
            if sector and sector.corruption_level > 0.3:
                corruption_increase = sector.corruption_level * 0.01
                agent.increase_corruption(corruption_increase)

                if agent.corruption_level > 0.5:
                    event = Event(
                        type=EventType.CORRUPTION_INCREASED,
                        tick=self.time.current_tick,
                        timestamp=self.time.get_timestamp(),
                        message=f"L'agent {agent.name} montre des signes de corruption. Niveau: {agent.corruption_level:.2f}",
                        severity="CORRUPTION",
                        data={'agent_id': agent.id, 'corruption_level': agent.corruption_level}
                    )
                    self.event_manager.emit(event)

    def _update_psychology(self):
        """Met à jour la psychologie des agents."""
        for agent in self.world.agents.values():
            if agent.is_destroyed:
                continue

            # Fatigue naturelle
            agent.increase_fatigue(0.005)

            # Stress lié à la corruption du secteur
            sector = self.world.sectors.get(agent.sector)
            if sector and sector.corruption_level > 0.5:
                agent.increase_stress(sector.corruption_level * 0.01)

            # Récupération en zone sûre
            if sector and sector.corruption_level < 0.2:
                agent.decrease_stress(0.01)
                agent.rest(0.01)

    def _update_world_state(self):
        """Met à jour l'état global du monde."""
        # Met à jour XANA
        if self.world.xana:
            active_towers = len(self.world.get_active_towers())
            active_monsters = self.world.get_active_monsters_count()

            self.world.xana.update_tower_count(active_towers)
            self.world.xana.update_monster_count(active_monsters)

            # XANA gagne des ressources passivement
            self.world.xana.gain_resources(active_towers * 2 + 5)

    def _get_world_state(self) -> Dict[str, Any]:
        """Retourne l'état actuel du monde pour l'IA."""
        return {
            'sectors': self.world.sectors,
            'agents': list(self.world.agents.values()),
            'agents_count': len(self.world.agents),
            'agents_active': self.world.get_operational_agents_count(),
            'active_towers': len(self.world.get_active_towers()),
            'active_monsters': self.world.get_active_monsters_count(),
            'global_corruption': self.world.global_corruption,
            'skid': self.world.skid,
            'skid_operational': self.world.skid.is_operational() if self.world.skid else False,
            'xana_power': self.world.xana.power_level if self.world.xana else 1.0,
            'resources': self.world.xana.resources if self.world.xana else 0
        }

    def get_status_summary(self) -> Dict[str, Any]:
        """Retourne un résumé de l'état de la simulation."""
        return {
            'tick': self.time.current_tick,
            'timestamp': self.time.get_timestamp(),
            'is_running': self.is_running,
            'is_paused': self.is_paused,
            'agents': self.world.get_operational_agents_count(),
            'monsters': self.world.get_active_monsters_count(),
            'active_towers': len(self.world.get_active_towers()),
            'global_corruption': f"{self.world.global_corruption:.2%}",
            'xana_power': self.world.xana.power_level if self.world.xana else 0,
            'xana_resources': self.world.xana.resources if self.world.xana else 0
        }
