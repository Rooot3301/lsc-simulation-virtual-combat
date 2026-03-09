"""
IA autonome des agents - v2.0.

Les agents peuvent réagir et décider de manière autonome.
"""

from dataclasses import dataclass
from typing import List, Optional, Any, Dict
from enum import Enum
import random


class AgentAction(Enum):
    """Actions possibles pour un agent."""
    PATROL = "patrol"
    DEACTIVATE_TOWER = "deactivate_tower"
    COMBAT_MONSTER = "combat_monster"
    SUPPORT_ALLY = "support_ally"
    RETREAT = "retreat"
    REST = "rest"
    SCAN_SECTOR = "scan_sector"
    PROTECT_SECTOR = "protect_sector"
    REGROUP = "regroup"
    INVESTIGATE = "investigate"


class AgentPriority(Enum):
    """Priorités d'action."""
    SURVIVAL = "survival"
    MISSION = "mission"
    SUPPORT = "support"
    DEFENSE = "defense"
    RECOVERY = "recovery"


@dataclass
class AgentDecision:
    """Décision prise par un agent."""
    action: AgentAction
    target: str  # Cible de l'action
    priority: AgentPriority
    confidence: float  # 0.0 à 1.0
    reasoning: str  # Explication en français


class AgentAI:
    """IA pour un agent individuel."""

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.current_decision: Optional[AgentDecision] = None
        self.decision_history: List[AgentDecision] = []
        self.ticks_on_current_action = 0

    def decide_action(
        self,
        agent: Any,
        world: Any,
        perception_range: Any
    ) -> Optional[AgentDecision]:
        """
        Prend une décision d'action autonome.

        Args:
            agent: L'agent
            world: État du monde
            perception_range: Portée de perception

        Returns:
            Décision ou None
        """
        # Évaluer la situation
        situation = self._evaluate_situation(agent, world)

        # Déterminer la priorité principale
        priority = self._determine_priority(agent, situation)

        # Choisir l'action selon la priorité
        decision = None

        if priority == AgentPriority.SURVIVAL:
            decision = self._decide_survival_action(agent, world, situation)

        elif priority == AgentPriority.RECOVERY:
            decision = self._decide_recovery_action(agent, world, situation)

        elif priority == AgentPriority.MISSION:
            decision = self._decide_mission_action(agent, world, situation)

        elif priority == AgentPriority.DEFENSE:
            decision = self._decide_defense_action(agent, world, situation)

        elif priority == AgentPriority.SUPPORT:
            decision = self._decide_support_action(agent, world, situation)

        if decision:
            self.current_decision = decision
            self.decision_history.append(decision)
            self.ticks_on_current_action = 0

            # Limiter l'historique
            if len(self.decision_history) > 50:
                self.decision_history = self.decision_history[-50:]

        return decision

    def _evaluate_situation(self, agent: Any, world: Any) -> Dict[str, Any]:
        """Évalue la situation tactique actuelle."""
        situation = {
            'immediate_threat': False,
            'nearby_threats': 0,
            'active_towers_nearby': 0,
            'allies_nearby': 0,
            'in_safe_sector': False,
            'sector_corruption': 0.0,
            'health_critical': False,
            'fatigue_high': False,
            'stress_high': False,
            'isolated': False
        }

        # Santé critique
        if agent.health < agent.max_health * 0.3:
            situation['health_critical'] = True

        # État psychologique
        if hasattr(agent, 'psychological_state'):
            psy = agent.psychological_state
            if psy.fatigue > 0.7:
                situation['fatigue_high'] = True
            if psy.stress > 0.7:
                situation['stress_high'] = True
            if psy.isolation_factor > 0.6:
                situation['isolated'] = True

        # Secteur actuel
        current_sector = world.sectors.get(agent.sector)
        if current_sector:
            situation['sector_corruption'] = current_sector.corruption_level
            situation['in_safe_sector'] = current_sector.is_safe()

            # Tours actives dans le secteur
            for tower_id in current_sector.tower_ids:
                tower = world.towers.get(tower_id)
                if tower and tower.is_active:
                    situation['active_towers_nearby'] += 1
                    situation['immediate_threat'] = True

        # Monstres proches
        for monster in world.monsters.values():
            if not monster.is_destroyed and monster.sector == agent.sector:
                situation['nearby_threats'] += 1
                situation['immediate_threat'] = True

        # Alliés proches
        for other_agent in world.agents.values():
            if other_agent.id != agent.id and other_agent.sector == agent.sector:
                if other_agent.is_operational():
                    situation['allies_nearby'] += 1

        return situation

    def _determine_priority(self, agent: Any, situation: Dict) -> AgentPriority:
        """Détermine la priorité d'action."""

        # Survie d'abord
        if situation['health_critical'] or (situation['immediate_threat'] and situation['allies_nearby'] == 0):
            return AgentPriority.SURVIVAL

        # Récupération si nécessaire
        if (situation['fatigue_high'] or situation['stress_high']) and situation['in_safe_sector']:
            return AgentPriority.RECOVERY

        # Défense si menace active
        if situation['active_towers_nearby'] > 0 or situation['nearby_threats'] > 0:
            return AgentPriority.DEFENSE

        # Support si allié en difficulté
        if situation['allies_nearby'] > 0 and random.random() < 0.3:
            return AgentPriority.SUPPORT

        # Sinon mission
        return AgentPriority.MISSION

    def _decide_survival_action(
        self,
        agent: Any,
        world: Any,
        situation: Dict
    ) -> AgentDecision:
        """Décide une action de survie."""

        # Fuir vers un secteur sûr
        safe_sectors = [s for s in world.sectors.values() if s.is_safe()]

        if safe_sectors:
            target_sector = random.choice(safe_sectors)
            return AgentDecision(
                action=AgentAction.RETREAT,
                target=target_sector.id,
                priority=AgentPriority.SURVIVAL,
                confidence=0.9,
                reasoning=f"Santé critique ou menace immédiate, repli vers {target_sector.id}"
            )

        # Si pas de secteur sûr, se regrouper
        return AgentDecision(
            action=AgentAction.REGROUP,
            target="allies",
            priority=AgentPriority.SURVIVAL,
            confidence=0.7,
            reasoning="Aucun secteur sûr, tentative de regroupement"
        )

    def _decide_recovery_action(
        self,
        agent: Any,
        world: Any,
        situation: Dict
    ) -> AgentDecision:
        """Décide une action de récupération."""

        return AgentDecision(
            action=AgentAction.REST,
            target=agent.sector,
            priority=AgentPriority.RECOVERY,
            confidence=0.8,
            reasoning="Récupération nécessaire (fatigue/stress élevé)"
        )

    def _decide_mission_action(
        self,
        agent: Any,
        world: Any,
        situation: Dict
    ) -> AgentDecision:
        """Décide une action de mission."""

        # Désactiver une tour inactive proche
        current_sector = world.sectors.get(agent.sector)
        if current_sector:
            for tower_id in current_sector.tower_ids:
                tower = world.towers.get(tower_id)
                if tower and not tower.is_active and not tower.is_deactivated:
                    return AgentDecision(
                        action=AgentAction.DEACTIVATE_TOWER,
                        target=tower_id,
                        priority=AgentPriority.MISSION,
                        confidence=0.7,
                        reasoning=f"Tentative de désactivation de la tour {tower_id}"
                    )

        # Scanner un secteur corrompu
        corrupted_sectors = [s for s in world.sectors.values()
                           if s.corruption_level > 0.3 and not s.is_safe()]

        if corrupted_sectors:
            target = random.choice(corrupted_sectors)
            return AgentDecision(
                action=AgentAction.SCAN_SECTOR,
                target=target.id,
                priority=AgentPriority.MISSION,
                confidence=0.6,
                reasoning=f"Reconnaissance du secteur corrompu {target.id}"
            )

        # Patrouille par défaut
        return AgentDecision(
            action=AgentAction.PATROL,
            target=agent.sector,
            priority=AgentPriority.MISSION,
            confidence=0.5,
            reasoning="Patrouille de routine"
        )

    def _decide_defense_action(
        self,
        agent: Any,
        world: Any,
        situation: Dict
    ) -> AgentDecision:
        """Décide une action défensive."""

        # Désactiver tour active en priorité
        if situation['active_towers_nearby'] > 0:
            current_sector = world.sectors.get(agent.sector)
            if current_sector:
                for tower_id in current_sector.tower_ids:
                    tower = world.towers.get(tower_id)
                    if tower and tower.is_active:
                        return AgentDecision(
                            action=AgentAction.DEACTIVATE_TOWER,
                            target=tower_id,
                            priority=AgentPriority.DEFENSE,
                            confidence=0.85,
                            reasoning=f"Désactivation urgente de la tour active {tower_id}"
                        )

        # Combattre monstres
        if situation['nearby_threats'] > 0:
            # Trouver un monstre
            for monster in world.monsters.values():
                if not monster.is_destroyed and monster.sector == agent.sector:
                    return AgentDecision(
                        action=AgentAction.COMBAT_MONSTER,
                        target=monster.id,
                        priority=AgentPriority.DEFENSE,
                        confidence=0.75,
                        reasoning=f"Engagement contre monstre {monster.id}"
                    )

        # Protéger le secteur
        return AgentDecision(
            action=AgentAction.PROTECT_SECTOR,
            target=agent.sector,
            priority=AgentPriority.DEFENSE,
            confidence=0.7,
            reasoning=f"Protection du secteur {agent.sector}"
        )

    def _decide_support_action(
        self,
        agent: Any,
        world: Any,
        situation: Dict
    ) -> AgentDecision:
        """Décide une action de support."""

        # Trouver un allié en difficulté
        for ally in world.agents.values():
            if ally.id != agent.id and ally.sector == agent.sector:
                if ally.health < ally.max_health * 0.5:
                    return AgentDecision(
                        action=AgentAction.SUPPORT_ALLY,
                        target=ally.id,
                        priority=AgentPriority.SUPPORT,
                        confidence=0.8,
                        reasoning=f"Support de {ally.id} en difficulté"
                    )

        # Regroupement par défaut
        return AgentDecision(
            action=AgentAction.REGROUP,
            target="allies",
            priority=AgentPriority.SUPPORT,
            confidence=0.6,
            reasoning="Regroupement avec les alliés"
        )


