"""
Formatters pour les logs.
"""

from ..core.events import Event


class LogFormatter:
    """Formatte les logs pour l'affichage."""

    @staticmethod
    def format_event(event: Event) -> str:
        """Formate un événement."""
        return f"[{event.severity}] {event.timestamp} - {event.message}"

    @staticmethod
    def format_status(status: dict) -> str:
        """Formate un statut."""
        lines = []
        lines.append("=== STATUT DE LA SIMULATION ===")
        for key, value in status.items():
            lines.append(f"{key}: {value}")
        return "\n".join(lines)
