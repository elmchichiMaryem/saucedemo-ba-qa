"""Page de connexion."""
from playwright.sync_api import Locator, Page

from pages.base_page import BasePage


class LoginPage(BasePage):
    chemin = "/"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.champ_identifiant = page.get_by_test_id("username")
        self.champ_mot_de_passe = page.get_by_test_id("password")
        self.bouton_connexion = page.get_by_test_id("login-button")

    def marqueur(self) -> Locator:
        return self.bouton_connexion

    def se_connecter(self, identifiant: str, mot_de_passe: str) -> None:
        self.champ_identifiant.fill(identifiant)
        self.champ_mot_de_passe.fill(mot_de_passe)
        self.bouton_connexion.click()
