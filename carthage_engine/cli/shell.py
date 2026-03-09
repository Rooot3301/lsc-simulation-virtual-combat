"""
Shell interactif principal avec interface Rich.
"""

from rich.prompt import Prompt
from ..core import CarthageEngine
from .commands import CommandHandler
from .ui.renderer import CarthageRenderer


class CarthageShell:
    """Shell interactif de Carthage Engine avec interface Rich."""

    def __init__(self):
        self.engine = CarthageEngine()
        self.command_handler = CommandHandler(self.engine)
        self.renderer = CarthageRenderer()
        self.running = True

    def run(self):
        """Lance le shell interactif."""
        self.renderer.print_banner()

        while self.running:
            try:
                user_input = Prompt.ask("\n[bright_cyan bold]carthage[/bright_cyan bold]").strip()

                if not user_input:
                    continue

                parts = user_input.split()
                command = parts[0]
                args = parts[1:] if len(parts) > 1 else []

                self.running = self.command_handler.handle_command(command, args)

            except KeyboardInterrupt:
                self.renderer.console.print()
                self.renderer.print_message("Interruption détectée. Utilisez 'quit' pour quitter proprement.", "yellow")
            except Exception as e:
                self.renderer.print_error(f"Erreur: {e}")

        self.renderer.console.print()
        self.renderer.print_message("Au revoir.", "cyan bold")
        self.renderer.console.print()
