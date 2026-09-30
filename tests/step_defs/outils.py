"""Fonctions utilitaires partagées par les step definitions."""
from decimal import ROUND_HALF_UP, Decimal

from playwright.sync_api import expect


def liste_produits(texte: str) -> list[str]:
    """``"A, B, C"`` → ``["A", "B", "C"]`` (les noms de produits ne contiennent pas de virgule)."""
    return [nom.strip() for nom in texte.split(",") if nom.strip()]


def prix_reference(donnees: dict, nom: str) -> Decimal:
    prix = next(p["prix"] for p in donnees["produits"] if p["nom"] == nom)
    return Decimal(str(prix))


def formater_prix(montant) -> str:
    """Format d'affichage de l'application : ``$29.99``."""
    return f"${Decimal(str(montant)):.2f}"


def arrondi_centime(montant: Decimal) -> Decimal:
    return montant.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def verifier_page(page_object, nom: str, donnees: dict, base_url: str) -> None:
    """Vérifie qu'une page est affichée : élément marqueur, URL et titre éventuel."""
    page_object.a_charge()
    expect(page_object.page).to_have_url(base_url + page_object.chemin)
    titre = donnees["titres"].get(nom)
    if titre:
        expect(page_object.titre).to_have_text(titre)
