"""
Couche stratégique XANA - v2.0.

Sélectionne les objectifs stratégiques et crée les plans.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum
import random


class StrategicGoal(Enum):
    """Objectifs stratégiques de XANA."""
    DOMINATE_SECTOR = "dominate_sector"
    SPREAD_CORRUPTION = "spread_corruption"
    INTERCEPT_SKID = "intercept_skid"
    CORRUPT_AGENT = "corrupt_agent"
    CREATE_DIVERSION = "create_diversion"
    ISOLATE_SECTOR5 = "isolate_sector5"
    EXHAUST_DEFENDERS = "exhaust_defenders"
    TRAP_AGENTS = "trap_agents"
    OVERLOAD_RESPONSE = "overload_response"
    NETWORK_DESTABILIZATION = "network_destabilization"
    PASSIVE_GROWTH = "passive_growth"


class PlanPhase(Enum):
    """Phase d'exécution d'un plan."""
    PREPARATION = "preparation"
    OBSERVATION = "observation"
    EXECUTION = "execution"
    COMPLETION = "completion"
    FAILED = "failed"


@dataclass
class StrategicPlan:
    """Plan stratégique multi-étapes."""
    goal: StrategicGoal
    target: str  # Cible du plan (secteur, agent, etc.)
    priority: float  # 0.0 à 1.0
    phase: PlanPhase = PlanPhase.PREPARATION

    # Étapes du plan
    steps: List[str] = field(default_factory=list)
    current_step: int = 0

    # Conditions
    success_conditions: List[str] = field(default_factory=list)
    failure_conditions: List[str] = field(default_factory=list)
    fallback_goal: Optional[StrategicGoal] = None

    # Métriques
    ticks_active: int = 0
    progress: float = 0.0

    def advance_step(self):
        """Avance à l'étape suivante."""
        self.current_step += 1
        if self.current_step >= len(self.steps):
            self.phase = PlanPhase.COMPLETION
            self.progress = 1.0
        else:
            self.progress = self.current_step / len(self.steps)

    def get_current_step_description(self) -> str:
        """Retourne la description de l'étape actuelle."""
        if 0 <= self.current_step < len(self.steps):
            return self.steps[self.current_step]
        return "Aucune étape"

    def mark_failed(self):
        """Marque le plan comme échoué."""
        self.phase = PlanPhase.FAILED
        self.progress = 0.0


