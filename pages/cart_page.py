"""
pages/cart_page.py
Page Object for the SauceDemo shopping cart page.
"""

from playwright.sync_api import Page

from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class CartPage(BasePage):
    """Encapsulates interactions with the SauceDemo cart page."""

    # ── Selectors ─────────────────────────────────────────────────────────────
    CART_ITEMS = ".cart_item"
    ITEM_NAME = ".inventory_item_name"
    ITEM_PRICE = ".inventory_item_price"
    REMOVE_BUTTON = "[data-test^='remove']"
    CHECKOUT_BUTTON = "[data-test='checkout']"
    CONTINUE_SHOPPING_BUTTON = "[data-test='continue-shopping']"

    # Checkout step-one selectors
    FIRST_NAME_INPUT = "[data-test='firstName']"
    LAST_NAME_INPUT = "[data-test='lastName']"
    POSTAL_CODE_INPUT = "[data-test='postalCode']"
    CONTINUE_BUTTON = "[data-test='continue']"

    # Checkout overview selectors
    FINISH_BUTTON = "[data-test='finish']"
    COMPLETE_HEADER = ".complete-header"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # ── Helpers ───────────────────────────────────────────────────────────────

    def get_cart_item_count(self) -> int:
        return self.page.locator(self.CART_ITEMS).count()

    def get_cart_item_names(self) -> list[str]:
        return self.page.locator(self.ITEM_NAME).all_inner_texts()

    # ── Actions ───────────────────────────────────────────────────────────────

    def remove_first_item(self) -> None:
        """Remove the first item from the cart."""
        self.page.locator(self.REMOVE_BUTTON).first.click()
        logger.info("Removed first item from cart")

    def click_checkout(self) -> None:
        self.page.click(self.CHECKOUT_BUTTON)

    def fill_checkout_info(self, first_name: str, last_name: str, postal_code: str) -> None:
        """Fill in the checkout step-one form."""
        self.page.fill(self.FIRST_NAME_INPUT, first_name)
        self.page.fill(self.LAST_NAME_INPUT, last_name)
        self.page.fill(self.POSTAL_CODE_INPUT, postal_code)
        self.page.click(self.CONTINUE_BUTTON)
        logger.info("Filled checkout info for %s %s", first_name, last_name)

    def finish_checkout(self) -> None:
        self.page.click(self.FINISH_BUTTON)

    def get_order_confirmation_message(self) -> str:
        return self.page.locator(self.COMPLETE_HEADER).inner_text()
