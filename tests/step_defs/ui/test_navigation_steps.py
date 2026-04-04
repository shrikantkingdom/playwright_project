"""
tests/step_defs/ui/test_navigation_steps.py
Step definitions for features/ui/navigation.feature.
"""

from pathlib import Path

from pytest_bdd import parsers, scenarios, then, when

FEATURES_DIR = Path(__file__).parent.parent.parent.parent / "features"
scenarios(str(FEATURES_DIR / "ui" / "navigation.feature"))


# ── Then ──────────────────────────────────────────────────────────────────────


@then("the inventory container should be visible")
def then_inventory_visible(inventory_page):
    assert inventory_page.is_loaded(), "Inventory container should be visible"


@then("the product list should not be empty")
def then_product_list_not_empty(inventory_page):
    assert inventory_page.get_product_count() > 0, "At least one product should be displayed"


@then(parsers.parse("I should see exactly {count:d} products"))
def then_exact_product_count(inventory_page, count):
    actual = inventory_page.get_product_count()
    assert actual == count, f"Expected {count} products, got {actual}"


@then("all product names should be non-empty")
def then_product_names_non_empty(inventory_page):
    names = inventory_page.get_product_names()
    assert all(name.strip() for name in names), "All product names should be non-empty"


@then('all product prices should start with "$"')
def then_prices_start_with_dollar(inventory_page):
    prices = inventory_page.get_product_prices()
    assert all(p.startswith("$") for p in prices), "All prices should start with '$'"


@then("the products should be sorted in descending alphabetical order")
def then_sorted_desc(inventory_page):
    names = inventory_page.get_product_names()
    assert names == sorted(names, reverse=True), "Products should be sorted Z→A"


@then("the products should be sorted in ascending alphabetical order")
def then_sorted_asc(inventory_page):
    names = inventory_page.get_product_names()
    assert names == sorted(names), "Products should be sorted A→Z"


@then("the products should be sorted by price ascending")
def then_sorted_price_asc(inventory_page):
    prices = [float(p.replace("$", "")) for p in inventory_page.get_product_prices()]
    assert prices == sorted(prices), "Prices should be ascending"


@then("the products should be sorted by price descending")
def then_sorted_price_desc(inventory_page):
    prices = [float(p.replace("$", "")) for p in inventory_page.get_product_prices()]
    assert prices == sorted(prices, reverse=True), "Prices should be descending"


# ── When ──────────────────────────────────────────────────────────────────────


@when(parsers.parse('I sort products by "{option}"'))
def when_sort_products(inventory_page, option):
    inventory_page.sort_products(option)
