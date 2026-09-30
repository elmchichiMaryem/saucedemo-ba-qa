"""Étapes du catalogue : affichage, prix, fiche produit, tri."""
from pytest_bdd import given, parsers, then, when
from playwright.sync_api import expect

from tests.step_defs.outils import formater_prix


def verifier_tri(inventory_page, donnees, tri: str) -> None:
    regle = donnees["tris"][tri]
    expect(inventory_page.tri_actif).to_have_text(regle["libelle"])
    valeurs = inventory_page.liste_noms() if regle["critere"] == "nom" else inventory_page.liste_prix()
    assert valeurs == sorted(valeurs, reverse=regle["decroissant"]), (
        f"Ordre attendu : {regle['libelle']} ; ordre obtenu : {valeurs}"
    )


@then("le catalogue affiche tous les produits du référentiel avec image, nom, description, prix et bouton d'ajout")
def catalogue_complet(inventory_page, donnees):
    expect(inventory_page.produits).to_have_count(len(donnees["produits"]))
    for produit in donnees["produits"]:
        carte = inventory_page.produit(produit["nom"])
        expect(carte.get_by_role("img")).to_be_visible()
        expect(carte.get_by_test_id("inventory-item-desc")).not_to_be_empty()
        expect(carte.get_by_test_id("inventory-item-price")).to_be_visible()
        expect(inventory_page.bouton_produit(produit["nom"])).to_have_text(donnees["boutons"]["ajouter"])


@then("le tri par défaut est appliqué")
def tri_par_defaut(inventory_page, donnees):
    verifier_tri(inventory_page, donnees, donnees["tri_par_defaut"])


@then("chaque produit est affiché au prix du référentiel")
def prix_conformes(inventory_page, donnees):
    for produit in donnees["produits"]:
        prix = inventory_page.produit(produit["nom"]).get_by_test_id("inventory-item-price")
        expect(prix).to_have_text(formater_prix(produit["prix"]))


@given(parsers.parse('j\'ouvre la fiche du produit "{nom}"'))
@when(parsers.parse('j\'ouvre la fiche du produit "{nom}"'))
def ouvrir_fiche(inventory_page, product_page, contexte, nom):
    contexte["infos_catalogue"] = inventory_page.infos_produit(nom)
    inventory_page.ouvrir_fiche(nom)
    product_page.a_charge()


@then(parsers.parse('la fiche du produit "{nom}" affiche les mêmes informations que le catalogue'))
def fiche_coherente(product_page, contexte, nom):
    expect(product_page.nom).to_have_text(nom)
    assert product_page.infos() == contexte["infos_catalogue"]


@when("je reviens au catalogue depuis la fiche")
def revenir_catalogue(product_page, inventory_page):
    product_page.revenir_au_catalogue()
    inventory_page.a_charge()


@when(parsers.parse('je trie le catalogue par "{tri}"'))
def trier(inventory_page, donnees, tri):
    inventory_page.trier_par(donnees["tris"][tri]["libelle"])


@then(parsers.parse('les produits sont triés par "{tri}"'))
def produits_tries(inventory_page, donnees, tri):
    verifier_tri(inventory_page, donnees, tri)
