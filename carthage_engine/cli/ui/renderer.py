"""
Renderer principal pour l'interface Rich.
"""

from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.columns import Columns
from rich.rule import Rule
from typing import List, Any
from .styles import STYLES, get_severity_style, get_corruption_style, get_health_style
from .panels import DashboardPanels


class CarthageRenderer:
    """Gestionnaire de rendu pour l'interface Carthage."""

    def __init__(self):
        self.console = Console()

    def clear(self):
        """Efface l'écran."""
        self.console.clear()

    def print_banner(self):
        """Affiche la bannière de bienvenue."""
        banner_text = Text()
        banner_text.append("╔" + "═" * 62 + "╗\n", style="bright_blue")
        banner_text.append("║" + " " * 62 + "║\n", style="bright_blue")
        banner_text.append("║", style="bright_blue")
        banner_text.append(" " * 15 + "CARTHAGE ENGINE v1.0" + " " * 27, style="bright_cyan bold")
        banner_text.append("║\n", style="bright_blue")
        banner_text.append("║" + " " * 62 + "║\n", style="bright_blue")
        banner_text.append("║", style="bright_blue")
        banner_text.append(" " * 8 + "Simulation Stratégique - Centre de Commande" + " " * 11, style="cyan")
        banner_text.append("║\n", style="bright_blue")
        banner_text.append("║" + " " * 62 + "║\n", style="bright_blue")
        banner_text.append("╚" + "═" * 62 + "╝", style="bright_blue")

        self.console.print(banner_text)
        self.console.print()
        self.console.print("[dim]Tapez [cyan bold]help[/cyan bold] pour voir les commandes disponibles[/dim]")
        self.console.print("[dim]Tapez [cyan bold]dashboard[/cyan bold] pour afficher le centre de contrôle[/dim]")
        self.console.print()

    def print_dashboard(self, status: dict, engine: Any):
        """Affiche le dashboard complet."""
        panels = DashboardPanels.create_dashboard(status, engine)

        self.console.print()
        for panel in panels:
            self.console.print(panel)
        self.console.print()

    def print_help(self):
        """Affiche l'aide formatée."""
        self.console.print()
        self.console.print(Rule("[bright_cyan bold]COMMANDES CARTHAGE ENGINE", style="bright_blue"))
        self.console.print()

        # Table des commandes par catégorie
        categories = {
            "Contrôle Simulation": [
                ("start", "Démarre la simulation"),
                ("pause", "Met en pause"),
                ("resume", "Reprend la simulation"),
                ("stop", "Arrête"),
                ("tick <n>", "Exécute N ticks"),
                ("run <n>", "Lance N ticks"),
                ("step", "1 tick + affichage")
            ],
            "Visualisation": [
                ("dashboard", "Centre de contrôle"),
                ("status", "Statut rapide"),
                ("world", "État du monde"),
                ("sectors", "Détails secteurs"),
            ],
            "Inspection": [
                ("agents", "Liste agents"),
                ("monsters", "Liste monstres"),
                ("towers", "État des tours"),
                ("skid", "État du Skid"),
                ("xana", "État de XANA"),
            ],
            "Timeline": [
                ("events <n>", "N derniers événements"),
                ("timeline <n>", "Timeline complète"),
            ],
            "Système": [
                ("save <fichier>", "Sauvegarde"),
                ("load <fichier>", "Charge"),
                ("help", "Affiche cette aide"),
                ("quit", "Quitter")
            ]
        }

        for category, commands in categories.items():
            table = Table(show_header=False, box=None, padding=(0, 2))
            table.add_column(style="cyan")
            table.add_column(style="white")

            for cmd, desc in commands:
                table.add_row(cmd, desc)

            self.console.print(Panel(
                table,
                title=f"[bright_cyan bold]{category}",
                border_style="blue",
                padding=(0, 1)
            ))
            self.console.print()

    def print_status(self, status: dict):
        """Affiche le statut compact."""
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column(style=STYLES['metric_label'])
        table.add_column(style=STYLES['metric_value'])

        for key, value in status.items():
            if key not in ['is_running', 'is_paused']:
                table.add_row(key, str(value))

        self.console.print()
        self.console.print(Panel(
            table,
            title="[bright_cyan bold]STATUT SYSTÈME",
            border_style="blue",
            padding=(0, 1)
        ))
        self.console.print()

    def print_agents(self, agents: List[Any]):
        """Affiche la liste des agents."""
        table = Table(show_header=True, padding=(0, 1))
        table.add_column("Agent", style="cyan bold")
        table.add_column("Type", style="white")
        table.add_column("Secteur", style="yellow")
        table.add_column("Santé", justify="right")
        table.add_column("Corruption", justify="right")
        table.add_column("Stress", justify="right")
        table.add_column("Fatigue", justify="right")
        table.add_column("État", justify="center")

        for agent in agents:
            health_pct = (agent.health / agent.max_health) * 100
            corruption = agent.corruption_level
            stress = agent.psychological_state.stress
            fatigue = agent.psychological_state.fatigue
            operational = "✓" if agent.is_operational() else "✗"

            table.add_row(
                agent.name,
                agent.agent_type.value,
                agent.sector,
                Text(f"{health_pct:.0f}%", style=get_health_style(health_pct)),
                Text(f"{corruption:.0%}", style=get_corruption_style(corruption)),
                Text(f"{stress:.0%}", style=get_corruption_style(stress)),
                Text(f"{fatigue:.0%}", style=get_corruption_style(fatigue)),
                Text(operational, style="green" if operational == "✓" else "red")
            )

        self.console.print()
        self.console.print(Panel(
            table,
            title="[cyan bold]AGENTS OPÉRATIONNELS",
            border_style="cyan"
        ))
        self.console.print()

    def print_monsters(self, monsters: List[Any]):
        """Affiche la liste des monstres."""
        if not monsters:
            self.console.print()
            self.console.print("[dim]Aucun monstre actif[/dim]")
            self.console.print()
            return

        table = Table(show_header=True, padding=(0, 1))
        table.add_column("Monstre", style="red bold")
        table.add_column("Type", style="white")
        table.add_column("Secteur", style="yellow")
        table.add_column("Santé", justify="right")
        table.add_column("Comportement", justify="center")

        for monster in monsters:
            health_pct = (monster.health / monster.max_health) * 100

            table.add_row(
                monster.name,
                monster.monster_type.value,
                monster.sector,
                Text(f"{health_pct:.0f}%", style=get_health_style(health_pct)),
                monster.behavior.value
            )

        self.console.print()
        self.console.print(Panel(
            table,
            title="[red bold]MONSTRES XANA",
            border_style="red"
        ))
        self.console.print()

    def print_events(self, events: List[Any], count: int = 10):
        """Affiche les événements."""
        self.console.print()
        self.console.print(Rule(f"[bright_cyan bold]{count} DERNIERS ÉVÉNEMENTS", style="blue"))
        self.console.print()

        for event in events[-count:]:
            severity_style = get_severity_style(event.severity)

            line = Text()
            line.append(f"[{event.timestamp}] ", style="bright_black")
            line.append(f"[{event.severity}] ", style=severity_style)
            line.append(event.message, style="white")

            self.console.print(line)

        self.console.print()

    def print_sectors(self, sectors: dict):
        """Affiche l'état des secteurs."""
        table = Table(show_header=True, padding=(0, 1))
        table.add_column("Secteur", style="cyan bold")
        table.add_column("Corruption", justify="right")
        table.add_column("Tours", justify="center")
        table.add_column("Entités", justify="center")
        table.add_column("Menace", justify="right")
        table.add_column("État", justify="center")

        for name, sector in sectors.items():
            corruption = sector.corruption_level
            state = "DOMINÉ" if sector.is_dominated_by_xana() else "SÛR" if sector.is_safe() else "CONTESTÉ"
            state_style = "red" if state == "DOMINÉ" else "green" if state == "SÛR" else "yellow"

            table.add_row(
                sector.name,
                Text(f"{corruption:.0%}", style=get_corruption_style(corruption)),
                str(len(sector.tower_ids)),
                str(len(sector.entity_ids)),
                f"{sector.threat_score:.1f}",
                Text(state, style=state_style)
            )

        self.console.print()
        self.console.print(Panel(
            table,
            title="[bright_cyan bold]SECTEURS VIRTUELS",
            border_style="blue"
        ))
        self.console.print()

    def print_xana(self, xana: Any, ai_state: dict):
        """Affiche l'état de XANA."""
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column(style=STYLES['metric_label'])
        table.add_column(style=STYLES['metric_value'])

        if not xana:
            self.console.print("[dim]XANA non initialisé[/dim]")
            return

        table.add_row("Niveau de puissance", f"{xana.power_level:.1f}/10.0")
        table.add_row("Influence", f"{xana.influence:.0%}")
        table.add_row("Ressources", str(xana.resources))
        table.add_row("Tours actives", str(xana.active_towers))
        table.add_row("Monstres actifs", str(xana.active_monsters))
        table.add_row("Objectif actuel", xana.current_goal or "Aucun")
        table.add_row("Plans actifs", str(len(xana.active_plans)))

        self.console.print()
        self.console.print(Panel(
            table,
            title="[magenta bold]XANA - INTELLIGENCE HOSTILE",
            border_style="magenta"
        ))

        # IA State
        ai_table = Table(show_header=False, box=None, padding=(0, 2))
        ai_table.add_column(style=STYLES['metric_label'])
        ai_table.add_column(style=STYLES['metric_value'])

        ai_table.add_row("Doctrine", ai_state.get('doctrine', 'inconnu').upper())
        ai_table.add_row("Agressivité", f"{ai_state.get('aggression', 0):.0%}")
        ai_table.add_row("Mémoires actives", str(ai_state.get('memory_count', 0)))
        ai_table.add_row("Vulnérabilités détectées", str(ai_state.get('vulnerabilities_detected', 0)))

        self.console.print(Panel(
            ai_table,
            title="[magenta bold]SYSTÈME IA",
            border_style="magenta"
        ))
        self.console.print()

    def print_message(self, message: str, style: str = "white"):
        """Affiche un message simple."""
        self.console.print(f"[{style}]{message}[/{style}]")

    def print_error(self, message: str):
        """Affiche une erreur."""
        self.console.print(f"[red bold]✗ {message}[/red bold]")

    def print_success(self, message: str):
        """Affiche un succès."""
        self.console.print(f"[green bold]✓ {message}[/green bold]")
