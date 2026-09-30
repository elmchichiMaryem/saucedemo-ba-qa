# Backlog produit — User stories

## 1. Conventions

- **Format** : « En tant que… je veux… afin de… ».
- **Critères d'acceptation** en Gherkin : mots-clés en anglais (`Given` / `When` / `Then` / `And`), texte en français. Les libellés de l'interface (en anglais) sont cités entre guillemets, tels qu'ils apparaissent à l'écran.
- **Priorité MoSCoW** : **M**ust (indispensable), **S**hould (important), **C**ould (souhaitable), **W**on't (pas dans cette version).
- **Estimation** en story points, suite de Fibonacci (1, 2, 3, 5, 8, 13). L'estimation est **relative** : elle mesure l'effort de spécification, de test et d'automatisation, pas une durée.
- Sauf mention contraire, le mot de passe utilisé est `secret_sauce`.

### Vérification INVEST

Chaque story a été relue avec la grille INVEST :

| Critère | Comment il est respecté |
|---|---|
| **I**ndépendante | Chaque story se teste seule. Les prérequis (être connecté, avoir un article au panier) sont posés dans le `Given`, pas hérités d'une autre story |
| **N**égociable | La story exprime un besoin, pas une solution technique : le « comment » reste ouvert |
| **V**aleur | Le « afin de » exprime un bénéfice pour le client ou pour le métier |
| **E**stimable | Le périmètre est borné par les critères d'acceptation, d'où une estimation possible |
| **S**mall | Aucune story ne dépasse 3 points : chacune tient largement dans un sprint |
| **T**estable | Chaque critère d'acceptation est un scénario Gherkin avec un résultat observable |

## 2. Definition of Ready (DoR)

Une story peut entrer en sprint lorsque :

- [ ] elle est rédigée au format « En tant que… je veux… afin de… » ;
- [ ] elle respecte la grille INVEST ;
- [ ] ses critères d'acceptation sont écrits en Gherkin et validés par le Product Owner ;
- [ ] les règles de gestion concernées sont identifiées (RG-xx) ;
- [ ] les données de test nécessaires sont connues (comptes, produits, saisies) ;
- [ ] elle est priorisée (MoSCoW) et estimée (story points) ;
- [ ] ses dépendances éventuelles sont identifiées.

## 3. Definition of Done (DoD)

Une story est terminée lorsque :

- [ ] tous ses critères d'acceptation sont vérifiés ;
- [ ] les cas de test manuels associés sont rédigés et exécutés avec `standard_user` ;
- [ ] les scénarios automatisés (pytest-bdd) correspondants passent en local **et** dans l'intégration continue ;
- [ ] les anomalies découvertes sont documentées (fiche BUG-xx) et reliées à la story ;
- [ ] la matrice de traçabilité est à jour (US ↔ CA ↔ CT ↔ scénario ↔ anomalie) ;
- [ ] le code et la documentation sont versionnés sur `main` avec un message au format Conventional Commits.

## 4. Vue d'ensemble

| Epic | ID | User story | MoSCoW | Points |
|---|---|---|---|---|
| EP-01 Authentification | US-01 | Connexion réussie | Must | 2 |
| | US-02 | Erreurs de connexion | Must | 3 |
| | US-03 | Utilisateur bloqué | Must | 1 |
| | US-04 | Déconnexion | Must | 2 |
| | US-05 | Protection des pages sans session | Should | 2 |
| EP-02 Catalogue | US-06 | Affichage du catalogue | Must | 2 |
| | US-07 | Détail d'un produit | Should | 2 |
| | US-08 | Tri du catalogue | Should | 3 |
| EP-03 Panier | US-09 | Ajout d'un article au panier | Must | 2 |
| | US-10 | Retrait d'un article du panier | Must | 2 |
| | US-11 | Badge du panier | Must | 1 |
| | US-12 | Consultation du panier | Must | 2 |
| | US-13 | Réinitialisation de l'état de l'application | Could | 2 |
| EP-04 Commande | US-14 | Saisie des informations client | Must | 3 |
| | US-15 | Récapitulatif de commande et totaux | Must | 3 |
| | US-16 | Confirmation de commande | Must | 1 |
| | US-17 | Annulation de commande | Should | 2 |
| **Total** | **17 US** | | **12 Must · 4 Should · 1 Could** | **35** |

