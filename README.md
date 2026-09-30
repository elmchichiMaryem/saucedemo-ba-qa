# SauceDemo — Projet Business Analysis & QA

[![Tests](https://github.com/elmchichiMaryem/saucedemo-ba-qa/actions/workflows/tests.yml/badge.svg)](https://github.com/elmchichiMaryem/saucedemo-ba-qa/actions/workflows/tests.yml)
![Python](https://img.shields.io/badge/Python-3.13-blue)
![Playwright](https://img.shields.io/badge/Playwright-1.63-green)
![pytest-bdd](https://img.shields.io/badge/pytest--bdd-8.1-orange)

Projet portfolio qui couvre **tout le cycle qualité** d'une application e-commerce : de l'analyse du besoin jusqu'aux tests automatisés exécutés en intégration continue. L'application testée est [Swag Labs (saucedemo.com)](https://www.saucedemo.com), la boutique de démonstration de Sauce Labs.

## En bref

| | |
|---|---|
| **17** user stories, 4 epics, **18** règles de gestion | **43** cas de test, **100 %** exécutés, **93 %** de réussite |
| **16** anomalies documentées et reproduites, avec captures | **43 / 43** cas automatisés (51 tests pytest-bdd) |
| **100 %** des critères d'acceptation tracés jusqu'au test | CI GitHub Actions à chaque push, rapport HTML publié |

## Compétences démontrées

| Domaine | Ce qui a été réalisé |
|---|---|
| **Business Analysis** | Note de cadrage (objectifs, périmètre, parties prenantes, risques), analyse du processus *as-is* avec diagramme Mermaid, backlog de user stories INVEST avec critères d'acceptation en Gherkin, priorisation MoSCoW, estimation en story points, DoR / DoD, règles de gestion, glossaire |
| **Test manuel** | Stratégie de test (critères d'entrée et de sortie, classification des anomalies), 43 cas de test conçus avec des techniques formelles (partitions d'équivalence, valeurs limites, transitions d'état), campagne d'exécution, 3 sessions exploratoires à charte, 16 fiches d'anomalie, matrice de traçabilité bidirectionnelle |
| **Automatisation** | BDD avec pytest-bdd et Playwright, Page Object Model, données de test externalisées, tags par epic, anomalies connues en `xfail` strict, capture d'écran automatique en cas d'échec, rapport HTML |
| **CI/CD** | Workflow GitHub Actions (push, pull request, lancement manuel), exécution headless, rapport publié en artefact |

## Démarche

1. **Rien n'est inventé.** Faute de spécification, les règles métier ont été **déduites par observation** du site, puis vérifiées par script avant d'être écrites.
2. **Chaque anomalie est prouvée.** Elle est reproduite par un script Playwright dans un navigateur neuf, comparée au comportement de référence (`standard_user`) et illustrée par une capture.
3. **Tout est traçable.** Chaque user story est reliée à ses critères d'acceptation, ses cas de test, ses scénarios automatisés et ses anomalies ([matrice](docs/qa/05_matrice_tracabilite.md)).
4. **Les bugs connus restent sous surveillance.** Leurs scénarios décrivent le comportement *attendu* et sont marqués `xfail` strict. Le jour où un bug est corrigé, la suite le signale.

## Stack technique

| Outil | Rôle |
|---|---|
| Python 3.13 | Langage |
| [pytest](https://docs.pytest.org/) | Moteur de test |
| [pytest-bdd](https://pytest-bdd.readthedocs.io/) | Scénarios Gherkin exécutables |
| [Playwright](https://playwright.dev/python/) + pytest-playwright | Pilotage du navigateur (Chromium) |
| pytest-html | Rapport HTML autonome avec captures |
| GitHub Actions | Intégration continue |
| Markdown + Mermaid | Documentation versionnée et diagrammes |

## Structure du projet

```
saucedemo-ba-qa/
├── docs/
│   ├── ba/                     # Analyse métier
│   └── qa/                     # Recette : stratégie, cas, campagne, anomalies, traçabilité, bilan
│       └── captures/           # Preuves des anomalies
├── features/                   # Scénarios Gherkin (un fichier par epic + anomalies connues)
├── pages/                      # Page Object Model (une classe par page)
├── tests/step_defs/            # Step definitions pytest-bdd, par domaine
├── data/test_data.json         # Données de test (comptes, messages, produits, prix…)
├── conftest.py                 # Fixtures, xfail des anomalies, captures en cas d'échec
├── pytest.ini                  # Configuration pytest (URL, tags, rapport)
├── requirements.txt            # Dépendances aux versions figées
└── .github/workflows/tests.yml # Pipeline d'intégration continue
```

## Installation

Prérequis : Python 3.13 et Git.

```bash
git clone https://github.com/elmchichiMaryem/saucedemo-ba-qa.git
cd saucedemo-ba-qa

python3 -m venv venv
source venv/bin/activate          # Windows : venv\Scripts\activate

pip install -r requirements.txt
playwright install chromium
```

## Lancer les tests

| Objectif | Commande |
|---|---|
| Toute la suite | `pytest` |
| Tests smoke (parcours critique, ~5 s) | `pytest -m smoke` |
| Epic Authentification | `pytest -m authentification` |
| Epic Catalogue | `pytest -m catalogue` |
| Epic Panier | `pytest -m panier` |
| Epic Commande | `pytest -m commande` |
| Non-régression sans les anomalies connues | `pytest -m "regression and not anomalies"` |
| Uniquement les anomalies connues (xfail) | `pytest -m anomalies` |
| Voir le navigateur pendant l'exécution | `pytest -m smoke --headed --slowmo 500` |

Le rapport est généré dans `reports/rapport_tests.html`, et les captures des échecs dans `reports/captures/`. En CI, le rapport se télécharge depuis l'onglet **Actions** (artefact `rapport-tests`).

**Résultat attendu** : `40 passed, 11 xfailed`. Les 11 `xfailed` sont les anomalies connues ([BUG-xx](docs/qa/04_rapports_anomalies.md)) : ils échouent volontairement tant que le site n'est pas corrigé.

## Documentation

### Analyse métier

| Document | Contenu |
|---|---|
| [01 — Note de cadrage](docs/ba/01_note_de_cadrage.md) | Contexte, objectifs, périmètre, parties prenantes, hypothèses, contraintes, risques |
| [02 — Analyse des processus](docs/ba/02_analyse_processus.md) | Parcours d'achat (diagramme Mermaid), étapes, flux alternatifs, points d'attention |
| [03 — Backlog et user stories](docs/ba/03_backlog_user_stories.md) | 4 epics, 17 US, critères d'acceptation en Gherkin, MoSCoW, story points, DoR / DoD |
| [04 — Règles de gestion](docs/ba/04_regles_de_gestion.md) | RG-01 à RG-18, reliées aux US |
| [05 — Glossaire](docs/ba/05_glossaire.md) | Termes métier, BA et QA |

### Qualité et tests

| Document | Contenu |
|---|---|
| [01 — Stratégie de test](docs/qa/01_strategie_de_test.md) | Objectifs, types et techniques de test, environnement, critères d'entrée et de sortie |
| [02 — Cas de test](docs/qa/02_cas_de_test.md) | CT-01 à CT-43 |
| [03 — Campagne d'exécution](docs/qa/03_campagne_execution.md) | Résultats par cas, sessions exploratoires |
| [04 — Rapports d'anomalies](docs/qa/04_rapports_anomalies.md) | BUG-01 à BUG-16, avec étapes de reproduction et captures |
| [05 — Matrice de traçabilité](docs/qa/05_matrice_tracabilite.md) | US ↔ critères ↔ cas ↔ scénarios automatisés ↔ anomalies |
| [06 — Bilan de test](docs/qa/06_bilan_de_test.md) | Indicateurs, couverture, critères de sortie, recommandations |

## Choix techniques

- **Sélecteurs `data-test`** : l'application fournit des attributs dédiés aux tests, plus stables que le CSS ou le texte. `get_by_test_id` est configuré pour les utiliser.
- **Attente d'éléments, jamais de pause fixe** : Swag Labs est une application React à page unique, où l'URL change avant l'affichage. Chaque Page Object attend donc un élément caractéristique de sa page, et les assertions `expect` de Playwright réessayent automatiquement.
- **Gherkin métier, données à part** : les scénarios parlent en termes métier (`le compte "bloqué"`), et les valeurs réelles sont dans `data/test_data.json`. Aucune donnée n'est écrite dans le code des tests.
- **Oracle de calcul** : les totaux de commande sont recalculés indépendamment (taxe de 8 %, arrondi au centime) au lieu d'être recopiés.
- **Isolation** : chaque test utilise un contexte navigateur neuf, sans session ni panier hérités.

## Auteure

**Maryem Elmchichi** — [github.com/elmchichiMaryem](https://github.com/elmchichiMaryem)
