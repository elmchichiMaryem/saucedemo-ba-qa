# language: en
@authentification @regression
Feature: Authentification (EP-01)
  En tant que client, je veux accéder à la boutique de manière sécurisée
  afin que seuls les comptes autorisés puissent acheter.
  Couvre US-01 à US-05.

  @smoke
  Scenario: CT-01 - Connexion avec des identifiants valides
    Given je suis sur la page de connexion
    When je me connecte avec le compte "standard"
    Then la page "catalogue" est affichée

  Scenario Outline: CT-02 à CT-07 - Message d'erreur selon la saisie
    Given je suis sur la page de connexion
    When je tente de me connecter avec les identifiants "<cas>"
    Then le message d'erreur "<message>" est affiché
    And je reste sur la page de connexion

    Examples:
      | cas                    | message                  |
      | champs vides           | identifiant obligatoire  |
      | identifiant vide       | identifiant obligatoire  |
      | mot de passe vide      | mot de passe obligatoire |
      | mot de passe incorrect | identifiants invalides   |
      | identifiant inconnu    | identifiants invalides   |
      | casse différente       | identifiants invalides   |

  @smoke
  Scenario: CT-08 - Connexion refusée pour un compte bloqué
    Given je suis sur la page de connexion
    When je me connecte avec le compte "bloqué"
    Then le message d'erreur "compte bloqué" est affiché
    And je reste sur la page de connexion

  @smoke
  Scenario: CT-09 - Déconnexion depuis le menu
    Given je suis connecté avec le compte "standard"
    When je me déconnecte depuis le menu
    Then la page de connexion est affichée

  Scenario: CT-10 - Le catalogue n'est plus accessible après déconnexion
    Given je suis connecté avec le compte "standard"
    And je me déconnecte depuis le menu
    When j'accède directement à la page "catalogue"
    Then l'accès à la page "catalogue" est refusé

  Scenario Outline: CT-11 et CT-12 - Accès direct à une page protégée sans être connecté
    Given je ne suis pas connecté
    When j'accède directement à la page "<page>"
    Then l'accès à la page "<page>" est refusé

    Examples:
      | page                |
      | panier              |
      | informations client |
