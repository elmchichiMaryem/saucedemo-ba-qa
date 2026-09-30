"""Étapes communes : connexion, navigation, pages affichées, messages, badge."""
from pytest_bdd import given, parsers, then, when
from playwright.sync_api import expect

from tests.step_defs.outils import verifier_page


# --- Connexion / déconnexion ------------------------------------------------
@given("je suis sur la page de connexion")
def sur_page_connexion(login_page):
    login_page.ouvrir().a_charge()


@given("je ne suis pas connecté")
def pas_connecte():
    """Rien à faire : chaque scénario démarre dans un contexte navigateur neuf."""


@given(parsers.parse('je suis connecté avec le compte "{compte}"'))
def connecte_avec(connexion, inventory_page, compte):
    connexion(compte)
    inventory_page.a_charge()


@when(parsers.parse('je me connecte avec le compte "{compte}"'))
def se_connecter_avec(connexion, compte):
    connexion(compte)


@when(parsers.parse('je tente de me connecter avec les identifiants "{cas}"'))
def tenter_connexion(login_page, donnees, cas):
    identifiants = donnees["identifiants_invalides"][cas]
    login_page.se_connecter(identifiants["identifiant"], identifiants["mot_de_passe"])


@given("je me déconnecte depuis le menu")
@when("je me déconnecte depuis le menu")
def se_deconnecter(inventory_page, login_page):
    inventory_page.se_deconnecter()
    login_page.a_charge()


# --- Navigation et pages ----------------------------------------------------
@when(parsers.parse('j\'accède directement à la page "{nom}"'))
def acceder_directement(pages_par_nom, nom):
    pages_par_nom[nom].ouvrir()


@then(parsers.parse('la page "{nom}" est affichée'))
def page_affichee(pages_par_nom, donnees, base_url, nom):
    verifier_page(pages_par_nom[nom], nom, donnees, base_url)


@then("la page de connexion est affichée")
@then("je reste sur la page de connexion")
def page_connexion_affichee(pages_par_nom, donnees, base_url):
    verifier_page(pages_par_nom["connexion"], "connexion", donnees, base_url)


@then("je reste sur l'étape des informations client")
def reste_informations_client(pages_par_nom, donnees, base_url):
    verifier_page(pages_par_nom["informations client"], "informations client", donnees, base_url)


@then(parsers.parse('l\'accès à la page "{nom}" est refusé'))
def acces_refuse(pages_par_nom, login_page, donnees, base_url, nom):
    verifier_page(login_page, "connexion", donnees, base_url)
    message = donnees["messages"]["accès refusé"].format(chemin=pages_par_nom[nom].chemin)
    expect(login_page.message_erreur).to_have_text(message)


# --- Messages et badge ------------------------------------------------------
@then(parsers.parse('le message d\'erreur "{message}" est affiché'))
def message_erreur_affiche(login_page, donnees, message):
    # L'élément « error » a le même data-test sur toutes les pages.
    expect(login_page.message_erreur).to_have_text(donnees["messages"][message])


@then(parsers.parse("le badge du panier affiche {nombre:d}"))
def badge_affiche(inventory_page, nombre):
    expect(inventory_page.badge_panier).to_have_text(str(nombre))


@then("le badge du panier n'est pas affiché")
def badge_absent(inventory_page):
    expect(inventory_page.badge_panier).to_be_hidden()
