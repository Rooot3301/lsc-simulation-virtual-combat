"""
Inspecteurs - affichent des informations détaillées.
"""

from ..core import CarthageEngine


class Inspector:
    """Inspecte l'état de la simulation."""

    def __init__(self, engine: CarthageEngine):
        self.engine = engine

    def inspect_world(self):
        """Affiche l'état du monde."""
        print("\n=== ÉTAT DU MONDE VIRTUEL ===\n")
        print(f"Corruption globale: {self.engine.world.global_corruption:.2%}")
        print(f"Agents opérationnels: {self.engine.world.get_operational_agents_count()}")
        print(f"Monstres actifs: {self.engine.world.get_active_monsters_count()}")
        print(f"Tours actives: {len(self.engine.world.get_active_towers())}")

    def inspect_sectors(self):
        """Affiche l'état des secteurs."""
        print("\n=== SECTEURS ===\n")
        for name, sector in self.engine.world.sectors.items():
            print(f"  {sector.name}:")
            print(f"    Corruption: {sector.corruption_level:.2%}")
            print(f"    Tours: {len(sector.tower_ids)}")
            print(f"    Entités: {len(sector.entity_ids)}")
            print(f"    Menace: {sector.threat_score:.1f}")

    def inspect_agents(self):
        """Affiche l'état des agents."""
        print("\n=== AGENTS ===\n")
        for agent in self.engine.world.agents.values():
            status = "✓" if agent.is_operational() else "✗"
            print(f"  [{status}] {agent.name} ({agent.agent_type.value})")
            print(f"      Santé: {agent.health:.0f}/{agent.max_health:.0f}")
            print(f"      Secteur: {agent.sector}")
            print(f"      Corruption: {agent.corruption_level:.2%}")
            print(f"      Stress: {agent.psychological_state.stress:.2%}")
            print(f"      Fatigue: {agent.psychological_state.fatigue:.2%}")

    def inspect_monsters(self):
        """Affiche l'état des monstres."""
        print("\n=== MONSTRES ===\n")
        active = [m for m in self.engine.world.monsters.values() if not m.is_destroyed]
        if not active:
            print("  Aucun monstre actif.")
            return

        for monster in active:
            print(f"  {monster.name} ({monster.monster_type.value})")
            print(f"    Santé: {monster.health:.0f}/{monster.max_health:.0f}")
            print(f"    Secteur: {monster.sector}")
            print(f"    Comportement: {monster.behavior.value}")

    def inspect_towers(self):
        """Affiche l'état des tours."""
        print("\n=== TOURS ===\n")
        for tower in self.engine.world.towers.values():
            print(f"  {tower.name} - {tower.state.value}")
            print(f"    Secteur: {tower.sector}")
            print(f"    Activation: {tower.activation_level:.0%}")
            if tower.defending_monsters:
                print(f"    Défenseurs: {len(tower.defending_monsters)}")

    def inspect_skid(self):
        """Affiche l'état du Skid."""
        print("\n=== SKID ===\n")
        skid = self.engine.world.skid
        if not skid:
            print("  Skid non disponible.")
            return

        print(f"  {skid.get_status_summary()}")

    def inspect_xana(self):
        """Affiche l'état de XANA."""
        print("\n=== XANA ===\n")
        xana = self.engine.world.xana
        if not xana:
            print("  XANA non initialisé.")
            return

        print(f"  Niveau de puissance: {xana.power_level:.1f}/10.0")
        print(f"  Influence: {xana.influence:.2%}")
        print(f"  Ressources: {xana.resources}")
        print(f"  Tours actives: {xana.active_towers}")
        print(f"  Monstres actifs: {xana.active_monsters}")
        print(f"  Objectif actuel: {xana.current_goal or 'Aucun'}")
        print(f"  Plans actifs: {len(xana.active_plans)}")

        ai_state = self.engine.xana_ai.get_current_state_summary()
        print(f"\n  IA XANA:")
        print(f"    Doctrine: {ai_state.get('doctrine')}")
        print(f"    Agressivité: {ai_state.get('aggression'):.2%}")
        print(f"    Mémoires actives: {ai_state.get('memory_count')}")
        print(f"    Vulnérabilités détectées: {ai_state.get('vulnerabilities_detected')}")