class XANAStrategicLayer:
    """Couche de décision stratégique de XANA."""

    def __init__(self):
        self.active_plans: List[StrategicPlan] = []
        self.completed_plans: List[StrategicPlan] = []
        self.failed_plans: List[StrategicPlan] = []

        # Préférences adaptatives
        self.goal_preferences: Dict[StrategicGoal, float] = {
            goal: 0.5 for goal in StrategicGoal
        }

        # Historique de succès
        self.goal_success_rates: Dict[StrategicGoal, List[bool]] = {
            goal: [] for goal in StrategicGoal
        }

    def select_strategic_goal(
        self,
        perception: Any,
        doctrine: Any,
        resources: Dict[str, Any]
    ) -> Optional[StrategicGoal]:
        """
        Sélectionne un objectif stratégique.

        Args:
            perception: Perception actuelle
            doctrine: Doctrine active
            resources: Ressources disponibles

        Returns:
            Objectif sélectionné ou None
        """
        # Limiter le nombre de plans actifs
        if len(self.active_plans) >= 3:
            return None

        # Évaluer chaque objectif potentiel
        goal_scores = {}

        for goal in StrategicGoal:
            score = self._evaluate_goal_viability(goal, perception, doctrine, resources)
            goal_scores[goal] = score

        # Filtrer les objectifs non viables
        viable_goals = {g: s for g, s in goal_scores.items() if s > 0.3}

        if not viable_goals:
            return StrategicGoal.PASSIVE_GROWTH

        # Sélection pondérée par score et préférences
        weighted_scores = {
            g: s * self.goal_preferences[g]
            for g, s in viable_goals.items()
        }

        # Sélection probabiliste
        total_weight = sum(weighted_scores.values())
        if total_weight == 0:
            return None

        rand = random.random() * total_weight
        cumulative = 0.0

        for goal, weight in weighted_scores.items():
            cumulative += weight
            if rand <= cumulative:
                return goal

        return list(weighted_scores.keys())[0]

    def _evaluate_goal_viability(
        self,
        goal: StrategicGoal,
        perception: Any,
        doctrine: Any,
        resources: Dict[str, Any]
    ) -> float:
        """Évalue la viabilité d'un objectif (0.0 à 1.0)."""

        score = 0.5  # Base

        if goal == StrategicGoal.DOMINATE_SECTOR:
            # Viable si secteurs vulnérables
            vulnerable = perception.get_most_vulnerable_sectors(1)
            if vulnerable:
                score = vulnerable[0].vulnerability * vulnerable[0].strategic_value

        elif goal == StrategicGoal.SPREAD_CORRUPTION:
            # Viable si corruption globale basse
            avg_corruption = perception.current_perception.global_opportunity
            score = (1.0 - avg_corruption) * 0.8

        elif goal == StrategicGoal.INTERCEPT_SKID:
            # Viable si Skid vulnérable
            score = perception.current_perception.skid_vulnerability

        elif goal == StrategicGoal.CORRUPT_AGENT:
            # Viable si agents vulnérables
            threats = perception.get_most_threatening_agents(1)
            if threats:
                score = threats[0].corruption_vulnerability * threats[0].strategic_importance

        elif goal == StrategicGoal.CREATE_DIVERSION:
            # Viable si menace globale élevée
            score = perception.current_perception.global_threat * 0.7

        elif goal == StrategicGoal.ISOLATE_SECTOR5:
            # Objectif à long terme, moins urgent
            score = 0.4

        elif goal == StrategicGoal.EXHAUST_DEFENDERS:
            # Viable si agents stressés
            agents = perception.current_perception.agent_threats.values()
            avg_stress = sum(a.stress_level for a in agents) / len(agents) if agents else 0
            score = avg_stress * 0.8

        elif goal == StrategicGoal.TRAP_AGENTS:
            # Tactique avancée
            score = 0.5

        elif goal == StrategicGoal.OVERLOAD_RESPONSE:
            # Viable si ressources suffisantes
            power_available = resources.get('power', {}).get('current', 0)
            score = min(1.0, power_available / 50.0) * 0.6

        elif goal == StrategicGoal.NETWORK_DESTABILIZATION:
            # Objectif réseau
            score = 0.5

        elif goal == StrategicGoal.PASSIVE_GROWTH:
            # Toujours viable mais peu prioritaire
            score = 0.3

        # Ajustement selon doctrine
        if hasattr(doctrine, 'primary_rule'):
            rule = doctrine.primary_rule.value
            if rule == 'opportuniste' and goal in [StrategicGoal.CORRUPT_AGENT, StrategicGoal.INTERCEPT_SKID]:
                score *= 1.3
            elif rule == 'agressif' and goal in [StrategicGoal.DOMINATE_SECTOR, StrategicGoal.TRAP_AGENTS]:
                score *= 1.4
            elif rule == 'manipulateur' and goal in [StrategicGoal.CORRUPT_AGENT, StrategicGoal.EXHAUST_DEFENDERS]:
                score *= 1.5

        return min(1.0, score)

    def create_plan(
        self,
        goal: StrategicGoal,
        perception: Any,
        priority: float = 0.7
    ) -> StrategicPlan:
        """
        Crée un plan pour un objectif.

        Args:
            goal: Objectif stratégique
            perception: Perception actuelle
            priority: Priorité (0.0 à 1.0)

        Returns:
            Plan créé
        """
        plan = StrategicPlan(goal=goal, target="", priority=priority)

        if goal == StrategicGoal.DOMINATE_SECTOR:
            vulnerable = perception.get_most_vulnerable_sectors(1)
            if vulnerable:
                sector = vulnerable[0]
                plan.target = sector.sector_id
                plan.steps = [
                    f"Observer le secteur {sector.sector_id}",
                    "Activer une tour dans le secteur",
                    "Déployer des monstres",
                    "Augmenter la corruption",
                    "Établir la domination"
                ]
                plan.success_conditions = [f"corruption_{sector.sector_id} > 0.7"]
                plan.failure_conditions = ["presence_agents > 2"]
                plan.fallback_goal = StrategicGoal.CREATE_DIVERSION

        elif goal == StrategicGoal.CORRUPT_AGENT:
            threats = perception.get_most_threatening_agents(1)
            if threats:
                agent = threats[0]
                plan.target = agent.agent_id
                plan.steps = [
                    f"Identifier la vulnérabilité de {agent.agent_id}",
                    "Augmenter l'exposition à la corruption",
                    "Isoler l'agent",
                    "Appliquer pression psychologique",
                    "Finaliser la corruption"
                ]
                plan.success_conditions = [f"corruption_{agent.agent_id} > 0.5"]
                plan.failure_conditions = ["agent_supported", "agent_in_safe_sector"]
                plan.fallback_goal = StrategicGoal.EXHAUST_DEFENDERS

        elif goal == StrategicGoal.INTERCEPT_SKID:
            plan.target = "skid"
            plan.steps = [
                "Détecter la route du Skid",
                "Identifier le corridor vulnérable",
                "Créer une diversion",
                "Positionner des monstres",
                "Lancer l'interception"
            ]
            plan.success_conditions = ["skid_damage > 30"]
            plan.failure_conditions = ["skid_escapes", "heavy_agent_support"]
            plan.fallback_goal = StrategicGoal.NETWORK_DESTABILIZATION

        elif goal == StrategicGoal.SPREAD_CORRUPTION:
            plan.target = "global"
            plan.steps = [
                "Activer tours dormantes",
                "Augmenter influence réseau",
                "Propager dans secteurs faibles",
                "Stabiliser la corruption"
            ]
            plan.success_conditions = ["global_corruption > 0.4"]
            plan.failure_conditions = ["towers_deactivated > 3"]

        elif goal == StrategicGoal.EXHAUST_DEFENDERS:
            plan.target = "agents"
            plan.steps = [
                "Créer multiples menaces simultanées",
                "Forcer déplacements constants",
                "Maintenir pression continue",
                "Exploiter la fatigue"
            ]
            plan.success_conditions = ["avg_agent_fatigue > 0.6"]
            plan.failure_conditions = ["agents_resting > 2"]

        else:
            # Plan générique
            plan.target = "general"
            plan.steps = [
                "Observer",
                "Préparer",
                "Exécuter",
                "Consolider"
            ]

        return plan

    def update_active_plans(self, perception: Any, world: Any):
        """Met à jour les plans actifs."""
        plans_to_remove = []

        for plan in self.active_plans:
            plan.ticks_active += 1

            # Vérifier conditions d'échec
            if self._check_failure_conditions(plan, perception, world):
                plan.mark_failed()
                self.failed_plans.append(plan)
                plans_to_remove.append(plan)
                self._record_goal_outcome(plan.goal, False)
                continue

            # Vérifier conditions de succès
            if self._check_success_conditions(plan, perception, world):
                plan.phase = PlanPhase.COMPLETION
                self.completed_plans.append(plan)
                plans_to_remove.append(plan)
                self._record_goal_outcome(plan.goal, True)
                continue

            # Progression naturelle
            if plan.phase == PlanPhase.PREPARATION and plan.ticks_active > 3:
                plan.phase = PlanPhase.OBSERVATION
            elif plan.phase == PlanPhase.OBSERVATION and plan.ticks_active > 6:
                plan.phase = PlanPhase.EXECUTION

            # Avancer les étapes progressivement
            if plan.phase == PlanPhase.EXECUTION and plan.ticks_active % 5 == 0:
                plan.advance_step()

        # Retirer plans terminés
        for plan in plans_to_remove:
            self.active_plans.remove(plan)

    def _check_success_conditions(self, plan: StrategicPlan, perception: Any, world: Any) -> bool:
        """Vérifie si les conditions de succès sont remplies."""
        # Simplification: succès après un certain temps en exécution
        if plan.phase == PlanPhase.EXECUTION and plan.progress >= 0.8:
            return True
        return False

    def _check_failure_conditions(self, plan: StrategicPlan, perception: Any, world: Any) -> bool:
        """Vérifie si les conditions d'échec sont remplies."""
        # Échec si trop long
        if plan.ticks_active > 50:
            return True
        return False

    def _record_goal_outcome(self, goal: StrategicGoal, success: bool):
        """Enregistre le résultat d'un objectif."""
        self.goal_success_rates[goal].append(success)

        # Limiter l'historique
        if len(self.goal_success_rates[goal]) > 10:
            self.goal_success_rates[goal] = self.goal_success_rates[goal][-10:]

        # Adapter les préférences
        success_rate = sum(self.goal_success_rates[goal]) / len(self.goal_success_rates[goal])
        self.goal_preferences[goal] = 0.3 + success_rate * 0.7

    def get_current_primary_goal(self) -> Optional[StrategicGoal]:
        """Retourne l'objectif principal actuel."""
        if not self.active_plans:
            return None

        # Plan avec la plus haute priorité
        primary = max(self.active_plans, key=lambda p: p.priority)
        return primary.goal