class AgentAICoordinator:
    """Coordonnateur pour toutes les IA d'agents."""

    def __init__(self):
        self.agent_ais: Dict[str, AgentAI] = {}

    def get_or_create_ai(self, agent_id: str) -> AgentAI:
        """Récupère ou crée une IA pour un agent."""
        if agent_id not in self.agent_ais:
            self.agent_ais[agent_id] = AgentAI(agent_id)
        return self.agent_ais[agent_id]

    def update_all_agents(self, world: Any, perception_range: Any):
        """Met à jour toutes les décisions d'agents."""
        decisions = {}

        for agent_id, agent in world.agents.items():
            if not agent.is_operational():
                continue

            ai = self.get_or_create_ai(agent_id)
            decision = ai.decide_action(agent, world, perception_range)

            if decision:
                decisions[agent_id] = decision

        return decisions

    def execute_agent_decision(
        self,
        agent_id: str,
        decision: AgentDecision,
        world: Any
    ) -> bool:
        """
        Exécute la décision d'un agent.

        Returns:
            True si exécution réussie
        """
        agent = world.agents.get(agent_id)
        if not agent:
            return False

        # Selon l'action
        if decision.action == AgentAction.DEACTIVATE_TOWER:
            tower = world.towers.get(decision.target)
            if tower:
                # Tentative de désactivation
                success_chance = 0.7
                if hasattr(agent, 'psychological_state'):
                    success_chance *= agent.psychological_state.get_effectiveness_multiplier()

                if random.random() < success_chance:
                    tower.is_active = False
                    tower.is_deactivated = True
                    return True

        elif decision.action == AgentAction.COMBAT_MONSTER:
            monster = world.monsters.get(decision.target)
            if monster and not monster.is_destroyed:
                # Combat simplifié
                damage = 30
                if hasattr(agent, 'psychological_state'):
                    damage *= agent.psychological_state.get_effectiveness_multiplier()

                monster.health -= damage
                if monster.health <= 0:
                    monster.is_destroyed = True
                return True

        elif decision.action == AgentAction.RETREAT:
            # Changer de secteur
            agent.sector = decision.target
            return True

        elif decision.action == AgentAction.REST:
            # Récupération
            if hasattr(agent, 'psychological_state'):
                from carthage_engine.systems.psychology import PsychologySystem
                current_sector = world.sectors.get(agent.sector)
                in_safe = current_sector.is_safe() if current_sector else False
                PsychologySystem.update_from_rest(agent.psychological_state, in_safe)
            return True

        return False
