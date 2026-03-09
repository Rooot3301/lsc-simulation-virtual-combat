"""
Gestionnaire de commandes CLI avec interface Rich.
"""

from typing import List
from ..core import CarthageEngine
from ..persistence import save_simulation, load_simulation
from .ui.renderer import CarthageRenderer


class CommandHandler:
    """Gère les commandes du CLI avec rendu Rich."""

    def __init__(self, engine: CarthageEngine):
        self.engine = engine
        self.renderer = CarthageRenderer()

    def handle_command(self, command: str, args: List[str]) -> bool:
        """
        Gère une commande.
        Retourne False pour quitter, True sinon.
        """
        command = command.lower()

        # Commandes système
        if command in ['quit', 'exit', 'q']:
            return False

        elif command == 'help':
            self.renderer.print_help()

        # Contrôle simulation
        elif command == 'start':
            self.engine.start()
            self.renderer.print_success("Simulation démarrée")

        elif command == 'pause':
            self.engine.pause()
            self.renderer.print_success("Simulation en pause")

        elif command == 'resume':
            self.engine.resume()
            self.renderer.print_success("Simulation reprise")

        elif command == 'stop':
            self.engine.stop()
            self.renderer.print_success("Simulation arrêtée")

        elif command == 'tick':
            count = int(args[0]) if args else 1
            self.engine.tick(count)
            self.renderer.print_success(f"{count} tick(s) exécuté(s)")

        elif command == 'run':
            count = int(args[0]) if args else 10
            self.engine.start()
            self.engine.tick(count)
            self.renderer.print_success(f"Simulation exécutée pendant {count} ticks")
            # Affiche le dashboard après exécution
            status = self.engine.get_status_summary()
            self.renderer.print_dashboard(status, self.engine)

        elif command == 'step':
            self.engine.tick(1)
            status = self.engine.get_status_summary()
            self.renderer.print_dashboard(status, self.engine)

        # Visualisation
        elif command == 'dashboard':
            status = self.engine.get_status_summary()
            self.renderer.print_dashboard(status, self.engine)

        elif command == 'status':
            status = self.engine.get_status_summary()
            self.renderer.print_status(status)

        elif command == 'world':
            status = self.engine.get_status_summary()
            self.renderer.print_dashboard(status, self.engine)

        elif command == 'sectors':
            self.renderer.print_sectors(self.engine.world.sectors)

        # Inspection
        elif command == 'agents':
            agents = list(self.engine.world.agents.values())
            self.renderer.print_agents(agents)

        elif command == 'monsters':
            monsters = [m for m in self.engine.world.monsters.values() if not m.is_destroyed]
            self.renderer.print_monsters(monsters)

        elif command == 'towers':
            self._print_towers()

        elif command == 'skid':
            self._print_skid()

        elif command == 'xana':
            ai_state = self.engine.xana_ai.get_current_state_summary()
            self.renderer.print_xana(self.engine.world.xana, ai_state)

        elif command == 'entities':
            agents = list(self.engine.world.agents.values())
            self.renderer.print_agents(agents)
            monsters = [m for m in self.engine.world.monsters.values() if not m.is_destroyed]
            self.renderer.print_monsters(monsters)

        # Timeline
        elif command == 'events':
            count = int(args[0]) if args else 10
            events = self.engine.event_manager.get_recent_events(count)
            self.renderer.print_events(events, count)

        elif command == 'timeline':
            count = int(args[0]) if args else 20
            events = self.engine.event_manager.get_recent_events(count)
            self.renderer.print_events(events, count)

        # Persistence
        elif command == 'save':
            filename = args[0] if args else "save.json"
            result = save_simulation(self.engine, filename)
            self.renderer.print_success(result)

        elif command == 'load':
            filename = args[0] if args else "save.json"
            result = load_simulation(self.engine, filename)
            self.renderer.print_message(result)

        else:
            self.renderer.print_error(f"Commande inconnue: {command}")
            self.renderer.print_message("Tapez 'help' pour voir les commandes disponibles", "dim")

        return True

    def _print_towers(self):
        """Affiche l'état des tours."""
        from rich.table import Table
        from rich.panel import Panel
        from ..entities.tower import TowerState
        from .ui.styles import STYLES

        table = Table(show_header=True, padding=(0, 1))
        table.add_column("Tour", style="cyan bold")
        table.add_column("Secteur", style="yellow")
        table.add_column("État", justify="center")
        table.add_column("Activation", justify="right")
        table.add_column("Défenseurs", justify="center")

        for tower in self.engine.world.towers.values():
            state_colors = {
                TowerState.INACTIVE: "bright_black",
                TowerState.ACTIVE: "yellow",
                TowerState.CONTESTED: "orange1",
                TowerState.CORRUPTED: "red bold",
                TowerState.DEACTIVATED: "green"
            }
            state_style = state_colors.get(tower.state, "white")

            from rich.text import Text
            table.add_row(
                tower.name,
                tower.sector,
                Text(tower.state.value.upper(), style=state_style),
                f"{tower.activation_level:.0%}",
                str(len(tower.defending_monsters))
            )

        self.renderer.console.print()
        self.renderer.console.print(Panel(
            table,
            title="[yellow bold]TOURS",
            border_style="yellow"
        ))
        self.renderer.console.print()

    def _print_skid(self):
        """Affiche l'état du Skid."""
        from rich.table import Table
        from rich.panel import Panel
        from rich.text import Text
        from .ui.styles import get_health_style

        skid = self.engine.world.skid
        if not skid:
            self.renderer.print_message("Skid non disponible", "dim")
            return

        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column(style=STYLES['metric_label'])
        table.add_column(style=STYLES['metric_value'])

        table.add_row("Mode", skid.mode.value.upper())
        table.add_row("Mission", skid.mission.value)
        table.add_row("Coque", Text(f"{skid.hull_integrity:.0f}%", style=get_health_style(skid.hull_integrity)))
        table.add_row("Énergie", Text(f"{skid.energy:.0f}%", style=get_health_style(skid.energy)))
        table.add_row("Position", skid.current_node)
        table.add_row("Destination", skid.destination_node or "-")
        table.add_row("Passagers", f"{len(skid.passengers)}/{skid.max_passengers}")
        table.add_row("Niveau danger", f"{skid.danger_level:.0%}")

        self.renderer.console.print()
        self.renderer.console.print(Panel(
            table,
            title="[cyan bold]SKID - VÉHICULE DE NAVIGATION",
            border_style="cyan"
        ))
        self.renderer.console.print()
