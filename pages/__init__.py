"""Page Object Model de Swag Labs : une classe par page de l'application."""
from pages.base_page import BasePage
from pages.cart_page import CartPage
from pages.checkout_pages import (
    CheckoutCompletePage,
    CheckoutInfoPage,
    CheckoutPage,
    CheckoutOverviewPage,
)
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from pages.product_page import ProductPage

__all__ = [
    "BasePage",
    "CartPage",
    "CheckoutCompletePage",
    "CheckoutInfoPage",
    "CheckoutPage",
    "CheckoutOverviewPage",
    "InventoryPage",
    "LoginPage",
    "ProductPage",
]
