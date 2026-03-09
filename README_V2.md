# CARTHAGE ENGINE v2.0

## 🚀 Simulation Stratégique Autonome

CARTHAGE ENGINE v2.0 est une **simulation stratégique totalement autonome** inspirée de Code Lyoko, où XANA et les agents évoluent de manière indépendante dans un conflit dynamique.

---

## ✨ Nouveautés v2.0

### Simulation Autonome

Lorsque vous lancez la simulation, **le monde évolue par lui-même** :

- ✓ **XANA** agit stratégiquement sans intervention
- ✓ **Agents** réagissent et décident automatiquement
- ✓ **Tours** s'activent dynamiquement
- ✓ **Corruption** se propage progressivement
- ✓ **Monstres** sont déployés tactiquement
- ✓ **Skid** peut naviguer en mode autonome
- ✓ **Secteurs** évoluent continuellement

### IA XANA Multicouche

XANA dispose d'une intelligence stratégique complète :

1. **Couche Perception** - Évalue le monde en temps réel
2. **Couche Stratégique** - Sélectionne des objectifs (dominer secteur, corrompre agent, intercepter Skid...)
3. **Couche Opérationnelle** - Génère des plans multi-étapes
4. **Couche Tactique** - Exécute les opérations (activer tours, déployer monstres)
5. **Adaptation** - Apprend de ses succès et échecs

### IA Agents Autonome

Les agents ne sont plus passifs :

- Évaluent les menaces localement
- Réagissent aux tours actives
- Protègent les secteurs vulnérables
- Soutiennent les alliés en difficulté
- Battent en retraite si submergés
- Récupèrent dans les zones sûres

### Psychologie Profonde

Chaque agent a un état psychologique complexe :

- **Fatigue** - Diminue l'efficacité
- **Stress** - Affecte les décisions
- **Moral** - Impact sur la performance
- **Isolation** - Vulnérabilité accrue
- **Exposition Corruption** - Dégradation progressive
- **Confiance** - Avec les alliés

###  Corruption Progressive

7 stades de corruption avec effets subtils :

1. **Clean** - Aucune corruption
2. **Exposed** - Exposition initiale
3. **Destabilized** - Réactions ralenties
4. **Influenced** - Jugement altéré
5. **Partially Corrupted** - Mauvaises décisions
6. **Heavily Corrupted** - Sabotage possible
7. **Lost** - Contrôle total par XANA

### Systèmes Avancés

- **Information Imparfaite** - Perception limitée, rapports bruités
- **Économie de Ressources** - XANA et agents ont des coûts pour agir
- **Métriques Complètes** - 40+ métriques suivies en temps réel
- **Historique** - Snapshot réguliers pour analyse

---

## 🎮 Utilisation

### Lancer la simulation

```bash
python3 main_v2.py
```

### Commandes Principales

#### Contrôles Simulation

```
start              # Démarre en mode manuel (tick par tick)
start_autonomous   # Démarre en mode autonome continu
run_live           # Mode live avec dashboard temps réel
pause              # Met en pause
resume             # Reprend
stop               # Arrête
step               # Exécute 1 tick
tick <n>           # Exécute N ticks
speed <n>          # Change la vitesse (0.5 à 10.0)
```

#### Informations

```
status             # État de la simulation
dashboard          # Tableau de bord complet
world              # État du monde
agents             # Liste des agents
xana               # État de XANA
metrics            # Métriques complètes
```

#### Utilitaires

```
help               # Aide complète
quit               # Quitter
```

---

## 📊 Mode Live

Le mode live est l'expérience ultime :

```
> run_live
```

Vous verrez :
- Dashboard mis à jour en continu
- Métriques évoluant en temps réel
- Événements stratégiques en direct
- XANA planifiant ses attaques
- Agents réagissant dynamiquement

**Appuyez sur CTRL+C pour quitter le mode live**

---

## 🏗️ Architecture v2.0

### Nouveaux Modules

```
carthage_engine/
├── core/
│   ├── engine_v2.py          # Moteur autonome
│   ├── autonomous_loop.py    # Boucle continue
│   └── metrics.py            # Métriques complètes
│
├── ai/
│   ├── perception.py         # Perception XANA
│   ├── strategic_layer.py    # Stratégie XANA
│   └── agent_ai.py           # IA agents autonome
│
├── systems/
│   ├── psychology.py         # État psychologique
│   ├── corruption.py         # Corruption progressive
│   ├── information.py        # Information imparfaite
│   └── resources.py          # Économie ressources
│
└── cli/
    └── shell_v2.py           # Shell interactif v2.0
```

