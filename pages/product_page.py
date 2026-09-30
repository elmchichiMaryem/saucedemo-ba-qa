"""Fiche détail d'un produit."""
from playwright.sync_api import Locator, Page

from pages.base_page import BasePage


class ProductPage(BasePage):
    chemin = "/inventory-item.html"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.nom = page.get_by_test_id("inventory-item-name")
        self.description = page.get_by_test_id("inventory-item-desc")
        self.prix = page.get_by_test_id("inventory-item-price")
        self.bouton_panier = page.locator("[data-test='add-to-cart'], [data-test='remove']")
        self.bouton_retour = page.get_by_test_id("back-to-products")

    def marqueur(self) -> Locator:
        return self.bouton_retour

    def infos(self) -> dict:
        return {
            "nom": self.nom.inner_text(),
            "description": self.description.inner_text(),
            "prix": self.prix.inner_text(),
        }

    def cliquer_bouton_panier(self) -> None:
        self.bouton_panier.click()

    def revenir_au_catalogue(self) -> None:
        self.bouton_retour.click()
