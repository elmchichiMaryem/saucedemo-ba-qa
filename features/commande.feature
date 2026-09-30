# language: en
@commande @regression
Feature: Commande (EP-04)
  En tant que client, je veux finaliser mon achat en toute confiance
  afin de recevoir les articles de mon panier.
  Couvre US-14 à US-17.

  Background:
    Given je suis connecté avec le compte "standard"

  @smoke
  Scenario: CT-30 - Saisie complète des informations client
    Given le produit "Sauce Labs Backpack" est dans mon panier
    And je démarre la commande
    When je saisis les informations du client "valide"
    Then la page "récapitulatif" est affichée

  Scenario Outline: CT-31 à CT-34 - Champ obligatoire manquant
    Given le produit "Sauce Labs Backpack" est dans mon panier
    And je démarre la commande
    When je saisis les informations du client "<client>"
    Then le message d'erreur "<message>" est affiché
    And je reste sur l'étape des informations client

    Examples:
      | client           | message                 |
      | vide             | prénom obligatoire      |
      | sans prénom      | prénom obligatoire      |
      | sans nom         | nom obligatoire         |
      | sans code postal | code postal obligatoire |

  Scenario: CT-36 - Le récapitulatif affiche les articles, le paiement et la livraison
    Given les produits "Sauce Labs Backpack, Sauce Labs Bike Light" sont dans mon panier
    And j'ai renseigné les informations du client "valide"
    Then le récapitulatif liste les produits "Sauce Labs Backpack, Sauce Labs Bike Light"
    And les informations de paiement et de livraison sont affichées

  Scenario Outline: CT-37 et CT-38 - Calcul des totaux avec la taxe
    Given les produits "<produits>" sont dans mon panier
    And j'ai renseigné les informations du client "valide"
    Then le sous-total, la taxe et le total correspondent au calcul attendu

    @smoke
    Examples: CT-37 - deux articles
      | produits                                   |
      | Sauce Labs Backpack, Sauce Labs Bike Light |

    Examples: CT-38 - trois articles
      | produits                                                        |
      | Sauce Labs Backpack, Sauce Labs Fleece Jacket, Sauce Labs Onesie |

  @smoke
  Scenario: CT-39 - Valider la commande
    Given le produit "Sauce Labs Backpack" est dans mon panier
    And j'ai renseigné les informations du client "valide"
    When je valide la commande
    Then la confirmation de commande est affichée
    And le badge du panier n'est pas affiché

  Scenario: CT-40 - Retourner au catalogue après la commande
    Given le produit "Sauce Labs Backpack" est dans mon panier
    And j'ai renseigné les informations du client "valide"
    And je valide la commande
    When je reviens à l'accueil
    Then la page "catalogue" est affichée

  Scenario: CT-41 - Annuler à l'étape des informations client
    Given le produit "Sauce Labs Backpack" est dans mon panier
    And je démarre la commande
    When j'annule la commande
    Then la page "panier" est affichée
    And le panier contient exactement les produits "Sauce Labs Backpack" au prix du référentiel et en quantité 1

  Scenario: CT-42 - Annuler à l'étape du récapitulatif
    Given le produit "Sauce Labs Backpack" est dans mon panier
    And j'ai renseigné les informations du client "valide"
    When j'annule la commande
    Then la page "catalogue" est affichée
    And le badge du panier affiche 1
