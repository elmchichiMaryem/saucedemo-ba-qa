# Campagne d'exécution — Recette n° 1

| Élément | Valeur |
|---|---|
| Date d'exécution | 30/09/2026 |
| Testeuse | Maryem Elmchichi |
| Version testée | <https://www.saucedemo.com> (production publique, septembre 2026) |
| Environnement | Chromium 153.0.8010.12 (Playwright 1.63.0), 1280 × 800, macOS |
| Référentiel | [Cas de test CT-01 à CT-43](02_cas_de_test.md) |

## 1. Mode opératoire

1. **Campagne scriptée** : les 43 cas de test ont été exécutés avec `standard_user`. L'exécution est **assistée par Playwright** : un script rejoue les étapes de chaque cas et compare le résultat obtenu au résultat attendu. Chaque cas démarre dans un **contexte navigateur neuf**, donc avec un panier vide et sans session. Les cas KO ont ensuite été rejoués un par un, captures d'écran à l'appui.
2. **Sessions exploratoires** : une session par compte spécifique, guidée par une charte. Chaque session parcourt le même chemin que `standard_user` (connexion, catalogue, tri, fiche, panier, commande, déconnexion) et compare chaque résultat à la référence.

Statuts : **OK** = résultat conforme · **KO** = écart constaté, anomalie ouverte · **Bloqué** = le cas n'a pas pu être exécuté.

## 2. Résultats de la campagne scriptée (`standard_user`)

