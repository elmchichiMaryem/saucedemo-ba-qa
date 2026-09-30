"""Étapes du tunnel de commande : informations client, récapitulatif, validation, annulation."""
from decimal import Decimal

from pytest_bdd import given, parsers, then, when
from playwright.sync_api import expect

from tests.step_defs.outils import arrondi_centime, liste_produits, prix_reference


def demarrer_commande(inventory_page, cart_page, checkout_info_page) -> None:
    inventory_page.ouvrir_panier()
    cart_page.a_charge()
    cart_page.commander()
    checkout_info_page.a_charge()


def saisir_client(checkout_info_page, donnees, client: str) -> None:
    infos = donnees["clients"][client]
    checkout_info_page.saisir(infos["prenom"], infos["nom"], infos["code_postal"])
    checkout_info_page.continuer()


@given("je démarre la commande")
def demarrer(inventory_page, cart_page, checkout_info_page):
    demarrer_commande(inventory_page, cart_page, checkout_info_page)


@when("je tente de démarrer la commande")
def tenter_demarrer(cart_page):
    cart_page.commander()
    cart_page.attendre_rendu()


@given(parsers.parse('j\'ai renseigné les informations du client "{client}"'))
def informations_renseignees(inventory_page, cart_page, checkout_info_page,
                             checkout_overview_page, donnees, client):
    demarrer_commande(inventory_page, cart_page, checkout_info_page)
    saisir_client(checkout_info_page, donnees, client)
    checkout_overview_page.a_charge()


@when(parsers.parse('je saisis les informations du client "{client}"'))
def saisir_informations(checkout_info_page, donnees, client):
    saisir_client(checkout_info_page, donnees, client)


@then(parsers.parse('le récapitulatif liste les produits "{produits}"'))
def recapitulatif_produits(checkout_overview_page, produits):
    expect(checkout_overview_page.noms).to_have_text(liste_produits(produits))


@then("les informations de paiement et de livraison sont affichées")
def paiement_livraison(checkout_overview_page, donnees):
    expect(checkout_overview_page.paiement).to_have_text(donnees["commande"]["paiement"])
    expect(checkout_overview_page.livraison).to_have_text(donnees["commande"]["livraison"])


@then("le sous-total, la taxe et le total correspondent au calcul attendu")
def totaux_corrects(checkout_overview_page, donnees, contexte):
    """Oracle indépendant : les montants sont recalculés à partir du référentiel produits."""
    regles = donnees["commande"]
    sous_total = sum(prix_reference(donnees, nom) for nom in contexte["panier"])
    taxe = arrondi_centime(sous_total * Decimal(str(regles["taux_taxe"])))
    total = sous_total + taxe
    libelles = regles["libelles_totaux"]
    expect(checkout_overview_page.sous_total).to_have_text(libelles["sous_total"].format(montant=f"{sous_total:.2f}"))
    expect(checkout_overview_page.taxe).to_have_text(libelles["taxe"].format(montant=f"{taxe:.2f}"))
    expect(checkout_overview_page.total).to_have_text(libelles["total"].format(montant=f"{total:.2f}"))


@given("je valide la commande")
@when("je valide la commande")
def valider_commande(checkout_overview_page):
    checkout_overview_page.terminer()


@then("la confirmation de commande est affichée")
def confirmation(checkout_complete_page, donnees, base_url):
    checkout_complete_page.a_charge()
    expect(checkout_complete_page.page).to_have_url(base_url + checkout_complete_page.chemin)
    expect(checkout_complete_page.titre).to_have_text(donnees["titres"]["confirmation"])
    expect(checkout_complete_page.message).to_have_text(donnees["messages"]["commande confirmée"])


@when("je reviens à l'accueil")
def revenir_accueil(checkout_complete_page):
    checkout_complete_page.revenir_accueil()


@when("j'annule la commande")
def annuler(checkout_page):
    checkout_page.annuler()
