# 🎮 CARTHAGE ENGINE v1.1 - Interface Complète

## ✅ AMÉLIORATION MAJEURE TERMINÉE

L'interface CLI du CARTHAGE ENGINE a été **significativement améliorée** pour créer une expérience de **centre de commande stratégique** de niveau professionnel.

---

## 🚀 NOUVELLES FONCTIONNALITÉS

### 1. Header Étendu
```
╭──────────────────────────────────────────────────────╮
│ CARTHAGE ENGINE v1.1                          ACTIF  │
│ Statut: ACTIF  Tick: 00182  Corruption: 31%  XANA: 72% │
│                Doctrine: OPPORTUNISTE                │
╰──────────────────────────────────────────────────────╯
```

**Affichage en temps réel :**
- Statut simulation (ACTIF / EN PAUSE / ARRÊTÉ)
- Tick actuel
- Corruption globale (%)
- Puissance XANA (%)
- Doctrine active

---

### 2. Panneau XANA Étendu
```
╭─── XANA - ANALYSE STRATÉGIQUE ────╮
│  Doctrine           OPPORTUNISTE  │
│  Objectif           Intercepter   │
│  Phase              Exécution     │
│  Cible prioritaire  Skid          │
│  Menace globale     ÉLEVÉE        │
│  Puissance          7.2/10.0      │
│  Ressources         342           │
│  Plans actifs       2             │
╰───────────────────────────────────╯
```

**Informations stratégiques :**
- Doctrine actuelle
- Objectif en cours
- Phase du plan (Observation/Exécution)
- Cible prioritaire
- Niveau de menace (FAIBLE/MOYENNE/ÉLEVÉE)

---

### 3. Carte Stratégique des Secteurs
```
╭──── SECTEURS - CARTE STRATÉGIQUE ────╮
│ Forêt           ██████████████░  critique         │
│ Désert          █████████░░░░░░  activité XANA    │
│ Banquise        ██████░░░░░░░░░  activité XANA    │
│ Montagne        ███░░░░░░░░░░░░  surveillance     │
│ Secteur 5       ░░░░░░░░░░░░░░░  stable           │
│ Mer Numérique   ░░░░░░░░░░░░░░░  stable           │
│ Réseau          ░░░░░░░░░░░░░░░  stable           │
╰───────────────────────────────────────╯
```

**Barres de menace visuelles :**
- Rouge : critique (≥7/10)
- Jaune : activité XANA (4-7/10)
- Cyan : surveillance (2-4/10)
- Vert : stable (<2/10)

---

### 4. Indicateurs Stratégiques
```
╭──── INDICATEURS STRATÉGIQUES ────╮
│ Corruption globale ━━━              11% │
│ Menace globale     ━━━━━━━━╸        29% │
│ Skid intégrité     ━━━━━━━━━━━━━━━ 100% │
│ Moral agents       ━━━━━━━━━━━━━━━ 100% │
╰────────────────────────────────────────╯
```

**Barres de progression pour :**
- Corruption globale
- Menace globale (moyenne secteurs)
- Intégrité du Skid
- Moral moyen des agents

---

### 5. Journal Opérationnel
```
╭──── JOURNAL OPÉRATIONNEL ────╮
│ [T+00:03:25] [STRATEGIE] XANA prépare interception │
│ [T+00:03:26] [ALERTE] Tour T-ICE-02 activée        │
│ [T+00:03:27] [RESEAU] Instabilité corridor N-3     │
│ [T+00:03:28] [COMBAT] Odd engage un Krabe          │
│ [T+00:03:29] [CORRUPTION] Aelita: exposition 15%   │
╰─────────────────────────────────────────────────────╯
```

**Affiche les 8 derniers événements avec :**
- Timestamp
- Catégorie colorée
- Message détaillé

---

### 6. Panneau Alertes
```
╭──── ALERTES ────╮
│ [CRITIQUE] Corruption Yumi > 70%     │
│ [ALERTE] Activation T-FOREST-01      │
│ [STRATEGIE] XANA: dominer secteur    │
│ [COMBAT] Engagement Hornets          │
╰──────────────────────────────────────╯
```

**Affiche les 5 alertes les plus critiques**

---

## 🎯 NOUVELLES COMMANDES

### Commande `inspect`
Inspection détaillée des entités.

**Syntaxe :**
```
inspect agent <nom>
inspect xana
inspect skid
```

**Exemples :**