| ID | Titre | Statut | Résultat obtenu | Anomalie |
|---|---|---|---|---|
| CT-01 | Connexion avec des identifiants valides | OK | Page `/inventory.html`, titre « Products » | |
| CT-02 | Connexion avec les deux champs vides | OK | « Epic sadface: Username is required » | |
| CT-03 | Connexion sans identifiant | OK | « Epic sadface: Username is required » | |
| CT-04 | Connexion sans mot de passe | OK | « Epic sadface: Password is required » | |
| CT-05 | Mot de passe incorrect | OK | « Epic sadface: Username and password do not match any user in this service » | |
| CT-06 | Identifiant inconnu | OK | Même message que CT-05 | |
| CT-07 | Sensibilité à la casse | OK | Même message que CT-05 | |
| CT-08 | Compte bloqué | OK | « Epic sadface: Sorry, this user has been locked out. » | |
| CT-09 | Déconnexion depuis le menu | OK | Page de connexion affichée | |
| CT-10 | Accès au catalogue après déconnexion | OK | Retour à la connexion, « You can only access '/inventory.html' when you are logged in. » | |
| CT-11 | Accès direct au panier sans session | OK | Retour à la connexion, message attendu | |
| CT-12 | Accès direct au formulaire sans session | OK | Retour à la connexion, message attendu | |
| CT-13 | Affichage complet du catalogue | OK | 6 produits complets, tri par défaut « Name (A to Z) » | |
| CT-14 | Prix conformes au référentiel | OK | 6 prix conformes | |
| CT-15 | Fiche produit cohérente | OK | Fiche « Sauce Labs Backpack », $29.99, identique au catalogue | |
| CT-16 | Retour au catalogue depuis la fiche | OK | `/inventory.html` | |
| CT-17 | Tri Z → A | OK | Ordre respecté, premier : Test.allTheThings() T-Shirt (Red) | |
| CT-18 | Tri prix croissant | OK | Ordre respecté, premier : Sauce Labs Onesie | |
| CT-19 | Tri prix décroissant | OK | Ordre respecté, premier : Sauce Labs Fleece Jacket | |
| CT-20 | Retour au tri A → Z | OK | Premier : Sauce Labs Backpack | |
| CT-21 | Ajout depuis le catalogue | OK | Bouton « Remove », badge « 1 » | |
| CT-22 | Ajout depuis la fiche produit | OK | Bouton « Remove », badge « 1 », état cohérent au catalogue | |
| CT-23 | Retrait depuis le catalogue | OK | Bouton « Add to cart », badge masqué | |
| CT-24 | Retrait depuis la page panier | OK | 1 article restant, badge « 1 » | |
| CT-25 | Évolution du badge | OK | Absent → 3 → 2 | |
| CT-26 | Contenu de la page panier | OK | Backpack $29.99 ×1, Bike Light $9.99 ×1 | |
| CT-27 | Continuer ses achats | OK | Catalogue, badge « 1 » | |
| CT-28 | Panier conservé après reconnexion | OK | Badge « 1 » après reconnexion | |
| CT-29 | Reset App State | **KO** | Badge masqué, mais **2 boutons restent sur « Remove »** | [BUG-03](04_rapports_anomalies.md#bug-03) |
| CT-30 | Saisie complète des informations | OK | « Checkout: Overview » | |
| CT-31 | Formulaire vide | OK | « Error: First Name is required » | |
| CT-32 | Prénom manquant | OK | « Error: First Name is required » | |
| CT-33 | Nom manquant | OK | « Error: Last Name is required » | |
| CT-34 | Code postal manquant | OK | « Error: Postal Code is required » | |
| CT-35 | Champs contenant uniquement des espaces | **KO** | Saisie **acceptée**, passage à « Checkout: Overview » sans message | [BUG-02](04_rapports_anomalies.md#bug-02) |
| CT-36 | Contenu du récapitulatif | OK | 2 articles, « SauceCard #31337 », « Free Pony Express Delivery! » | |
| CT-37 | Totaux pour 2 articles | OK | Item total: $39.98 / Tax: $3.20 / Total: $43.18 | |
| CT-38 | Totaux pour 3 articles | OK | Item total: $87.97 / Tax: $7.04 / Total: $95.01 | |
| CT-39 | Validation de la commande | OK | « Checkout: Complete! », « Thank you for your order! », badge masqué | |
| CT-40 | Retour après la commande | OK | `/inventory.html` | |
| CT-41 | Annulation à l'étape 1 | OK | Page panier, 1 article | |
| CT-42 | Annulation à l'étape 2 | OK | Catalogue, badge « 1 » | |
| CT-43 | Commande impossible avec un panier vide | **KO** | « Checkout » **ouvre le formulaire**, et la commande va jusqu'à « Thank you for your order! » avec un total de $0.00 | [BUG-01](04_rapports_anomalies.md#bug-01) |

### Synthèse

| Indicateur | Valeur |
|---|---|
| Cas prévus | 43 |
| Cas exécutés | 43 (100 %) |
| OK | 40 (93,0 %) |
| KO | 3 (7,0 %) |
| Bloqués | 0 |
| Cas de priorité Haute exécutés / OK | 24 / 24 |
| Cas smoke OK | 9 / 9 |

| Epic | Exécutés | OK | KO |
|---|---|---|---|
| EP-01 Authentification | 12 | 12 | 0 |
| EP-02 Catalogue | 8 | 8 | 0 |
| EP-03 Panier | 9 | 8 | 1 |
| EP-04 Commande | 14 | 12 | 2 |

Le **parcours nominal** de `standard_user` est entièrement conforme. Les 3 KO portent sur des cas limites (priorité Moyenne ou Basse) : aucun n'empêche un client d'acheter.

---

## 3. Sessions exploratoires

Chaque session suit une **charte** : une mission, un compte, des zones à explorer. La même exploration a d'abord été faite avec `standard_user` pour servir d'oracle.

### Session 1 — `problem_user`

| Élément | Contenu |
|---|---|
| Charte | Explorer le parcours d'achat complet avec `problem_user` pour découvrir les écarts de comportement par rapport à `standard_user` |
| Zones | Catalogue (images, tri, liens), panier (ajout / retrait), formulaire de commande |
| Constats | 6 anomalies |

| # | Observation | Anomalie |
|---|---|---|
| 1 | Les 6 produits affichent la **même image** (un chien, fichier `sl-404`) à la place de la photo du produit | [BUG-04](04_rapports_anomalies.md#bug-04) |
| 2 | Le tri est **sans effet** : quelle que soit l'option choisie, la liste reste dans l'ordre A → Z et le sélecteur revient à « Name (A to Z) » | [BUG-05](04_rapports_anomalies.md#bug-05) |
| 3 | Cliquer sur un produit ouvre la fiche **d'un autre produit** (Backpack → Fleece Jacket) ; le Fleece Jacket mène à une fiche « ITEM NOT FOUND » | [BUG-06](04_rapports_anomalies.md#bug-06) |
| 4 | « Add to cart » est **sans effet** pour Bolt T-Shirt, Fleece Jacket et Test.allTheThings() T-Shirt (Red) | [BUG-07](04_rapports_anomalies.md#bug-07) |
| 5 | « Remove » est **sans effet** sur le catalogue (le retrait fonctionne depuis la page panier) | [BUG-08](04_rapports_anomalies.md#bug-08) |
| 6 | Saisir le nom **écrase le prénom** ; le champ nom reste vide, et la commande est donc impossible | [BUG-09](04_rapports_anomalies.md#bug-09) |
| — | Non reproduit : l'ajout depuis la fiche produit (id 4) et le retrait depuis la page panier fonctionnent | — |

### Session 2 — `error_user`

| Élément | Contenu |
|---|---|
| Charte | Explorer le parcours d'achat avec `error_user` en surveillant les messages d'erreur, les alertes navigateur et la console JavaScript |
| Zones | Tri, panier, formulaire, validation de la commande |
| Constats | 5 anomalies (dont 2 partagées avec `problem_user`) |

| # | Observation | Anomalie |
|---|---|---|
| 1 | Chaque changement de tri déclenche une alerte « Sorting is broken! This error has been reported to Backtrace. » ; la liste n'est pas triée | [BUG-10](04_rapports_anomalies.md#bug-10) |
| 2 | « Add to cart » est sans effet pour les 3 mêmes produits que `problem_user`. La console JavaScript affiche pendant la session des erreurs « This component failed to render! », absentes avec `standard_user` | [BUG-07](04_rapports_anomalies.md#bug-07) |
| 3 | « Remove » est sans effet sur le catalogue | [BUG-08](04_rapports_anomalies.md#bug-08) |
| 4 | Le champ « Last Name » **n'accepte aucune saisie**, et le formulaire est **pourtant validé** avec un nom vide | [BUG-11](04_rapports_anomalies.md#bug-11) |
| 5 | « Finish » est **sans effet** : on reste sur « Checkout: Overview », sans confirmation, et le panier n'est pas vidé | [BUG-12](04_rapports_anomalies.md#bug-12) |

### Session 3 — `visual_user`

| Élément | Contenu |
|---|---|
| Charte | Comparer visuellement (captures d'écran) chaque page de `visual_user` avec celles de `standard_user` |
| Zones | En-tête, catalogue, panier, formulaire, récapitulatif |
| Constats | 3 anomalies |

| # | Observation | Anomalie |
|---|---|---|
| 1 | Les **prix du catalogue sont faux** et **changent à chaque chargement** (Backpack : $68.46, $47.78, $47.55…), alors que le panier et la fiche affichent le bon prix ($29.99) | [BUG-13](04_rapports_anomalies.md#bug-13) |
| 2 | Le Backpack affiche l'image d'un chien au lieu du sac à dos (catalogue uniquement) | [BUG-14](04_rapports_anomalies.md#bug-14) |
| 3 | Mise en page décalée : icône du panier déplacée sous l'en-tête, bouton « Checkout » collé en haut à droite de l'écran, noms de produits et bouton « Add to cart » désalignés | [BUG-15](04_rapports_anomalies.md#bug-15) |
| — | Non reproduit : formulaire de commande et récapitulatif conformes (totaux corrects) | — |

### Observation complémentaire — `performance_glitch_user`

Les temps de réponse ont été mesurés 3 fois, sans objectif de performance formel (hors périmètre) :

| Action | `standard_user` | `performance_glitch_user` |
|---|---|---|
| Connexion → catalogue affiché | 0,06 à 0,09 s | **5,09 à 5,11 s** |
| Changement de tri | 0,01 s | **5,01 s** |
| Ouverture d'une fiche produit | 0,05 s | 0,06 s |

→ [BUG-16](04_rapports_anomalies.md#bug-16)

## 4. Bilan de la campagne

| Source | Anomalies |
|---|---|
| Campagne scriptée (`standard_user`) | 3 (BUG-01, BUG-02, BUG-03) |
| Session `problem_user` | 6 (BUG-04 à BUG-09) |
| Session `error_user` | 3 nouvelles (BUG-10 à BUG-12) + 2 partagées (BUG-07, BUG-08) |
| Session `visual_user` | 3 (BUG-13 à BUG-15) |
| `performance_glitch_user` | 1 (BUG-16) |
| **Total** | **16 anomalies distinctes** |

Détail des fiches : [04_rapports_anomalies.md](04_rapports_anomalies.md).