### Systèmes Intégrés

1. **Boucle Autonome** - Thread-safe, contrôles temps réel
2. **IA XANA** - 5 couches de décision
3. **IA Agents** - Comportement réactif intelligent
4. **Psychologie** - 10+ facteurs humains
5. **Corruption** - 7 stades progressifs
6. **Ressources** - Coûts et contraintes
7. **Métriques** - Tracking complet

---

## 🎯 Objectifs Stratégiques XANA

XANA peut poursuivre dynamiquement :

- **DOMINATE_SECTOR** - Dominer un secteur
- **SPREAD_CORRUPTION** - Propager la corruption
- **INTERCEPT_SKID** - Intercepter le Skid
- **CORRUPT_AGENT** - Corrompre un agent
- **CREATE_DIVERSION** - Créer une diversion
- **ISOLATE_SECTOR5** - Isoler le Secteur 5
- **EXHAUST_DEFENDERS** - Épuiser les défenseurs
- **TRAP_AGENTS** - Piéger les agents
- **OVERLOAD_RESPONSE** - Surcharger la réponse
- **NETWORK_DESTABILIZATION** - Déstabiliser le réseau

---

## 📈 Métriques Suivies

### Globales
- Tick actuel, temps simulation, vitesse
- Menace globale, corruption globale, stabilité
- État simulation (running/paused/stopped)

### XANA
- Puissance, influence, ressources
- Plans actifs, doctrine active
- Tours/monstres déployés

### Agents
- Agents opérationnels
- Santé, moral, stress, fatigue moyens
- Corruption moyenne
- Efficacité combat

### Secteurs
- Stables, contestés, corrompus, dominés
- Niveau corruption par secteur
- Présence agents/tours

### Skid
- Intégrité coque, énergie
- Mode navigation
- Niveau de danger
- Passagers

---

## 🔧 Compatibilité

Le v2.0 est **rétrocompatible** avec le système v1.0 existant :

- Le moteur original (`engine.py`) reste fonctionnel
- Le shell original (`shell.py`) reste utilisable
- Les entités ont été étendues sans casser l'ancien code
- `main.py` lance toujours la v1.0

Pour v2.0, utilisez `python3 main_v2.py`

---

## 🚦 État du Projet

### ✅ Implémenté

- Boucle simulation autonome thread-safe
- IA XANA multicouche (perception + stratégie)
- IA agents avec comportement réactif
- Système psychologie profonde
- Corruption progressive 7 stades
- Information imparfaite
- Économie de ressources
- Métriques complètes + historique
- Shell interactif v2.0
- Commandes complètes (start/pause/resume/stop/step/speed)
- Mode live avec dashboard temps réel

### 🔄 À Améliorer

- Corrections mineures compatibilité attributs legacy
- Extension réseau numérique (corridors, nodes)
- Système Skid autonome complet
- Système replay/analyse
- Support multi-scénarios
- Mode benchmark/expérimental
- Dashboard live plus riche

---

## 💡 Philosophie v2.0

> **"La simulation doit vivre par elle-même"**

Contrairement à la v1.0 où chaque action nécessitait une commande, la v2.0 est une **simulation vivante** :

- Le monde évolue continuellement
- XANA pense et agit stratégiquement
- Les agents réagissent de manière crédible
- Les événements émergent naturellement
- L'observateur surveille un conflit réel

Vous ne **jouez** pas, vous **observez** un conflit stratégique autonome se dérouler.

---

## 🎬 Démarrage Rapide

```bash
# Lancer la simulation
python3 main_v2.py

# Dans le shell
> help                # Voir toutes les commandes
> start_autonomous    # Démarrer en autonome
> run_live            # Observer en temps réel
```

**Le terminal devient un centre de commandement surveillant un conflit actif.**

---

## 📚 Documentation Technique

Voir les fichiers du projet pour détails d'implémentation :

- `CARTHAGE_ENGINE_GUIDE.md` - Guide complet du moteur
- `INTERFACE_v1.1_COMPLETE.md` - Documentation interface
- `CHANGELOG_v1.1.md` - Historique changements
- Code source dans `carthage_engine/`

---

## 🌟 Prochaines Étapes

La v2.0 pose les fondations d'une simulation stratégique autonome complète. Les prochaines itérations ajouteront :

- Réseau numérique comme espace opérationnel stratégique
- Système Skid pleinement autonome avec modes multiples
- Replay temporel et analyse approfondie
- Scénarios variés et mode expérimental
- Visualisations avancées
- Persistance et sauvegarde états

**CARTHAGE ENGINE v2.0 - Une simulation qui vit.**
