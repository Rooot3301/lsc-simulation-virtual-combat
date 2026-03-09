"""
Système d'information imparfaite - v2.0.

Les agents et XANA ne disposent pas toujours d'informations complètes.
"""

from dataclasses import dataclass
from typing import Any, Optional, List
from enum import Enum
import random


class DetectionQuality(Enum):
    """Qualité de détection."""
    NONE = "none"
    UNCERTAIN = "uncertain"
    PARTIAL = "partial"
    GOOD = "good"
    PERFECT = "perfect"


@dataclass
class PerceptionRange:
    """Portée de perception d'une entité."""
    scan_range: int = 1  # Secteurs adjacents
    detection_threshold: float = 0.3  # Seuil de détection
    accuracy: float = 0.8  # Précision des détections


@dataclass
class ObservationReport:
    """Rapport d'observation (peut être imparfait)."""
    observed_entity: str
    entity_type: str
    location: str
    confidence: float  # 0.0 à 1.0
    quality: DetectionQuality
    noise_level: float = 0.0
    timestamp: int = 0
    observer_id: str = ""

    def is_reliable(self) -> bool:
        """Le rapport est-il fiable?"""
        return self.confidence >= 0.7 and self.quality in [DetectionQuality.GOOD, DetectionQuality.PERFECT]

    def get_noisy_location(self) -> str:
        """Retourne une localisation potentiellement bruitée."""
        if self.noise_level > 0.5 and random.random() < self.noise_level:
            # Fausse localisation
            return f"{self.location}_uncertain"
        return self.location


class InformationSystem:
    """Système gérant l'information imparfaite."""

    @staticmethod
    def calculate_detection_probability(
        observer_range: PerceptionRange,
        target_signature: float,
        distance: int,
        interference: float = 0.0
    ) -> float:
        """
        Calcule la probabilité de détection.

        Args:
            observer_range: Portée de l'observateur
            target_signature: Signature de la cible (0.0 à 1.0)
            distance: Distance en secteurs
            interference: Interférence (0.0 à 1.0)

        Returns:
            Probabilité entre 0.0 et 1.0
        """
        if distance > observer_range.scan_range:
            return 0.0

        # Base sur la signature
        base_prob = target_signature

        # Réduction avec la distance
        distance_penalty = (distance / (observer_range.scan_range + 1)) * 0.4
        base_prob -= distance_penalty

        # Réduction avec l'interférence
        base_prob *= (1.0 - interference * 0.5)

        # Seuil de détection
        if base_prob < observer_range.detection_threshold:
            return 0.0

        return max(0.0, min(1.0, base_prob))

    @staticmethod
    def generate_observation_report(
        observer_id: str,
        target: Any,
        distance: int,
        observer_perception: PerceptionRange,
        observer_stress: float = 0.0,
        observer_corruption: float = 0.0,
        tick: int = 0
    ) -> Optional[ObservationReport]:
        """
        Génère un rapport d'observation.

        Args:
            observer_id: ID de l'observateur
            target: Cible observée
            distance: Distance
            observer_perception: Capacités de perception
            observer_stress: Niveau de stress de l'observateur
            observer_corruption: Niveau de corruption
            tick: Tick actuel

        Returns:
            Rapport ou None si non détecté
        """
        # Signature de la cible
        target_signature = getattr(target, 'signature', 0.7)

        # Probabilité de détection
        detection_prob = InformationSystem.calculate_detection_probability(
            observer_perception,
            target_signature,
            distance
        )

        # Facteurs humains dégradent la détection
        detection_prob *= (1.0 - observer_stress * 0.3)
        detection_prob *= (1.0 - observer_corruption * 0.4)

        # Test de détection
        if random.random() > detection_prob:
            return None

        # Calculer la qualité
        if detection_prob >= 0.9:
            quality = DetectionQuality.PERFECT
            confidence = 1.0
        elif detection_prob >= 0.7:
            quality = DetectionQuality.GOOD
            confidence = 0.8
        elif detection_prob >= 0.5:
            quality = DetectionQuality.PARTIAL
            confidence = 0.6
        else:
            quality = DetectionQuality.UNCERTAIN
            confidence = 0.4

        # Bruit introduit par stress et corruption
        noise = observer_stress * 0.3 + observer_corruption * 0.5

        # Type d'entité
        entity_type = target.__class__.__name__

        # Localisation
        location = getattr(target, 'sector', getattr(target, 'current_node', 'unknown'))

        return ObservationReport(
            observed_entity=target.id,
            entity_type=entity_type,
            location=location,
            confidence=confidence,
            quality=quality,
            noise_level=noise,
            timestamp=tick,
            observer_id=observer_id
        )

    @staticmethod
    def can_detect_corruption(
        observer_corruption: float,
        target_corruption: float,
        observer_experience: float = 0.5
    ) -> bool:
        """
        Un observateur peut-il détecter la corruption d'une cible?

        Args:
            observer_corruption: Corruption de l'observateur
            target_corruption: Corruption de la cible
            observer_experience: Expérience de l'observateur

        Returns:
            True si détectable
        """
        # Un observateur corrompu détecte mal la corruption
        if observer_corruption > 0.3:
            return False

        # Corruption forte est plus facilement détectable
        if target_corruption > 0.7:
            return random.random() < (0.6 + observer_experience * 0.3)

        # Corruption modérée
        if target_corruption > 0.4:
            return random.random() < (0.3 + observer_experience * 0.4)

        # Corruption faible difficile à détecter
        return random.random() < (0.1 + observer_experience * 0.2)

    @staticmethod
    def introduce_report_errors(
        report: ObservationReport,
        error_probability: float = 0.0
    ) -> ObservationReport:
        """
        Introduit des erreurs dans un rapport.

        Args:
            report: Rapport original
            error_probability: Probabilité d'erreur

        Returns:
            Rapport potentiellement altéré
        """
        if random.random() < error_probability:
            # Réduire la confiance
            report.confidence *= 0.6

            # Augmenter le bruit
            report.noise_level = min(1.0, report.noise_level + 0.3)

            # Dégrader la qualité
            if report.quality == DetectionQuality.PERFECT:
                report.quality = DetectionQuality.GOOD
            elif report.quality == DetectionQuality.GOOD:
                report.quality = DetectionQuality.PARTIAL
            elif report.quality == DetectionQuality.PARTIAL:
                report.quality = DetectionQuality.UNCERTAIN

        return report

    @staticmethod
    def aggregate_reports(reports: List[ObservationReport]) -> ObservationReport:
        """
        Agrège plusieurs rapports sur la même entité.

        Args:
            reports: Liste de rapports

        Returns:
            Rapport agrégé
        """
        if not reports:
            raise ValueError("Pas de rapports à agréger")

        if len(reports) == 1:
            return reports[0]

        # Prendre le rapport le plus récent comme base
        latest = max(reports, key=lambda r: r.timestamp)

        # Moyenne pondérée de la confiance
        total_confidence = sum(r.confidence for r in reports) / len(reports)

        # Meilleure qualité observée
        best_quality = max(r.quality for r in reports, key=lambda q: {
            DetectionQuality.PERFECT: 5,
            DetectionQuality.GOOD: 4,
            DetectionQuality.PARTIAL: 3,
            DetectionQuality.UNCERTAIN: 2,
            DetectionQuality.NONE: 1
        }[q])

        # Minimum de bruit
        min_noise = min(r.noise_level for r in reports)

        latest.confidence = total_confidence
        latest.quality = best_quality
        latest.noise_level = min_noise

        return latest
