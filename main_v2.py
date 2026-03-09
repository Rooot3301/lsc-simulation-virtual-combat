"""
Point d'entrée principal de Carthage Engine v2.0.

SIMULATION STRATÉGIQUE AUTONOME.
"""

from carthage_engine.cli.shell_v2 import CarthageShellV2


def main():
    """Lance le shell interactif v2.0."""
    print("\n🚀 Lancement de CARTHAGE ENGINE v2.0...\n")
    shell = CarthageShellV2()
    shell.run()


if __name__ == "__main__":
    main()
