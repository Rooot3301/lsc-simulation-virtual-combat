"""
Gestionnaire de commandes CLI.
"""

from typing import List
from ..core import CarthageEngine
from .inspectors import Inspector
from .timeline import Timeline
from ..persistence import save_simulation, load_simulation


class CommandHandler:
    """Gère les commandes du CLI."""

    def __init__(self, engine: CarthageEngine):
        self.engine = engine
        self.inspector = Inspector(engine)
        self.timeline = Timeline(engine.event_manager)

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
            self.show_help()

        # Contrôle simulation
        elif command == 'start':
            self.engine.start()
            print("Simulation démarrée.")

        elif command == 'pause':
            self.engine.pause()
            print("Simulation en pause.")

        elif command == 'resume':
            self.engine.resume()
            print("Simulation reprise.")

        elif command == 'stop':
            self.engine.stop()
            print("Simulation arrêtée.")

        elif command == 'tick':
            count = int(args[0]) if args else 1
            self.engine.tick(count)
            print(f"{count} tick(s) exécuté(s).")

        elif command == 'run':
            count = int(args[0]) if args else 10
            self.engine.start()
            self.engine.tick(count)
            print(f"Simulation exécutée pendant {count} ticks.")

        elif command == 'step':
            self.engine.tick(1)
            self.inspector.inspect_world()

        # Inspection
        elif command == 'status':
            status = self.engine.get_status_summary()
            for key, value in status.items():
                print(f"{key}: {value}")

        elif command == 'world':
            self.inspector.inspect_world()

        elif command == 'sectors':
            self.inspector.inspect_sectors()

        elif command == 'agents':
            self.inspector.inspect_agents()

        elif command == 'monsters':
            self.inspector.inspect_monsters()

        elif command == 'towers':
            self.inspector.inspect_towers()

        elif command == 'skid':
            self.inspector.inspect_skid()

        elif command == 'xana':
            self.inspector.inspect_xana()

        elif command == 'entities':
            self.inspector.inspect_agents()
            self.inspector.inspect_monsters()

        # Timeline
        elif command == 'events':
            count = int(args[0]) if args else 10
            self.timeline.show_recent(count)

        elif command == 'timeline':
            count = int(args[0]) if args else 20
            self.timeline.show_recent(count)

        # Persistence
        elif command == 'save':
            filename = args[0] if args else "save.json"
            result = save_simulation(self.engine, filename)
            print(result)

        elif command == 'load':
            filename = args[0] if args else "save.json"
            result = load_simulation(self.engine, filename)
            print(result)

        else:
            print(f"Commande inconnue: {command}")
            print("Tapez 'help' pour voir les commandes disponibles.")

        return True

    def show_help(self):
        """Affiche l'aide."""
        help_text = """
=== COMMANDES CARTHAGE ENGINE ===

Contrôle de la simulation:
  start                 - Démarre la simulation
  pause                 - Met en pause
  resume                - Reprend
  stop                  - Arrête
  tick <n>              - Exécute N ticks (défaut: 1)
  run <n>               - Lance la simulation pendant N ticks (défaut: 10)
  step                  - Exécute 1 tick et affiche l'état

Inspection:
  status                - Statut général
  world                 - État du monde
  sectors               - État des secteurs
  agents                - Liste des agents
  monsters              - Liste des monstres
  towers                - Liste des tours
  skid                  - État du Skid
  xana                  - État de XANA
  entities              - Agents et monstres

Timeline:
  events <n>            - Affiche les N derniers événements (défaut: 10)
  timeline <n>          - Affiche la timeline (défaut: 20)

Persistance:
  save <fichier>        - Sauvegarde (défaut: save.json)
  load <fichier>        - Charge (défaut: save.json)

Système:
  help                  - Affiche cette aide
  quit / exit / q       - Quitte
"""
        print(help_text)
