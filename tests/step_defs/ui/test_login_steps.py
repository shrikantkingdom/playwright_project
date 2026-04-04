"""
tests/step_defs/ui/test_login_steps.py
Step definitions for features/ui/login.feature.
"""

from pathlib import Path

from pytest_bdd import given, parsers, scenarios, then, when

from pages.login_page import LoginPage

FEATURES_DIR = Path(__file__).parent.parent.parent.parent / "features"
scenarios(str(FEATURES_DIR / "ui" / "login.feature"))


# ── Given ─────────────────────────────────────────────────────────────────────


@given("I am on the login page", target_fixture="login_page")
def given_on_login_page(page, config):
    """Navigate to the SauceDemo login page and return a LoginPage object."""
    lp = LoginPage(page)
    lp.open(config.ui_base_url)
    return lp


# ── When ──────────────────────────────────────────────────────────────────────


@when(parsers.parse('I login with username "{username}" and password "{password}"'))
def when_login(login_page, username, password):
    login_page.login(username, password)


@when("I click login without entering credentials")
def when_click_login_empty(login_page):
    login_page.click_login()


@when(parsers.parse('I enter username "{username}" and click login without a password'))
def when_login_no_password(login_page, username):
    login_page.enter_username(username).click_login()


@when("I logout from the application")
def when_logout(inventory_page):
    inventory_page.logout()


# ── Then ──────────────────────────────────────────────────────────────────────


@then("I should be redirected to the inventory page")
def then_on_inventory_page(page):
    page.wait_for_url("**/inventory.html")
    assert "inventory.html" in page.url, "Should redirect to inventory page after login"


@then(parsers.parse('the page title should be "{title}"'))
def then_page_title(login_page, title):
    assert login_page.get_title() == title


@then(parsers.parse('I should see the error message containing "{text}"'))
def then_see_error_containing(login_page, text):
    error = login_page.get_error_message()
    assert text.lower() in error.lower(), f"Expected '{text}' in error message, got: '{error}'"


@then("I should not be redirected to the inventory page")
def then_not_on_inventory(page, login_page):
    assert login_page.is_error_displayed(), "Error message should be visible"
    assert "inventory.html" not in page.url, "Should NOT redirect on invalid login"


@then("I should see an error about missing username")
def then_missing_username_error(login_page):
    error = login_page.get_error_message()
    assert "username" in error.lower(), f"Expected username error, got: '{error}'"


@then("I should see an error about missing password")
def then_missing_password_error(login_page):
    error = login_page.get_error_message()
    assert "password" in error.lower(), f"Expected password error, got: '{error}'"


@then("I should be on the login page")
def then_on_login_page(page, config):
    page.wait_for_url("**/")
    assert page.url.startswith(config.ui_base_url), "Should be on the SauceDemo login page"
    assert "inventory.html" not in page.url, "Should NOT be on the inventory page"