Hors version (**Won't**, identifié lors de l'analyse) : modification de la quantité d'un article dans le panier, conservation du critère de tri, blocage d'une commande avec un panier vide.

---

## EP-01 — Authentification

> Permettre aux clients autorisés, et à eux seuls, d'accéder à la boutique.

### US-01 — Connexion réussie

**En tant que** client disposant d'un compte actif,
**je veux** me connecter avec mon identifiant et mon mot de passe
**afin d'**accéder au catalogue de la boutique.

| MoSCoW | Points | Règles |
|---|---|---|
| Must | 2 | RG-01, RG-05 |

```gherkin
Scenario: Connexion avec des identifiants valides
  Given je suis sur la page de connexion
  When je saisis l'identifiant "standard_user" et le mot de passe "secret_sauce"
  And je clique sur "Login"
  Then je suis redirigé vers la page du catalogue
  And le titre de la page est "Products"
```

### US-02 — Erreurs de connexion

**En tant que** client,
**je veux** être informé clairement lorsque ma connexion échoue
**afin de** corriger ma saisie.

| MoSCoW | Points | Règles |
|---|---|---|
| Must | 3 | RG-01, RG-02 |

```gherkin
Scenario Outline: Message d'erreur selon la saisie
  Given je suis sur la page de connexion
  When je saisis l'identifiant "<identifiant>" et le mot de passe "<mot_de_passe>"
  And je clique sur "Login"
  Then le message d'erreur "<message>" est affiché
  And je reste sur la page de connexion

  Examples:
    | identifiant   | mot_de_passe | message                                                                    |
    |               |              | Epic sadface: Username is required                                         |
    |               | secret_sauce | Epic sadface: Username is required                                         |
    | standard_user |              | Epic sadface: Password is required                                         |
    | standard_user | mauvais_mdp  | Epic sadface: Username and password do not match any user in this service |
    | inconnu       | secret_sauce | Epic sadface: Username and password do not match any user in this service |
    | Standard_User | secret_sauce | Epic sadface: Username and password do not match any user in this service |
```

### US-03 — Utilisateur bloqué

**En tant que** responsable de la boutique,
**je veux** qu'un compte bloqué ne puisse pas se connecter
**afin de** protéger la boutique contre les comptes suspendus.

| MoSCoW | Points | Règles |
|---|---|---|
| Must | 1 | RG-03 |

```gherkin
Scenario: Tentative de connexion avec un compte bloqué
  Given je suis sur la page de connexion
  When je saisis l'identifiant "locked_out_user" et le mot de passe "secret_sauce"
  And je clique sur "Login"
  Then le message d'erreur "Epic sadface: Sorry, this user has been locked out." est affiché
  And je reste sur la page de connexion
```

### US-04 — Déconnexion

**En tant que** client connecté,
**je veux** me déconnecter depuis le menu
**afin qu'**une autre personne utilisant le même poste ne puisse pas accéder à mon compte.

| MoSCoW | Points | Règles |
|---|---|---|
| Must | 2 | RG-06, RG-12 |

```gherkin
Scenario: Déconnexion depuis le menu
  Given je suis connecté en tant que "standard_user"
  When j'ouvre le menu
  And je clique sur "Logout"
  Then je suis redirigé vers la page de connexion

Scenario: Les pages protégées ne sont plus accessibles après déconnexion
  Given je me suis connecté puis déconnecté
  When j'accède directement à la page "/inventory.html"
  Then je suis redirigé vers la page de connexion
  And le message d'erreur "Epic sadface: You can only access '/inventory.html' when you are logged in." est affiché
```

### US-05 — Protection des pages sans session

**En tant que** responsable de la boutique,
**je veux** que les pages de la boutique ne soient accessibles qu'après connexion
**afin qu'**aucun visiteur anonyme ne consulte le catalogue ou ne passe commande.

| MoSCoW | Points | Règles |
|---|---|---|
| Should | 2 | RG-04 |

