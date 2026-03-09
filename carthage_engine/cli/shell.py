"""
Shell interactif principal.
"""

from ..core import CarthageEngine
from .commands import CommandHandler


class CarthageShell:
    """Shell interactif de Carthage Engine."""

    def __init__(self):
        self.engine = CarthageEngine()
        self.command_handler = CommandHandler(self.engine)
        self.running = True

    def run(self):
        """Lance le shell interactif."""
        self.print_banner()
        print("\nTapez 'help' pour voir les commandes disponibles.")
        print("Tapez 'run 10' pour lancer une simulation de démonstration.\n")

        while self.running:
            try:
                user_input = input("carthage> ").strip()

                if not user_input:
                    continue

                parts = user_input.split()
                command = parts[0]
                args = parts[1:] if len(parts) > 1 else []

                self.running = self.command_handler.handle_command(command, args)

            except KeyboardInterrupt:
                print("\nInterruption détectée.")
                print("Utilisez 'quit' pour quitter proprement.")
            except Exception as e:
                print(f"Erreur: {e}")

        print("\nAu revoir.")

    def print_banner(self):
        """Affiche la bannière de bienvenue."""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║              CARTHAGE ENGINE v1.0                            ║
║                                                              ║
║        Simulation Stratégique Inspirée de Code Lyoko        ║
║                                                              ║
║              Python CLI Simulation Engine                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
        print(banner)
