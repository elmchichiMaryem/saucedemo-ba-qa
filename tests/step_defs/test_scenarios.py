"""Point d'entrée pytest : génère un test par scénario des fichiers .feature."""
from pytest_bdd import scenarios

scenarios(
    "authentification.feature",
    "catalogue.feature",
    "panier.feature",
    "commande.feature",
    "anomalies_connues.feature",
)
