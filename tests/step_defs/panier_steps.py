"""Étapes du panier : ajout, retrait, contenu, réinitialisation."""
from pytest_bdd import given, parsers, then, when
from playwright.sync_api import expect

from tests.step_defs.outils import formater_prix, liste_produits, prix_reference


def ajouter_depuis_catalogue(inventory_page, contexte, produits: str) -> list[str]:
    noms = liste_produits(produits)
    for nom in noms:
        inventory_page.cliquer_bouton_produit(nom)
    contexte["panier"].extend(noms)
    return noms


@given(parsers.parse('le produit "{produits}" est dans mon panier'))
@given(parsers.parse('les produits "{produits}" sont dans mon panier'))
def produits_dans_panier(inventory_page, donnees, contexte, produits):
    for nom in ajouter_depuis_catalogue(inventory_page, contexte, produits):
        expect(inventory_page.bouton_produit(nom)).to_have_text(donnees["boutons"]["retirer"])


@when(parsers.parse('j\'ajoute le produit "{produits}" au panier depuis le catalogue'))
@when(parsers.parse('j\'ajoute les produits "{produits}" au panier depuis le catalogue'))
def ajouter_produits(inventory_page, contexte, produits):
    ajouter_depuis_catalogue(inventory_page, contexte, produits)


@when(parsers.parse('je retire le produit "{produits}" depuis le catalogue'))
@when(parsers.parse('je retire les produits "{produits}" depuis le catalogue'))
def retirer_du_catalogue(inventory_page, contexte, produits):
    for nom in liste_produits(produits):
        inventory_page.cliquer_bouton_produit(nom)
        contexte["panier"].remove(nom)


@when("j'ajoute le produit au panier depuis sa fiche")
def ajouter_depuis_fiche(product_page):
    product_page.cliquer_bouton_panier()


@then("la fiche indique que le produit est ajouté au panier")
def fiche_produit_ajoute(product_page, donnees):
    expect(product_page.bouton_panier).to_have_text(donnees["boutons"]["retirer"])


@then(parsers.parse('le produit "{nom}" est indiqué comme ajouté au panier'))
def produit_ajoute(inventory_page, donnees, nom):
    expect(inventory_page.bouton_produit(nom)).to_have_text(donnees["boutons"]["retirer"])


@then(parsers.parse('le produit "{nom}" est indiqué comme disponible à l\'ajout'))
def produit_disponible(inventory_page, donnees, nom):
    expect(inventory_page.bouton_produit(nom)).to_have_text(donnees["boutons"]["ajouter"])


@then("tous les produits sont indiqués comme disponibles à l'ajout")
def tous_disponibles(inventory_page, donnees):
    for produit in donnees["produits"]:
        produit_disponible(inventory_page, donnees, produit["nom"])


@given("j'ouvre le panier")
@when("j'ouvre le panier")
def ouvrir_panier(inventory_page, cart_page):
    inventory_page.ouvrir_panier()
    cart_page.a_charge()


@when(parsers.parse('je retire le produit "{nom}" depuis la page panier'))
def retirer_du_panier(cart_page, contexte, nom):
    cart_page.retirer(nom)
    contexte["panier"].remove(nom)


@then(parsers.parse('le panier ne contient pas le produit "{nom}"'))
def panier_sans_produit(cart_page, nom):
    expect(cart_page.article(nom)).to_have_count(0)


@then(parsers.parse(
    'le panier contient exactement les produits "{produits}" au prix du référentiel et en quantité {quantite:d}'
))
def contenu_panier(cart_page, donnees, produits, quantite):
    noms = liste_produits(produits)
    expect(cart_page.noms).to_have_text(noms)
    attendu = [
        {"nom": nom, "prix": formater_prix(prix_reference(donnees, nom)), "quantite": str(quantite)}
        for nom in noms
    ]
    assert cart_page.lignes() == attendu


@when("je continue mes achats")
def continuer_achats(cart_page, inventory_page):
    cart_page.continuer_achats()
    inventory_page.a_charge()


@when("je réinitialise l'application depuis le menu")
def reinitialiser(inventory_page, contexte):
    inventory_page.reinitialiser_application()
    contexte["panier"].clear()
