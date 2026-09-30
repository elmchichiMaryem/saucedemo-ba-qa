"""Page panier (« Your Cart »)."""
from playwright.sync_api import Locator, Page

from pages.base_page import BasePage


class CartPage(BasePage):
    chemin = "/cart.html"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.articles = page.get_by_test_id("inventory-item")
        self.noms = page.get_by_test_id("inventory-item-name")
        self.bouton_continuer = page.get_by_test_id("continue-shopping")
        self.bouton_commander = page.get_by_test_id("checkout")

    def marqueur(self) -> Locator:
        return self.bouton_commander

    def article(self, nom: str) -> Locator:
        return self.articles.filter(
            has=self.page.get_by_test_id("inventory-item-name").get_by_text(nom, exact=True)
        )

    def lignes(self) -> list[dict]:
        return [
            {
                "nom": ligne.get_by_test_id("inventory-item-name").inner_text(),
                "prix": ligne.get_by_test_id("inventory-item-price").inner_text(),
                "quantite": ligne.get_by_test_id("item-quantity").inner_text(),
            }
            for ligne in self.articles.all()
        ]

    def retirer(self, nom: str) -> None:
        self.article(nom).locator("button").click()

    def continuer_achats(self) -> None:
        self.bouton_continuer.click()

    def commander(self) -> None:
        self.bouton_commander.click()
