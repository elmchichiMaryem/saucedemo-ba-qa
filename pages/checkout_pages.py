"""Pages du tunnel de commande : informations client, récapitulatif, confirmation."""
from playwright.sync_api import Locator, Page

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    """Éléments communs aux deux étapes de commande (bouton « Cancel »)."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.bouton_annuler = page.get_by_test_id("cancel")

    def annuler(self) -> None:
        self.bouton_annuler.click()


class CheckoutInfoPage(CheckoutPage):
    """Étape 1 : « Checkout: Your Information »."""

    chemin = "/checkout-step-one.html"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.champ_prenom = page.get_by_test_id("firstName")
        self.champ_nom = page.get_by_test_id("lastName")
        self.champ_code_postal = page.get_by_test_id("postalCode")
        self.bouton_continuer = page.get_by_test_id("continue")

    def marqueur(self) -> Locator:
        return self.champ_prenom

    def saisir(self, prenom: str, nom: str, code_postal: str) -> None:
        # Saisie touche par touche, comme un utilisateur réel : c'est ce qui
        # révèle BUG-09 (problem_user) et BUG-11 (error_user).
        for champ, valeur in (
            (self.champ_prenom, prenom),
            (self.champ_nom, nom),
            (self.champ_code_postal, code_postal),
        ):
            champ.clear()
            champ.press_sequentially(valeur)

    def valeurs(self) -> dict:
        return {
            "prenom": self.champ_prenom.input_value(),
            "nom": self.champ_nom.input_value(),
            "code_postal": self.champ_code_postal.input_value(),
        }

    def continuer(self) -> None:
        self.bouton_continuer.click()


class CheckoutOverviewPage(CheckoutPage):
    """Étape 2 : « Checkout: Overview »."""

    chemin = "/checkout-step-two.html"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.noms = page.get_by_test_id("inventory-item-name")
        self.paiement = page.get_by_test_id("payment-info-value")
        self.livraison = page.get_by_test_id("shipping-info-value")
        self.sous_total = page.get_by_test_id("subtotal-label")
        self.taxe = page.get_by_test_id("tax-label")
        self.total = page.get_by_test_id("total-label")
        self.bouton_terminer = page.get_by_test_id("finish")

    def marqueur(self) -> Locator:
        return self.bouton_terminer

    def terminer(self) -> None:
        self.bouton_terminer.click()


class CheckoutCompletePage(BasePage):
    """Confirmation : « Checkout: Complete! »."""

    chemin = "/checkout-complete.html"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.message = page.get_by_test_id("complete-header")
        self.bouton_accueil = page.get_by_test_id("back-to-products")

    def marqueur(self) -> Locator:
        return self.message

    def revenir_accueil(self) -> None:
        self.bouton_accueil.click()
