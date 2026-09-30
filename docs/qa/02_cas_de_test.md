# Cas de test

**43 cas de test**, conçus à partir des critères d'acceptation du [backlog](../ba/03_backlog_user_stories.md) et des [règles de gestion](../ba/04_regles_de_gestion.md).

## Conventions

- **Compte par défaut** : `standard_user` / `secret_sauce`. On part d'un navigateur neuf, donc d'un panier vide.
- **« Connecté »** en précondition signifie : connexion effectuée avec `standard_user`, catalogue « Products » affiché.
- **Priorité** : Haute / Moyenne / Basse (importance métier du scénario).
- **Type** : Positif (usage nominal) / Négatif (saisie invalide ou usage interdit).
- **Smoke** : ✅ = fait partie du jeu de tests rapides à exécuter en premier.
- Les libellés entre guillemets sont ceux affichés par l'application.

## Répartition

| Epic | Cas | Positifs | Négatifs | Haute | Moyenne | Basse | Smoke |
|---|---|---|---|---|---|---|---|
| EP-01 Authentification | CT-01 → CT-12 | 2 | 10 | 8 | 4 | 0 | 3 |
| EP-02 Catalogue | CT-13 → CT-20 | 8 | 0 | 2 | 4 | 2 | 1 |
| EP-03 Panier | CT-21 → CT-29 | 9 | 0 | 5 | 2 | 2 | 2 |
| EP-04 Commande | CT-30 → CT-43 | 8 | 6 | 9 | 4 | 1 | 3 |
| **Total** | **43** | **27** | **16** | **24** | **14** | **5** | **9** |

---

## EP-01 — Authentification

| ID | US | Titre | Préconditions | Étapes | Données | Résultat attendu | Priorité | Type | Smoke |
|---|---|---|---|---|---|---|---|---|---|
| CT-01 | US-01 | Connexion avec des identifiants valides | Page de connexion affichée | 1. Saisir l'identifiant<br>2. Saisir le mot de passe<br>3. Cliquer sur « Login » | `standard_user` / `secret_sauce` | Page `/inventory.html` affichée, titre « Products » | Haute | Positif | ✅ |
| CT-02 | US-02 | Connexion avec les deux champs vides | Page de connexion affichée | 1. Laisser les deux champs vides<br>2. Cliquer sur « Login » | — | Message « Epic sadface: Username is required », reste sur la page de connexion | Haute | Négatif | |
| CT-03 | US-02 | Connexion sans identifiant | Page de connexion affichée | 1. Saisir uniquement le mot de passe<br>2. Cliquer sur « Login » | mot de passe `secret_sauce` | Message « Epic sadface: Username is required » | Moyenne | Négatif | |
| CT-04 | US-02 | Connexion sans mot de passe | Page de connexion affichée | 1. Saisir uniquement l'identifiant<br>2. Cliquer sur « Login » | `standard_user` | Message « Epic sadface: Password is required » | Haute | Négatif | |
| CT-05 | US-02 | Connexion avec un mot de passe incorrect | Page de connexion affichée | 1. Saisir un identifiant valide et un mauvais mot de passe<br>2. Cliquer sur « Login » | `standard_user` / `mauvais_mdp` | Message « Epic sadface: Username and password do not match any user in this service » | Haute | Négatif | |
| CT-06 | US-02 | Connexion avec un identifiant inconnu | Page de connexion affichée | 1. Saisir un identifiant inexistant<br>2. Cliquer sur « Login » | `inconnu` / `secret_sauce` | Même message qu'au CT-05 | Moyenne | Négatif | |
| CT-07 | US-02 | Sensibilité à la casse de l'identifiant | Page de connexion affichée | 1. Saisir l'identifiant avec des majuscules<br>2. Cliquer sur « Login » | `Standard_User` / `secret_sauce` | Même message qu'au CT-05, connexion refusée | Moyenne | Négatif | |
| CT-08 | US-03 | Connexion d'un compte bloqué | Page de connexion affichée | 1. Saisir les identifiants du compte bloqué<br>2. Cliquer sur « Login » | `locked_out_user` / `secret_sauce` | Message « Epic sadface: Sorry, this user has been locked out. », reste sur la page de connexion | Haute | Négatif | ✅ |
| CT-09 | US-04 | Déconnexion depuis le menu | Connecté | 1. Ouvrir le menu ☰<br>2. Cliquer sur « Logout » | — | Page de connexion affichée | Haute | Positif | ✅ |
| CT-10 | US-04, US-05 | Accès au catalogue après déconnexion | Connecté puis déconnecté | 1. Saisir l'URL `/inventory.html` | — | Retour à la page de connexion, message « Epic sadface: You can only access '/inventory.html' when you are logged in. » | Haute | Négatif | |
| CT-11 | US-05 | Accès direct au panier sans session | Aucune session | 1. Saisir l'URL `/cart.html` | — | Retour à la page de connexion, message « … You can only access '/cart.html' when you are logged in. » | Moyenne | Négatif | |
| CT-12 | US-05 | Accès direct au formulaire de commande sans session | Aucune session | 1. Saisir l'URL `/checkout-step-one.html` | — | Retour à la page de connexion, message « … You can only access '/checkout-step-one.html' when you are logged in. » | Haute | Négatif | |