```gherkin
Scenario Outline: Accès direct à une page protégée sans être connecté
  Given je ne suis pas connecté
  When j'accède directement à la page "<page>"
  Then je suis redirigé vers la page de connexion
  And le message d'erreur "Epic sadface: You can only access '<page>' when you are logged in." est affiché

  Examples:
    | page                    |
    | /inventory.html         |
    | /cart.html              |
    | /checkout-step-one.html |
```

---

## EP-02 — Catalogue

> Présenter l'offre de produits de manière claire et navigable.

### US-06 — Affichage du catalogue

**En tant que** client connecté,
**je veux** voir la liste des produits avec leurs informations principales
**afin de** choisir ce que je souhaite acheter.

| MoSCoW | Points | Règles |
|---|---|---|
| Must | 2 | RG-07, RG-08 |

```gherkin
Scenario: Le catalogue affiche tous les produits
  Given je suis connecté en tant que "standard_user"
  Then le catalogue affiche 6 produits
  And chaque produit présente une image, un nom, une description, un prix et un bouton "Add to cart"
  And les produits sont triés par nom de A à Z

Scenario: Les prix affichés sont ceux du référentiel produits
  Given je suis connecté en tant que "standard_user"
  Then le produit "Sauce Labs Backpack" est affiché au prix de "$29.99"
  And le produit "Sauce Labs Onesie" est affiché au prix de "$7.99"
```

### US-07 — Détail d'un produit

**En tant que** client connecté,
**je veux** consulter la fiche détaillée d'un produit
**afin d'**en savoir plus avant de l'ajouter au panier.

| MoSCoW | Points | Règles |
|---|---|---|
| Should | 2 | RG-07, RG-09 |

```gherkin
Scenario: Ouvrir la fiche d'un produit depuis le catalogue
  Given je suis connecté en tant que "standard_user"
  When je clique sur le nom du produit "Sauce Labs Backpack"
  Then la fiche du produit "Sauce Labs Backpack" est affichée
  And elle présente le même nom, la même description et le même prix "$29.99" que dans le catalogue

Scenario: Revenir au catalogue depuis la fiche produit
  Given je consulte la fiche du produit "Sauce Labs Backpack"
  When je clique sur "Back to products"
  Then la page du catalogue est affichée
```

### US-08 — Tri du catalogue

**En tant que** client connecté,
**je veux** trier les produits par nom ou par prix
**afin de** trouver plus vite l'article qui correspond à mon besoin ou à mon budget.

| MoSCoW | Points | Règles |
|---|---|---|
| Should | 3 | RG-08 |

```gherkin
Scenario Outline: Trier le catalogue
  Given je suis connecté en tant que "standard_user"
  When je choisis le tri "<option>"
  Then les produits sont triés par <critère> dans l'ordre <ordre>
  And le premier produit affiché est "<premier_produit>"

  Examples:
    | option              | critère | ordre       | premier_produit                   |
    | Name (A to Z)       | nom     | croissant   | Sauce Labs Backpack               |
    | Name (Z to A)       | nom     | décroissant | Test.allTheThings() T-Shirt (Red) |
    | Price (low to high) | prix    | croissant   | Sauce Labs Onesie                 |
    | Price (high to low) | prix    | décroissant | Sauce Labs Fleece Jacket          |
```

---

## EP-03 — Panier

> Permettre au client de constituer et d'ajuster sa sélection avant de commander.

### US-09 — Ajout d'un article au panier

**En tant que** client connecté,
**je veux** ajouter un produit à mon panier depuis le catalogue ou depuis sa fiche
**afin de** le commander plus tard.

| MoSCoW | Points | Règles |
|---|---|---|
| Must | 2 | RG-09, RG-10, RG-11 |

```gherkin
Scenario: Ajouter un produit depuis le catalogue
  Given je suis connecté en tant que "standard_user"
  And mon panier est vide
  When j'ajoute le produit "Sauce Labs Backpack" au panier depuis le catalogue
  Then le bouton du produit "Sauce Labs Backpack" affiche "Remove"
  And le badge du panier affiche "1"

Scenario: Ajouter un produit depuis sa fiche
  Given je consulte la fiche du produit "Sauce Labs Backpack"
  And mon panier est vide
  When je clique sur "Add to cart"
  Then le bouton affiche "Remove"
  And le badge du panier affiche "1"
```

