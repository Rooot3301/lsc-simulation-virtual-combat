"""
Système de psychologie profonde pour les agents - v2.0.

Gère les facteurs humains complexes influençant le comportement.
"""

from dataclasses import dataclass, field
from typing import Dict
from enum import Enum


class MentalState(Enum):
    """État mental de l'agent."""
    OPTIMAL = "optimal"
    STABLE = "stable"
    STRESSED = "stressé"
    FATIGUED = "fatigué"
    ANXIOUS = "anxieux"
    PANICKED = "paniqué"
    BROKEN = "effondré"


@dataclass
class PsychologicalState:
    """
    État psychologique complet d'un agent.

    Tous les valeurs entre 0.0 et 1.0.
    """

    # États de base
    stress: float = 0.0
    fatigue: float = 0.0
    morale: float = 1.0

    # Résistance et stabilité
    mental_resistance: float = 0.8
    stability: float = 1.0
    operational_confidence: float = 1.0

    # Facteurs sociaux
    trust_with_team: Dict[str, float] = field(default_factory=dict)
    isolation_factor: float = 0.0

    # Récupération
    recovery_rate: float = 0.1
    safe_time: int = 0  # Ticks passés en sécurité

    # Exposition corruption
    corruption_exposure: float = 0.0
    corruption_resistance: float = 0.9

    def get_mental_state(self) -> MentalState:
        """Détermine l'état mental actuel."""
        if self.stress > 0.9 or self.fatigue > 0.9:
            return MentalState.BROKEN
        elif self.stress > 0.7:
            return MentalState.PANICKED
        elif self.stress > 0.5 or self.fatigue > 0.6:
            return MentalState.ANXIOUS
        elif self.fatigue > 0.4:
            return MentalState.FATIGUED
        elif self.stress > 0.3:
            return MentalState.STRESSED
        elif self.stress < 0.1 and self.fatigue < 0.2:
            return MentalState.OPTIMAL
        else:
            return MentalState.STABLE

    def get_effectiveness_multiplier(self) -> float:
        """
        Multiplicateur d'efficacité basé sur l'état psychologique.

        Returns:
            float entre 0.0 et 1.2 (peut dépasser 1.0 si optimal)
        """
        state = self.get_mental_state()

        if state == MentalState.OPTIMAL:
            return 1.2
        elif state == MentalState.STABLE:
            return 1.0
        elif state == MentalState.STRESSED:
            return 0.85
        elif state == MentalState.FATIGUED:
            return 0.7
        elif state == MentalState.ANXIOUS:
            return 0.6
        elif state == MentalState.PANICKED:
            return 0.4
        else:  # BROKEN
            return 0.2

    def get_decision_quality(self) -> float:
        """
        Qualité des décisions (précision, jugement).

        Returns:
            float entre 0.1 et 1.0
        """
        base = 1.0 - (self.stress * 0.5) - (self.fatigue * 0.3)
        base *= self.operational_confidence
        return max(0.1, min(1.0, base))

    def get_reaction_speed(self) -> float:
        """
        Vitesse de réaction.

        Returns:
            float entre 0.3 et 1.0
        """
        return max(0.3, 1.0 - (self.fatigue * 0.6) - (self.stress * 0.2))

    def get_corruption_vulnerability(self) -> float:
        """
        Vulnérabilité à la corruption.

        Returns:
            float entre 0.0 et 1.0 (plus haut = plus vulnérable)
        """
        # Le stress et l'isolation augmentent la vulnérabilité
        vulnerability = (self.stress * 0.4) + (self.isolation_factor * 0.3)
        vulnerability += (1.0 - self.mental_resistance) * 0.2
        vulnerability -= self.corruption_resistance * 0.3
        vulnerability += self.corruption_exposure * 0.1

        return max(0.0, min(1.0, vulnerability))


