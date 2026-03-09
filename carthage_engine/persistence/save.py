"""
Sauvegarde de l'état de la simulation.
"""

import json
from pathlib import Path
from typing import Any


def save_simulation(engine: Any, filename: str = "save.json"):
    """Sauvegarde l'état complet de la simulation."""
    save_data = {
        'tick': engine.time.current_tick,
        'timestamp': engine.time.get_timestamp(),
        'world': engine.world.to_dict(),
        'xana_ai': {
            'current_goal': engine.xana_ai.current_goal.value if engine.xana_ai.current_goal else None,
            'doctrine': engine.xana_ai.doctrine.primary_rule.value,
            'aggression': engine.xana_ai.doctrine.aggression_level
        }
    }

    filepath = Path(filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(save_data, f, indent=2, ensure_ascii=False)

    return f"Simulation sauvegardée dans {filename}"
