"""
Système de planification stratégique de XANA.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any, Optional
import random


class StrategicGoal(Enum):
    """Objectifs stratégiques de XANA."""
    DOMINATE_SECTOR = "dominer_secteur"
    SPREAD_CORRUPTION = "propager_corruption"
    INTERCEPT_SKID = "intercepter_skid"
    CORRUPT_AGENT = "corrompre_agent"
    CREATE_DIVERSION = "créer_diversion"
    TRAP_AGENTS = "piéger_agents"
    ISOLATE_SECTOR5 = "isoler_secteur5"
    ACTIVATE_TOWERS = "activer_tours"
    DEFEND_TERRITORY = "défendre_territoire"
    ELIMINATE_THREAT = "éliminer_menace"


@dataclass
class PlanAction:
    """Action dans un plan stratégique."""

    action_type: str
    target: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    priority: int = 1
    is_completed: bool = False
    tick_created: int = 0
    tick_executed: int = 0


@dataclass
class StrategicPlan:
    """Plan stratégique de XANA."""

    id: str
    goal: StrategicGoal
    target_sector: str
    actions: List[PlanAction] = field(default_factory=list)
    priority: int = 1
    is_active: bool = True
    is_completed: bool = False
    success_probability: float = 0.5
    tick_created: int = 0
    tick_completed: int = 0

    def add_action(self, action: PlanAction):
        """Ajoute une action au plan."""
        self.actions.append(action)

    def get_next_action(self) -> Optional[PlanAction]:
        """Retourne la prochaine action à exécuter."""
        for action in self.actions:
            if not action.is_completed:
                return action
        return None

    def complete_action(self, action: PlanAction, tick: int):
        """Marque une action comme complétée."""
        action.is_completed = True
        action.tick_executed = tick

        # Vérifie si toutes les actions sont complétées
        if all(a.is_completed for a in self.actions):
            self.is_completed = True
            self.tick_completed = tick

    def get_progress(self) -> float:
        """Retourne le progrès du plan (0.0 à 1.0)."""
        if not self.actions:
            return 0.0
        completed = sum(1 for a in self.actions if a.is_completed)
        return completed / len(self.actions)


class XANAPlanner:
    """Planificateur stratégique de XANA."""

    def __init__(self):
        self.plans: List[StrategicPlan] = []
        self.plan_counter = 0

    def create_plan(
        self,
        goal: StrategicGoal,
        target_sector: str,
        tick: int,
        world_state: Dict[str, Any]
    ) -> StrategicPlan:
        """Crée un plan stratégique basé sur l'objectif."""
        plan_id = f"PLAN_{self.plan_counter:04d}"
        self.plan_counter += 1

        plan = StrategicPlan(
            id=plan_id,
            goal=goal,
            target_sector=target_sector,
            tick_created=tick,
            priority=self._calculate_priority(goal, world_state)
        )

        # Génère les actions selon l'objectif
        actions = self._generate_actions_for_goal(goal, target_sector, tick, world_state)
        for action in actions:
            plan.add_action(action)

        # Calcule la probabilité de succès
        plan.success_probability = self._estimate_success_probability(plan, world_state)

        self.plans.append(plan)
        return plan

    def _calculate_priority(self, goal: StrategicGoal, world_state: Dict[str, Any]) -> int:
        """Calcule la priorité d'un objectif."""
        priorities = {
            StrategicGoal.ELIMINATE_THREAT: 10,
            StrategicGoal.DEFEND_TERRITORY: 9,
            StrategicGoal.INTERCEPT_SKID: 8,
            StrategicGoal.CORRUPT_AGENT: 7,
            StrategicGoal.DOMINATE_SECTOR: 6,
            StrategicGoal.TRAP_AGENTS: 6,
            StrategicGoal.ISOLATE_SECTOR5: 5,
            StrategicGoal.ACTIVATE_TOWERS: 4,
            StrategicGoal.SPREAD_CORRUPTION: 3,
            StrategicGoal.CREATE_DIVERSION: 2
        }
        return priorities.get(goal, 5)

    def _generate_actions_for_goal(
        self,
        goal: StrategicGoal,
        target_sector: str,
        tick: int,
        world_state: Dict[str, Any]
    ) -> List[PlanAction]:
        """Génère les actions pour un objectif donné."""
        actions = []

        if goal == StrategicGoal.DOMINATE_SECTOR:
            actions = [
                PlanAction("activate_tower", target_sector, {"count": 2}, 1, tick_created=tick),
                PlanAction("spawn_monsters", target_sector, {"type": "kankrelat", "count": 3}, 2, tick_created=tick),
                PlanAction("spread_corruption", target_sector, {"intensity": 0.3}, 3, tick_created=tick),
                PlanAction("fortify_towers", target_sector, {"defenders": 2}, 4, tick_created=tick)
            ]

        elif goal == StrategicGoal.INTERCEPT_SKID:
            actions = [
                PlanAction("detect_skid", "network", {}, 1, tick_created=tick),
                PlanAction("block_corridor", "network", {"corridor": "C-5"}, 2, tick_created=tick),
                PlanAction("spawn_monsters", "network", {"type": "manta", "count": 2}, 3, tick_created=tick),
                PlanAction("ambush", "network", {"position": "N-HUB-1"}, 4, tick_created=tick)
            ]

        elif goal == StrategicGoal.CORRUPT_AGENT:
            actions = [
                PlanAction("identify_vulnerable_agent", target_sector, {}, 1, tick_created=tick),
                PlanAction("isolate_agent", target_sector, {"method": "divide"}, 2, tick_created=tick),
                PlanAction("increase_sector_corruption", target_sector, {"intensity": 0.5}, 3, tick_created=tick),
                PlanAction("psychological_pressure", target_sector, {"duration": 5}, 4, tick_created=tick),
                PlanAction("corruption_attempt", target_sector, {}, 5, tick_created=tick)
            ]

        elif goal == StrategicGoal.ACTIVATE_TOWERS:
            actions = [
                PlanAction("activate_tower", target_sector, {"tower_id": "auto"}, 1, tick_created=tick),
                PlanAction("activate_tower", target_sector, {"tower_id": "auto"}, 2, tick_created=tick),
                PlanAction("spawn_defenders", target_sector, {"count": 2}, 3, tick_created=tick)
            ]

        elif goal == StrategicGoal.SPREAD_CORRUPTION:
            actions = [
                PlanAction("activate_tower", target_sector, {}, 1, tick_created=tick),
                PlanAction("spread_corruption", target_sector, {"intensity": 0.4}, 2, tick_created=tick),
                PlanAction("corrupt_adjacent_sectors", target_sector, {}, 3, tick_created=tick)
            ]

        elif goal == StrategicGoal.TRAP_AGENTS:
            actions = [
                PlanAction("create_lure", target_sector, {"type": "fake_tower"}, 1, tick_created=tick),
                PlanAction("position_ambush", target_sector, {"monsters": 4}, 2, tick_created=tick),
                PlanAction("block_exits", target_sector, {}, 3, tick_created=tick),
                PlanAction("spring_trap", target_sector, {}, 4, tick_created=tick)
            ]

        elif goal == StrategicGoal.DEFEND_TERRITORY:
            actions = [
                PlanAction("spawn_monsters", target_sector, {"type": "blok", "count": 2}, 1, tick_created=tick),
                PlanAction("fortify_towers", target_sector, {}, 2, tick_created=tick),
                PlanAction("patrol_sector", target_sector, {"routes": 3}, 3, tick_created=tick)
            ]

        elif goal == StrategicGoal.ISOLATE_SECTOR5:
            actions = [
                PlanAction("corrupt_corridor", "network", {"corridor": "C-1"}, 1, tick_created=tick),
                PlanAction("activate_tower", "sector5", {}, 2, tick_created=tick),
                PlanAction("spawn_monsters", "sector5", {"type": "megatank", "count": 1}, 3, tick_created=tick),
                PlanAction("block_access", "sector5", {}, 4, tick_created=tick)
            ]

        elif goal == StrategicGoal.CREATE_DIVERSION:
            actions = [
                PlanAction("activate_tower", target_sector, {}, 1, tick_created=tick),
                PlanAction("spawn_monsters", target_sector, {"count": 5}, 2, tick_created=tick),
                PlanAction("create_distraction", target_sector, {}, 3, tick_created=tick)
            ]

        elif goal == StrategicGoal.ELIMINATE_THREAT:
            actions = [
                PlanAction("identify_threat", target_sector, {}, 1, tick_created=tick),
                PlanAction("spawn_hunters", target_sector, {"type": "hornet", "count": 3}, 2, tick_created=tick),
                PlanAction("engage_target", target_sector, {}, 3, tick_created=tick)
            ]

        return actions

    def _estimate_success_probability(
        self,
        plan: StrategicPlan,
        world_state: Dict[str, Any]
    ) -> float:
        """Estime la probabilité de succès d'un plan."""
        base_probability = 0.5

        # Facteurs positifs
        if world_state.get('xana_power', 1.0) > 3.0:
            base_probability += 0.2

        if world_state.get('active_towers', 0) > 5:
            base_probability += 0.15

        # Facteurs négatifs
        if world_state.get('agents_active', 0) > 3:
            base_probability -= 0.2

        if world_state.get('skid_operational', False):
            base_probability -= 0.1

        return max(0.1, min(0.9, base_probability))

    def get_active_plans(self) -> List[StrategicPlan]:
        """Retourne tous les plans actifs."""
        return [p for p in self.plans if p.is_active and not p.is_completed]

    def get_highest_priority_plan(self) -> Optional[StrategicPlan]:
        """Retourne le plan de plus haute priorité."""
        active_plans = self.get_active_plans()
        if not active_plans:
            return None
        return max(active_plans, key=lambda p: p.priority)

    def complete_plan(self, plan_id: str, tick: int, success: bool):
        """Marque un plan comme complété."""
        for plan in self.plans:
            if plan.id == plan_id:
                plan.is_completed = True
                plan.is_active = False
                plan.tick_completed = tick
                return

    def abandon_plan(self, plan_id: str):
        """Abandonne un plan."""
        for plan in self.plans:
            if plan.id == plan_id:
                plan.is_active = False
                return

    def clear_completed_plans(self):
        """Nettoie les plans complétés."""
        self.plans = [p for p in self.plans if not p.is_completed]
