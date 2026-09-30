# Glossaire

## Termes métier (application Swag Labs)

| Terme | Libellé à l'écran | Définition |
|---|---|---|
| **Swag Labs** | Swag Labs | Nom de la boutique en ligne de démonstration hébergée sur saucedemo.com |
| **Client** | — | Personne disposant d'un compte, qui se connecte pour acheter des produits |
| **Compte bloqué** | — | Compte dont l'accès est refusé malgré des identifiants valides (`locked_out_user`) |
| **Identifiant** | Username | Nom unique du compte, sensible à la casse |
| **Session** | — | Période pendant laquelle le client est reconnu comme connecté. Elle commence à la connexion et se termine à la déconnexion ou à l'expiration |
| **Déconnexion** | Logout | Action qui ferme la session et renvoie vers la page de connexion |
| **Menu latéral** | Open Menu (icône ☰) | Menu contenant All Items, Dynamic Catalog, About, Logout et Reset App State |
| **Catalogue** | Products | Page listant les 6 produits en vente |
| **Produit / article** | — | Élément vendu, caractérisé par un nom, une description, un prix et une image |
| **Fiche produit** | — | Page de détail d'un produit, accessible depuis son nom ou son image |
| **Tri** | Name (A to Z)… | Ordre d'affichage des produits : par nom ou par prix, croissant ou décroissant |
| **Panier** | Your Cart | Liste des produits sélectionnés par le client en vue de la commande |
| **Badge du panier** | — | Pastille numérique sur l'icône du panier, indiquant le nombre de produits sélectionnés |
| **Quantité** | QTY | Nombre d'exemplaires d'un produit dans le panier (toujours 1) |
| **Commande** | Checkout | Processus en deux étapes qui transforme le panier en achat |
| **Informations client** | Checkout: Your Information | Étape 1 de la commande : prénom, nom, code postal |
| **Récapitulatif** | Checkout: Overview | Étape 2 de la commande : articles, paiement, livraison et totaux |
| **Sous-total** | Item total | Somme des prix des articles, hors taxe |
| **Taxe** | Tax | Montant de taxe, égal à 8 % du sous-total |
| **Total** | Total | Montant à payer : sous-total + taxe |
| **Confirmation** | Checkout: Complete! | Page affichée après la validation de la commande |
| **Réinitialisation** | Reset App State | Option du menu qui remet l'application à son état initial (panier vidé) |

## Termes Business Analysis

| Terme | Définition |
|---|---|
| **Note de cadrage** | Document qui fixe le contexte, les objectifs, le périmètre, les parties prenantes et les risques d'un projet |
| **As-Is / To-Be** | Description du processus actuel / du processus cible |
| **Epic** | Grand ensemble fonctionnel regroupant plusieurs user stories (ex. EP-03 Panier) |
| **User story (US)** | Besoin exprimé du point de vue de l'utilisateur : « En tant que… je veux… afin de… » |
| **Critère d'acceptation (CA)** | Condition vérifiable qu'une US doit remplir pour être acceptée |
| **Règle de gestion (RG)** | Règle métier que le système doit appliquer (calcul, contrôle, contrainte) |
| **INVEST** | Grille de qualité d'une US : Indépendante, Négociable, Valeur, Estimable, Small, Testable |
| **MoSCoW** | Méthode de priorisation : Must, Should, Could, Won't |
| **Story point** | Unité d'estimation relative de l'effort, sur la suite de Fibonacci (1, 2, 3, 5, 8…) |
| **Definition of Ready (DoR)** | Conditions qu'une US doit remplir pour entrer en sprint |
| **Definition of Done (DoD)** | Conditions qu'une US doit remplir pour être considérée comme terminée |
| **Partie prenante** | Personne ou groupe concerné par le projet ou influent sur celui-ci |

## Termes Test / QA

| Terme | Définition |
|---|---|
| **Gherkin** | Langage structuré (Given / When / Then) pour écrire des scénarios lisibles par le métier et exécutables |
| **BDD** | Behaviour-Driven Development : développement guidé par des scénarios de comportement écrits en Gherkin |
| **Cas de test (CT)** | Suite d'étapes, avec données et résultat attendu, permettant de vérifier une exigence |
| **Anomalie (BUG)** | Écart entre le résultat obtenu et le résultat attendu |
| **Sévérité** | Gravité de l'impact d'une anomalie sur le système (bloquante, majeure, mineure…) |
| **Priorité** | Urgence de la correction d'une anomalie du point de vue métier |
| **Smoke test** | Petit ensemble de tests critiques qui vérifie rapidement que l'application est utilisable |
| **Non-régression** | Tests qui vérifient qu'une évolution n'a pas cassé l'existant |
| **Test exploratoire** | Test sans script préétabli, guidé par l'expérience et la curiosité du testeur |
| **Matrice de traçabilité** | Tableau reliant les exigences aux tests et aux anomalies |
| **Page Object Model (POM)** | Patron de conception qui regroupe dans une classe par page les sélecteurs et les actions de l'interface |
| **`data-test`** | Attribut HTML dédié aux tests, plus stable que les classes CSS pour localiser un élément |
| **xfail** | Marqueur pytest indiquant qu'un test doit échouer à cause d'une anomalie connue |
| **CI (intégration continue)** | Exécution automatique des tests à chaque modification du code (ici avec GitHub Actions) |
