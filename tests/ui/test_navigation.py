"""
tests/ui/test_navigation.py
UI tests for product listing, sorting, and navigation.

Markers: ui, smoke, regression
"""

import pytest

from pages.inventory_page import InventoryPage


@pytest.mark.ui
@pytest.mark.smoke
class TestInventoryPage:
    """Tests for the main product/inventory page."""

    def test_inventory_loads_with_products(self, authenticated_page):
        """Inventory page should load and display at least one product."""
        inventory = InventoryPage(authenticated_page)
        assert inventory.is_loaded(), "Inventory container should be visible"
        assert inventory.get_product_count() > 0, "At least one product should be displayed"

    def test_expected_product_count(self, authenticated_page):
        """SauceDemo always ships exactly 6 products."""
        inventory = InventoryPage(authenticated_page)
        assert inventory.get_product_count() == 6, "SauceDemo should show 6 products"

    def test_product_names_are_non_empty(self, authenticated_page):
        """Every product should have a non-empty name."""
        inventory = InventoryPage(authenticated_page)
        names = inventory.get_product_names()
        assert all(name.strip() for name in names), "All product names should be non-empty"

    def test_product_prices_are_displayed(self, authenticated_page):
        """Every product should have a price starting with '$'."""
        inventory = InventoryPage(authenticated_page)
        prices = inventory.get_product_prices()
        assert all(p.startswith("$") for p in prices), "All prices should start with $"


@pytest.mark.ui
@pytest.mark.regression
class TestProductSorting:
    """Tests for the product sort dropdown."""

    def test_sort_by_name_z_to_a(self, authenticated_page):
        """Sorting Z→A should place 'Test.allTheThings()' first."""
        inventory = InventoryPage(authenticated_page)
        inventory.sort_products("za")
        names = inventory.get_product_names()
        assert names == sorted(names, reverse=True), "Products should be sorted Z→A"

    def test_sort_by_name_a_to_z(self, authenticated_page):
        """Default A→Z sort should produce an ascending name list."""
        inventory = InventoryPage(authenticated_page)
        inventory.sort_products("az")
        names = inventory.get_product_names()
        assert names == sorted(names), "Products should be sorted A→Z"

    def test_sort_by_price_low_to_high(self, authenticated_page):
        """Price low→high sort should produce ascending prices."""
        inventory = InventoryPage(authenticated_page)
        inventory.sort_products("lohi")
        prices = inventory.get_product_prices()
        numeric = [float(p.replace("$", "")) for p in prices]
        assert numeric == sorted(numeric), "Prices should be ascending after lohi sort"

    def test_sort_by_price_high_to_low(self, authenticated_page):
        """Price high→low sort should produce descending prices."""
        inventory = InventoryPage(authenticated_page)
        inventory.sort_products("hilo")
        prices = inventory.get_product_prices()
        numeric = [float(p.replace("$", "")) for p in prices]
        assert numeric == sorted(numeric, reverse=True), "Prices should be descending after hilo sort"
