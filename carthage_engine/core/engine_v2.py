"""
Moteur principal de la simulation Carthage Engine v2.0 - VERSION AUTONOME.

Intègre tous les systèmes v2.0 pour une simulation complètement autonome.
"""

from typing import Dict, Any, Optional
from .world import World
from .scheduler import Scheduler, Priority
from .events import EventManager, Event, EventType
from .time import SimulationTime
from .metrics import MetricsTracker
from .autonomous_loop import AutonomousSimulationLoop

# Systèmes v2.0
from ..systems.psychology import PsychologySystem
from ..systems.information import InformationSystem, PerceptionRange
from ..systems.resources import ResourceSystem
from ..world.corruption import CorruptionSystem

# IA v2.0
from ..ai.perception import XANAPerceptionLayer
from ..ai.strategic_layer import XANAStrategicLayer
from ..ai.agent_ai import AgentAICoordinator
from ..ai import XANACore

# Entités
from ..entities import XANAEntity, Skid, Agent, Monster, Tower, AgentType, MonsterType
from ..entities.tower import TowerState

import random


class CarthageEngineV2:
    """
    Moteur principal de simulation v2.0 - AUTONOME.

    Cette version intègre:
    - Boucle autonome continue
    - IA XANA multicouche
    - IA agents autonomes
    - Psychologie profonde
    - Corruption progressive
    - Information imparfaite
    - Économie de ressources
    - Métriques complètes
    """

    def __init__(self):
        # Core systems
        self.world = World()
        self.scheduler = Scheduler()
        self.event_manager = EventManager()
        self.time = SimulationTime()

        # v2.0 - Systèmes autonomes
        self.autonomous_loop = AutonomousSimulationLoop(self._execute_tick)
        self.metrics = MetricsTracker()

        # v2.0 - IA multicouche
        self.xana_perception = XANAPerceptionLayer()
        self.xana_strategy = XANAStrategicLayer()
        self.xana_ai = XANACore()  # Legacy AI (garde doctrine)

        # v2.0 - IA agents
        self.agent_ai_coordinator = AgentAICoordinator()

        # v2.0 - Systèmes
        self.psychology_system = PsychologySystem()
        self.information_system = InformationSystem()
        self.corruption_system = CorruptionSystem()
        self.resource_system = ResourceSystem()

        # État
        self.is_initialized = False

        # Initialisation
        self._initialize_world()
        self._setup_scheduler()

    def _initialize_world(self):
        """Initialise le monde avec les entités par défaut."""
        # XANA avec ressources v2.0
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

        # Agents avec psychologie v2.0
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

        self.is_initialized = True

    def _setup_scheduler(self):
        """Configure l'ordonnanceur des tâches v2.0."""
        # XANA AI multicouche
        self.scheduler.add_task(
            "update_xana_perception",
            self._update_xana_perception,
            Priority.CRITICAL
        )
        self.scheduler.add_task(
            "update_xana_strategy",
            self._update_xana_strategy,
            Priority.CRITICAL
        )
        self.scheduler.add_task(
            "execute_xana_operations",
            self._execute_xana_operations,
            Priority.HIGH
        )

        # Agent AI autonome
        self.scheduler.add_task(
            "update_agent_ai",
            self._update_agent_ai,
            Priority.HIGH
        )
        self.scheduler.add_task(
            "execute_agent_decisions",
            self._execute_agent_decisions,
            Priority.HIGH
        )

        # Systèmes v2.0
        self.scheduler.add_task(
            "update_psychology",
            self._update_psychology_v2,
            Priority.NORMAL
        )
        self.scheduler.add_task(
            "update_corruption",
            self._update_corruption_v2,
            Priority.NORMAL
        )
        self.scheduler.add_task(
            "update_resources",
            self._update_resources,
            Priority.NORMAL
        )

        # Legacy systems
        self.scheduler.add_task(
            "update_towers",
            self._update_towers,
            Priority.HIGH
        )
        self.scheduler.add_task(
            "update_world_state",
            self._update_world_state,
            Priority.LOW
        )

        # Métriques
        self.scheduler.add_task(
            "update_metrics",
            self._update_metrics,
            Priority.LOW
        )

    # ============================================================
    # CONTRÔLES SIMULATION
    # ============================================================

    def start(self):
        """Démarre la simulation en mode manuel (tick par tick)."""
        self.autonomous_loop.state = self.autonomous_loop.state.__class__.STOPPED
        self.time.is_running = True

        event = Event(
            type=EventType.SIMULATION_START,
            tick=self.time.current_tick,
            timestamp=self.time.get_timestamp(),
            message="[SIMULATION] Démarrage de CARTHAGE ENGINE v2.0",
            severity="INFO"
        )
        self.event_manager.emit(event)

    def start_autonomous(self):
        """Démarre la simulation en mode autonome continu."""
        self.time.is_running = True
        self.autonomous_loop.start()

        event = Event(
            type=EventType.SIMULATION_START,
            tick=self.time.current_tick,
            timestamp=self.time.get_timestamp(),
            message="[SIMULATION] Démarrage autonome de CARTHAGE ENGINE v2.0",
            severity="INFO"
        )
        self.event_manager.emit(event)

    def pause(self):
        """Met en pause."""
        self.autonomous_loop.pause()

        event = Event(
            type=EventType.SIMULATION_PAUSE,
            tick=self.time.current_tick,
            timestamp=self.time.get_timestamp(),
            message="[SIMULATION] Pause",
            severity="INFO"
        )
        self.event_manager.emit(event)

    def resume(self):
        """Reprend depuis la pause."""
        self.autonomous_loop.resume()

        event = Event(
            type=EventType.SIMULATION_PAUSE,
            tick=self.time.current_tick,
            timestamp=self.time.get_timestamp(),
            message="[SIMULATION] Reprise",
            severity="INFO"
        )
        self.event_manager.emit(event)

    def stop(self):
        """Arrête complètement."""
        self.autonomous_loop.stop()
        self.time.is_running = False

        event = Event(
            type=EventType.SIMULATION_STOP,
            tick=self.time.current_tick,
            timestamp=self.time.get_timestamp(),
            message="[SIMULATION] Arrêt",
            severity="INFO"
        )
        self.event_manager.emit(event)

    def step(self):
        """Exécute un seul tick (mode pas-à-pas)."""
        self.autonomous_loop.step()

    def set_speed(self, multiplier: float):
        """Définit la vitesse de simulation."""
        self.autonomous_loop.set_speed(multiplier)

    # ============================================================
    # TICK EXECUTION
    # ============================================================

    def _execute_tick(self):
        """Exécute un tick de simulation (appelé par la boucle autonome)."""
        # Avance le temps
        self.time.advance()

        # Exécute toutes les tâches
        self.scheduler.execute_all()

    # ============================================================
    # XANA AI MULTICOUCHE v2.0
    # ============================================================

    def _update_xana_perception(self):
        """XANA perçoit le monde."""
        perception = self.xana_perception.perceive_world(
            self.world,
            self.time.current_tick
        )

        # Log des opportunités détectées
        if perception.opportunity_windows:
            for opportunity in perception.opportunity_windows[:2]:  # Top 2
                event = Event(
                    type=EventType.XANA_GOAL_SET,
                    tick=self.time.current_tick,
                    timestamp=self.time.get_timestamp(),
                    message=f"[IA] XANA détecte une opportunité: {opportunity}",
                    severity="IA",
                    data={'opportunity': opportunity}
                )
                self.event_manager.emit(event)

    def _update_xana_strategy(self):
        """XANA prend des décisions stratégiques."""
        # Sélectionner un nouvel objectif si possible
        goal = self.xana_strategy.select_strategic_goal(
            self.xana_perception,
            self.xana_ai.doctrine if hasattr(self.xana_ai, 'doctrine') else None,
            self.world.xana.resource_pools if self.world.xana else {}
        )

        if goal:
            # Créer un plan
            plan = self.xana_strategy.create_plan(
                goal,
                self.xana_perception,
                priority=0.8
            )

            self.xana_strategy.active_plans.append(plan)

            # Log
            event = Event(
                type=EventType.XANA_GOAL_SET,
                tick=self.time.current_tick,
                timestamp=self.time.get_timestamp(),
                message=f"[STRATEGIE] XANA sélectionne l'objectif: {goal.value} (cible: {plan.target})",
                severity="STRATEGIE",
                data={'goal': goal.value, 'target': plan.target}
            )
            self.event_manager.emit(event)

        # Mettre à jour les plans actifs
        self.xana_strategy.update_active_plans(self.xana_perception, self.world)

    def _execute_xana_operations(self):
        """XANA exécute ses opérations tactiques."""
        if not self.world.xana:
            return

        # Régénérer les ressources
        ResourceSystem.regenerate_all_pools(self.world.xana.resource_pools)

        # Activer tours de façon opportuniste
        if random.random() < 0.1:  # 10% de chance par tick
            if ResourceSystem.can_afford_xana_operation(
                self.world.xana.resource_pools,
                'activate_tower'
            ):
                # Trouver un secteur vulnérable
                vulnerable = self.xana_perception.get_most_vulnerable_sectors(1)
                if vulnerable:
                    sector = vulnerable[0]
                    self._xana_activate_tower(sector.sector_id)
                    ResourceSystem.consume_xana_operation(
                        self.world.xana.resource_pools,
                        'activate_tower'
                    )

        # Déployer monstres si tours actives
        active_towers = len(self.world.get_active_towers())
        if active_towers > 0 and random.random() < 0.15:
            if ResourceSystem.can_afford_xana_operation(
                self.world.xana.resource_pools,
                'deploy_monster'
            ):
                # Secteur avec tour active
                for tower in self.world.get_active_towers():
                    if random.random() < 0.3:
                        self._xana_spawn_monsters(tower.sector, 'kankrelat', 1)
                        ResourceSystem.consume_xana_operation(
                            self.world.xana.resource_pools,
                            'deploy_monster'
                        )
                        break

    # ============================================================
    # AGENT AI AUTONOME v2.0
    # ============================================================

    def _update_agent_ai(self):
        """Met à jour les décisions autonomes des agents."""
        perception_range = PerceptionRange(scan_range=1, accuracy=0.8)
        decisions = self.agent_ai_coordinator.update_all_agents(
            self.world,
            perception_range
        )

        # Log des décisions importantes
        for agent_id, decision in decisions.items():
            if decision.priority.value in ['survival', 'defense']:
                event = Event(
                    type=EventType.AGENT_ACTION,
                    tick=self.time.current_tick,
                    timestamp=self.time.get_timestamp(),
                    message=f"[AGENT] {agent_id}: {decision.reasoning}",
                    severity="AGENT",
                    data={'agent_id': agent_id, 'action': decision.action.value}
                )
                self.event_manager.emit(event)

    def _execute_agent_decisions(self):
        """Exécute les décisions des agents."""
        for agent_id, ai in self.agent_ai_coordinator.agent_ais.items():
            if ai.current_decision:
                ai.ticks_on_current_action += 1

                # Exécuter toutes les 3 ticks
                if ai.ticks_on_current_action >= 3:
                    success = self.agent_ai_coordinator.execute_agent_decision(
                        agent_id,
                        ai.current_decision,
                        self.world
                    )

                    if success:
                        agent = self.world.agents.get(agent_id)
                        if agent and hasattr(agent, 'psychological_state_v2'):
                            # Mise à jour psychologique selon le résultat
                            PsychologySystem.update_from_mission_outcome(
                                agent.psychological_state_v2,
                                success=True,
                                importance=0.5
                            )

                    ai.ticks_on_current_action = 0

    # ============================================================
    # SYSTÈMES v2.0
    # ============================================================

    def _update_psychology_v2(self):
        """Met à jour la psychologie avancée des agents."""
        for agent in self.world.agents.values():
            if not agent.is_operational():
                continue

            psy = agent.psychological_state_v2

            # Déterminer si isolé
            allies_nearby = len([a for a in self.world.agents.values()
                               if a.id != agent.id and a.sector == agent.sector and a.is_operational()])
            alone = (allies_nearby == 0)
            PsychologySystem.update_from_isolation(psy, alone, 1)

            # Exposition corruption
            sector = self.world.sectors.get(agent.sector)
            if sector:
                exposure = CorruptionSystem.calculate_sector_corruption_pressure(
                    sector,
                    len([t for t in self.world.get_towers_in_sector(sector.id) if t.is_active]),
                    0.5
                )
                PsychologySystem.update_from_corruption_exposure(psy, exposure)

            # Repos si en sécurité
            in_safe = sector.is_safe() if sector else False
            PsychologySystem.update_from_rest(psy, in_safe)

    def _update_corruption_v2(self):
        """Met à jour la corruption progressive."""
        for agent in self.world.agents.values():
            if not agent.is_operational():
                continue

            # Sources de corruption
            sources = {}

            sector = self.world.sectors.get(agent.sector)
            if sector:
                if sector.corruption_level > 0:
                    sources['corrupted_sector'] = sector.corruption_level

                # Tours actives
                active_towers = [t for t in self.world.get_towers_in_sector(sector.id) if t.is_active]
                if active_towers:
                    sources['tower_proximity'] = len(active_towers) * 0.3

            # Stress
            if hasattr(agent, 'psychological_state_v2'):
                sources['stress'] = agent.psychological_state_v2.stress
                sources['isolation'] = agent.psychological_state_v2.isolation_factor

            # Calculer résistance
            resistance = agent.psychological_state_v2.corruption_resistance if hasattr(agent, 'psychological_state_v2') else 0.8

            # Accumuler corruption
            new_level = CorruptionSystem.accumulate_corruption(
                agent.corruption_level,
                sources,
                resistance,
                dt=1.0
            )

            if new_level > agent.corruption_level:
                agent.corruption_level = new_level
                agent.increase_corruption(0)  # Met à jour le stade

                # Log si augmentation significative
                if new_level > 0.5 and agent.corruption_level <= 0.5:
                    event = Event(
                        type=EventType.CORRUPTION_INCREASED,
                        tick=self.time.current_tick,
                        timestamp=self.time.get_timestamp(),
                        message=f"[CORRUPTION] {agent.name} présente une corruption significative ({new_level:.0%})",
                        severity="CORRUPTION",
                        data={'agent_id': agent.id, 'level': new_level}
                    )
                    self.event_manager.emit(event)

    def _update_resources(self):
        """Met à jour les ressources."""
        # Régénération agents
        for agent in self.world.agents.values():
            if agent.is_operational() and hasattr(agent, 'resources'):
                ResourceSystem.regenerate_all_pools(agent.resources)

        # Régénération XANA
        if self.world.xana and hasattr(self.world.xana, 'resource_pools'):
            ResourceSystem.regenerate_all_pools(self.world.xana.resource_pools)

    # ============================================================
    # LEGACY SYSTEMS (conservés)
    # ============================================================

    def _update_towers(self):
        """Met à jour les tours."""
        for tower in self.world.towers.values():
            tower.update()

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
                message=f"[ALERTE] Tour {tower.name} activée dans {sector_name}",
                severity="ALERTE",
                data={'tower_id': tower.id, 'sector': sector_name}
            )
            self.event_manager.emit(event)

    def _xana_spawn_monsters(self, sector_name: str, monster_type_str: str, count: int):
        """XANA spawne des monstres."""
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
            message=f"[ALERTE] XANA déploie {count} {monster_type_str}(s) dans {sector_name}",
            severity="ALERTE",
            data={'monster_type': monster_type_str, 'count': count, 'sector': sector_name}
        )
        self.event_manager.emit(event)

    def _update_world_state(self):
        """Met à jour l'état global du monde."""
        if self.world.xana:
            active_towers = len(self.world.get_active_towers())
            active_monsters = self.world.get_active_monsters_count()

            self.world.xana.update_tower_count(active_towers)
            self.world.xana.update_monster_count(active_monsters)

            # Ressources passives legacy
            self.world.xana.gain_resources(active_towers * 2 + 5)

        # Corruption globale
        self.world.update_global_corruption()

    def _update_metrics(self):
        """Met à jour les métriques."""
        self.metrics.current.current_tick = self.time.current_tick
        self.metrics.current.simulation_time = self.time.elapsed_time
        self.metrics.current.is_running = self.autonomous_loop.state.value == 'running'
        self.metrics.current.is_paused = self.autonomous_loop.state.value == 'paused'
        self.metrics.current.simulation_speed = self.autonomous_loop.speed_multiplier

        # Mettre à jour depuis le monde
        self.metrics.update_from_world(self.world, self.xana_ai)

        # Snapshot périodique
        if self.time.current_tick % 10 == 0:
            self.metrics.snapshot()

    # ============================================================
    # QUERIES
    # ============================================================

    def get_status_summary(self) -> Dict[str, Any]:
        """Résumé de l'état de la simulation."""
        status = self.autonomous_loop.get_status()

        return {
            'tick': self.time.current_tick,
            'state': status['state'],
            'speed': status['speed_multiplier'],
            'tps_actual': status['actual_tps'],
            'agents_operational': self.world.get_operational_agents_count(),
            'monsters_active': self.world.get_active_monsters_count(),
            'towers_active': len(self.world.get_active_towers()),
            'corruption_global': f"{self.world.global_corruption:.0%}",
            'xana_power': self.world.xana.power_level if self.world.xana else 0,
            'metrics': self.metrics.current.to_dict()
        }
