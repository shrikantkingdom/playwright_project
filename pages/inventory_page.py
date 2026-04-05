"""
pages/inventory_page.py
Page Object for the SauceDemo products / inventory page.
"""

from playwright.sync_api import Page

from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class InventoryPage(BasePage):
    """Encapsulates interactions with the SauceDemo inventory/products page."""

    # ── Selectors ─────────────────────────────────────────────────────────────
    INVENTORY_CONTAINER = ".inventory_container"
    INVENTORY_ITEMS = ".inventory_item"
    ITEM_TITLE = ".inventory_item_name"
    ITEM_PRICE = ".inventory_item_price"
    ADD_TO_CART_BUTTON = "[data-test^='add-to-cart']"
    CART_BADGE = ".shopping_cart_badge"
    CART_ICON = ".shopping_cart_link"
    SORT_DROPDOWN = "[data-test='product-sort-container']"
    BURGER_MENU = "#react-burger-menu-btn"
    LOGOUT_LINK = "#logout_sidebar_link"
    PAGE_TITLE = ".title"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # ── Helpers ───────────────────────────────────────────────────────────────

    def is_loaded(self) -> bool:
        """Return True when the inventory container is visible."""
        return self.page.locator(self.INVENTORY_CONTAINER).is_visible()

    def get_product_names(self) -> list[str]:
        """Return a list of all visible product names."""
        return self.page.locator(self.ITEM_TITLE).all_inner_texts()

    def get_product_prices(self) -> list[str]:
        """Return a list of all visible product prices (as strings)."""
        return self.page.locator(self.ITEM_PRICE).all_inner_texts()

    def get_product_count(self) -> int:
        """Return the number of products displayed."""
        return self.page.locator(self.INVENTORY_ITEMS).count()

    # ── Actions ───────────────────────────────────────────────────────────────

    def add_item_to_cart(self, item_index: int = 0) -> str:
        """
        Add the product at *item_index* to the cart.
        Returns the product name that was added.
        """
        items = self.page.locator(self.INVENTORY_ITEMS)
        item = items.nth(item_index)
        product_name = item.locator(self.ITEM_TITLE).inner_text()
        item.locator("[data-test^='add-to-cart']").click()
        logger.info("Added '%s' to cart", product_name)
        return product_name

    def get_cart_badge_count(self) -> int:
        """Return the integer cart item count shown on the cart icon."""
        badge = self.page.locator(self.CART_BADGE)
        if badge.is_visible():
            return int(badge.inner_text())
        return 0

    def go_to_cart(self) -> None:
        """Click the cart icon to navigate to the cart page."""
        self.page.click(self.CART_ICON)

    def sort_products(self, option_value: str) -> None:
        """
        Sort products using the dropdown.
        *option_value* examples: 'az', 'za', 'lohi', 'hilo'
        """
        self.page.select_option(self.SORT_DROPDOWN, option_value)
        logger.info("Sorted products by: %s", option_value)

    def logout(self) -> None:
        """Open the burger menu and click Logout."""
        self.page.click(self.BURGER_MENU)
        self.page.click(self.LOGOUT_LINK)
        logger.info("Logged out")
