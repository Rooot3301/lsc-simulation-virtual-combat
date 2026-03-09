# CARTHAGE ENGINE

**Simulation Stratégique Inspirée de Code Lyoko**

Carthage Engine est un moteur de simulation stratégique en Python, entièrement en CLI, qui simule un conflit entre une intelligence artificielle hostile (XANA) et des agents défensifs dans un monde virtuel.

## 🎯 Caractéristiques

- **Simulation systémique** : Émergence de comportements stratégiques complexes
- **IA XANA** : Intelligence artificielle multi-couches avec planification, mémoire et adaptation
- **Psychologie des agents** : Fatigue, stress, moral, corruption progressive
- **Corruption dynamique** : Propagation de la corruption à travers les secteurs
- **Réseau et navigation** : Système de navigation pour le Skid avec corridors et nœuds
- **CLI interactif** : Interface en ligne de commande complète et intuitive
- **Événements en temps réel** : Journal détaillé de tous les événements
- **Persistance** : Sauvegarde et chargement de l'état de simulation

## 📦 Architecture

```
carthage_engine/
├── core/           # Moteur de simulation (engine, world, scheduler, events, time)
├── entities/       # Entités (agents, monstres, tours, skid, xana)
├── ai/             # IA de XANA (planification, mémoire, doctrine, menaces, vulnérabilités)
├── simulation/     # Systèmes de gameplay
├── world/          # Secteurs, réseau, routes
├── logging/        # Système de journalisation
├── cli/            # Interface CLI (shell, commandes, inspecteurs, timeline)
├── persistence/    # Sauvegarde et chargement
├── tests/          # Tests unitaires
└── scenarios/      # Scénarios de démonstration
```

## 🚀 Installation

Aucune dépendance externe requise. Python 3.8+ seulement.

```bash
cd carthage_engine
python main.py
```

## 🎮 Utilisation

### Lancer la simulation

```bash
python main.py
```

### Commandes principales

```
start               - Démarre la simulation
run <n>             - Lance la simulation pendant N ticks
tick <n>            - Exécute N ticks
pause / resume      - Contrôle de la simulation
step                - Exécute 1 tick et affiche l'état
```

### Inspection

```
status              - Statut général
world               - État du monde
sectors             - État des secteurs
agents              - Liste des agents
monsters            - Liste des monstres
towers              - Liste des tours
skid                - État du Skid
xana                - État de XANA
```

### Timeline

```
events <n>          - Affiche les N derniers événements
timeline <n>        - Affiche la timeline complète
```

### Sauvegarde

```
save <fichier>      - Sauvegarde l'état
load <fichier>      - Charge l'état
```

## 🌍 Monde Virtuel

### Secteurs

- **Forêt** : Secteur de base, corruption modérée
- **Désert** : Secteur hostile avec haute température
- **Banquise** : Secteur froid, difficile
- **Montagne** : Secteur montagneux, très difficile
- **Secteur 5** : Secteur stratégique central
- **Mer Numérique** : Zone de navigation pour le Skid
- **Réseau** : Corridors et nœuds de transport

### Entités

#### Agents
- **Guerrier** : Combat rapproché, haute défense
- **Éclaireur** : Rapide, faible défense
- **Hackeur** : Spécialiste désactivation de tours
- **Soutien** : Équilibré, support d'équipe

#### Monstres
- **Kankrelat** : Monstre de base, rapide
- **Blok** : Défenseur solide
- **Hornet** : Volant, attaque à distance
- **Megatank** : Tank lourd, très résistant
- **Krabe** : Équilibré
- **Manta** : Volant, puissant
- **Tarantula** : Tireur d'élite

## 🧠 Intelligence Artificielle XANA

### Systèmes

1. **Perception** : Analyse de l'état du monde
2. **Mémoire** : Stockage des observations et patterns
3. **Planification** : Création de plans stratégiques multi-étapes
4. **Doctrine** : Règles de comportement (agressif, défensif, opportuniste, etc.)
5. **Carte des menaces** : Évaluation tactique du terrain
6. **Analyse de vulnérabilités** : Détection des faiblesses adverses
7. **Adaptation** : Apprentissage et ajustement