## EP-02 — Catalogue

| ID | US | Titre | Préconditions | Étapes | Données | Résultat attendu | Priorité | Type | Smoke |
|---|---|---|---|---|---|---|---|---|---|
| CT-13 | US-06 | Affichage complet du catalogue | Connecté | 1. Observer la liste des produits | — | 6 produits, chacun avec image, nom, description, prix et bouton « Add to cart » ; tri par défaut « Name (A to Z) » | Haute | Positif | ✅ |
| CT-14 | US-06 | Prix conformes au référentiel | Connecté | 1. Relever le prix de chaque produit | Référentiel de RG-07 | Les 6 prix correspondent au référentiel (ex. Backpack $29.99, Onesie $7.99) | Haute | Positif | |
| CT-15 | US-07 | Fiche produit cohérente avec le catalogue | Connecté | 1. Relever nom, description et prix du Backpack<br>2. Cliquer sur son nom | Sauce Labs Backpack | Fiche du « Sauce Labs Backpack », mêmes nom, description et prix ($29.99) | Moyenne | Positif | |
| CT-16 | US-07 | Retour au catalogue depuis la fiche | Connecté | 1. Cliquer sur l'image d'un produit<br>2. Cliquer sur « Back to products » | — | Page `/inventory.html` affichée | Basse | Positif | |
| CT-17 | US-08 | Tri par nom Z → A | Connecté | 1. Choisir « Name (Z to A) » | — | Noms en ordre alphabétique décroissant, premier : « Test.allTheThings() T-Shirt (Red) » | Moyenne | Positif | |
| CT-18 | US-08 | Tri par prix croissant | Connecté | 1. Choisir « Price (low to high) » | — | Prix croissants, premier : « Sauce Labs Onesie » ($7.99) | Moyenne | Positif | |
| CT-19 | US-08 | Tri par prix décroissant | Connecté | 1. Choisir « Price (high to low) » | — | Prix décroissants, premier : « Sauce Labs Fleece Jacket » ($49.99) | Moyenne | Positif | |
| CT-20 | US-08 | Retour au tri par nom A → Z | Connecté | 1. Choisir « Price (high to low) »<br>2. Choisir « Name (A to Z) » | — | Noms en ordre alphabétique croissant, premier : « Sauce Labs Backpack » | Basse | Positif | |

## EP-03 — Panier

| ID | US | Titre | Préconditions | Étapes | Données | Résultat attendu | Priorité | Type | Smoke |
|---|---|---|---|---|---|---|---|---|---|
| CT-21 | US-09, US-11 | Ajout depuis le catalogue | Connecté, panier vide | 1. Cliquer sur « Add to cart » du Backpack | Sauce Labs Backpack | Le bouton affiche « Remove », le badge affiche « 1 » | Haute | Positif | ✅ |
| CT-22 | US-09 | Ajout depuis la fiche produit | Connecté, panier vide | 1. Ouvrir la fiche du Backpack<br>2. Cliquer sur « Add to cart »<br>3. Cliquer sur « Back to products » | Sauce Labs Backpack | Sur la fiche : bouton « Remove », badge « 1 » ; au catalogue : le bouton du Backpack affiche « Remove » | Moyenne | Positif | |
| CT-23 | US-10 | Retrait depuis le catalogue | Connecté, Backpack au panier | 1. Cliquer sur « Remove » du Backpack | Sauce Labs Backpack | Le bouton redevient « Add to cart », le badge est masqué | Haute | Positif | |
| CT-24 | US-10 | Retrait depuis la page panier | Connecté, Backpack et Bike Light au panier | 1. Ouvrir le panier<br>2. Cliquer sur « Remove » du Bike Light | Backpack, Bike Light | Le Bike Light disparaît du panier, le badge affiche « 1 » | Haute | Positif | |
| CT-25 | US-11 | Évolution du badge | Connecté, panier vide | 1. Vérifier l'absence de badge<br>2. Ajouter 3 produits<br>3. Retirer le Bike Light | Backpack, Bike Light, Onesie | Badge : absent → « 3 » → « 2 » | Haute | Positif | |
| CT-26 | US-12 | Contenu de la page panier | Connecté, Backpack et Bike Light au panier | 1. Cliquer sur l'icône du panier | Backpack, Bike Light | Page « Your Cart » : Backpack $29.99 et Bike Light $9.99, quantité 1 chacun | Haute | Positif | ✅ |
| CT-27 | US-12 | Continuer ses achats depuis le panier | Connecté, 1 article au panier | 1. Ouvrir le panier<br>2. Cliquer sur « Continue Shopping » | — | Catalogue affiché, badge « 1 » | Moyenne | Positif | |
| CT-28 | US-12 | Panier conservé après reconnexion | Connecté, Onesie au panier | 1. Se déconnecter<br>2. Se reconnecter avec le même compte | Sauce Labs Onesie | Le badge affiche « 1 » | Basse | Positif | |
| CT-29 | US-13 | Reset App State vide le panier | Connecté, Backpack et Bike Light au panier | 1. Ouvrir le menu ☰<br>2. Cliquer sur « Reset App State » | — | Badge masqué **et** tous les boutons du catalogue affichent « Add to cart » | Basse | Positif | |

