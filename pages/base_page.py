"""Page de base : éléments communs à toutes les pages connectées (en-tête, menu, panier)."""
from playwright.sync_api import Locator, Page, expect


class BasePage:
    """Classe mère des Page Objects.

    Les sélecteurs utilisent l'attribut ``data-test`` (via ``get_by_test_id``),
    configuré comme attribut de test dans ``conftest.py``.
    """

    #: Chemin de la page, relatif à ``base_url`` (défini par chaque sous-classe).
    chemin = "/"

    def __init__(self, page: Page) -> None:
        self.page = page
        self.titre = page.get_by_test_id("title")
        self.lien_panier = page.get_by_test_id("shopping-cart-link")
        self.badge_panier = page.get_by_test_id("shopping-cart-badge")
        self.bouton_menu = page.locator("#react-burger-menu-btn")
        self.bouton_fermer_menu = page.locator("#react-burger-cross-btn")
        self.lien_deconnexion = page.get_by_test_id("logout-sidebar-link")
        self.lien_reinitialisation = page.get_by_test_id("reset-sidebar-link")
        self.message_erreur = page.get_by_test_id("error")

    # --- Chargement -------------------------------------------------------
    def marqueur(self) -> Locator:
        """Élément dont la présence prouve que la page est affichée."""
        return self.titre

    def a_charge(self):
        """Attend que la page soit réellement affichée.

        L'application est une SPA React : l'URL change avant le rendu. On attend
        donc un élément propre à la page plutôt que l'URL ou une pause fixe.
        """
        expect(self.marqueur()).to_be_visible()
        return self

    def attendre_rendu(self) -> None:
        """Laisse React terminer son rendu (deux images d'affichage).

        Utile avant de vérifier qu'un clic n'a PAS changé de page : sans cela,
        l'assertion pourrait réussir avant même que la navigation ait lieu.
        """
        self.page.evaluate(
            "() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)))"
        )

    def ouvrir(self):
        self.page.goto(self.chemin)
        return self

    # --- Menu latéral -----------------------------------------------------
    def _cliquer_dans_menu(self, lien: Locator) -> None:
        self.bouton_menu.click()
        expect(lien).to_be_visible()
        lien.click()

    def se_deconnecter(self) -> None:
        self._cliquer_dans_menu(self.lien_deconnexion)

    def reinitialiser_application(self) -> None:
        self._cliquer_dans_menu(self.lien_reinitialisation)
        self.bouton_fermer_menu.click()

    # --- Panier -----------------------------------------------------------
    def ouvrir_panier(self) -> None:
        self.lien_panier.click()