### Objectifs Stratégiques

- Dominer un secteur
- Propager la corruption
- Intercepter le Skid
- Corrompre un agent
- Créer une diversion
- Piéger les agents
- Isoler le Secteur 5
- Activer des tours
- Défendre le territoire
- Éliminer une menace

## 🔄 Système de Corruption

Les agents sont progressivement vulnérables à la corruption selon :

- Niveau de stress
- Isolation
- Exposition à la corruption du secteur
- Proximité des tours actives
- Fatigue
- Moral

### Stades de Corruption

1. **Propre** : Aucune corruption
2. **Exposé** : Début d'exposition
3. **Déstabilisé** : Premiers signes
4. **Influencé** : Corruption visible
5. **Partiellement corrompu** : Contrôle partiel perdu
6. **Lourdement corrompu** : Presque perdu
7. **Perdu** : Contrôle total par XANA

## 📊 Logs

Tous les logs sont en français avec différents niveaux :

- **INFO** : Information générale
- **ALERTE** : Événement important
- **CRITIQUE** : Situation critique
- **DEBUG** : Information de débogage
- **IA** : Décisions de l'IA
- **COMBAT** : Événements de combat
- **CORRUPTION** : Propagation de corruption
- **STRATEGIE** : Décisions stratégiques
- **RESEAU** : Événements réseau
- **SKID** : Actions du Skid

## 🧪 Exemple de Session

```bash
carthage> run 10
Simulation exécutée pendant 10 ticks.

carthage> status
tick: 10
agents: 4
monsters: 8
active_towers: 3
global_corruption: 12.5%
xana_power: 1.5

carthage> agents
=== AGENTS ===
  [✓] Yumi (guerrier)
      Santé: 120/120
      Secteur: forest
      Corruption: 5%
      Stress: 12%
      Fatigue: 8%

carthage> xana
=== XANA ===
  Niveau de puissance: 1.5/10.0
  Influence: 45%
  Ressources: 250
  Tours actives: 3
  Objectif actuel: dominer_secteur

carthage> events 5
[INFO] T+00:00:10 - Simulation Carthage Engine démarrée.
[ALERTE] T+00:00:15 - Activation de la tour T-FOREST-01 détectée.
[STRATEGIE] T+00:00:18 - XANA sélectionne l'objectif : dominer_secteur
[ALERTE] T+00:00:22 - XANA déploie 3 kankrelat(s) dans le secteur forest.
[CORRUPTION] T+00:00:25 - Corruption propagée dans le secteur forest.
```

## 🏗️ Conception

### Principes

- **Modularité** : Architecture en modules indépendants
- **Émergence** : Comportements complexes issus de règles simples
- **Réalisme** : Simulation cohérente et crédible
- **Performance** : Optimisé pour des milliers de ticks
- **Maintenabilité** : Code propre, commenté, structuré

### Technologies

- Python 3.8+ standard library uniquement
- Dataclasses pour les structures de données
- Enums pour les types
- Type hints pour la clarté
- Architecture événementielle

## 📝 Développement

### Tests

```bash
python -m pytest tests/
```

### Structure de Code

- Utilisation de dataclasses
- Type hints systématiques
- Commentaires en français
- Documentation inline
- Patterns clairs et lisibles

## 🎯 Roadmap

- [ ] Système de combat détaillé
- [ ] Missions complexes
- [ ] Réplication XANA
- [ ] Multi-threading pour performance
- [ ] Export des statistiques
- [ ] Replay de simulations
- [ ] Modes de jeu supplémentaires

## 📄 Licence

Projet éducatif et démonstratif.

## 👥 Crédits

Inspiré de l'univers Code Lyoko.
Développé comme démonstration d'architecture de simulation stratégique.

---

**Carthage Engine v1.0** - Simulation Stratégique Python CLI
