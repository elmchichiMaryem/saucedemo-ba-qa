# language: en
@panier @regression
Feature: Panier (EP-03)
  En tant que client connecté, je veux constituer et ajuster mon panier
  afin de ne commander que ce que je souhaite.
  Couvre US-09 à US-13.

  Background:
    Given je suis connecté avec le compte "standard"

  @smoke
  Scenario: CT-21 - Ajouter un produit depuis le catalogue
    When j'ajoute le produit "Sauce Labs Backpack" au panier depuis le catalogue
    Then le produit "Sauce Labs Backpack" est indiqué comme ajouté au panier
    And le badge du panier affiche 1

  Scenario: CT-22 - Ajouter un produit depuis sa fiche
    Given j'ouvre la fiche du produit "Sauce Labs Backpack"
    When j'ajoute le produit au panier depuis sa fiche
    Then la fiche indique que le produit est ajouté au panier
    And le badge du panier affiche 1
    When je reviens au catalogue depuis la fiche
    Then le produit "Sauce Labs Backpack" est indiqué comme ajouté au panier

  Scenario: CT-23 - Retirer un produit depuis le catalogue
    Given le produit "Sauce Labs Backpack" est dans mon panier
    When je retire le produit "Sauce Labs Backpack" depuis le catalogue
    Then le produit "Sauce Labs Backpack" est indiqué comme disponible à l'ajout
    And le badge du panier n'est pas affiché

  Scenario: CT-24 - Retirer un produit depuis la page panier
    Given les produits "Sauce Labs Backpack, Sauce Labs Bike Light" sont dans mon panier
    And j'ouvre le panier
    When je retire le produit "Sauce Labs Bike Light" depuis la page panier
    Then le panier ne contient pas le produit "Sauce Labs Bike Light"
    And le badge du panier affiche 1

  Scenario: CT-25 - Le badge reflète le nombre d'articles
    Then le badge du panier n'est pas affiché
    When j'ajoute les produits "Sauce Labs Backpack, Sauce Labs Bike Light, Sauce Labs Onesie" au panier depuis le catalogue
    Then le badge du panier affiche 3
    When je retire le produit "Sauce Labs Bike Light" depuis le catalogue
    Then le badge du panier affiche 2

  @smoke
  Scenario: CT-26 - Le panier liste les articles ajoutés
    Given les produits "Sauce Labs Backpack, Sauce Labs Bike Light" sont dans mon panier
    When j'ouvre le panier
    Then le panier contient exactement les produits "Sauce Labs Backpack, Sauce Labs Bike Light" au prix du référentiel et en quantité 1

  Scenario: CT-27 - Continuer ses achats depuis le panier
    Given le produit "Sauce Labs Backpack" est dans mon panier
    And j'ouvre le panier
    When je continue mes achats
    Then la page "catalogue" est affichée
    And le badge du panier affiche 1

  Scenario: CT-28 - Le panier est conservé après déconnexion
    Given le produit "Sauce Labs Onesie" est dans mon panier
    When je me déconnecte depuis le menu
    And je me connecte avec le compte "standard"
    Then le badge du panier affiche 1
