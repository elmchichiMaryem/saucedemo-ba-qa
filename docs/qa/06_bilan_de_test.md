# Bilan de test — Recette du parcours d'achat Swag Labs

| Élément | Valeur |
|---|---|
| Application | Swag Labs — <https://www.saucedemo.com> (version de septembre 2026) |
| Période | 30/09/2026 |
| Rédactrice | Maryem Elmchichi |
| Documents de référence | [Stratégie](01_strategie_de_test.md) · [Cas de test](02_cas_de_test.md) · [Campagne](03_campagne_execution.md) · [Anomalies](04_rapports_anomalies.md) · [Traçabilité](05_matrice_tracabilite.md) |

## 1. Synthèse

> Le **parcours d'achat nominal est conforme** pour un client standard : les 24 cas de priorité Haute et les 9 cas smoke passent, et aucune anomalie bloquante n'a été trouvée avec `standard_user`.
> La recette révèle cependant **16 anomalies**, dont **2 bloquantes** et **9 majeures**, presque toutes liées aux comptes spécifiques. Pour `standard_user`, 3 anomalies portent sur des cas limites (panier vide, champs remplis d'espaces, Reset App State).
> Les 43 cas de test sont **automatisés** et exécutés à chaque push par l'intégration continue.

**Recommandation : GO conditionnel** pour le parcours standard, sous réserve de corriger BUG-01 (commande vide confirmée) avant la mise en production. Les anomalies des comptes spécifiques sont à corriger dans l'ordre de priorité P1 → P3 (voir § 7).

## 2. Exécution des tests manuels

| Indicateur | Valeur |
|---|---|
| Cas de test conçus | 43 (27 positifs, 16 négatifs) |
| Cas exécutés | **43 / 43 (100 %)** |
| OK | **40 (93,0 %)** |
| KO | 3 (7,0 %) — CT-29, CT-35, CT-43 |
| Bloqués | 0 |
| Priorité Haute | 24 / 24 OK (100 %) |
| Smoke | 9 / 9 OK (100 %) |

| Epic | Exécutés | OK | KO | Taux de réussite |
|---|---|---|---|---|
| EP-01 Authentification | 12 | 12 | 0 | 100 % |
| EP-02 Catalogue | 8 | 8 | 0 | 100 % |
| EP-03 Panier | 9 | 8 | 1 | 88,9 % |
| EP-04 Commande | 14 | 12 | 2 | 85,7 % |
| **Total** | **43** | **40** | **3** | **93,0 %** |

**Tests exploratoires** : 3 sessions à charte (`problem_user`, `error_user`, `visual_user`) et 1 série de mesures des temps de réponse (`performance_glitch_user`). Elles ont produit 13 des 16 anomalies.

## 3. Anomalies

### Par sévérité

| Sévérité | Nombre | Anomalies |
|---|---|---|
| Bloquante | 2 | BUG-09, BUG-12 |
| Majeure | 9 | BUG-01, BUG-04, BUG-05, BUG-06, BUG-07, BUG-08, BUG-10, BUG-11, BUG-13 |
| Mineure | 5 | BUG-02, BUG-03, BUG-14, BUG-15, BUG-16 |
| Cosmétique | 0 | — |
| **Total** | **16** | 16 ouvertes, 0 corrigée |

### Par priorité

| Priorité | Nombre | Anomalies |
|---|---|---|
| P1 | 6 | BUG-06, BUG-07, BUG-09, BUG-11, BUG-12, BUG-13 |
| P2 | 5 | BUG-01, BUG-04, BUG-05, BUG-08, BUG-10 |
| P3 | 5 | BUG-02, BUG-03, BUG-14, BUG-15, BUG-16 |

### Par compte et par epic

| Compte | Anomalies |
|---|---|
| `standard_user` | 3 (BUG-01, BUG-02, BUG-03) |
| `problem_user` | 6 (BUG-04 à BUG-09 ; BUG-07 et BUG-08 en commun avec `error_user`) |
| `error_user` | 5 (BUG-07, BUG-08, BUG-10, BUG-11, BUG-12) |
| `visual_user` | 3 (BUG-13, BUG-14, BUG-15) |
| `performance_glitch_user` | 1 (BUG-16) |
| `locked_out_user` | 0 (comportement conforme) |

| Epic | Anomalies | Remarque |
|---|---|---|
| EP-01 Authentification | 1 | Uniquement une lenteur (BUG-16) : la sécurité d'accès est conforme |
| EP-02 Catalogue | 7 | L'epic la plus touchée : images, tri, prix, liens vers les fiches |
| EP-03 Panier | 3 | Ajout / retrait défaillants pour 2 comptes, Reset App State incomplet |
| EP-04 Commande | 5 | Les 2 anomalies bloquantes sont dans le tunnel de commande |

## 4. Couverture des exigences

| Indicateur | Valeur |
|---|---|
| User stories couvertes par au moins un cas de test | **17 / 17 (100 %)** |
| Critères d'acceptation couverts | **28 / 28 (100 %)** |
| US conformes pour `standard_user` | 14 / 17 (US-13, US-14 et US-16 ont un cas KO) |
| Règles de gestion vérifiées | 18 / 18 |
| US touchées par au moins une anomalie (tous comptes) | 11 / 17 |

## 5. Automatisation

| Indicateur | Valeur |
|---|---|
| Cas de test automatisés | **43 / 43 (100 %)** |
| Tests pytest générés | 51 (43 cas + 8 scénarios d'anomalies sur les comptes spécifiques) |
| Résultat | **40 passés, 11 xfail** (anomalies connues), 0 échec |
| Stabilité | Résultats identiques sur toutes les exécutions locales successives et en CI |
| Durée | environ 80 s en local ; 2 min 41 s en CI, installation comprise |
| Répartition par tag | `@smoke` 9 · `@authentification` 12 · `@catalogue` 12 · `@panier` 11 · `@commande` 16 · `@anomalies` 11 |
| Anomalies couvertes par un test xfail | 10 / 16 (BUG-01, 02, 03, 05, 06, 07, 09, 10, 12, 13) |

Anomalies non automatisées : BUG-04, BUG-14 et BUG-15 sont purement visuelles et BUG-16 concerne la performance ; elles relèvent de tests de régression visuelle et de performance, hors du périmètre de cette suite (voir § 7). BUG-08 et BUG-11 sont fonctionnelles et pourraient être automatisées dans un prochain incrément.

## 6. Critères de sortie

| Critère (stratégie § 7) | Seuil | Résultat | Statut |
|---|---|---|---|
| Cas de priorité Haute exécutés | 100 % | 100 % (24 / 24) | ✅ |
| Ensemble des cas exécutés | ≥ 95 % | 100 % (43 / 43) | ✅ |
| Anomalie bloquante ouverte sur le parcours `standard_user` | 0 | 0 | ✅ |
| Anomalies documentées et tracées | 100 % | 100 % (16 / 16) | ✅ |
| Couverture des US | 100 % | 100 % (17 / 17) | ✅ |
| Suite automatisée passante en CI (hors xfail) | 100 % | 100 % | ✅ |

Les 6 critères de sortie sont atteints.

## 7. Recommandations

### Corrections

1. **Avant la mise en production** : corriger BUG-01 (commande vide confirmée, visible par tous les clients) et les 6 anomalies P1, en commençant par les 2 bloquantes (BUG-09, BUG-12), qui empêchent tout achat.
2. **Version suivante** : BUG-02 (normaliser les saisies en supprimant les espaces avant la validation) et BUG-03 (synchroniser l'état des boutons après Reset App State).
3. **Après chaque correction** : retirer le tag `@BUG-xx` du scénario correspondant. Le xfail strict fait échouer la suite dès qu'un bug est corrigé, ce qui garantit que le tag est retiré.

### Backlog (Business Analysis)

4. Ajouter aux critères d'acceptation les deux **exigences implicites** révélées par la recette : US-14 « un champ composé uniquement d'espaces est considéré comme vide » (CT-35) et US-16 « la commande ne peut pas être lancée avec un panier vide » (CT-43).
5. Définir une **exigence de performance** (par exemple : catalogue affiché en moins de 2 s après la connexion) pour pouvoir qualifier objectivement BUG-16.
6. Étudier les évolutions « Won't » identifiées en analyse : modifier la quantité dans le panier, conserver le tri choisi.

### Stratégie de test

7. **Régression visuelle** : comparer des captures de référence (`expect(page).to_have_screenshot()`) pour couvrir automatiquement BUG-04, BUG-14 et BUG-15.
8. **Multi-navigateur** : ajouter Firefox et WebKit dans une matrice GitHub Actions (`pytest --browser firefox --browser webkit`).
9. **Exécution planifiée** (tâche `schedule` nocturne) : le site étant hébergé par un tiers, elle détecterait ses évolutions même sans commit de notre part.
10. **Accessibilité** : intégrer un contrôle automatique (par exemple axe-core) sur les pages du parcours.
11. **Parallélisation** (`pytest-xdist`) si la suite grossit : chaque test utilisant son propre contexte navigateur, les tests sont déjà indépendants.