### US-10 — Retrait d'un article du panier

**En tant que** client connecté,
**je veux** retirer un produit de mon panier
**afin de** ne commander que ce que je souhaite vraiment.

| MoSCoW | Points | Règles |
|---|---|---|
| Must | 2 | RG-09, RG-11 |

```gherkin
Scenario: Retirer un produit depuis le catalogue
  Given je suis connecté en tant que "standard_user"
  And le produit "Sauce Labs Backpack" est dans mon panier
  When je clique sur "Remove" pour le produit "Sauce Labs Backpack" dans le catalogue
  Then le bouton du produit "Sauce Labs Backpack" affiche "Add to cart"
  And le badge du panier n'est plus affiché

Scenario: Retirer un produit depuis la page panier
  Given les produits "Sauce Labs Backpack" et "Sauce Labs Bike Light" sont dans mon panier
  And je suis sur la page du panier
  When je clique sur "Remove" pour le produit "Sauce Labs Bike Light"
  Then le produit "Sauce Labs Bike Light" n'apparaît plus dans le panier
  And le badge du panier affiche "1"
```

### US-11 — Badge du panier

**En tant que** client connecté,
**je veux** voir en permanence le nombre d'articles dans mon panier
**afin de** savoir où j'en suis sans ouvrir le panier.

| MoSCoW | Points | Règles |
|---|---|---|
| Must | 1 | RG-11 |

```gherkin
Scenario: Le badge reflète le nombre d'articles
  Given je suis connecté en tant que "standard_user"
  And mon panier est vide
  Then le badge du panier n'est pas affiché
  When j'ajoute les produits "Sauce Labs Backpack", "Sauce Labs Bike Light" et "Sauce Labs Onesie" au panier
  Then le badge du panier affiche "3"
  When je retire le produit "Sauce Labs Bike Light" du panier
  Then le badge du panier affiche "2"
```

### US-12 — Consultation du panier

**En tant que** client connecté,
**je veux** consulter le contenu de mon panier
**afin de** vérifier ma sélection avant de commander.

| MoSCoW | Points | Règles |
|---|---|---|
| Must | 2 | RG-10, RG-12 |

```gherkin
Scenario: Le panier liste les articles ajoutés
  Given je suis connecté en tant que "standard_user"
  And les produits "Sauce Labs Backpack" et "Sauce Labs Bike Light" sont dans mon panier
  When j'ouvre le panier
  Then la page "Your Cart" liste "Sauce Labs Backpack" au prix de "$29.99" avec la quantité 1
  And elle liste "Sauce Labs Bike Light" au prix de "$9.99" avec la quantité 1

Scenario: Continuer ses achats depuis le panier
  Given je suis sur la page du panier avec un article
  When je clique sur "Continue Shopping"
  Then la page du catalogue est affichée
  And le badge du panier affiche "1"

Scenario: Le panier est conservé après déconnexion
  Given le produit "Sauce Labs Onesie" est dans mon panier
  When je me déconnecte puis me reconnecte avec le même compte
  Then le badge du panier affiche "1"
```

### US-13 — Réinitialisation de l'état de l'application

**En tant que** client connecté,
**je veux** réinitialiser l'application depuis le menu
**afin de** repartir d'un panier vide en une seule action.

| MoSCoW | Points | Règles |
|---|---|---|
| Could | 2 | RG-18 |

```gherkin
Scenario: Reset App State vide le panier
  Given je suis connecté en tant que "standard_user"
  And les produits "Sauce Labs Backpack" et "Sauce Labs Bike Light" sont dans mon panier
  When j'ouvre le menu
  And je clique sur "Reset App State"
  Then le badge du panier n'est plus affiché
  And tous les boutons du catalogue affichent "Add to cart"
```

---

## EP-04 — Commande

> Permettre au client de finaliser son achat en toute confiance.

### US-14 — Saisie des informations client

**En tant que** client ayant des articles dans son panier,
**je veux** renseigner mon prénom, mon nom et mon code postal
**afin que** ma commande puisse m'être livrée.

| MoSCoW | Points | Règles |
|---|---|---|
| Must | 3 | RG-13 |

