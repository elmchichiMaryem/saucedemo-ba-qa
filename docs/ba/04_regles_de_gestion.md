# Règles de gestion

Chaque règle ci-dessous a été **déduite par observation** du site avec le compte de référence `standard_user`, puis vérifiée par un script Playwright (septembre 2026). Les messages et les libellés sont cités tels qu'ils s'affichent à l'écran.

## Synthèse

| ID | Règle | Epic | US liées |
|---|---|---|---|
| RG-01 | Identifiant et mot de passe obligatoires | Authentification | US-01, US-02 |
| RG-02 | Identifiants reconnus, sensibles à la casse | Authentification | US-02 |
| RG-03 | Refus de connexion d'un compte bloqué | Authentification | US-03 |
| RG-04 | Pages accessibles uniquement avec une session | Authentification | US-04, US-05 |
| RG-05 | Ouverture de session | Authentification | US-01 |
| RG-06 | Fermeture de session | Authentification | US-04 |
| RG-07 | Contenu du catalogue et de la fiche produit | Catalogue | US-06, US-07 |
| RG-08 | Tri du catalogue | Catalogue | US-06, US-08 |
| RG-09 | Bascule du bouton Add to cart / Remove | Panier | US-07, US-09, US-10 |
| RG-10 | Quantité unitaire par produit | Panier | US-09, US-12 |
| RG-11 | Comportement du badge panier | Panier | US-09, US-10, US-11 |
| RG-12 | Persistance du panier | Panier | US-04, US-12 |
| RG-13 | Champs obligatoires du formulaire client | Commande | US-14 |
| RG-14 | Calcul des totaux avec une taxe de 8 % | Commande | US-15 |
| RG-15 | Paiement et livraison par défaut | Commande | US-15 |
| RG-16 | Validation de la commande | Commande | US-16 |
| RG-17 | Annulation de la commande | Commande | US-17 |
| RG-18 | Réinitialisation de l'état de l'application | Panier | US-13 |

---

## EP-01 — Authentification

### RG-01 — Identifiant et mot de passe obligatoires
Les deux champs « Username » et « Password » doivent être renseignés. L'identifiant est contrôlé **en premier** :
- identifiant vide (quel que soit le mot de passe) → `Epic sadface: Username is required` ;
- identifiant renseigné et mot de passe vide → `Epic sadface: Password is required`.

L'utilisateur reste sur la page de connexion. Le message peut être fermé avec la croix.
*US liées : US-01, US-02*

### RG-02 — Identifiants reconnus, sensibles à la casse
La connexion n'aboutit que si le couple identifiant / mot de passe correspond **exactement** à un compte existant. La comparaison est **sensible à la casse** (`Standard_User` est refusé). Dans tous les cas d'échec, le message est le même, sans préciser lequel des deux champs est faux : `Epic sadface: Username and password do not match any user in this service`.
*US liées : US-02*

### RG-03 — Refus de connexion d'un compte bloqué
Un compte bloqué (`locked_out_user`) fournit des identifiants valides mais se voit refuser l'accès avec le message `Epic sadface: Sorry, this user has been locked out.`
*US liées : US-03*

### RG-04 — Pages accessibles uniquement avec une session
Toutes les pages autres que la connexion (`/inventory.html`, `/inventory-item.html`, `/cart.html`, `/checkout-step-one.html`, `/checkout-step-two.html`, `/checkout-complete.html`) exigent une session. En accès direct sans session, l'utilisateur est renvoyé vers la page de connexion avec le message `Epic sadface: You can only access '<page>' when you are logged in.` (où `<page>` est le chemin demandé, sans paramètres).
*US liées : US-04, US-05*

### RG-05 — Ouverture de session
Une connexion réussie crée une session (cookie `session-username`, valable environ 10 minutes d'après la date d'expiration observée) et affiche le catalogue « Products ».
*US liées : US-01*

### RG-06 — Fermeture de session
L'option **Logout** du menu latéral ferme la session et affiche la page de connexion. Les pages protégées redeviennent inaccessibles (RG-04).
*US liées : US-04*

---

## EP-02 — Catalogue

### RG-07 — Contenu du catalogue et de la fiche produit
Le catalogue présente **6 produits**. Chacun a une image, un nom (lien vers sa fiche), une description, un prix en dollars US (format `$xx.xx`) et un bouton d'ajout. Le nom et l'image mènent à la fiche produit, qui reprend **les mêmes** nom, description et prix, avec un bouton **Back to products**.

Référentiel produits observé :

