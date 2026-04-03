"""
tests/ui/test_cart.py
UI tests for the shopping cart and checkout flow.

Markers: ui, regression
"""

import pytest

from data.test_data import CheckoutData
from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage


@pytest.mark.ui
@pytest.mark.regression
class TestCartOperations:
    """Tests for adding, removing, and verifying cart items."""

    def test_add_item_to_cart_increments_badge(self, authenticated_page):
        """Adding one item should show badge count of 1."""
        inventory = InventoryPage(authenticated_page)
        inventory.add_item_to_cart(0)
        assert inventory.get_cart_badge_count() == 1

    def test_add_multiple_items_to_cart(self, authenticated_page):
        """Adding two items should show badge count of 2."""
        inventory = InventoryPage(authenticated_page)
        inventory.add_item_to_cart(0)
        inventory.add_item_to_cart(1)
        assert inventory.get_cart_badge_count() == 2

    def test_cart_contains_added_item(self, authenticated_page):
        """The cart page should list the item added from inventory."""
        inventory = InventoryPage(authenticated_page)
        product_name = inventory.add_item_to_cart(0)
        inventory.go_to_cart()

        cart = CartPage(authenticated_page)
        cart_items = cart.get_cart_item_names()
        assert product_name in cart_items, f"'{product_name}' should be in cart"

    def test_remove_item_from_cart(self, authenticated_page):
        """Removing an item from the cart should decrease item count."""
        inventory = InventoryPage(authenticated_page)
        inventory.add_item_to_cart(0)
        inventory.add_item_to_cart(1)
        inventory.go_to_cart()

        cart = CartPage(authenticated_page)
        initial_count = cart.get_cart_item_count()
        cart.remove_first_item()
        assert cart.get_cart_item_count() == initial_count - 1


@pytest.mark.ui
@pytest.mark.regression
class TestCheckoutFlow:
    """End-to-end checkout flow tests."""

    def test_complete_checkout_flow(self, authenticated_page):
        """
        Full checkout flow:
        1. Add item to cart
        2. Navigate to cart
        3. Proceed to checkout
        4. Fill shipping info
        5. Complete the order
        6. Assert order confirmation
        """
        # Add item to cart
        inventory = InventoryPage(authenticated_page)
        inventory.add_item_to_cart(0)
        inventory.go_to_cart()

        # Start checkout
        cart = CartPage(authenticated_page)
        cart.click_checkout()

        # Fill in customer information
        info = CheckoutData.valid_info()
        cart.fill_checkout_info(
            info["first_name"],
            info["last_name"],
            info["postal_code"],
        )

        # Finish order
        cart.finish_checkout()

        # Assert confirmation
        confirmation = cart.get_order_confirmation_message()
        assert "Thank you" in confirmation, f"Expected order confirmation, got: {confirmation}"
