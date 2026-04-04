"""
tests/step_defs/ui/test_cart_steps.py
Step definitions for features/ui/cart.feature.
"""

from pathlib import Path

from pytest_bdd import parsers, scenarios, then, when

from data.test_data import CheckoutData
from pages.cart_page import CartPage

FEATURES_DIR = Path(__file__).parent.parent.parent.parent / "features"
scenarios(str(FEATURES_DIR / "ui" / "cart.feature"))


# ── When ──────────────────────────────────────────────────────────────────────


@when(parsers.parse("I add the item at index {index:d} to the cart"))
def when_add_item(inventory_page, index):
    inventory_page.add_item_to_cart(index)


@when("I navigate to the cart", target_fixture="cart_page")
def when_navigate_to_cart(inventory_page, page):
    """Go to the cart page and return a CartPage object."""
    inventory_page.go_to_cart()
    return CartPage(page)


@when("I remove the first item from the cart")
def when_remove_first_item(cart_page):
    cart_page.remove_first_item()


@when("I click checkout")
def when_click_checkout(cart_page):
    cart_page.click_checkout()


@when("I fill in checkout information")
def when_fill_checkout(cart_page):
    info = CheckoutData.valid_info()
    cart_page.fill_checkout_info(info["first_name"], info["last_name"], info["postal_code"])


@when("I finish the checkout")
def when_finish_checkout(cart_page):
    cart_page.finish_checkout()


# ── Then ──────────────────────────────────────────────────────────────────────


@then(parsers.parse("the cart badge should show {count:d}"))
def then_cart_badge(inventory_page, count):
    actual = inventory_page.get_cart_badge_count()
    assert actual == count, f"Expected cart badge to show {count}, got {actual}"


@then(parsers.re(r"the cart should contain (?P<count>\d+) items?"))
def then_cart_item_count(cart_page, count):
    actual = cart_page.get_cart_item_count()
    assert actual == int(count), f"Expected {count} item(s) in cart, got {actual}"


@then("I should see the order confirmation")
def then_order_confirmation(cart_page):
    msg = cart_page.get_order_confirmation_message()
    assert "Thank you" in msg, f"Expected order confirmation, got: '{msg}'"
