"""
Styles et couleurs pour l'interface Rich.
"""

from rich.style import Style

# Palette de couleurs pour centre de commande
STYLES = {
    # Niveaux de logs
    'INFO': Style(color='bright_cyan'),
    'ALERTE': Style(color='yellow', bold=True),
    'CRITIQUE': Style(color='red', bold=True),
    'DEBUG': Style(color='bright_black'),
    'IA': Style(color='magenta', bold=True),
    'COMBAT': Style(color='red'),
    'CORRUPTION': Style(color='dark_orange', bold=True),
    'STRATEGIE': Style(color='bright_magenta', bold=True),
    'RESEAU': Style(color='blue'),
    'SKID': Style(color='cyan', bold=True),

    # Éléments UI
    'header': Style(color='bright_white', bold=True),
    'panel_border': Style(color='blue'),
    'panel_title': Style(color='bright_cyan', bold=True),
    'metric_label': Style(color='bright_black'),
    'metric_value': Style(color='bright_white', bold=True),
    'metric_good': Style(color='green', bold=True),
    'metric_warning': Style(color='yellow', bold=True),
    'metric_danger': Style(color='red', bold=True),

    # Statuts
    'status_active': Style(color='green'),
    'status_inactive': Style(color='bright_black'),
    'status_corrupted': Style(color='red', bold=True),
    'status_warning': Style(color='yellow'),

    # Texte
    'title': Style(color='bright_cyan', bold=True),
    'subtitle': Style(color='cyan'),
    'emphasis': Style(color='bright_white', bold=True),
    'dim': Style(color='bright_black'),
}

def get_severity_style(severity: str) -> Style:
    """Retourne le style pour un niveau de sévérité."""
    return STYLES.get(severity, STYLES['INFO'])

def get_corruption_style(level: float) -> Style:
    """Retourne le style selon le niveau de corruption."""
    if level >= 0.7:
        return STYLES['metric_danger']
    elif level >= 0.4:
        return STYLES['metric_warning']
    else:
        return STYLES['metric_good']

def get_health_style(percentage: float) -> Style:
    """Retourne le style selon le niveau de santé."""
    if percentage <= 30:
        return STYLES['metric_danger']
    elif percentage <= 60:
        return STYLES['metric_warning']
    else:
        return STYLES['metric_good']
