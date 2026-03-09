"""
Chargement de l'état de la simulation.
"""

import json
from pathlib import Path
from typing import Any


def load_simulation(engine: Any, filename: str = "save.json"):
    """Charge l'état de la simulation depuis un fichier."""
    filepath = Path(filename)

    if not filepath.exists():
        return f"Fichier {filename} introuvable."

    with open(filepath, 'r', encoding='utf-8') as f:
        save_data = json.load(f)

    # Note: Implémentation simplifiée
    # Une vraie implémentation recréerait toutes les entités
    return f"Chargement depuis {filename} (fonctionnalité en développement)"
