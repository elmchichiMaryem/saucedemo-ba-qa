# language: en
@catalogue @regression
Feature: Catalogue (EP-02)
  En tant que client connecté, je veux consulter et trier les produits
  afin de choisir ce que je souhaite acheter.
  Couvre US-06 à US-08.

  Background:
    Given je suis connecté avec le compte "standard"

  @smoke
  Scenario: CT-13 - Le catalogue affiche tous les produits
    Then le catalogue affiche tous les produits du référentiel avec image, nom, description, prix et bouton d'ajout
    And le tri par défaut est appliqué

  Scenario: CT-14 - Les prix affichés sont ceux du référentiel
    Then chaque produit est affiché au prix du référentiel

  Scenario: CT-15 - La fiche produit reprend les informations du catalogue
    When j'ouvre la fiche du produit "Sauce Labs Backpack"
    Then la fiche du produit "Sauce Labs Backpack" affiche les mêmes informations que le catalogue

  Scenario: CT-16 - Retour au catalogue depuis la fiche produit
    Given j'ouvre la fiche du produit "Sauce Labs Backpack"
    When je reviens au catalogue depuis la fiche
    Then la page "catalogue" est affichée

  Scenario Outline: CT-17 à CT-19 - Trier le catalogue
    When je trie le catalogue par "<tri>"
    Then les produits sont triés par "<tri>"

    Examples:
      | tri             |
      | nom décroissant |
      | prix croissant  |
      | prix décroissant |

  Scenario: CT-20 - Revenir au tri par nom croissant
    When je trie le catalogue par "prix décroissant"
    And je trie le catalogue par "nom croissant"
    Then les produits sont triés par "nom croissant"
