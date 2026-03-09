"""
Cœur de l'intelligence artificielle XANA.
Orchestre tous les sous-systèmes d'IA.
"""

from typing import Dict, Any, List, Optional
from .xana_planner import XANAPlanner, StrategicGoal, StrategicPlan
from .xana_memory import XANAMemory, MemoryType
from .xana_doctrine import XANADoctrine, DoctrineRule
from .threat_map import ThreatMap
from .vulnerability import VulnerabilityAnalyzer, Vulnerability
import random


class XANACore:
    """
    Cœur de l'IA XANA.
    Orchestre la planification, la mémoire, la doctrine et l'analyse.
    """

    def __init__(self):
        self.planner = XANAPlanner()
        self.memory = XANAMemory(max_size=1000)
        self.doctrine = XANADoctrine(
            primary_rule=DoctrineRule.OPPORTUNISTIC,
            aggression_level=0.5,
            risk_tolerance=0.5
        )
        self.threat_map = ThreatMap()
        self.vulnerability_analyzer = VulnerabilityAnalyzer()

        # État interne
        self.current_goal: Optional[StrategicGoal] = None
        self.current_plan: Optional[StrategicPlan] = None
        self.decision_cooldown: int = 0

    def perceive(self, world_state: Dict[str, Any], tick: int, timestamp: str):
        """
        Perception de l'état du monde.
        Analyse la situation et met à jour les systèmes internes.
        """
        # Met à jour la carte des menaces
        self._update_threat_map(world_state)

        # Analyse les vulnérabilités
        self._analyze_vulnerabilities(world_state, tick)

        # Enregistre l'observation en mémoire
        self.memory.add_memory(
            memory_type=MemoryType.OBSERVATION,
            tick=tick,
            timestamp=timestamp,
            data={
                'agents_count': world_state.get('agents_count', 0),
                'active_towers': world_state.get('active_towers', 0),
                'corruption_level': world_state.get('global_corruption', 0.0),
                'skid_operational': world_state.get('skid_operational', False)
            },
            importance=0.3,
            tags=['perception', 'world_state']
        )

    def decide(self, world_state: Dict[str, Any], tick: int, timestamp: str) -> Optional[StrategicPlan]:
        """
        Prise de décision stratégique.
        Retourne un plan d'action ou None.
        """
        # Cooldown entre les décisions
        if self.decision_cooldown > 0:
            self.decision_cooldown -= 1
            return None

        # Vérifie si un plan est en cours
        if self.current_plan and not self.current_plan.is_completed:
            return self.current_plan

        # Adapte la doctrine à la situation
        self.doctrine.adapt_to_situation(world_state)

        # Sélectionne un nouvel objectif
        goal = self._select_strategic_goal(world_state)
        if not goal:
            return None

        # Détermine le secteur cible
        target_sector = self._select_target_sector(goal, world_state)

        # Crée un plan
        plan = self.planner.create_plan(goal, target_sector, tick, world_state)

        self.current_goal = goal
        self.current_plan = plan
        self.decision_cooldown = 5

        # Enregistre en mémoire
        self.memory.add_memory(
            memory_type=MemoryType.PATTERN,
            tick=tick,
            timestamp=timestamp,
            data={
                'goal': goal.value,
                'target_sector': target_sector,
                'plan_id': plan.id
            },
            importance=0.7,
            tags=['decision', 'planning', goal.value]
        )

        return plan

    def _select_strategic_goal(self, world_state: Dict[str, Any]) -> Optional[StrategicGoal]:
        """Sélectionne un objectif stratégique."""
        # Priorités selon la doctrine
        if self.doctrine.primary_rule == DoctrineRule.AGGRESSIVE:
            goals = [
                StrategicGoal.DOMINATE_SECTOR,
                StrategicGoal.ELIMINATE_THREAT,
                StrategicGoal.ACTIVATE_TOWERS
            ]
        elif self.doctrine.primary_rule == DoctrineRule.DEFENSIVE:
            goals = [
                StrategicGoal.DEFEND_TERRITORY,
                StrategicGoal.ACTIVATE_TOWERS
            ]
        elif self.doctrine.primary_rule == DoctrineRule.SUBTLE:
            goals = [
                StrategicGoal.CORRUPT_AGENT,
                StrategicGoal.SPREAD_CORRUPTION,
                StrategicGoal.TRAP_AGENTS
            ]
        elif self.doctrine.primary_rule == DoctrineRule.OPPORTUNISTIC:
            # Exploite les vulnérabilités
            vulns = self.vulnerability_analyzer.get_exploitable_vulnerabilities()
            if vulns:
                vuln = vulns[0]
                if 'agent' in vuln.target:
                    return StrategicGoal.CORRUPT_AGENT
                if vuln.vulnerability_type.value == 'skid_exposé':
                    return StrategicGoal.INTERCEPT_SKID

            goals = [
                StrategicGoal.DOMINATE_SECTOR,
                StrategicGoal.SPREAD_CORRUPTION,
                StrategicGoal.ACTIVATE_TOWERS
            ]
        else:
            goals = [
                StrategicGoal.DOMINATE_SECTOR,
                StrategicGoal.SPREAD_CORRUPTION
            ]

        # Conditions spéciales
        if world_state.get('skid_operational', False):
            if random.random() < 0.3:
                return StrategicGoal.INTERCEPT_SKID

        if world_state.get('under_attack', False):
            return StrategicGoal.DEFEND_TERRITORY

        # Sélection aléatoire pondérée
        return random.choice(goals) if goals else None

    def _select_target_sector(self, goal: StrategicGoal, world_state: Dict[str, Any]) -> str:
        """Sélectionne le secteur cible selon l'objectif."""
        sectors = world_state.get('sectors', {})

        if goal == StrategicGoal.DOMINATE_SECTOR:
            # Secteur avec faible défense
            for name, sector in sectors.items():
                if len(sector.entity_ids) < 2 and sector.corruption_level < 0.5:
                    return name

        elif goal == StrategicGoal.DEFEND_TERRITORY:
            # Secteur avec tours actives
            for name, sector in sectors.items():
                if len(sector.tower_ids) > 0 and sector.corruption_level > 0.5:
                    return name

        elif goal == StrategicGoal.INTERCEPT_SKID:
            return 'network'

        # Par défaut, secteur aléatoire
        sector_names = ['forest', 'desert', 'ice', 'mountain', 'sector5']
        return random.choice(sector_names)

    def _update_threat_map(self, world_state: Dict[str, Any]):
        """Met à jour la carte des menaces."""
        sectors = world_state.get('sectors', {})

        for sector_name, sector in sectors.items():
            enemy_count = len(sector.entity_ids)
            enemy_strength = enemy_count * 2.0
            strategic_value = 5.0 if sector_name == 'sector5' else 3.0

            self.threat_map.update_zone_threat(
                sector_name,
                enemy_count,
                enemy_strength,
                strategic_value
            )

    def _analyze_vulnerabilities(self, world_state: Dict[str, Any], tick: int):
        """Analyse les vulnérabilités."""
        # Nettoie les vieilles vulnérabilités
        self.vulnerability_analyzer.clear_old_vulnerabilities(tick, max_age=20)

        # Analyse agents
        agents = world_state.get('agents', [])
        self.vulnerability_analyzer.analyze_agents(agents, tick)

        # Analyse secteurs
        sectors = world_state.get('sectors', {})
        self.vulnerability_analyzer.analyze_sectors(sectors, tick)

        # Analyse Skid
        skid = world_state.get('skid', None)
        if skid:
            self.vulnerability_analyzer.analyze_skid(skid, tick)

    def adapt(self, success: bool, tick: int, timestamp: str):
        """S'adapte en fonction du résultat d'une action."""
        if success:
            self.memory.add_memory(
                memory_type=MemoryType.SUCCESS,
                tick=tick,
                timestamp=timestamp,
                data={'goal': self.current_goal.value if self.current_goal else 'unknown'},
                importance=0.8,
                tags=['success', 'adaptation']
            )
            self.doctrine.aggression_level = min(1.0, self.doctrine.aggression_level + 0.05)
        else:
            self.memory.add_memory(
                memory_type=MemoryType.FAILURE,
                tick=tick,
                timestamp=timestamp,
                data={'goal': self.current_goal.value if self.current_goal else 'unknown'},
                importance=0.9,
                tags=['failure', 'adaptation']
            )
            self.doctrine.aggression_level = max(0.1, self.doctrine.aggression_level - 0.05)
            self.doctrine.adapt_to_situation({'under_heavy_attack': True})

    def get_current_state_summary(self) -> Dict[str, Any]:
        """Retourne un résumé de l'état de l'IA."""
        return {
            'current_goal': self.current_goal.value if self.current_goal else None,
            'active_plans': len(self.planner.get_active_plans()),
            'memory_count': self.memory.get_memory_count(),
            'doctrine': self.doctrine.primary_rule.value,
            'aggression': self.doctrine.aggression_level,
            'vulnerabilities_detected': len(self.vulnerability_analyzer.vulnerabilities),
            'highest_threat_zone': (
                self.threat_map.get_highest_threat_zone().location
                if self.threat_map.get_highest_threat_zone()
                else None
            )
        }
