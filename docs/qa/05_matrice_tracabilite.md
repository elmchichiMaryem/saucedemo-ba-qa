# Matrice de traçabilité

Elle relie chaque **user story** à ses **critères d'acceptation**, ses **cas de test**, ses **scénarios automatisés** et ses **anomalies**. Elle permet de répondre à deux questions : *chaque exigence est-elle testée ?* et *quelle exigence est touchée par une anomalie ?*

**Identifiants des critères d'acceptation** : `US-xx-CAn` correspond au n-ième scénario Gherkin de la story dans le [backlog](../ba/03_backlog_user_stories.md).

> **Scénario automatisé** : `fichier › titre du scénario` dans [`features/`](../../features/). Les scénarios du fichier `anomalies_connues.feature` décrivent le comportement attendu et sont marqués **xfail strict** avec la référence de l'anomalie. S'ils se mettent à passer, la suite échoue pour signaler que le bug est corrigé.

## 1. Matrice détaillée

| US | Critère d'acceptation | Cas de test | Statut | Scénario automatisé | Anomalies |
|---|---|---|---|---|---|
| **US-01** Connexion réussie | US-01-CA1 Connexion avec des identifiants valides | CT-01 | OK | `authentification › CT-01` | BUG-16 (`performance_glitch_user`) |
| **US-02** Erreurs de connexion | US-02-CA1 Message d'erreur selon la saisie (6 exemples) | CT-02, CT-03, CT-04, CT-05, CT-06, CT-07 | OK | `authentification › CT-02 à CT-07 (6 exemples)` | — |
| **US-03** Utilisateur bloqué | US-03-CA1 Connexion d'un compte bloqué | CT-08 | OK | `authentification › CT-08` | — |
| **US-04** Déconnexion | US-04-CA1 Déconnexion depuis le menu | CT-09 | OK | `authentification › CT-09` | — |
| | US-04-CA2 Pages protégées inaccessibles après déconnexion | CT-10 | OK | `authentification › CT-10` | — |
| **US-05** Protection des pages | US-05-CA1 Accès direct sans session (3 pages) | CT-10, CT-11, CT-12 | OK | `authentification › CT-10` ; `authentification › CT-11 et CT-12 (2 exemples)` | — |
| **US-06** Affichage du catalogue | US-06-CA1 Le catalogue affiche tous les produits | CT-13 | OK | `catalogue › CT-13` | BUG-04, BUG-14, BUG-15 |
| | US-06-CA2 Prix conformes au référentiel | CT-14 | OK | `catalogue › CT-14` | BUG-13 |
| **US-07** Détail d'un produit | US-07-CA1 Ouvrir la fiche depuis le catalogue | CT-15 | OK | `catalogue › CT-15` | BUG-06 |
| | US-07-CA2 Revenir au catalogue | CT-16 | OK | `catalogue › CT-16` | — |
| **US-08** Tri du catalogue | US-08-CA1 Trier le catalogue (4 options) | CT-17, CT-18, CT-19, CT-20 | OK | `catalogue › CT-17 à CT-19 (3 exemples) + CT-20` | BUG-05, BUG-10, BUG-16 |
| **US-09** Ajout au panier | US-09-CA1 Ajout depuis le catalogue | CT-21 | OK | `panier › CT-21` | BUG-07 |
| | US-09-CA2 Ajout depuis la fiche | CT-22 | OK | `panier › CT-22` | — |
| **US-10** Retrait du panier | US-10-CA1 Retrait depuis le catalogue | CT-23 | OK | `panier › CT-23` | BUG-08 |
| | US-10-CA2 Retrait depuis la page panier | CT-24 | OK | `panier › CT-24` | — |
| **US-11** Badge du panier | US-11-CA1 Le badge reflète le nombre d'articles | CT-21, CT-25 | OK | `panier › CT-21` ; `panier › CT-25` | — |
| **US-12** Consultation du panier | US-12-CA1 Le panier liste les articles | CT-26 | OK | `panier › CT-26` | BUG-15 |
| | US-12-CA2 Continuer ses achats | CT-27 | OK | `panier › CT-27` | — |
| | US-12-CA3 Panier conservé après déconnexion | CT-28 | OK | `panier › CT-28` | — |
| **US-13** Reset App State | US-13-CA1 Reset App State vide le panier | CT-29 | **KO** | `anomalies_connues › CT-29 (xfail BUG-03)` | **BUG-03** |
| **US-14** Informations client | US-14-CA1 Saisie complète | CT-30 | OK | `commande › CT-30` | BUG-09, BUG-11 |
| | US-14-CA2 Champ obligatoire manquant (4 exemples) | CT-31, CT-32, CT-33, CT-34 | OK | `commande › CT-31 à CT-34 (4 exemples)` | BUG-11 |
| | *Exigence implicite* : espaces refusés | CT-35 | **KO** | `anomalies_connues › CT-35 (xfail BUG-02)` | **BUG-02** |
| **US-15** Récapitulatif et totaux | US-15-CA1 Articles, paiement, livraison | CT-36 | OK | `commande › CT-36` | — |
| | US-15-CA2 Calcul des totaux avec une taxe de 8 % (2 exemples) | CT-37, CT-38 | OK | `commande › CT-37 et CT-38 (2 exemples)` | BUG-13 |
| **US-16** Confirmation de commande | US-16-CA1 Valider la commande | CT-39 | OK | `commande › CT-39` | BUG-12 |
| | US-16-CA2 Retour au catalogue | CT-40 | OK | `commande › CT-40` | — |
| | *Exigence implicite* : pas de commande avec un panier vide | CT-43 | **KO** | `anomalies_connues › CT-43 (xfail BUG-01)` | **BUG-01** |
| **US-17** Annulation de commande | US-17-CA1 Annuler à l'étape 1 | CT-41 | OK | `commande › CT-41` | — |
| | US-17-CA2 Annuler à l'étape 2 | CT-42 | OK | `commande › CT-42` | — |

