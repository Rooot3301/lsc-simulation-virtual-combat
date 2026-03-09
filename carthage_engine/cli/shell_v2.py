"""
Shell interactif v2.0 avec support des commandes autonomes.
"""

from rich.prompt import Prompt
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from ..core.engine_v2 import CarthageEngineV2
from .ui.renderer import CarthageRenderer
import time


class CarthageShellV2:
    """Shell interactif v2.0 de Carthage Engine avec simulation autonome."""

    def __init__(self):
        self.engine = CarthageEngineV2()
        self.renderer = CarthageRenderer()
        self.console = Console()
        self.running = True
        self.live_mode = False

    def run(self):
        """Lance le shell interactif."""
        self._print_banner_v2()
        self._print_help_quick()

        while self.running:
            try:
                if self.live_mode:
                    self._run_live_mode()
                    continue

                user_input = Prompt.ask("\n[bright_cyan bold]carthage-v2[/bright_cyan bold]").strip()

                if not user_input:
                    continue

                parts = user_input.split()
                command = parts[0].lower()
                args = parts[1:] if len(parts) > 1 else []

                self._handle_command(command, args)

            except KeyboardInterrupt:
                self.console.print()
                if self.live_mode:
                    self.live_mode = False
                    self.engine.pause()
                    self.console.print("[yellow]Mode live interrompu. Pause.[/yellow]")
                else:
                    self.console.print("[yellow]Utilisez 'quit' pour quitter.[/yellow]")
            except Exception as e:
                self.console.print(f"[red]Erreur: {e}[/red]")
                import traceback
                traceback.print_exc()

        self.engine.stop()
        self.console.print("\n[cyan bold]Au revoir.[/cyan bold]\n")

    def _print_banner_v2(self):
        """Bannière v2.0."""
        banner_text = Text()
        banner_text.append("╔═══════════════════════════════════════════════════════════╗\n", style="bright_cyan")
        banner_text.append("║          ", style="bright_cyan")
        banner_text.append("CARTHAGE ENGINE v2.0", style="bold bright_white")
        banner_text.append("                        ║\n", style="bright_cyan")
        banner_text.append("║          ", style="bright_cyan")
        banner_text.append("Simulation Stratégique Autonome", style="bright_yellow")
        banner_text.append("               ║\n", style="bright_cyan")
        banner_text.append("╚═══════════════════════════════════════════════════════════╝", style="bright_cyan")

        self.console.print(banner_text)

    def _print_help_quick(self):
        """Aide rapide au démarrage."""
        help_text = """
[bright_white]Commandes principales:[/bright_white]
  [cyan]help[/cyan]              - Aide complète
  [cyan]start[/cyan]             - Démarrer la simulation (mode manuel)
  [cyan]run_live[/cyan]          - Lancer en mode live continu
  [cyan]dashboard[/cyan]         - Voir le tableau de bord
  [cyan]status[/cyan]            - État de la simulation
  [cyan]quit[/cyan]              - Quitter

[bright_white]Contrôles autonomes:[/bright_white]
  [cyan]pause[/cyan]             - Mettre en pause
  [cyan]resume[/cyan]            - Reprendre
  [cyan]stop[/cyan]              - Arrêter
  [cyan]step[/cyan]              - Un seul tick
  [cyan]speed <n>[/cyan]         - Vitesse (0.5 à 10.0)
"""
        self.console.print(help_text)

    def _handle_command(self, command: str, args: list):
        """Gère les commandes."""

        # Commandes de contrôle
        if command == "quit" or command == "exit":
            self.running = False

        elif command == "help":
            self._show_help()

        # Simulation
        elif command == "start":
            self.engine.start()
            self.console.print("[green]✓ Simulation démarrée (mode manuel)[/green]")

        elif command == "start_autonomous" or command == "auto":
            self.engine.start_autonomous()
            self.console.print("[green]✓ Simulation démarrée en mode autonome[/green]")

        elif command == "run_live" or command == "live":
            self.live_mode = True
            self.engine.start_autonomous()
            self.console.print("[green]✓ Mode live activé. CTRL+C pour quitter.[/green]")

        elif command == "pause":
            self.engine.pause()
            self.console.print("[yellow]⏸ Pause[/yellow]")

        elif command == "resume":
            self.engine.resume()
            self.console.print("[green]▶ Reprise[/green]")

        elif command == "stop":
            self.engine.stop()
            self.console.print("[red]⏹ Arrêt[/red]")

        elif command == "step":
            self.engine.step()
            self.console.print(f"[cyan]→ Tick {self.engine.time.current_tick}[/cyan]")

        elif command == "speed":
            if args:
                try:
                    speed = float(args[0])
                    self.engine.set_speed(speed)
                    self.console.print(f"[green]✓ Vitesse: {speed}x[/green]")
                except:
                    self.console.print("[red]Usage: speed <multiplicateur>[/red]")
            else:
                self.console.print("[red]Usage: speed <multiplicateur>[/red]")

        # Informations
        elif command == "status":
            self._show_status()

        elif command == "dashboard" or command == "dash":
            self._show_dashboard()

        elif command == "world":
            self._show_world()

        elif command == "agents":
            self._show_agents()

        elif command == "xana":
            self._show_xana()

        elif command == "metrics":
            self._show_metrics()

        # Utilitaires
        elif command == "tick":
            count = int(args[0]) if args else 1
            for _ in range(count):
                self.engine.step()
            self.console.print(f"[cyan]✓ {count} tick(s) exécuté(s)[/cyan]")

        else:
            self.console.print(f"[red]Commande inconnue: {command}[/red]")
            self.console.print("[yellow]Tapez 'help' pour la liste des commandes.[/yellow]")

    def _show_help(self):
        """Affiche l'aide complète."""
        help_content = """
[bold bright_white]═══ CARTHAGE ENGINE v2.0 - AIDE ═══[/bold bright_white]

[bright_yellow]CONTRÔLES SIMULATION[/bright_yellow]
  start              Démarre en mode manuel (tick par tick)
  start_autonomous   Démarre en mode autonome continu
  run_live           Mode live avec rafraîchissement continu
  pause              Met en pause
  resume             Reprend
  stop               Arrête complètement
  step               Exécute 1 tick
  tick <n>           Exécute N ticks
  speed <n>          Change la vitesse (0.5 à 10.0)

[bright_yellow]INFORMATIONS[/bright_yellow]
  status             État de la simulation
  dashboard          Tableau de bord complet
  world              État du monde
  agents             Liste des agents
  xana               État de XANA
  metrics            Métriques complètes

[bright_yellow]UTILITAIRES[/bright_yellow]
  help               Cette aide
  quit               Quitter

[bright_white]La simulation v2.0 est AUTONOME:[/bright_white]
  - XANA agit de façon stratégique
  - Les agents réagissent automatiquement
  - Le monde évolue sans intervention
  - Observez le conflit se dérouler en temps réel
"""
        panel = Panel(help_content, title="[cyan]Aide[/cyan]", border_style="cyan")
        self.console.print(panel)

    def _show_status(self):
        """Affiche le statut."""
        summary = self.engine.get_status_summary()

        status_text = f"""
[bright_white]Tick:[/bright_white] {summary['tick']}
[bright_white]État:[/bright_white] {summary['state']}
[bright_white]Vitesse:[/bright_white] {summary['speed']}x
[bright_white]TPS réel:[/bright_white] {summary['tps_actual']:.1f}

[bright_white]Agents opérationnels:[/bright_white] {summary['agents_operational']}
[bright_white]Monstres actifs:[/bright_white] {summary['monsters_active']}
[bright_white]Tours actives:[/bright_white] {summary['towers_active']}
[bright_white]Corruption globale:[/bright_white] {summary['corruption_global']}
[bright_white]Puissance XANA:[/bright_white] {summary['xana_power']:.1f}
"""
        panel = Panel(status_text, title="[cyan]Statut[/cyan]", border_style="cyan")
        self.console.print(panel)

    def _show_dashboard(self):
        """Affiche le dashboard."""
        metrics = self.engine.metrics.current
        self.console.print(Panel(metrics.summary(), title="[cyan]Dashboard[/cyan]", border_style="cyan"))

    def _show_world(self):
        """Affiche l'état du monde."""
        lines = ["[bold]Secteurs:[/bold]"]
        for sector_id, sector in self.engine.world.sectors.items():
            corruption_color = "red" if sector.corruption_level > 0.5 else "yellow" if sector.corruption_level > 0.2 else "green"
            lines.append(f"  [{corruption_color}]{sector_id}[/{corruption_color}]: corruption {sector.corruption_level:.0%}")

        self.console.print(Panel("\n".join(lines), title="[cyan]Monde[/cyan]", border_style="cyan"))

    def _show_agents(self):
        """Affiche les agents."""
        lines = ["[bold]Agents:[/bold]"]
        for agent in self.engine.world.agents.values():
            health_pct = agent.health / agent.max_health
            health_color = "green" if health_pct > 0.7 else "yellow" if health_pct > 0.3 else "red"

            status = "✓" if agent.is_operational() else "✗"
            lines.append(f"  {status} [{health_color}]{agent.name}[/{health_color}] - {agent.sector} - Santé: {agent.health:.0f}/{agent.max_health:.0f}")

        self.console.print(Panel("\n".join(lines), title="[cyan]Agents[/cyan]", border_style="cyan"))

    def _show_xana(self):
        """Affiche l'état de XANA."""
        xana = self.engine.world.xana
        if not xana:
            self.console.print("[red]XANA non disponible[/red]")
            return

        lines = [
            f"[bold]Puissance:[/bold] {xana.power_level:.1f}",
            f"[bold]Influence:[/bold] {xana.influence:.0%}",
            f"[bold]Ressources:[/bold] {xana.resources}",
            f"[bold]Tours actives:[/bold] {xana.active_towers}",
            f"[bold]Monstres actifs:[/bold] {xana.active_monsters}",
            f"[bold]Plans actifs:[/bold] {len(self.engine.xana_strategy.active_plans)}"
        ]

        # Plans actifs
        if self.engine.xana_strategy.active_plans:
            lines.append("\n[bold]Plans stratégiques:[/bold]")
            for plan in self.engine.xana_strategy.active_plans[:3]:
                lines.append(f"  • {plan.goal.value} ({plan.target}) - Phase: {plan.phase.value}")

        self.console.print(Panel("\n".join(lines), title="[red]XANA[/red]", border_style="red"))

    def _show_metrics(self):
        """Affiche les métriques."""
        m = self.engine.metrics.current

        text = f"""
[bold bright_white]Métriques Simulation[/bold bright_white]

Tick: {m.current_tick} | Temps: {m.simulation_time:.1f}s
Vitesse: {m.simulation_speed}x | État: {m.is_running}

[bold]Menaces:[/bold]
  Menace globale: {m.global_threat:.0%}
  Corruption globale: {m.global_corruption:.0%}
  Stabilité: {m.global_stability:.0%}

[bold]XANA:[/bold]
  Puissance: {m.xana_power_level:.1f}
  Influence: {m.xana_influence:.0%}
  Ressources: {m.xana_resources}
  Plans actifs: {m.xana_active_plans}

[bold]Agents:[/bold]
  Actifs: {m.active_agents}
  Santé moyenne: {m.average_agent_health:.0f}%
  Moral moyen: {m.average_agent_morale:.0%}
  Stress moyen: {m.average_agent_stress:.0%}
  Fatigue moyenne: {m.average_agent_fatigue:.0%}

[bold]Secteurs:[/bold]
  Stables: {m.sectors_stable}
  Contestés: {m.sectors_contested}
  Corrompus: {m.sectors_corrupted}

[bold]Combat:[/bold]
  Monstres actifs: {m.active_monsters}
  Tours actives: {m.active_towers}
"""
        self.console.print(Panel(text, title="[cyan]Métriques Complètes[/cyan]", border_style="cyan"))

    def _run_live_mode(self):
        """Mode live avec rafraîchissement continu."""
        from rich.live import Live
        from rich.layout import Layout
        from rich.panel import Panel

        with Live(self._generate_live_display(), refresh_per_second=2, console=self.console) as live:
            while self.live_mode:
                try:
                    time.sleep(0.5)
                    live.update(self._generate_live_display())
                except KeyboardInterrupt:
                    break

        self.live_mode = False
        self.engine.pause()

    def _generate_live_display(self):
        """Génère l'affichage live."""
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main"),
            Layout(name="footer", size=3)
        )

        # Header
        status = self.engine.get_status_summary()
        header_text = f"CARTHAGE ENGINE v2.0 | Tick: {status['tick']} | {status['state'].upper()} | Vitesse: {status['speed']}x"
        layout["header"].update(Panel(header_text, style="cyan bold"))

        # Main
        metrics = self.engine.metrics.current
        main_text = f"""
[bold]Menace:[/bold] {metrics.global_threat:.0%}  [bold]Corruption:[/bold] {metrics.global_corruption:.0%}  [bold]XANA:[/bold] {metrics.xana_power_level:.1f}

[yellow]Agents:[/yellow] {metrics.active_agents} actifs | Moral: {metrics.average_agent_morale:.0%} | Stress: {metrics.average_agent_stress:.0%}
[red]XANA:[/red] {metrics.xana_active_plans} plans | {metrics.active_towers} tours | {metrics.active_monsters} monstres
[green]Secteurs:[/green] {metrics.sectors_stable} stables | {metrics.sectors_contested} contestés | {metrics.sectors_corrupted} corrompus

[dim]CTRL+C pour quitter le mode live[/dim]
"""
        layout["main"].update(Panel(main_text, title="Dashboard Live", border_style="bright_cyan"))

        # Footer
        recent_events = list(self.engine.event_manager.events[-3:])
        events_text = "\n".join([f"{e.message}" for e in recent_events]) if recent_events else "Aucun événement récent"
        layout["footer"].update(Panel(events_text, title="Événements", border_style="yellow"))

        return layout
