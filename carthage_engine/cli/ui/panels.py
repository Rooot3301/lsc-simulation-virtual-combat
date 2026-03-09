"""
Panneaux de dashboard pour l'interface.
"""

from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.columns import Columns
from rich.progress import Progress, BarColumn, TextColumn
from rich.console import Group
from typing import Dict, Any, List
from .styles import STYLES, get_corruption_style, get_health_style


class DashboardPanels:
    """Générateur de panneaux pour le dashboard."""

    @staticmethod
    def create_header(status: Dict[str, Any], engine: Any) -> Panel:
        """Crée l'en-tête système étendu avec métriques clés."""
        tick = status.get('tick', 0)
        corruption_val = engine.world.global_corruption if engine else 0
        corruption = f"{corruption_val:.0%}"
        xana_power = status.get('xana_power', 0)
        running = status.get('is_running', False)
        paused = status.get('is_paused', False)

        # Doctrine XANA
        doctrine = "INCONNUE"
        if engine and engine.xana_ai and engine.xana_ai.doctrine:
            doctrine = engine.xana_ai.doctrine.primary_rule.value.upper()

        # État simulation
        if paused:
            sim_status = Text("EN PAUSE", style="yellow bold")
        elif running:
            sim_status = Text("ACTIF", style="green bold")
        else:
            sim_status = Text("ARRÊTÉ", style="red")

        # Construction de l'en-tête étendu
        header_content = Table.grid(padding=(0, 1))
        header_content.add_column(justify="left", ratio=1)
        header_content.add_column(justify="center", ratio=1)
        header_content.add_column(justify="center", ratio=1)
        header_content.add_column(justify="right", ratio=1)

        # Ligne 1
        header_content.add_row(
            Text("CARTHAGE ENGINE v1.1", style=STYLES['header']),
            "",
            "",
            sim_status
        )

        # Ligne 2 - Métriques clés
        corruption_text = Text(f"{corruption}", style=get_corruption_style(corruption_val))

        header_content.add_row(
            Text(f"Statut: ", style=STYLES['metric_label']) + sim_status,
            Text(f"Tick: ", style=STYLES['metric_label']) + Text(f"{tick:05d}", style=STYLES['metric_value']),
            Text(f"Corruption: ", style=STYLES['metric_label']) + corruption_text,
            Text(f"Puissance XANA: ", style=STYLES['metric_label']) + Text(f"{xana_power:.0%}", style=get_corruption_style(xana_power))
        )

        # Ligne 3 - Doctrine
        header_content.add_row(
            "",
            Text(f"Doctrine: ", style=STYLES['metric_label']) + Text(doctrine, style=STYLES['STRATEGIE']),
            "",
            ""
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
    def create_operational_log(events: List[Any]) -> Panel:
        """Crée le panneau Journal Opérationnel."""
        content = []

        recent_events = events[-8:] if len(events) > 8 else events

        if not recent_events:
            content.append(Text("Aucun événement récent", style=STYLES['dim']))
        else:
            for event in recent_events:
                severity_style = STYLES.get(event.severity, STYLES['INFO'])
                line = Text()
                line.append(f"[{event.timestamp}] ", style=STYLES['dim'])
                line.append(f"[{event.severity}] ", style=severity_style)
                line.append(event.message[:65], style="white")
                content.append(line)

        return Panel(
            Group(*content),
            title="[bright_white bold]JOURNAL OPÉRATIONNEL",
            border_style="blue",
            padding=(0, 1),
            height=10
        )

    @staticmethod
    def create_sectors_strategic_map(sectors: Dict[str, Any]) -> Panel:
        """Crée la carte stratégique des secteurs avec barres de menace."""
        content = []

        for name, sector in sectors.items():
            threat = sector.threat_score
            corruption = sector.corruption_level

            # Barre de menace (sur 10)
            bar_length = 15
            filled = int((threat / 10.0) * bar_length)
            bar = "█" * filled + "░" * (bar_length - filled)

            # Couleur selon menace
            if threat >= 7:
                bar_style = "red"
                status = "critique"
            elif threat >= 4:
                bar_style = "yellow"
                status = "activité XANA"
            elif threat >= 2:
                bar_style = "cyan"
                status = "surveillance"
            else:
                bar_style = "green"
                status = "stable"

            line = Text()
            line.append(f"{sector.name:15} ", style="cyan")
            line.append(bar, style=bar_style)
            line.append(f"  {status}", style=bar_style)

            content.append(line)

        return Panel(
            Group(*content),
            title="[bright_cyan bold]SECTEURS - CARTE STRATÉGIQUE",
            border_style="cyan",
            padding=(0, 1)
        )

    @staticmethod
    def create_visual_meters(engine: Any) -> Panel:
        """Crée les jauges visuelles."""
        corruption = engine.world.global_corruption

        # Menace globale (calculée à partir des secteurs)
        threat_avg = sum(s.threat_score for s in engine.world.sectors.values()) / len(engine.world.sectors)
        threat_normalized = min(threat_avg / 10.0, 1.0)

        # Skid
        skid_hull = engine.world.skid.hull_integrity / 100.0 if engine.world.skid else 0

        # Moral moyen des agents
        agents = list(engine.world.agents.values())
        if agents:
            morale_avg = sum(1.0 - a.psychological_state.stress for a in agents) / len(agents)
        else:
            morale_avg = 0

        # Création des barres
        progress = Progress(
            TextColumn("{task.description:20}"),
            BarColumn(bar_width=30),
            TextColumn("{task.percentage:>3.0f}%"),
            expand=False
        )

        task1 = progress.add_task("[orange bold]Corruption globale", total=100, completed=corruption * 100)
        task2 = progress.add_task("[red bold]Menace globale", total=100, completed=threat_normalized * 100)
        task3 = progress.add_task("[cyan bold]Skid intégrité", total=100, completed=skid_hull * 100)
        task4 = progress.add_task("[green bold]Moral agents", total=100, completed=morale_avg * 100)

        return Panel(
            progress,
            title="[bright_white bold]INDICATEURS STRATÉGIQUES",
            border_style="blue",
            padding=(0, 1)
        )

    @staticmethod
    def create_xana_extended_panel(xana: Any, ai_state: dict) -> Panel:
        """Panneau XANA étendu avec détails stratégiques."""
        table = Table(show_header=False, box=None, padding=(0, 1))
        table.add_column(style=STYLES['metric_label'])
        table.add_column(style=STYLES['metric_value'])

        if not xana:
            return Panel(
                Text("XANA NON INITIALISÉ", style=STYLES['dim']),
                title="[magenta bold]XANA",
                border_style="magenta",
                padding=(0, 1)
            )

        power = xana.power_level
        resources = xana.resources
        doctrine = ai_state.get('doctrine', 'inconnu').upper()
        goal = xana.current_goal if xana.current_goal else '-'

        # Cible prioritaire
        target = "Aucune"
        if xana.active_plans:
            target = "Skid" if "skid" in str(xana.active_plans[0]).lower() else "Secteur"

        # Phase du plan
        phase = "Observation"
        if xana.active_plans:
            phase = "Exécution"

        # Score de menace
        threat_score = ai_state.get('aggression', 0.5)
        if threat_score >= 0.7:
            threat_level = Text("ÉLEVÉE", style="red bold")
        elif threat_score >= 0.4:
            threat_level = Text("MOYENNE", style="yellow bold")
        else:
            threat_level = Text("FAIBLE", style="green")

        table.add_row("Doctrine", doctrine)
        table.add_row("Objectif", goal)
        table.add_row("Phase", phase)
        table.add_row("Cible prioritaire", target)
        table.add_row("Menace globale", threat_level)
        table.add_row("", "")
        table.add_row("Puissance", f"{power:.1f}/10.0")
        table.add_row("Ressources", str(resources))
        table.add_row("Plans actifs", str(len(xana.active_plans)))

        return Panel(
            table,
            title="[magenta bold]XANA - ANALYSE STRATÉGIQUE",
            border_style="magenta",
            padding=(0, 1)
        )

    @staticmethod
    def create_dashboard(status: Dict[str, Any], engine: Any) -> List[Any]:
        """Crée le dashboard complet amélioré."""
        # Header étendu
        header = DashboardPanels.create_header(status, engine)

        # Indicateurs visuels
        meters = DashboardPanels.create_visual_meters(engine)

        # World data
        world_data = {
            'global_corruption': engine.world.global_corruption,
            'agents_operational': engine.world.get_operational_agents_count(),
            'monsters_active': engine.world.get_active_monsters_count(),
            'active_towers': len(engine.world.get_active_towers())
        }

        # XANA data étendu
        xana = engine.world.xana
        ai_state = engine.xana_ai.get_current_state_summary()

        # Panels
        world_panel = DashboardPanels.create_world_panel(world_data)
        xana_panel = DashboardPanels.create_xana_extended_panel(xana, ai_state)
        agents_panel = DashboardPanels.create_agents_panel(list(engine.world.agents.values()))
        skid_panel = DashboardPanels.create_skid_panel(engine.world.skid)

        # Nouveaux panneaux
        sectors_map = DashboardPanels.create_sectors_strategic_map(engine.world.sectors)
        alerts_panel = DashboardPanels.create_alerts_panel(engine.event_manager.get_recent_events(20))
        operational_log = DashboardPanels.create_operational_log(engine.event_manager.get_recent_events(50))

        # Layout amélioré
        row1 = Columns([world_panel, xana_panel], equal=True, expand=True)
        row2 = Columns([agents_panel, skid_panel], equal=True, expand=True)
        row3 = sectors_map
        row4 = Columns([alerts_panel, meters], equal=True, expand=True)
        row5 = operational_log

        return [header, row1, row2, row3, row4, row5]
