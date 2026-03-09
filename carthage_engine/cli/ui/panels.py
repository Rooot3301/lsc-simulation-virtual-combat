"""
Panneaux de dashboard pour l'interface.
"""

from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.columns import Columns
from rich.progress import BarColumn, Progress, TextColumn
from typing import Dict, Any, List
from .styles import STYLES, get_corruption_style, get_health_style


class DashboardPanels:
    """Générateur de panneaux pour le dashboard."""

    @staticmethod
    def create_header(status: Dict[str, Any]) -> Panel:
        """Crée l'en-tête système."""
        tick = status.get('tick', 0)
        corruption = status.get('global_corruption', '0%')
        xana_power = status.get('xana_power', 0)
        running = status.get('is_running', False)
        paused = status.get('is_paused', False)

        # État simulation
        if paused:
            sim_status = Text("EN PAUSE", style="yellow bold")
        elif running:
            sim_status = Text("ACTIF", style="green bold")
        else:
            sim_status = Text("ARRÊTÉ", style="red")

        # Construction de l'en-tête
        header_content = Table.grid(padding=(0, 2))
        header_content.add_column(justify="left")
        header_content.add_column(justify="center")
        header_content.add_column(justify="right")

        header_content.add_row(
            Text("CARTHAGE ENGINE", style=STYLES['header']),
            Text(f"TICK {tick:05d}", style=STYLES['title']),
            sim_status
        )

        header_content.add_row(
            Text(f"Puissance XANA: {xana_power:.1f}", style=STYLES['metric_label']),
            Text(f"Corruption Globale: {corruption}", style=get_corruption_style(0.15)),
            Text("v1.0", style=STYLES['dim'])
        )

        return Panel(
            header_content,
            border_style=STYLES['panel_border'],
            padding=(0, 1)
        )

    @staticmethod
    def create_world_panel(world_data: Dict[str, Any]) -> Panel:
        """Crée le panneau état du monde."""
        table = Table(show_header=False, box=None, padding=(0, 1))
        table.add_column(style=STYLES['metric_label'])
        table.add_column(style=STYLES['metric_value'])

        corruption = world_data.get('global_corruption', 0.0)
        agents = world_data.get('agents_operational', 0)
        monsters = world_data.get('monsters_active', 0)
        towers = world_data.get('active_towers', 0)

        table.add_row("Corruption", Text(f"{corruption:.1%}", style=get_corruption_style(corruption)))
        table.add_row("Agents", f"{agents}")
        table.add_row("Monstres", f"{monsters}")
        table.add_row("Tours", f"{towers}")

        return Panel(
            table,
            title="[bright_cyan bold]MONDE",
            border_style=STYLES['panel_border'],
            padding=(0, 1)
        )

    @staticmethod
    def create_xana_panel(xana_data: Dict[str, Any]) -> Panel:
        """Crée le panneau XANA."""
        table = Table(show_header=False, box=None, padding=(0, 1))
        table.add_column(style=STYLES['metric_label'])
        table.add_column(style=STYLES['metric_value'])

        power = xana_data.get('power_level', 0)
        resources = xana_data.get('resources', 0)
        doctrine = xana_data.get('doctrine', 'opportuniste')
        goal = xana_data.get('current_goal', 'Aucun')

        table.add_row("Puissance", f"{power:.1f}/10.0")
        table.add_row("Ressources", f"{resources}")
        table.add_row("Doctrine", doctrine.upper())
        table.add_row("Objectif", goal if goal != 'Aucun' else '-')

        return Panel(
            table,
            title="[magenta bold]XANA",
            border_style="magenta",
            padding=(0, 1)
        )

    @staticmethod
    def create_agents_panel(agents: List[Any]) -> Panel:
        """Crée le panneau agents."""
        table = Table(show_header=True, box=None, padding=(0, 1))
        table.add_column("Agent", style=STYLES['emphasis'])
        table.add_column("Santé", justify="right")
        table.add_column("Corrupt.", justify="right")
        table.add_column("État", justify="center")

        for agent in agents[:4]:  # Max 4 agents
            name = agent.name
            health_pct = (agent.health / agent.max_health) * 100
            corruption = agent.corruption_level
            operational = "✓" if agent.is_operational() else "✗"

            health_text = Text(f"{health_pct:.0f}%", style=get_health_style(health_pct))
            corruption_text = Text(f"{corruption:.0%}", style=get_corruption_style(corruption))
            status_text = Text(operational, style="green" if operational == "✓" else "red")

            table.add_row(name, health_text, corruption_text, status_text)

        return Panel(
            table,
            title="[cyan bold]AGENTS",
            border_style="cyan",
            padding=(0, 1)
        )

    @staticmethod
    def create_skid_panel(skid: Any) -> Panel:
        """Crée le panneau Skid."""
        if not skid:
            return Panel(
                Text("NON DISPONIBLE", style=STYLES['dim']),
                title="[cyan bold]SKID",
                border_style="cyan",
                padding=(0, 1)
            )

        table = Table(show_header=False, box=None, padding=(0, 1))
        table.add_column(style=STYLES['metric_label'])
        table.add_column(style=STYLES['metric_value'])

        hull = skid.hull_integrity
        energy = skid.energy
        mode = skid.mode.value
        passengers = len(skid.passengers)

        hull_text = Text(f"{hull:.0f}%", style=get_health_style(hull))
        energy_text = Text(f"{energy:.0f}%", style=get_health_style(energy))

        table.add_row("Coque", hull_text)
        table.add_row("Énergie", energy_text)
        table.add_row("Mode", mode.upper())
        table.add_row("Passagers", f"{passengers}/4")

        return Panel(
            table,
            title="[cyan bold]SKID",
            border_style="cyan",
            padding=(0, 1)
        )

    @staticmethod
    def create_alerts_panel(events: List[Any]) -> Panel:
        """Crée le panneau d'alertes."""
        content = []

        critical_events = [e for e in events if e.severity in ['CRITIQUE', 'ALERTE', 'STRATEGIE']][-5:]

        if not critical_events:
            content.append(Text("Aucune alerte active", style=STYLES['dim']))
        else:
            for event in critical_events:
                severity_style = STYLES.get(event.severity, STYLES['INFO'])
                line = Text()
                line.append(f"[{event.severity}] ", style=severity_style)
                line.append(event.message[:60], style="white")
                content.append(line)

        from rich.console import Group
        return Panel(
            Group(*content),
            title="[yellow bold]ALERTES",
            border_style="yellow",
            padding=(0, 1),
            height=7
        )

    @staticmethod
    def create_dashboard(status: Dict[str, Any], engine: Any) -> List[Any]:
        """Crée le dashboard complet."""
        from rich.console import Group

        # Header
        header = DashboardPanels.create_header(status)

        # World data
        world_data = {
            'global_corruption': engine.world.global_corruption,
            'agents_operational': engine.world.get_operational_agents_count(),
            'monsters_active': engine.world.get_active_monsters_count(),
            'active_towers': len(engine.world.get_active_towers())
        }

        # XANA data
        xana = engine.world.xana
        xana_data = {
            'power_level': xana.power_level if xana else 0,
            'resources': xana.resources if xana else 0,
            'doctrine': engine.xana_ai.doctrine.primary_rule.value if engine.xana_ai.doctrine else 'inconnu',
            'current_goal': xana.current_goal if xana and xana.current_goal else 'Aucun'
        }

        # Panels
        world_panel = DashboardPanels.create_world_panel(world_data)
        xana_panel = DashboardPanels.create_xana_panel(xana_data)
        agents_panel = DashboardPanels.create_agents_panel(list(engine.world.agents.values()))
        skid_panel = DashboardPanels.create_skid_panel(engine.world.skid)
        alerts_panel = DashboardPanels.create_alerts_panel(engine.event_manager.get_recent_events(20))

        # Layout en colonnes
        top_row = Columns([world_panel, xana_panel, agents_panel], equal=True, expand=True)
        bottom_row = Columns([skid_panel, alerts_panel], equal=True, expand=True)

        return [header, top_row, bottom_row]