| Produit | Prix |
|---|---|
| Sauce Labs Backpack | $29.99 |
| Sauce Labs Bike Light | $9.99 |
| Sauce Labs Bolt T-Shirt | $15.99 |
| Sauce Labs Fleece Jacket | $49.99 |
| Sauce Labs Onesie | $7.99 |
| Test.allTheThings() T-Shirt (Red) | $15.99 |

*US liées : US-06, US-07*

### RG-08 — Tri du catalogue
Quatre options de tri sont proposées. L'option par défaut est **Name (A to Z)** :

| Option | Ordre | Premier produit |
|---|---|---|
| Name (A to Z) | nom alphabétique croissant | Sauce Labs Backpack |
| Name (Z to A) | nom alphabétique décroissant | Test.allTheThings() T-Shirt (Red) |
| Price (low to high) | prix croissant | Sauce Labs Onesie ($7.99) |
| Price (high to low) | prix décroissant | Sauce Labs Fleece Jacket ($49.99) |

Le tri choisi n'est pas conservé après un rechargement de la page : on revient à Name (A to Z).
*US liées : US-06, US-08*

---

## EP-03 — Panier

### RG-09 — Bascule du bouton Add to cart / Remove
Ajouter un produit transforme son bouton **Add to cart** en **Remove**. Cliquer sur **Remove** le retire du panier et rétablit **Add to cart**. L'état du bouton est **cohérent** entre le catalogue et la fiche produit.
*US liées : US-07, US-09, US-10*

### RG-10 — Quantité unitaire par produit
Un produit ne peut être présent qu'**une seule fois** dans le panier. La quantité affichée (colonne « QTY ») vaut toujours `1` et ne peut pas être modifiée : il n'y a aucun champ de saisie.
*US liées : US-09, US-12*

### RG-11 — Comportement du badge panier
Le badge sur l'icône du panier affiche le **nombre de produits distincts** dans le panier (de 1 à 6). Il est mis à jour immédiatement à chaque ajout ou retrait, et **masqué** quand le panier est vide.
*US liées : US-09, US-10, US-11*

### RG-12 — Persistance du panier
Le contenu du panier est enregistré dans le navigateur (`localStorage`, clé `cart-contents`). Il est donc conservé quand on navigue entre les pages, qu'on clique sur **Continue Shopping** ou qu'on se déconnecte puis se reconnecte dans le même navigateur.
*US liées : US-04, US-12*

### RG-18 — Réinitialisation de l'état de l'application
L'option **Reset App State** du menu latéral vide le panier et masque le badge.
*US liées : US-13*

---

## EP-04 — Commande

### RG-13 — Champs obligatoires du formulaire client
À l'étape « Checkout: Your Information », les champs **First Name**, **Last Name** et **Zip/Postal Code** sont obligatoires. Ils sont contrôlés **dans cet ordre**, et seul le premier champ manquant est signalé :
- `Error: First Name is required`
- `Error: Last Name is required`
- `Error: Postal Code is required`

Le format du code postal n'est pas contrôlé.
*US liées : US-14*

### RG-14 — Calcul des totaux avec une taxe de 8 %
À l'étape « Checkout: Overview » :
- **Item total** = somme des prix des articles du panier ;
- **Tax** = 8 % de l'Item total, arrondi au centime ;
- **Total** = Item total + Tax.

| Exemple | Item total | Tax (8 %) | Total |
|---|---|---|---|
| Backpack + Bike Light | $39.98 | $3.20 (3,1984 arrondi) | $43.18 |
| Backpack + Fleece Jacket + Onesie | $87.97 | $7.04 (7,0376 arrondi) | $95.01 |

*US liées : US-15*

### RG-15 — Paiement et livraison par défaut
Le récapitulatif affiche un moyen de paiement unique, `SauceCard #31337`, et un mode de livraison unique et gratuit, `Free Pony Express Delivery!`. Le client n'a rien à choisir ni à saisir.
*US liées : US-15*

### RG-16 — Validation de la commande
Cliquer sur **Finish** affiche « Checkout: Complete! » avec le message `Thank you for your order!`, **vide le panier** et masque le badge. Le bouton **Back Home** ramène au catalogue.
*US liées : US-16*

### RG-17 — Annulation de la commande
Le bouton **Cancel** est disponible aux deux étapes de la commande :
- à l'étape 1 (« Your Information ») → retour à la **page panier** ;
- à l'étape 2 (« Overview ») → retour au **catalogue**.

Dans les deux cas, le contenu du panier est **conservé**.
*US liées : US-17*
