# language: en
@regression @anomalies
Feature: Anomalies connues
  Ces scénarios décrivent le comportement ATTENDU de l'application.
  Ils échouent tant que l'anomalie référencée n'est pas corrigée :
  le tag @BUG-xx les marque « xfail » strict (voir conftest.py).
  Si une anomalie est corrigée, le scénario passe, la suite le signale
  (XPASS strict = échec) et il faut retirer le tag.
  Détail des anomalies : docs/qa/04_rapports_anomalies.md

  @commande @BUG-01
  Scenario: CT-43 - Une commande ne peut pas être lancée avec un panier vide
    Given je suis connecté avec le compte "standard"
    And j'ouvre le panier
    When je tente de démarrer la commande
    Then la page "panier" est affichée

  @commande @BUG-02
  Scenario: CT-35 - Des champs composés uniquement d'espaces sont refusés
    Given je suis connecté avec le compte "standard"
    And le produit "Sauce Labs Backpack" est dans mon panier
    And je démarre la commande
    When je saisis les informations du client "espaces"
    Then le message d'erreur "prénom obligatoire" est affiché
    And je reste sur l'étape des informations client

  @panier @BUG-03
  Scenario: CT-29 - Reset App State vide le panier et réinitialise les boutons
    Given je suis connecté avec le compte "standard"
    And les produits "Sauce Labs Backpack, Sauce Labs Bike Light" sont dans mon panier
    When je réinitialise l'application depuis le menu
    Then le badge du panier n'est pas affiché
    And tous les produits sont indiqués comme disponibles à l'ajout

  @catalogue
  Scenario Outline: Le tri du catalogue fonctionne pour les comptes spécifiques
    Given je suis connecté avec le compte "<compte>"
    When je trie le catalogue par "prix décroissant"
    Then les produits sont triés par "prix décroissant"

    @BUG-05
    Examples: BUG-05
      | compte   |
      | problème |

    @BUG-10
    Examples: BUG-10
      | compte |
      | erreur |

  @catalogue @BUG-06
  Scenario: La fiche ouverte est celle du produit cliqué (compte "problème")
    Given je suis connecté avec le compte "problème"
    When j'ouvre la fiche du produit "Sauce Labs Backpack"
    Then la fiche du produit "Sauce Labs Backpack" affiche les mêmes informations que le catalogue

  @panier
  Scenario Outline: Tous les produits peuvent être ajoutés au panier (comptes spécifiques)
    Given je suis connecté avec le compte "<compte>"
    When j'ajoute le produit "Sauce Labs Bolt T-Shirt" au panier depuis le catalogue
    Then le badge du panier affiche 1

    @BUG-07
    Examples: BUG-07
      | compte   |
      | problème |
      | erreur   |

  @commande @BUG-09
  Scenario: Les informations client saisies sont conservées (compte "problème")
    Given je suis connecté avec le compte "problème"
    And le produit "Sauce Labs Backpack" est dans mon panier
    And je démarre la commande
    When je saisis les informations du client "valide"
    Then la page "récapitulatif" est affichée

  @commande @BUG-12
  Scenario: La commande peut être validée (compte "erreur")
    Given je suis connecté avec le compte "erreur"
    And le produit "Sauce Labs Backpack" est dans mon panier
    And j'ai renseigné les informations du client "valide"
    When je valide la commande
    Then la confirmation de commande est affichée

  @catalogue @BUG-13
  Scenario: Les prix du catalogue sont ceux du référentiel (compte "visuel")
    Given je suis connecté avec le compte "visuel"
    Then chaque produit est affiché au prix du référentiel
