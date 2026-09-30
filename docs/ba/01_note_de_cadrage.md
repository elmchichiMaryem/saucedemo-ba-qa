# Note de cadrage — Parcours d'achat Swag Labs

| Élément | Valeur |
|---|---|
| Projet | Analyse métier et recette du parcours d'achat Swag Labs |
| Application | Swag Labs — <https://www.saucedemo.com> |
| Rédactrice | Maryem Elmchichi (Business Analyst / QA) |
| Version | 1.0 |
| Statut | Validé pour la phase de conception des tests |

---

## 1. Contexte

Swag Labs est une boutique en ligne de démonstration éditée par Sauce Labs. Elle vend des articles de marque (sac à dos, t-shirts, veste, etc.) à des utilisateurs authentifiés.

Dans ce projet, on la traite **comme une vraie application e-commerce en recette**. L'équipe métier veut s'assurer que le parcours d'achat fonctionne de bout en bout avant une mise en production fictive, et disposer d'un filet de non-régression automatisé.

> Le contexte organisationnel (sponsor, équipe, mise en production) est **simulé** pour les besoins du portfolio. Les fonctionnalités décrites, elles, sont **réelles** : chacune a été observée sur le site en septembre 2026.

## 2. Problématique

- Aucune documentation fonctionnelle n'est disponible : les règles métier doivent être **déduites par observation** de l'application (rétro-ingénierie fonctionnelle).
- Plusieurs comptes de test ont des comportements différents (compte bloqué, compte « à problèmes », compte lent…). On ne sait pas précisément quels écarts ils provoquent.
- Les tests manuels répétés à chaque livraison coûtent cher et ne sont pas fiables.

## 3. Objectifs métier

| # | Objectif | Indicateur de succès |
|---|---|---|
| OBJ-1 | Formaliser le besoin du parcours d'achat | Backlog de user stories avec critères d'acceptation validés, règles de gestion numérotées |
| OBJ-2 | Garantir qu'un client peut acheter de bout en bout | 100 % des cas de test du parcours nominal (priorité haute) exécutés et passants avec `standard_user` |
| OBJ-3 | Identifier et documenter les anomalies | Chaque anomalie reproduite, qualifiée (sévérité / priorité) et tracée vers une US |
| OBJ-4 | Réduire le coût de la non-régression | Suite automatisée exécutée à chaque push via l'intégration continue |

## 4. Périmètre

### 4.1 Inclus

| Domaine (Epic) | Fonctionnalités |
|---|---|
| Authentification | Connexion, messages d'erreur, compte bloqué, déconnexion, protection des pages sans session |
| Catalogue | Liste des 6 produits, fiche détail produit, tri (4 options) |
| Panier | Ajout / retrait (depuis le catalogue, la fiche produit et le panier), badge compteur, consultation du panier, réinitialisation de l'état (« Reset App State ») |
| Commande | Formulaire d'informations (champs obligatoires), récapitulatif avec calcul des totaux, confirmation, annulation |

Comptes utilisés : `standard_user`, `locked_out_user`, `problem_user`, `performance_glitch_user`, `error_user`, `visual_user` (mot de passe commun `secret_sauce`).

Navigateur de référence : Chromium (piloté par Playwright), résolution bureau.

### 4.2 Exclu

| Élément exclu | Justification |
|---|---|
| Menu « Dynamic Catalog » (pages Lazy Load, Spinner, Slider) | Vitrines de démonstration du chargement asynchrone : elles n'ont **pas de bouton d'ajout au panier** et ne font donc pas partie du parcours d'achat |
| Lien « About » et liens réseaux sociaux (X, Facebook, LinkedIn) | Redirigent vers des sites externes à Sauce Labs, hors application |
| Paiement réel | Le moyen de paiement (« SauceCard #31337 ») et la livraison (« Free Pony Express Delivery! ») sont affichés en dur : il n'y a aucun paiement à saisir |
| Tests de performance / charge, sécurité, accessibilité | Hors objectifs de cette recette (le comportement de `performance_glitch_user` est seulement observé) |
| Navigateurs mobiles, Firefox, WebKit | Un seul navigateur de référence pour limiter l'effort |
| API / base de données | Aucun accès : application testée en boîte noire, par l'interface |

## 5. Parties prenantes

| Rôle | Acteur | Responsabilités | Intérêt / influence |
|---|---|---|---|
| Sponsor (simulé) | Direction e-commerce | Valide les objectifs et le go / no-go | Fort / Fort |
| Product Owner (simulé) | Responsable produit | Priorise le backlog, valide les critères d'acceptation | Fort / Fort |
| Business Analyst & QA | Maryem Elmchichi | Analyse, rédaction des US et RG, stratégie de test, exécution, automatisation, reporting | Fort / Moyen |
| Équipe de développement | Sauce Labs (externe) | Corrige les anomalies — hors de notre contrôle | Moyen / Fort |
| Clients finaux | Acheteurs Swag Labs | Utilisent le parcours d'achat | Fort / Faible |

## 6. Hypothèses

- H1 : l'application publique <https://www.saucedemo.com> représente la version « candidate » à recetter.
- H2 : les 6 comptes fournis et le mot de passe `secret_sauce` restent valides pendant le projet.
- H3 : `standard_user` est le compte de référence et doit avoir un comportement **conforme**. Les écarts constatés avec les autres comptes sont des anomalies à documenter.
- H4 : les libellés de l'interface sont en anglais. Ils sont cités **tels quels** dans la documentation (en français).
- H5 : le catalogue (6 produits, prix en dollars) est stable.

## 7. Contraintes

- C1 : **boîte noire** — pas d'accès au code source, aux logs ni à la base de données.
- C2 : site public hébergé par un tiers. Il peut être modifié ou indisponible sans préavis.
- C3 : l'application ne conserve rien côté serveur. Le panier est stocké dans le navigateur (`localStorage`) et la session dans un cookie.
- C4 : outillage open source uniquement (Python, pytest-bdd, Playwright, GitHub Actions).
- C5 : une seule personne pour l'analyse, les tests et l'automatisation.

## 8. Risques

| ID | Risque | Probabilité | Impact | Réponse |
|---|---|---|---|---|
| R1 | Le site évolue (nouveaux éléments, sélecteurs modifiés) et casse les tests automatisés | Moyenne | Élevé | Sélecteurs `data-test`, Page Object Model pour centraliser les changements |
| R2 | Indisponibilité ou lenteur du site pendant l'exécution (CI) | Faible | Moyen | Attentes explicites sur les éléments, relance possible du workflow |
| R3 | Tests instables (« flaky ») : l'application React met à jour l'URL avant d'afficher la page | Élevée | Moyen | Attendre un élément caractéristique de la page, jamais une durée fixe |
| R4 | Confondre un comportement volontaire du site de démo avec une anomalie | Moyenne | Moyen | Comparer systématiquement avec `standard_user` (référence) et vérifier chaque anomalie par script avant de la documenter |
| R5 | Règles métier mal déduites faute de spécifications | Moyenne | Élevé | Chaque règle est issue d'une observation reproductible et tracée dans la matrice |

## 9. Livrables

| Phase | Livrables |
|---|---|
| Analyse métier | Note de cadrage, analyse des processus, backlog (US + critères d'acceptation), règles de gestion, glossaire |
| Test manuel | Stratégie de test, cas de test, campagne d'exécution, rapports d'anomalies, matrice de traçabilité |
| Automatisation | Suite pytest-bdd + Playwright (Page Object Model), rapport HTML |
| Intégration continue | Workflow GitHub Actions |
| Clôture | Bilan de test, README |
