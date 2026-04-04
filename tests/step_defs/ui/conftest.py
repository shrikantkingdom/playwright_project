"""
tests/step_defs/ui/conftest.py
Shared UI step definitions available to all UI step modules.

Defines the common 'Given I am logged in' step used as a Background
in navigation and cart feature files.
"""

from pytest_bdd import given, parsers

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


@given(
    parsers.parse('I am logged in as "{username}" with password "{password}"'),
    target_fixture="inventory_page",
)
def given_logged_in(page, config, username, password):
    """Log in to SauceDemo and return an InventoryPage object."""
    login_page = LoginPage(page)
    login_page.open(config.ui_base_url)
    login_page.login(username, password)
    page.wait_for_url("**/inventory.html")
    return InventoryPage(page)