#### `inspect agent yumi`
```
╭──── YUMI ────╮ ╭──── RELATIONS ────╮
│ Santé:  85%  │ │ Odd → confiance élevée    │
│ Stress: 12%  │ │ Ulrich → confiance élevée │
│ Fatigue: 4%  │ │ Aelita → confiance moyenne│
│ Corruption:0%│ ╰───────────────────────────╯
╰──────────────╯
```

#### `inspect xana`
```
╭──── ÉTAT XANA ────╮ ╭──── STRATÉGIE ────╮
│ Puissance: 7.2/10 │ │ Doctrine: MANIPUL.│
│ Ressources: 456   │ │ Agressivité: 78%  │
│ Plans actifs: 3   │ │ Vulnéra.: 127     │
╰───────────────────╯ ╰───────────────────╯

╭──── PLANS ACTIFS ────╮
│ 1. Intercepter Skid corridor N-3    │
│ 2. Corrompre agent Yumi             │
│ 3. Activer tour T-MOUNTAIN-02       │
╰─────────────────────────────────────╯
```

#### `inspect skid`
```
╭──── ÉTAT ────╮ ╭──── NAVIGATION ────╮ ╭──── PASSAGERS ────╮
│ Mode: NAV    │ │ Position: N-3      │ │ • Yumi            │
│ Coque: 87%   │ │ Destination: SEC5  │ │ • Odd             │
│ Énergie: 92% │ │ Danger: 45%        │ ╰───────────────────╯
╰──────────────╯ ╰────────────────────╯
```

---

### Commande `run_live`
Mode simulation avec rafraîchissement automatique.

**Syntaxe :**
```
run_live <n>
```

**Exemple :**
```
carthage: run_live 50

[Le dashboard se rafraîchit automatiquement toutes les 0.5s
 pendant 50 ticks, permettant de voir l'évolution en temps réel]
```

---

## 📊 DISPOSITION DU DASHBOARD

```
┌─────────────────────────────────────────────────┐
│              HEADER (v1.1)                      │
│  Statut | Tick | Corruption | XANA | Doctrine  │
└─────────────────────────────────────────────────┘

┌──── MONDE ────┐  ┌──── XANA ────────┐
│ Corruption    │  │ Analyse          │
│ Agents        │  │ Stratégique      │
│ Monstres      │  │                  │
└───────────────┘  └──────────────────┘

┌──── AGENTS ───┐  ┌──── SKID ────────┐
│ Tableau       │  │ État             │
│ Détaillé      │  │                  │
└───────────────┘  └──────────────────┘

┌──────────────────────────────────────┐
│   SECTEURS - CARTE STRATÉGIQUE       │
│   [Barres de menace visuelles]       │
└──────────────────────────────────────┘

┌──── ALERTES ──┐  ┌──── INDICATEURS ─┐
│ 5 critiques   │  │ Barres progress. │
└───────────────┘  └──────────────────┘

┌──────────────────────────────────────┐
│     JOURNAL OPÉRATIONNEL             │
│     [8 derniers événements]          │
└──────────────────────────────────────┘
```

---

## 🎨 CODES COULEUR

| Catégorie | Couleur | Barre | Usage |
|-----------|---------|-------|-------|
| INFO | Cyan clair | █ | Informations |
| ALERTE | Jaune gras | █ | Avertissements |
| CRITIQUE | Rouge gras | █ | Urgences |
| STRATEGIE | Magenta | █ | Plans XANA |
| IA | Magenta gras | █ | Décisions IA |
| COMBAT | Rouge | █ | Affrontements |
| CORRUPTION | Orange | █ | Propagation |
| RESEAU | Bleu | █ | Réseau |
| SKID | Cyan gras | █ | Skid |

**Indicateurs de santé :**
- Vert (> 60%) : ✓
- Jaune (30-60%) : ⚠
- Rouge (< 30%) : ✗

---

## 🎯 COMMANDES COMPLÈTES

