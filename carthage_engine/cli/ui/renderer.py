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
        self.console.print(Rule("[bright_cyan bold]COMMANDES CARTHAGE ENGINE v1.1", style="bright_blue"))
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
                ("step", "1 tick + affichage"),
                ("run_live <n>", "Mode live avec rafraîchissement auto")
            ],
            "Visualisation": [
                ("dashboard", "Centre de contrôle complet"),
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
                ("inspect agent <nom>", "Détails d'un agent"),
                ("inspect xana", "Analyse XANA détaillée"),
                ("inspect skid", "État Skid détaillé"),
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

    def inspect_agent(self, agent: Any):
        """Affiche l'inspection détaillée d'un agent."""
        from rich.table import Table
        from rich.panel import Panel
        from rich.columns import Columns

        # Informations principales
        main_table = Table(show_header=False, box=None, padding=(0, 2))
        main_table.add_column(style=STYLES['metric_label'])
        main_table.add_column(style=STYLES['metric_value'])

        health_pct = (agent.health / agent.max_health) * 100
        corruption = agent.corruption_level
        stress = agent.psychological_state.stress
        fatigue = agent.psychological_state.fatigue

        main_table.add_row("Santé", Text(f"{health_pct:.0f}%", style=get_health_style(health_pct)))
        main_table.add_row("Stress", Text(f"{stress:.0%}", style=get_corruption_style(stress)))
        main_table.add_row("Fatigue", Text(f"{fatigue:.0%}", style=get_corruption_style(fatigue)))
        main_table.add_row("Corruption", Text(f"{corruption:.0%}", style=get_corruption_style(corruption)))
        main_table.add_row("", "")
        main_table.add_row("Type", agent.agent_type.value)
        main_table.add_row("Secteur", agent.sector)
        main_table.add_row("Spécialisation", agent.specialization.value if hasattr(agent, 'specialization') else '-')

        # Relations
        relations_table = Table(show_header=False, box=None, padding=(0, 1))
        relations_table.add_column(style="cyan")
        relations_table.add_column(style="white")

        if hasattr(agent, 'relationships') and agent.relationships:
            for target, trust in agent.relationships.items():
                if trust >= 0.7:
                    level = Text("confiance élevée", style="green")
                elif trust >= 0.4:
                    level = Text("confiance moyenne", style="yellow")
                else:
                    level = Text("confiance faible", style="red")
                relations_table.add_row(f"{target} →", level)
        else:
            relations_table.add_row("Aucune relation", "")

        # Panels
        main_panel = Panel(main_table, title=f"[cyan bold]{agent.name.upper()}", border_style="cyan")
        relations_panel = Panel(relations_table, title="[cyan bold]RELATIONS", border_style="cyan")

        self.console.print()
        self.console.print(Columns([main_panel, relations_panel], equal=True, expand=True))
        self.console.print()

    def inspect_xana_detailed(self, xana: Any, ai_state: dict, engine: Any):
        """Inspection détaillée de XANA."""
        from rich.table import Table
        from rich.panel import Panel
        from rich.columns import Columns

        # Panneau principal
        main_table = Table(show_header=False, box=None, padding=(0, 2))
        main_table.add_column(style=STYLES['metric_label'])
        main_table.add_column(style=STYLES['metric_value'])

        if not xana:
            self.console.print("[dim]XANA non initialisé[/dim]")
            return

        main_table.add_row("Niveau de puissance", f"{xana.power_level:.1f}/10.0")
        main_table.add_row("Influence", f"{xana.influence:.0%}")
        main_table.add_row("Ressources", str(xana.resources))
        main_table.add_row("Tours actives", str(xana.active_towers))
        main_table.add_row("Monstres actifs", str(xana.active_monsters))
        main_table.add_row("Plans actifs", str(len(xana.active_plans)))

        # Stratégie
        strat_table = Table(show_header=False, box=None, padding=(0, 2))
        strat_table.add_column(style=STYLES['metric_label'])
        strat_table.add_column(style=STYLES['metric_value'])

        strat_table.add_row("Doctrine", ai_state.get('doctrine', 'inconnu').upper())
        strat_table.add_row("Agressivité", f"{ai_state.get('aggression', 0):.0%}")
        strat_table.add_row("Objectif actuel", xana.current_goal or "Aucun")
        strat_table.add_row("Vulnérabilités détectées", str(ai_state.get('vulnerabilities_detected', 0)))
        strat_table.add_row("Mémoires actives", str(ai_state.get('memory_count', 0)))

        # Plans
        plans_content = []
        if xana.active_plans:
            for i, plan in enumerate(xana.active_plans[:3], 1):
                plans_content.append(Text(f"{i}. {plan}", style="white"))
        else:
            plans_content.append(Text("Aucun plan actif", style=STYLES['dim']))

        from rich.console import Group
        plans_panel = Panel(Group(*plans_content), title="[magenta bold]PLANS ACTIFS", border_style="magenta", padding=(0, 1))

        # Layout
        main_panel = Panel(main_table, title="[magenta bold]ÉTAT XANA", border_style="magenta")
        strat_panel = Panel(strat_table, title="[magenta bold]STRATÉGIE", border_style="magenta")

        self.console.print()
        self.console.print(Columns([main_panel, strat_panel], equal=True, expand=True))
        self.console.print(plans_panel)
        self.console.print()

    def inspect_skid_detailed(self, skid: Any):
        """Inspection détaillée du Skid."""
        from rich.table import Table
        from rich.panel import Panel
        from rich.columns import Columns

        if not skid:
            self.print_message("Skid non disponible", "dim")
            return

        # État
        state_table = Table(show_header=False, box=None, padding=(0, 2))
        state_table.add_column(style=STYLES['metric_label'])
        state_table.add_column(style=STYLES['metric_value'])

        state_table.add_row("Mode", skid.mode.value.upper())
        state_table.add_row("Mission", skid.mission.value)
        state_table.add_row("Coque", Text(f"{skid.hull_integrity:.0f}%", style=get_health_style(skid.hull_integrity)))
        state_table.add_row("Énergie", Text(f"{skid.energy:.0f}%", style=get_health_style(skid.energy)))

        # Navigation
        nav_table = Table(show_header=False, box=None, padding=(0, 2))
        nav_table.add_column(style=STYLES['metric_label'])
        nav_table.add_column(style=STYLES['metric_value'])

        nav_table.add_row("Position", skid.current_node)
        nav_table.add_row("Destination", skid.destination_node or "-")
        nav_table.add_row("Passagers", f"{len(skid.passengers)}/{skid.max_passengers}")
        nav_table.add_row("Niveau danger", Text(f"{skid.danger_level:.0%}", style=get_corruption_style(skid.danger_level)))

        # Passagers
        passengers_content = []
        if skid.passengers:
            for p in skid.passengers:
                passengers_content.append(Text(f"• {p}", style="cyan"))
        else:
            passengers_content.append(Text("Aucun passager", style=STYLES['dim']))

        from rich.console import Group
        passengers_panel = Panel(
            Group(*passengers_content),
            title="[cyan bold]PASSAGERS",
            border_style="cyan",
            padding=(0, 1)
        )

        state_panel = Panel(state_table, title="[cyan bold]ÉTAT", border_style="cyan")
        nav_panel = Panel(nav_table, title="[cyan bold]NAVIGATION", border_style="cyan")

        self.console.print()
        self.console.print(Columns([state_panel, nav_panel, passengers_panel], equal=True, expand=True))
        self.console.print()

    def run_live_simulation(self, engine: Any, ticks: int = 50, interval: float = 0.5):
        """Mode simulation live avec rafraîchissement automatique."""
        from rich.live import Live
        import time

        with Live(self.console, refresh_per_second=2, screen=False) as live:
            for i in range(ticks):
                engine.tick(1)
                status = engine.get_status_summary()

                # Création du dashboard
                panels = DashboardPanels.create_dashboard(status, engine)

                # Affichage
                from rich.console import Group
                live.update(Group(*panels))

                time.sleep(interval)
