"""
tests/ui/test_login.py
UI tests for the SauceDemo login page.

Markers: ui, smoke, regression
"""

import pytest

from data.test_data import SauceDemoUsers
from pages.login_page import LoginPage


@pytest.mark.ui
@pytest.mark.smoke
class TestLogin:
    """Tests for valid and invalid login scenarios."""

    def test_successful_login_with_standard_user(self, page, config):
        """Standard user should land on the inventory page after login."""
        login_page = LoginPage(page)
        login_page.open(config.ui_base_url)
        login_page.login(
            SauceDemoUsers.STANDARD["username"],
            SauceDemoUsers.STANDARD["password"],
        )
        page.wait_for_url("**/inventory.html")
        assert "inventory.html" in page.url, "Should redirect to inventory page after login"

    def test_login_page_title(self, page, config):
        """The login page should display the correct app title."""
        login_page = LoginPage(page)
        login_page.open(config.ui_base_url)
        assert page.locator(".login_logo").inner_text() == "Swag Labs"

    def test_locked_out_user_sees_error(self, page, config):
        """Locked-out user should see a descriptive error message."""
        login_page = LoginPage(page)
        login_page.open(config.ui_base_url)
        login_page.login(
            SauceDemoUsers.LOCKED_OUT["username"],
            SauceDemoUsers.LOCKED_OUT["password"],
        )
        assert login_page.is_error_displayed(), "Error message should be visible"
        assert "locked out" in login_page.get_error_message().lower()

    def test_invalid_credentials_show_error(self, page, config):
        """Invalid credentials should show an error, not redirect."""
        login_page = LoginPage(page)
        login_page.open(config.ui_base_url)
        login_page.login(
            SauceDemoUsers.INVALID["username"],
            SauceDemoUsers.INVALID["password"],
        )
        assert login_page.is_error_displayed(), "Error message should appear for invalid creds"
        assert "inventory.html" not in page.url, "Should NOT redirect to inventory on bad login"

    def test_empty_username_shows_error(self, page, config):
        """Submitting without a username should show a validation error."""
        login_page = LoginPage(page)
        login_page.open(config.ui_base_url)
        login_page.enter_password("secret_sauce")
        login_page.click_login()
        assert login_page.is_error_displayed()
        error_text = login_page.get_error_message()
        assert "username" in error_text.lower()

    def test_empty_password_shows_error(self, page, config):
        """Submitting without a password should show a validation error."""
        login_page = LoginPage(page)
        login_page.open(config.ui_base_url)
        login_page.enter_username("standard_user")
        login_page.click_login()
        assert login_page.is_error_displayed()
        error_text = login_page.get_error_message()
        assert "password" in error_text.lower()


@pytest.mark.ui
@pytest.mark.regression
class TestLogout:
    """Tests for logout functionality."""

    def test_logout_redirects_to_login(self, authenticated_page):
        """After logout, user should be redirected back to the login page."""
        from pages.inventory_page import InventoryPage

        inventory = InventoryPage(authenticated_page)
        inventory.logout()
        authenticated_page.wait_for_url("**/")
        assert "saucedemo.com" in authenticated_page.url
        assert "inventory.html" not in authenticated_page.url