```gherkin
Scenario: Saisie complète des informations
  Given je suis sur l'étape "Checkout: Your Information" avec un article dans mon panier
  When je saisis le prénom "Marie", le nom "Curie" et le code postal "75005"
  And je clique sur "Continue"
  Then l'étape "Checkout: Overview" est affichée

Scenario Outline: Champ obligatoire manquant
  Given je suis sur l'étape "Checkout: Your Information" avec un article dans mon panier
  When je saisis le prénom "<prenom>", le nom "<nom>" et le code postal "<code_postal>"
  And je clique sur "Continue"
  Then le message d'erreur "<message>" est affiché
  And je reste sur l'étape "Checkout: Your Information"

  Examples:
    | prenom | nom   | code_postal | message                        |
    |        |       |             | Error: First Name is required  |
    |        | Curie | 75005       | Error: First Name is required  |
    | Marie  |       | 75005       | Error: Last Name is required   |
    | Marie  | Curie |             | Error: Postal Code is required |
```

### US-15 — Récapitulatif de commande et totaux

**En tant que** client,
**je veux** voir un récapitulatif de ma commande avec le détail des montants
**afin de** vérifier ce que je vais payer avant de valider.

| MoSCoW | Points | Règles |
|---|---|---|
| Must | 3 | RG-14, RG-15 |

```gherkin
Scenario: Le récapitulatif affiche les articles et les informations de paiement et de livraison
  Given j'ai ajouté "Sauce Labs Backpack" et "Sauce Labs Bike Light" à mon panier
  And j'ai renseigné mes informations client
  When l'étape "Checkout: Overview" est affichée
  Then elle liste "Sauce Labs Backpack" et "Sauce Labs Bike Light"
  And le moyen de paiement "SauceCard #31337" est affiché
  And le mode de livraison "Free Pony Express Delivery!" est affiché

Scenario Outline: Calcul des totaux avec une taxe de 8 %
  Given j'ai ajouté les produits <produits> à mon panier
  And j'ai renseigné mes informations client
  When l'étape "Checkout: Overview" est affichée
  Then le sous-total affiché est "Item total: <sous_total>"
  And la taxe affichée est "Tax: <taxe>"
  And le total affiché est "Total: <total>"

  Examples:
    | produits                                                              | sous_total | taxe  | total  |
    | "Sauce Labs Backpack", "Sauce Labs Bike Light"                        | $39.98     | $3.20 | $43.18 |
    | "Sauce Labs Backpack", "Sauce Labs Fleece Jacket", "Sauce Labs Onesie" | $87.97     | $7.04 | $95.01 |
```

### US-16 — Confirmation de commande

**En tant que** client,
**je veux** recevoir une confirmation lorsque je valide ma commande
**afin d'**être certain que mon achat est pris en compte.

| MoSCoW | Points | Règles |
|---|---|---|
| Must | 1 | RG-16 |

```gherkin
Scenario: Valider la commande
  Given je suis sur l'étape "Checkout: Overview" avec un article dans mon panier
  When je clique sur "Finish"
  Then la page "Checkout: Complete!" est affichée
  And le message "Thank you for your order!" est affiché
  And le badge du panier n'est plus affiché

Scenario: Retourner au catalogue après la commande
  Given ma commande est confirmée
  When je clique sur "Back Home"
  Then la page du catalogue est affichée
```

### US-17 — Annulation de commande

**En tant que** client en cours de commande,
**je veux** pouvoir annuler à chaque étape
**afin de** modifier mon panier ou renoncer à mon achat sans rien perdre.

| MoSCoW | Points | Règles |
|---|---|---|
| Should | 2 | RG-17 |

```gherkin
Scenario: Annuler à l'étape des informations client
  Given je suis sur l'étape "Checkout: Your Information" avec un article dans mon panier
  When je clique sur "Cancel"
  Then la page du panier est affichée
  And mon panier contient toujours 1 article

Scenario: Annuler à l'étape du récapitulatif
  Given je suis sur l'étape "Checkout: Overview" avec un article dans mon panier
  When je clique sur "Cancel"
  Then la page du catalogue est affichée
  And le badge du panier affiche "1"
```
