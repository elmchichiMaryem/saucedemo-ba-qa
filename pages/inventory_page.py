"""Page catalogue (« Products »)."""
from playwright.sync_api import Locator, Page

from pages.base_page import BasePage


class InventoryPage(BasePage):
    chemin = "/inventory.html"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.selecteur_tri = page.get_by_test_id("product-sort-container")
        self.tri_actif = page.get_by_test_id("active-option")
        self.produits = page.get_by_test_id("inventory-item")
        self.noms = page.get_by_test_id("inventory-item-name")
        self.prix = page.get_by_test_id("inventory-item-price")
        self.boutons_retirer = page.locator("[data-test^='remove']")

    def marqueur(self) -> Locator:
        return self.selecteur_tri

    def produit(self, nom: str) -> Locator:
        """Carte du produit, retrouvée par son nom (indépendant de l'ordre d'affichage)."""
        return self.produits.filter(
            has=self.page.get_by_test_id("inventory-item-name").get_by_text(nom, exact=True)
        )

    def bouton_produit(self, nom: str) -> Locator:
        # Balise <button> : le nom et l'image du produit sont aussi des liens role="button".
        return self.produit(nom).locator("button")

    def cliquer_bouton_produit(self, nom: str) -> None:
        self.bouton_produit(nom).click()

    def ouvrir_fiche(self, nom: str) -> None:
        self.produit(nom).get_by_test_id("inventory-item-name").click()

    def trier_par(self, libelle: str) -> None:
        self.selecteur_tri.select_option(label=libelle)

    def liste_noms(self) -> list[str]:
        return self.noms.all_inner_texts()

    def liste_prix(self) -> list[float]:
        return [float(p.lstrip("$")) for p in self.prix.all_inner_texts()]

    def infos_produit(self, nom: str) -> dict:
        carte = self.produit(nom)
        return {
            "nom": carte.get_by_test_id("inventory-item-name").inner_text(),
            "description": carte.get_by_test_id("inventory-item-desc").inner_text(),
            "prix": carte.get_by_test_id("inventory-item-price").inner_text(),
        }