class PsychologySystem:
    """Système gérant l'évolution psychologique des agents."""

    @staticmethod
    def update_from_combat(state: PsychologicalState, victory: bool, intensity: float):
        """
        Met à jour après un combat.

        Args:
            state: État psychologique
            victory: True si victoire
            intensity: Intensité du combat (0.0 à 1.0)
        """
        if victory:
            # Victoire réduit le stress, augmente la confiance
            state.stress = max(0.0, state.stress - 0.05 * intensity)
            state.operational_confidence = min(1.0, state.operational_confidence + 0.02)
            state.morale = min(1.0, state.morale + 0.03)
        else:
            # Défaite augmente stress et fatigue
            state.stress = min(1.0, state.stress + 0.15 * intensity)
            state.fatigue = min(1.0, state.fatigue + 0.1 * intensity)
            state.operational_confidence = max(0.0, state.operational_confidence - 0.05)
            state.morale = max(0.0, state.morale - 0.05)

    @staticmethod
    def update_from_isolation(state: PsychologicalState, alone: bool, ticks: int):
        """
        Met à jour en fonction de l'isolation.

        Args:
            state: État psychologique
            alone: Si l'agent est isolé
            ticks: Nombre de ticks d'isolation
        """
        if alone:
            # L'isolation augmente progressivement
            increase = min(0.01 * ticks, 0.5)
            state.isolation_factor = min(1.0, increase)
            state.stress = min(1.0, state.stress + 0.005 * ticks)
        else:
            # Récupération de l'isolation
            state.isolation_factor = max(0.0, state.isolation_factor - 0.05)

    @staticmethod
    def update_from_corruption_exposure(state: PsychologicalState, exposure_level: float):
        """
        Met à jour l'exposition à la corruption.

        Args:
            state: État psychologique
            exposure_level: Niveau d'exposition (0.0 à 1.0)
        """
        # Accumulation progressive
        increase = exposure_level * (1.0 - state.corruption_resistance) * 0.01
        state.corruption_exposure = min(1.0, state.corruption_exposure + increase)

        # L'exposition augmente le stress
        state.stress = min(1.0, state.stress + increase * 0.5)

    @staticmethod
    def update_from_rest(state: PsychologicalState, in_safe_sector: bool):
        """
        Met à jour pendant une période de repos.

        Args:
            state: État psychologique
            in_safe_sector: Si dans un secteur sûr
        """
        if in_safe_sector:
            state.safe_time += 1

            # Récupération progressive
            recovery_amount = state.recovery_rate * 0.1

            state.stress = max(0.0, state.stress - recovery_amount)
            state.fatigue = max(0.0, state.fatigue - recovery_amount * 0.8)
            state.corruption_exposure = max(0.0, state.corruption_exposure - recovery_amount * 0.3)

            # Amélioration du moral si repos prolongé
            if state.safe_time > 5:
                state.morale = min(1.0, state.morale + 0.01)
        else:
            state.safe_time = 0

    @staticmethod
    def update_from_mission_outcome(state: PsychologicalState, success: bool, importance: float):
        """
        Met à jour après une mission.

        Args:
            state: État psychologique
            success: Succès ou échec
            importance: Importance de la mission (0.0 à 1.0)
        """
        if success:
            state.operational_confidence = min(1.0, state.operational_confidence + 0.05 * importance)
            state.morale = min(1.0, state.morale + 0.03 * importance)
            state.stress = max(0.0, state.stress - 0.02)
        else:
            state.operational_confidence = max(0.0, state.operational_confidence - 0.08 * importance)
            state.morale = max(0.0, state.morale - 0.05 * importance)
            state.stress = min(1.0, state.stress + 0.1 * importance)

    @staticmethod
    def update_trust(state: PsychologicalState, ally_id: str, delta: float):
        """
        Met à jour la confiance envers un allié.

        Args:
            state: État psychologique
            ally_id: ID de l'allié
            delta: Changement de confiance (-1.0 à +1.0)
        """
        current = state.trust_with_team.get(ally_id, 0.5)
        new_trust = max(0.0, min(1.0, current + delta))
        state.trust_with_team[ally_id] = new_trust

    @staticmethod
    def get_report_reliability(state: PsychologicalState) -> float:
        """
        Fiabilité des rapports de l'agent.

        Returns:
            float entre 0.0 et 1.0
        """
        # Affecté par stress, fatigue, et corruption
        reliability = 1.0
        reliability -= state.stress * 0.3
        reliability -= state.fatigue * 0.2
        reliability -= state.corruption_exposure * 0.4

        return max(0.0, min(1.0, reliability))