Les anomalies en **gras** ont été détectées par un cas de test avec `standard_user`. Les autres viennent des sessions exploratoires avec les comptes spécifiques ; le cas de test de la ligne est alors OK pour `standard_user`.

## 2. Scénarios automatisés supplémentaires (comptes spécifiques)

Ces scénarios automatisent la vérification des anomalies trouvées en exploratoire. Ils passeront au vert quand les anomalies seront corrigées.

| Scénario (`anomalies_connues.feature`) | Compte | US | Anomalie |
|---|---|---|---|
| Le tri du catalogue fonctionne pour les comptes spécifiques — exemple BUG-05 | problème (`problem_user`) | US-08 | BUG-05 |
| Le tri du catalogue fonctionne pour les comptes spécifiques — exemple BUG-10 | erreur (`error_user`) | US-08 | BUG-10 |
| La fiche ouverte est celle du produit cliqué | problème | US-07 | BUG-06 |
| Tous les produits peuvent être ajoutés au panier (2 exemples) | problème, erreur | US-09 | BUG-07 |
| Les informations client saisies sont conservées | problème | US-14 | BUG-09 |
| La commande peut être validée | erreur | US-16 | BUG-12 |
| Les prix du catalogue sont ceux du référentiel | visuel (`visual_user`) | US-06 | BUG-13 |

## 3. Couverture par user story

| US | Nb CA | CA couverts | Nb CT | CT automatisés | Statut `standard_user` | Anomalies liées |
|---|---|---|---|---|---|---|
| US-01 | 1 | 1 | 1 | 1 | ✅ | 1 |
| US-02 | 1 | 1 | 6 | 6 | ✅ | 0 |
| US-03 | 1 | 1 | 1 | 1 | ✅ | 0 |
| US-04 | 2 | 2 | 2 | 2 | ✅ | 0 |
| US-05 | 1 | 1 | 3 | 3 | ✅ | 0 |
| US-06 | 2 | 2 | 2 | 2 | ✅ | 4 |
| US-07 | 2 | 2 | 2 | 2 | ✅ | 1 |
| US-08 | 1 | 1 | 4 | 4 | ✅ | 3 |
| US-09 | 2 | 2 | 2 | 2 | ✅ | 1 |
| US-10 | 2 | 2 | 2 | 2 | ✅ | 1 |
| US-11 | 1 | 1 | 2 | 2 | ✅ | 0 |
| US-12 | 3 | 3 | 3 | 3 | ✅ | 1 |
| US-13 | 1 | 1 | 1 | 1 | ❌ | 1 |
| US-14 | 2 | 2 | 6 | 6 | ❌ (CT-35) | 3 |
| US-15 | 2 | 2 | 3 | 3 | ✅ | 1 |
| US-16 | 2 | 2 | 3 | 3 | ❌ (CT-43) | 2 |
| US-17 | 2 | 2 | 2 | 2 | ✅ | 0 |
| **Total** | **28** | **28 (100 %)** | **43** | **43 (100 %)** | **14 / 17 US conformes** | **16 distinctes** |

*Un cas de test peut couvrir plusieurs US : CT-10 couvre US-04 et US-05, et CT-21 couvre US-09 et US-11.*

## 4. Matrice inverse : anomalie → exigence

| Anomalie | Sévérité | US | Règle | Détectée par |
|---|---|---|---|---|
| BUG-01 | Majeure | US-16 | RG-16 | CT-43 |
| BUG-02 | Mineure | US-14 | RG-13 | CT-35 |
| BUG-03 | Mineure | US-13 | RG-18 | CT-29 |
| BUG-04 | Majeure | US-06 | RG-07 | Session `problem_user` |
| BUG-05 | Majeure | US-08 | RG-08 | Session `problem_user` |
| BUG-06 | Majeure | US-07 | RG-07 | Session `problem_user` |
| BUG-07 | Majeure | US-09 | RG-09 | Sessions `problem_user`, `error_user` |
| BUG-08 | Majeure | US-10 | RG-09 | Sessions `problem_user`, `error_user` |
| BUG-09 | Bloquante | US-14 | RG-13 | Session `problem_user` |
| BUG-10 | Majeure | US-08 | RG-08 | Session `error_user` |
| BUG-11 | Majeure | US-14 | RG-13 | Session `error_user` |
| BUG-12 | Bloquante | US-16 | RG-16 | Session `error_user` |
| BUG-13 | Majeure | US-06, US-15 | RG-07 | Session `visual_user` |
| BUG-14 | Mineure | US-06 | RG-07 | Session `visual_user` |
| BUG-15 | Mineure | US-06, US-12 | — (ergonomie) | Session `visual_user` |
| BUG-16 | Mineure | US-01, US-08 | — (performance) | Observation `performance_glitch_user` |