```
═══════════════════════════════════════════
           CARTHAGE ENGINE v1.1
═══════════════════════════════════════════

CONTRÔLE SIMULATION
  start              Démarre
  pause              Pause
  resume             Reprend
  stop               Arrête
  tick <n>           N ticks
  run <n>            Lance N ticks
  step               1 tick + affichage
  run_live <n>       Mode live auto-refresh

VISUALISATION
  dashboard          Centre de contrôle complet
  status             Statut rapide
  world              État monde
  sectors            Détails secteurs

INSPECTION
  agents             Liste agents
  monsters           Liste monstres
  towers             État tours
  skid               État Skid
  xana               État XANA
  inspect agent <nom> Détails agent
  inspect xana       Analyse XANA
  inspect skid       État Skid détaillé

TIMELINE
  events <n>         N événements
  timeline <n>       Timeline

SYSTÈME
  save <fichier>     Sauvegarde
  load <fichier>     Charge
  help               Aide
  quit               Quitter
```

---

## 🚀 EXEMPLES D'UTILISATION

### Session type

```bash
$ python3 main.py

carthage: dashboard
[Affiche le centre de contrôle complet]

carthage: run 50
✓ Simulation exécutée pendant 50 ticks
[Dashboard affiché automatiquement]

carthage: inspect agent yumi
[Détails de Yumi avec relations]

carthage: inspect xana
[Analyse stratégique XANA complète]

carthage: run_live 30
[Simulation live 30 ticks avec refresh auto]

carthage: quit
Au revoir.
```

---

## ✅ FONCTIONNALITÉS IMPLÉMENTÉES

- ✓ Header avec 5 métriques temps réel
- ✓ Panneau XANA étendu (9 informations)
- ✓ Carte stratégique secteurs (barres colorées)
- ✓ 4 indicateurs avec barres de progression
- ✓ Journal opérationnel (8 événements)
- ✓ Panneau alertes (5 critiques)
- ✓ Commande `inspect agent <nom>`
- ✓ Commande `inspect xana`
- ✓ Commande `inspect skid`
- ✓ Commande `run_live <n>`
- ✓ Aide améliorée et catégorisée
- ✓ Tous les textes en français
- ✓ Interface responsive et lisible
- ✓ Codes couleur cohérents
- ✓ Dashboard structuré (6 zones)

---

## 🎯 OBJECTIFS ATTEINTS

- ✅ Centre de commande professionnel
- ✅ Esthétique superordinateur
- ✅ Compréhension globale < 2 secondes
- ✅ Interface propre et structurée
- ✅ Minimal mais complet
- ✅ Immersif et stratégique
- ✅ Lisibilité maximale
- ✅ Codes couleur efficaces
- ✅ Simulation core intacte
- ✅ Architecture modulaire préservée

---

## 📊 COMPARAISON v1.0 → v1.1

| Fonctionnalité | v1.0 | v1.1 |
|----------------|------|------|
| Panneaux dashboard | 5 | 7 |
| Métriques header | 3 | 5 |
| Barres visuelles | 0 | 4 |
| Commandes inspect | 0 | 3 |
| Mode live | ✗ | ✓ |
| Carte secteurs | ✗ | ✓ |
| Journal opérationnel | ✗ | ✓ |
| Analyse XANA | Basique | Stratégique |
| Indicateurs | Texte | Barres |

---

## 🔧 ARCHITECTURE

### Structure des fichiers
```
carthage_engine/cli/
├── ui/
│   ├── styles.py       # Palette de couleurs
│   ├── panels.py       # 7 panneaux + dashboard
│   └── renderer.py     # Moteur de rendu + inspect + live
├── shell.py            # Shell Rich
└── commands.py         # Handlers + nouvelles commandes
```

### Nouveaux composants
- `create_operational_log()` → Journal
- `create_sectors_strategic_map()` → Carte secteurs
- `create_visual_meters()` → Barres progression
- `create_xana_extended_panel()` → XANA étendu
- `inspect_agent()` → Inspect agent
- `inspect_xana_detailed()` → Inspect XANA
- `inspect_skid_detailed()` → Inspect Skid
- `run_live_simulation()` → Mode live

---

## 🎮 EXPÉRIENCE UTILISATEUR

L'interface transforme le CLI en un **véritable centre de commande stratégique** :

1. **Vision globale immédiate** via le dashboard
2. **Analyse tactique** via la carte des secteurs
3. **Suivi opérationnel** via le journal
4. **Alertes prioritaires** en évidence
5. **Inspection détaillée** sur demande
6. **Simulation live** pour observer l'évolution

L'utilisateur peut **comprendre la situation en < 2 secondes** et **prendre des décisions stratégiques informées**.

---

**CARTHAGE ENGINE v1.1**
Interface CLI Professionnelle - Centre de Commande Stratégique Complet
Version majeure terminée et testée avec succès