## EP-04 — Commande

| ID | US | Titre | Préconditions | Étapes | Données | Résultat attendu | Priorité | Type | Smoke |
|---|---|---|---|---|---|---|---|---|---|
| CT-30 | US-14 | Saisie complète des informations client | Connecté, 1 article au panier, étape « Checkout: Your Information » | 1. Saisir prénom, nom, code postal<br>2. Cliquer sur « Continue » | Marie / Curie / 75005 | Étape « Checkout: Overview » affichée | Haute | Positif | ✅ |
| CT-31 | US-14 | Formulaire entièrement vide | Idem CT-30 | 1. Cliquer sur « Continue » sans rien saisir | — | Message « Error: First Name is required », reste sur l'étape 1 | Haute | Négatif | |
| CT-32 | US-14 | Prénom manquant | Idem CT-30 | 1. Saisir le nom et le code postal uniquement<br>2. Cliquer sur « Continue » | — / Curie / 75005 | Message « Error: First Name is required » | Haute | Négatif | |
| CT-33 | US-14 | Nom manquant | Idem CT-30 | 1. Saisir le prénom et le code postal uniquement<br>2. Cliquer sur « Continue » | Marie / — / 75005 | Message « Error: Last Name is required » | Haute | Négatif | |
| CT-34 | US-14 | Code postal manquant | Idem CT-30 | 1. Saisir le prénom et le nom uniquement<br>2. Cliquer sur « Continue » | Marie / Curie / — | Message « Error: Postal Code is required » | Haute | Négatif | |
| CT-35 | US-14 | Champs contenant uniquement des espaces | Idem CT-30 | 1. Saisir 3 espaces dans chaque champ<br>2. Cliquer sur « Continue » | `"   "` × 3 | Saisie refusée avec un message d'erreur (un champ composé d'espaces n'est pas renseigné) — *exigence implicite, cf. RG-13* | Moyenne | Négatif | |
| CT-36 | US-15 | Contenu du récapitulatif | Connecté, Backpack et Bike Light au panier, informations saisies | 1. Observer l'étape « Checkout: Overview » | — | Les 2 articles sont listés ; paiement « SauceCard #31337 » ; livraison « Free Pony Express Delivery! » | Haute | Positif | |
| CT-37 | US-15 | Totaux pour 2 articles | Connecté, Backpack + Bike Light, informations saisies | 1. Observer le bloc « Price Total » | $29.99 + $9.99 | « Item total: $39.98 », « Tax: $3.20 », « Total: $43.18 » | Haute | Positif | ✅ |
| CT-38 | US-15 | Totaux pour 3 articles | Connecté, Backpack + Fleece Jacket + Onesie, informations saisies | 1. Observer le bloc « Price Total » | $29.99 + $49.99 + $7.99 | « Item total: $87.97 », « Tax: $7.04 », « Total: $95.01 » | Haute | Positif | |
| CT-39 | US-16 | Validation de la commande | Connecté, étape « Checkout: Overview » avec 1 article | 1. Cliquer sur « Finish » | — | Page « Checkout: Complete! », message « Thank you for your order! », badge masqué | Haute | Positif | ✅ |
| CT-40 | US-16 | Retour au catalogue après la commande | Commande confirmée | 1. Cliquer sur « Back Home » | — | Page `/inventory.html` affichée | Basse | Positif | |
| CT-41 | US-17 | Annulation à l'étape 1 | Connecté, 1 article au panier, étape « Checkout: Your Information » | 1. Cliquer sur « Cancel » | — | Page panier affichée, l'article est toujours présent | Moyenne | Positif | |
| CT-42 | US-17 | Annulation à l'étape 2 | Connecté, 1 article au panier, étape « Checkout: Overview » | 1. Cliquer sur « Cancel » | — | Catalogue affiché, badge « 1 » | Moyenne | Positif | |
| CT-43 | US-16 | Commande impossible avec un panier vide | Connecté, panier vide | 1. Ouvrir le panier<br>2. Cliquer sur « Checkout » | — | La commande ne peut pas être lancée (bouton inactif ou message), l'utilisateur reste sur le panier — *exigence implicite* | Moyenne | Négatif | |

> **CT-35 et CT-43** testent des **exigences implicites** : elles ne figurent pas dans les critères d'acceptation, mais un Product Owner les attendrait raisonnablement. Leur échec est remonté comme anomalie, avec la recommandation d'ajouter le critère correspondant au backlog.
