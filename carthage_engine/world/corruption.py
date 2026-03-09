"""
Système de corruption progressive et systémique - v2.0.

La corruption est progressive, peut être subtile, et a des effets variés.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Any, List


class CorruptionStage(Enum):
    """Stades de corruption d'un agent."""
    CLEAN = "clean"
    EXPOSED = "exposed"
    DESTABILIZED = "destabilized"
    INFLUENCED = "influenced"
    PARTIALLY_CORRUPTED = "partially_corrupted"
    HEAVILY_CORRUPTED = "heavily_corrupted"
    LOST = "lost"


@dataclass
class CorruptionEffect:
    """Effet de corruption."""
    type: str
    severity: float  # 0.0 à 1.0
    visible: bool  # Si l'effet est immédiatement visible
    description: str


class CorruptionSystem:
    """Système gérant la corruption progressive."""

    # Seuils pour chaque stade
    STAGE_THRESHOLDS = {
        CorruptionStage.CLEAN: 0.0,
        CorruptionStage.EXPOSED: 0.05,
        CorruptionStage.DESTABILIZED: 0.15,
        CorruptionStage.INFLUENCED: 0.30,
        CorruptionStage.PARTIALLY_CORRUPTED: 0.50,
        CorruptionStage.HEAVILY_CORRUPTED: 0.75,
        CorruptionStage.LOST: 0.95
    }

    @staticmethod
    def get_corruption_stage(level: float) -> CorruptionStage:
        """Détermine le stade de corruption."""
        if level >= 0.95:
            return CorruptionStage.LOST
        elif level >= 0.75:
            return CorruptionStage.HEAVILY_CORRUPTED
        elif level >= 0.50:
            return CorruptionStage.PARTIALLY_CORRUPTED
        elif level >= 0.30:
            return CorruptionStage.INFLUENCED
        elif level >= 0.15:
            return CorruptionStage.DESTABILIZED
        elif level >= 0.05:
            return CorruptionStage.EXPOSED
        else:
            return CorruptionStage.CLEAN

    @staticmethod
    def accumulate_corruption(
        current_level: float,
        sources: dict,
        resistance: float,
        dt: float = 1.0
    ) -> float:
        """
        Accumule la corruption depuis multiples sources.

        Args:
            current_level: Niveau actuel
            sources: Dict {source: intensity}
            resistance: Résistance (0.0 à 1.0)
            dt: Delta temps

        Returns:
            Nouveau niveau de corruption
        """
        total_accumulation = 0.0

        for source, intensity in sources.items():
            # Calcul accumulation selon la source
            if source == 'tower_proximity':
                rate = 0.01 * intensity * (1.0 - resistance)
            elif source == 'corrupted_sector':
                rate = 0.005 * intensity * (1.0 - resistance)
            elif source == 'failed_combat':
                rate = 0.03 * intensity * (1.0 - resistance)
            elif source == 'stress':
                rate = 0.008 * intensity * (1.0 - resistance)
            elif source == 'isolation':
                rate = 0.006 * intensity * (1.0 - resistance)
            elif source == 'xana_operation':
                rate = 0.05 * intensity * (1.0 - resistance)
            elif source == 'corrupted_route':
                rate = 0.015 * intensity * (1.0 - resistance)
            else:
                rate = 0.01 * intensity * (1.0 - resistance)

            total_accumulation += rate * dt

        new_level = min(1.0, current_level + total_accumulation)
        return new_level

    @staticmethod
    def recover_corruption(
        current_level: float,
        recovery_sources: dict,
        dt: float = 1.0
    ) -> float:
        """
        Récupération de la corruption.

        Args:
            current_level: Niveau actuel
            recovery_sources: Dict {source: intensity}
            dt: Delta temps

        Returns:
            Nouveau niveau
        """
        total_recovery = 0.0

        for source, intensity in recovery_sources.items():
            if source == 'safe_sector':
                rate = 0.01 * intensity
            elif source == 'allied_support':
                rate = 0.015 * intensity
            elif source == 'rest':
                rate = 0.008 * intensity
            elif source == 'successful_deactivation':
                rate = 0.02 * intensity
            else:
                rate = 0.005 * intensity

            total_recovery += rate * dt

        new_level = max(0.0, current_level - total_recovery)
        return new_level

    @staticmethod
    def get_corruption_effects(level: float, stage: CorruptionStage) -> List[CorruptionEffect]:
        """
        Liste les effets actifs de corruption.

        Returns:
            Liste d'effets
        """
        effects = []

        if stage == CorruptionStage.EXPOSED:
            effects.append(CorruptionEffect(
                type='stress_increase',
                severity=0.1,
                visible=False,
                description='Augmentation légère du stress'
            ))

        elif stage == CorruptionStage.DESTABILIZED:
            effects.append(CorruptionEffect(
                type='reaction_slowdown',
                severity=0.15,
                visible=False,
                description='Temps de réaction ralenti'
            ))
            effects.append(CorruptionEffect(
                type='stress_increase',
                severity=0.2,
                visible=True,
                description='Stress accru visible'
            ))

        elif stage == CorruptionStage.INFLUENCED:
            effects.append(CorruptionEffect(
                type='poor_evaluation',
                severity=0.3,
                visible=False,
                description='Évaluation des menaces altérée'
            ))
            effects.append(CorruptionEffect(
                type='hesitation',
                severity=0.25,
                visible=True,
                description='Hésitations dans les décisions'
            ))
            effects.append(CorruptionEffect(
                type='false_reports',
                severity=0.2,
                visible=False,
                description='Rapports parfois inexacts'
            ))

        elif stage == CorruptionStage.PARTIALLY_CORRUPTED:
            effects.append(CorruptionEffect(
                type='bad_decisions',
                severity=0.5,
                visible=True,
                description='Mauvaises décisions tactiques'
            ))
            effects.append(CorruptionEffect(
                type='weak_support',
                severity=0.4,
                visible=True,
                description='Soutien aux alliés affaibli'
            ))
            effects.append(CorruptionEffect(
                type='route_errors',
                severity=0.3,
                visible=False,
                description='Choix de routes risquées'
            ))

        elif stage == CorruptionStage.HEAVILY_CORRUPTED:
            effects.append(CorruptionEffect(
                type='panic',
                severity=0.7,
                visible=True,
                description='Réactions paniquées'
            ))
            effects.append(CorruptionEffect(
                type='minor_sabotage',
                severity=0.5,
                visible=False,
                description='Sabotage mineur possible'
            ))
            effects.append(CorruptionEffect(
                type='hidden_influence',
                severity=0.6,
                visible=False,
                description='Influence XANA cachée'
            ))

        elif stage == CorruptionStage.LOST:
            effects.append(CorruptionEffect(
                type='full_control',
                severity=1.0,
                visible=True,
                description='Contrôle total par XANA'
            ))
            effects.append(CorruptionEffect(
                type='active_sabotage',
                severity=0.9,
                visible=True,
                description='Sabotage actif'
            ))

        return effects

    @staticmethod
    def apply_effects_to_agent(agent: Any, effects: List[CorruptionEffect]):
        """
        Applique les effets de corruption à un agent.

        Args:
            agent: Agent à affecter
            effects: Liste d'effets
        """
        for effect in effects:
            if effect.type == 'stress_increase':
                if hasattr(agent, 'psychological_state'):
                    agent.psychological_state.stress = min(1.0,
                        agent.psychological_state.stress + effect.severity * 0.1)

            elif effect.type == 'reaction_slowdown':
                # Affecte la vitesse de réaction (géré via psychological_state)
                pass

            elif effect.type == 'poor_evaluation':
                # Affecte la qualité des décisions
                if hasattr(agent, 'psychological_state'):
                    agent.psychological_state.operational_confidence *= (1.0 - effect.severity * 0.2)

            elif effect.type == 'hesitation':
                if hasattr(agent, 'psychological_state'):
                    agent.psychological_state.stress = min(1.0,
                        agent.psychological_state.stress + effect.severity * 0.15)

    @staticmethod
    def calculate_sector_corruption_pressure(
        sector: Any,
        active_towers: int,
        xana_presence: float
    ) -> float:
        """
        Calcule la pression de corruption d'un secteur.

        Returns:
            float entre 0.0 et 1.0
        """
        pressure = sector.corruption_level * 0.5
        pressure += active_towers * 0.2
        pressure += xana_presence * 0.3

        return min(1.0, pressure)
