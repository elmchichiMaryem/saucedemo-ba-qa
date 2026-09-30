# Stratégie de test — Parcours d'achat Swag Labs

| Élément | Valeur |
|---|---|
| Application | Swag Labs — <https://www.saucedemo.com> |
| Référentiel d'exigences | [Backlog US-01 à US-17](../ba/03_backlog_user_stories.md), [règles RG-01 à RG-18](../ba/04_regles_de_gestion.md) |
| Rédactrice | Maryem Elmchichi (QA) |
| Version | 1.0 |

## 1. Objectifs

1. Vérifier que chaque user story respecte ses critères d'acceptation et les règles de gestion associées.
2. Garantir qu'un client standard (`standard_user`) peut acheter de bout en bout sans anomalie bloquante.
3. Détecter et documenter les écarts de comportement des comptes de test spécifiques (`problem_user`, `error_user`, `visual_user`, `performance_glitch_user`).
4. Constituer une base de non-régression automatisée, exécutée à chaque modification du code.

## 2. Périmètre

| Inclus | Exclu |
|---|---|
| EP-01 Authentification (US-01 à US-05) | Menu « Dynamic Catalog » (pages sans ajout au panier) |
| EP-02 Catalogue (US-06 à US-08) | Liens externes (About, réseaux sociaux) |
| EP-03 Panier (US-09 à US-13) | Tests de charge, sécurité, accessibilité |
| EP-04 Commande (US-14 à US-17) | Navigateurs autres que Chromium, affichage mobile |

Le détail et les justifications figurent dans la [note de cadrage](../ba/01_note_de_cadrage.md#4-périmètre).

## 3. Approche et types de tests

| Type | Objectif | Moment | Moyen |
|---|---|---|---|
| **Smoke** | Vérifier en quelques minutes que le parcours critique fonctionne (connexion → ajout → commande) | À chaque livraison, avant toute autre campagne ; à chaque push en CI | Sous-ensemble des cas marqués « Smoke » (tag `@smoke`) |
| **Fonctionnel** | Vérifier chaque critère d'acceptation, en cas positifs et négatifs | Campagne de recette | 43 cas de test, techniques ci-dessous |
| **Non-régression** | S'assurer qu'une évolution ne casse pas l'existant | À chaque push / pull request | Suite pytest-bdd complète (tag `@regression`) en intégration continue |
| **Exploratoire** | Trouver les défauts non prévus par les cas écrits, surtout sur les comptes spécifiques | Après la campagne fonctionnelle | Sessions à charte (une par compte), comparées à `standard_user` |

### Techniques de conception utilisées

| Technique | Application |
|---|---|
| **Partitions d'équivalence** | Identifiants : valide / invalide / vide / bloqué ; champs du formulaire : renseigné / vide |
| **Test de toutes les options** | Les 4 options de tri, les 3 champs obligatoires, les 2 boutons Cancel |
| **Tables de décision** | Ordre de contrôle des champs (l'identifiant avant le mot de passe ; le prénom avant le nom et le code postal) |
| **Valeurs limites** | Panier vide (0 article), badge de 0 à 3 articles, champs contenant uniquement des espaces |
| **Test de transitions d'état** | Bouton Add to cart ↔ Remove ; session ouverte → fermée → pages protégées |
| **Oracle de calcul** | Les totaux sont recalculés indépendamment (somme + 8 %, arrondi au centime) et comparés à l'affichage |

## 4. Comptes de test et usage

| Compte | Usage dans la campagne |
|---|---|
| `standard_user` | **Référence** : exécution de tous les cas de test |
| `locked_out_user` | Cas négatif de connexion (US-03) |
| `problem_user` | Session exploratoire n° 1 |
| `error_user` | Session exploratoire n° 2 |
| `visual_user` | Session exploratoire n° 3 (contrôle visuel par captures) |
| `performance_glitch_user` | Observation des temps de réponse (hors objectif de performance) |

Mot de passe commun : `secret_sauce`. Les données de test (produits, prix, saisies du formulaire) sont centralisées dans `data/test_data.json` pour l'automatisation.

## 5. Environnement de test

| Composant | Valeur |
|---|---|
| Application | <https://www.saucedemo.com> (production publique, version de septembre 2026) |
| Navigateur | Chromium 153.0.8010.12, via Playwright 1.63.0 |
| Résolution | 1280 × 800 (bureau) |
| Poste local | macOS (Darwin 24.6), Python 3.13 |
| Intégration continue | GitHub Actions, runner Ubuntu, mode headless |

## 6. Critères d'entrée

- Le site est accessible, et la connexion avec `standard_user` fonctionne (test smoke passant).
- Les user stories à tester respectent la Definition of Ready.
- Les cas de test sont rédigés et relus, et les données de test sont disponibles.
- L'environnement (Python, Playwright, Chromium) est installé.

## 7. Critères de sortie

| Critère | Seuil |
|---|---|
| Cas de test de priorité **Haute** exécutés | 100 % |
| Ensemble des cas de test exécutés | ≥ 95 % |
| Anomalie **bloquante** ouverte sur le parcours de `standard_user` | 0 |
| Anomalies découvertes documentées et tracées vers une US | 100 % |
| Couverture des US par au moins un cas de test | 100 % |
| Suite automatisée passante en CI (hors `xfail` liés à un bug connu) | 100 % |

## 8. Classification des anomalies

| Sévérité | Définition |
|---|---|
| **Bloquante** | Empêche de terminer un processus métier (connexion, commande) et aucun contournement n'existe |
| **Majeure** | Fonction importante incorrecte, résultat erroné ou impact financier / de confiance. Un contournement peut exister |
| **Mineure** | Gêne limitée ; la fonction principale reste utilisable |
| **Cosmétique** | Défaut purement visuel, sans impact fonctionnel |

| Priorité | Définition |
|---|---|
| **P1** | À corriger immédiatement, bloque la mise en production |
| **P2** | À corriger avant la mise en production |
| **P3** | Peut être planifiée dans une version ultérieure |

La sévérité mesure l'**impact technique**, la priorité l'**urgence métier**. Les deux sont évaluées séparément.

## 9. Risques liés aux tests

| Risque | Mesure |
|---|---|
| Le site public change sans préavis | Sélecteurs `data-test`, Page Object Model, exécution régulière en CI pour détecter tôt les changements |
| Tests instables : React met à jour l'URL avant d'afficher la page | Attente explicite d'un élément propre à chaque page, jamais de pause fixe dans la suite automatisée |
| Confusion entre un comportement volontaire du site de démo et une anomalie | `standard_user` sert de référence ; chaque écart est reproduit par script avant d'être documenté |
| Panier conservé dans le `localStorage` d'un test à l'autre | Nouveau contexte navigateur pour chaque test (isolation) |

## 10. Outils

| Besoin | Outil |
|---|---|
| Gestion des exigences et des cas de test | Markdown versionné dans Git (ce dépôt) |
| Exécution assistée et captures d'écran | Playwright (Python) |
| Automatisation BDD | pytest + pytest-bdd + pytest-playwright |
| Rapport d'exécution | pytest-html |
| Intégration continue | GitHub Actions |
| Diagrammes | Mermaid |

## 11. Livrables de test

[Cas de test](02_cas_de_test.md) · [Campagne d'exécution](03_campagne_execution.md) · [Rapports d'anomalies](04_rapports_anomalies.md) · [Matrice de traçabilité](05_matrice_tracabilite.md) · Bilan de test (phase 5)
