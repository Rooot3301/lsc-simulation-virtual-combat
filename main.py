"""
Point d'entrée principal de Carthage Engine.
"""

from carthage_engine.cli.shell import CarthageShell


def main():
    """Lance le shell interactif."""
    shell = CarthageShell()
    shell.run()


if __name__ == "__main__":
    main()
