"""
Couche de perception XANA - v2.0.

XANA évalue continuellement l'état du monde.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any
from enum import Enum


class ThreatLevel(Enum):
    """Niveau de menace."""
    MINIMAL = "minimal"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class SectorAssessment:
    """Évaluation d'un secteur."""
    sector_id: str
    corruption_level: float
    agent_presence: int
    tower_status: str  # 'none', 'inactive', 'active'
    threat_to_xana: ThreatLevel
    opportunity_score: float
    strategic_value: float
    vulnerability: float


@dataclass
class AgentThreatAssessment:
    """Évaluation de menace d'un agent."""
    agent_id: str
    combat_capability: float
    current_threat: float
    corruption_vulnerability: float
    stress_level: float
    isolation_factor: float
    strategic_importance: float


@dataclass
class PerceptionSnapshot:
    """Snapshot de la perception XANA à un instant T."""
    tick: int
    global_threat: float = 0.0
    global_opportunity: float = 0.0
    sector_assessments: Dict[str, SectorAssessment] = field(default_factory=dict)
    agent_threats: Dict[str, AgentThreatAssessment] = field(default_factory=dict)
    skid_threat: float = 0.0
    skid_vulnerability: float = 0.0
    opportunity_windows: List[str] = field(default_factory=list)


class XANAPerceptionLayer:
    """Couche de perception stratégique de XANA."""

    def __init__(self):
        self.current_perception: PerceptionSnapshot = PerceptionSnapshot(tick=0)
        self.perception_history: List[PerceptionSnapshot] = []

    def perceive_world(self, world: Any, tick: int) -> PerceptionSnapshot:
        """
        Évalue l'état actuel du monde.

        Args:
            world: État du monde
            tick: Tick actuel

        Returns:
            Snapshot de perception
        """
        snapshot = PerceptionSnapshot(tick=tick)

        # Évaluer les secteurs
        for sector_id, sector in world.sectors.items():
            assessment = self._assess_sector(sector, world)
            snapshot.sector_assessments[sector_id] = assessment

        # Évaluer les agents
        for agent_id, agent in world.agents.items():
            assessment = self._assess_agent(agent, world)
            snapshot.agent_threats[agent_id] = assessment

        # Évaluer le Skid
        if world.skid:
            snapshot.skid_threat = self._assess_skid_threat(world.skid)
            snapshot.skid_vulnerability = self._assess_skid_vulnerability(world.skid)

        # Calculer menace globale
        snapshot.global_threat = self._calculate_global_threat(snapshot)

        # Calculer opportunités globales
        snapshot.global_opportunity = self._calculate_global_opportunity(snapshot)

        # Identifier fenêtres d'opportunité
        snapshot.opportunity_windows = self._identify_opportunity_windows(snapshot)

        # Sauvegarder
        self.current_perception = snapshot
        self.perception_history.append(snapshot)

        # Limiter l'historique
        if len(self.perception_history) > 100:
            self.perception_history = self.perception_history[-100:]

        return snapshot

    def _assess_sector(self, sector: Any, world: Any) -> SectorAssessment:
        """Évalue un secteur."""

        # Présence d'agents
        agent_count = len([a for a in world.agents.values() if a.sector == sector.name])

        # Statut tours
        tower_status = 'none'
        for tower_id in sector.tower_ids:
            tower = world.towers.get(tower_id)
            if tower:
                if tower.is_active:
                    tower_status = 'active'
                elif tower_status != 'active':
                    tower_status = 'inactive'

        # Niveau de menace pour XANA
        threat = ThreatLevel.MINIMAL
        if agent_count >= 3:
            threat = ThreatLevel.CRITICAL
        elif agent_count == 2:
            threat = ThreatLevel.HIGH
        elif agent_count == 1:
            threat = ThreatLevel.MODERATE

        # Score d'opportunité
        opportunity = sector.corruption_level * 0.5
        opportunity += (1.0 - agent_count / 4.0) * 0.3
        if tower_status == 'inactive':
            opportunity += 0.2

        # Valeur stratégique
        strategic_value = 0.5
        if sector.name == 'sector5':
            strategic_value = 1.0
        elif 'network' in sector.name.lower():
            strategic_value = 0.8

        # Vulnérabilité
        vulnerability = 1.0 - agent_count / 4.0
        vulnerability *= (1.0 - sector.corruption_level) * 0.5
        vulnerability += 0.5 if tower_status == 'inactive' else 0.0

        return SectorAssessment(
            sector_id=sector.name,
            corruption_level=sector.corruption_level,
            agent_presence=agent_count,
            tower_status=tower_status,
            threat_to_xana=threat,
            opportunity_score=min(1.0, opportunity),
            strategic_value=strategic_value,
            vulnerability=min(1.0, vulnerability)
        )

    def _assess_agent(self, agent: Any, world: Any) -> AgentThreatAssessment:
        """Évalue la menace d'un agent."""

        # Capacité de combat
        combat_cap = (agent.health / agent.max_health) * 0.6
        if hasattr(agent, 'psychological_state'):
            combat_cap += (1.0 - agent.psychological_state.stress) * 0.4

        # Menace actuelle
        threat = combat_cap * 0.5
        threat += (1.0 - agent.corruption_level) * 0.3
        if hasattr(agent, 'psychological_state'):
            threat += (1.0 - agent.psychological_state.fatigue) * 0.2

        # Vulnérabilité à la corruption
        corruption_vuln = agent.corruption_level * 0.3
        if hasattr(agent, 'psychological_state'):
            corruption_vuln += agent.psychological_state.stress * 0.4
            # Utilise isolation (legacy) ou isolation_factor (v2)
            isolation_val = getattr(agent.psychological_state, 'isolation_factor', getattr(agent.psychological_state, 'isolation', 0.0))
            corruption_vuln += isolation_val * 0.3

        # Niveau de stress
        stress = getattr(agent.psychological_state, 'stress', 0.0) if hasattr(agent, 'psychological_state') else 0.0

        # Facteur d'isolation
        isolation = getattr(agent.psychological_state, 'isolation_factor', getattr(agent.psychological_state, 'isolation', 0.0)) if hasattr(agent, 'psychological_state') else 0.0

        # Importance stratégique (certains agents sont plus importants)
        importance = 0.7
        if 'aelita' in agent.id.lower():
            importance = 1.0  # Aelita est critique

        return AgentThreatAssessment(
            agent_id=agent.id,
            combat_capability=combat_cap,
            current_threat=threat,
            corruption_vulnerability=min(1.0, corruption_vuln),
            stress_level=stress,
            isolation_factor=isolation,
            strategic_importance=importance
        )

    def _assess_skid_threat(self, skid: Any) -> float:
        """Évalue la menace du Skid."""
        threat = (skid.hull_integrity / 100.0) * 0.5
        threat += (skid.energy / 100.0) * 0.3
        threat += len(skid.passengers) / 4.0 * 0.2
        return min(1.0, threat)

    def _assess_skid_vulnerability(self, skid: Any) -> float:
        """Évalue la vulnérabilité du Skid."""
        vuln = 1.0 - (skid.hull_integrity / 100.0) * 0.4
        vuln += skid.danger_level * 0.4
        vuln += (1.0 - skid.energy / 100.0) * 0.2
        return min(1.0, vuln)

    def _calculate_global_threat(self, snapshot: PerceptionSnapshot) -> float:
        """Calcule la menace globale pour XANA."""
        if not snapshot.agent_threats:
            return 0.0

        # Moyenne pondérée des menaces agents
        total_threat = sum(
            assessment.current_threat * assessment.strategic_importance
            for assessment in snapshot.agent_threats.values()
        )

        agent_count = len(snapshot.agent_threats)
        threat = total_threat / agent_count if agent_count > 0 else 0.0

        # Ajout menace Skid
        threat += snapshot.skid_threat * 0.2

        return min(1.0, threat)

    def _calculate_global_opportunity(self, snapshot: PerceptionSnapshot) -> float:
        """Calcule l'opportunité globale."""
        if not snapshot.sector_assessments:
            return 0.0

        # Somme des opportunités sectorielles
        total_opportunity = sum(
            assessment.opportunity_score * assessment.strategic_value
            for assessment in snapshot.sector_assessments.values()
        )

        sector_count = len(snapshot.sector_assessments)
        opportunity = total_opportunity / sector_count if sector_count > 0 else 0.0

        return min(1.0, opportunity)

    def _identify_opportunity_windows(self, snapshot: PerceptionSnapshot) -> List[str]:
        """Identifie les fenêtres d'opportunité tactique."""
        opportunities = []

        # Secteurs vulnérables
        for sector_id, assessment in snapshot.sector_assessments.items():
            if assessment.vulnerability > 0.6 and assessment.threat_to_xana == ThreatLevel.MINIMAL:
                opportunities.append(f"sector_vulnerable:{sector_id}")

        # Agents isolés et vulnérables
        for agent_id, assessment in snapshot.agent_threats.items():
            if assessment.isolation_factor > 0.6 and assessment.corruption_vulnerability > 0.5:
                opportunities.append(f"agent_vulnerable:{agent_id}")

        # Skid vulnérable
        if snapshot.skid_vulnerability > 0.7:
            opportunities.append("skid_vulnerable")

        return opportunities

    def get_most_threatening_agents(self, top_n: int = 3) -> List[AgentThreatAssessment]:
        """Retourne les N agents les plus menaçants."""
        threats = list(self.current_perception.agent_threats.values())
        threats.sort(key=lambda x: x.current_threat * x.strategic_importance, reverse=True)
        return threats[:top_n]

    def get_most_vulnerable_sectors(self, top_n: int = 3) -> List[SectorAssessment]:
        """Retourne les N secteurs les plus vulnérables."""
        sectors = list(self.current_perception.sector_assessments.values())
        sectors.sort(key=lambda x: x.vulnerability * x.strategic_value, reverse=True)
        return sectors[:top_n]
