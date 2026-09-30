"""Configuration globale de la suite pytest-bdd + Playwright.

- chargement des données de test (data/test_data.json) ;
- fixtures Page Object et fixture de connexion ;
- conversion des tags @BUG-xx en xfail strict ;
- capture d'écran automatique en cas d'échec, jointe au rapport HTML.
"""
import base64
import json
import re
from functools import lru_cache
from pathlib import Path

import pytest
import pytest_html

from pages import (
    CartPage,
    CheckoutCompletePage,
    CheckoutInfoPage,
    CheckoutOverviewPage,
    CheckoutPage,
    InventoryPage,
    LoginPage,
    ProductPage,
)

RACINE = Path(__file__).parent
FICHIER_DONNEES = RACINE / "data" / "test_data.json"
DOSSIER_CAPTURES = RACINE / "reports" / "captures"

# Les step definitions sont des modules « plugins » : leurs étapes sont
# visibles par tous les scénarios, sans duplication.
pytest_plugins = [
    "tests.step_defs.commun_steps",
    "tests.step_defs.catalogue_steps",
    "tests.step_defs.panier_steps",
    "tests.step_defs.commande_steps",
]


@lru_cache(maxsize=1)
def charger_donnees() -> dict:
    return json.loads(FICHIER_DONNEES.read_text(encoding="utf-8"))


# --- Hooks pytest -----------------------------------------------------------
def pytest_configure(config):
    for bug in charger_donnees()["anomalies"]:
        config.addinivalue_line("markers", f"{bug}: anomalie connue (voir docs/qa/04_rapports_anomalies.md)")


def pytest_collection_modifyitems(config, items):
    """Transforme chaque tag @BUG-xx (scénario ou bloc Examples) en xfail strict."""
    anomalies = charger_donnees()["anomalies"]
    for item in items:
        for bug in sorted({m.name for m in item.iter_markers() if m.name.startswith("BUG-")}):
            item.add_marker(pytest.mark.xfail(reason=f"{bug} : {anomalies[bug]}", strict=True))


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture d'écran si le test échoue (ou échoue comme attendu : preuve du bug)."""
    resultat = yield
    rapport = resultat.get_result()
    page = getattr(item, "_page", None)
    if rapport.when != "call" or page is None:
        return
    if not (rapport.failed or hasattr(rapport, "wasxfail")):
        return
    DOSSIER_CAPTURES.mkdir(parents=True, exist_ok=True)
    nom = re.sub(r"[^\w.-]+", "_", item.name)[:150]
    image = page.screenshot(path=DOSSIER_CAPTURES / f"{nom}.png", full_page=True)
    rapport.extras = getattr(rapport, "extras", []) + [
        pytest_html.extras.png(base64.b64encode(image).decode(), name=nom)
    ]


# --- Fixtures navigateur ----------------------------------------------------
@pytest.fixture(scope="session", autouse=True)
def attribut_de_test(playwright):
    """``get_by_test_id`` cible l'attribut ``data-test`` utilisé par Swag Labs."""
    playwright.selectors.set_test_id_attribute("data-test")


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {**browser_context_args, "viewport": {"width": 1280, "height": 800}}


@pytest.fixture(autouse=True)
def _page_pour_capture(request, page):
    """Mémorise la page du test pour le hook de capture d'écran.

    ``page`` (pytest-playwright) crée un contexte navigateur neuf par test :
    ni session ni panier ne fuient d'un scénario à l'autre.
    """
    request.node._page = page
    yield


# --- Fixtures métier --------------------------------------------------------
@pytest.fixture(scope="session")
def donnees() -> dict:
    return charger_donnees()


@pytest.fixture
def contexte() -> dict:
    """Mémoire partagée entre les étapes d'un même scénario."""
    return {"panier": []}


@pytest.fixture
def login_page(page):
    return LoginPage(page)


@pytest.fixture
def inventory_page(page):
    return InventoryPage(page)


@pytest.fixture
def product_page(page):
    return ProductPage(page)


@pytest.fixture
def cart_page(page):
    return CartPage(page)


@pytest.fixture
def checkout_page(page):
    return CheckoutPage(page)


@pytest.fixture
def checkout_info_page(page):
    return CheckoutInfoPage(page)


@pytest.fixture
def checkout_overview_page(page):
    return CheckoutOverviewPage(page)


@pytest.fixture
def checkout_complete_page(page):
    return CheckoutCompletePage(page)


@pytest.fixture
def pages_par_nom(login_page, inventory_page, cart_page, checkout_info_page,
                  checkout_overview_page, checkout_complete_page) -> dict:
    """Associe le nom métier d'une page (utilisé dans le Gherkin) à son Page Object."""
    return {
        "connexion": login_page,
        "catalogue": inventory_page,
        "panier": cart_page,
        "informations client": checkout_info_page,
        "récapitulatif": checkout_overview_page,
        "confirmation": checkout_complete_page,
    }


@pytest.fixture
def connexion(login_page, donnees):
    """Fabrique de connexion : ``connexion("standard")`` ouvre la page et se connecte."""
    def _se_connecter(compte: str) -> None:
        login_page.ouvrir().a_charge()
        login_page.se_connecter(donnees["comptes"][compte], donnees["mot_de_passe"])
    return _se_connecter
