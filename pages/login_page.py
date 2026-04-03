"""
pages/login_page.py
Page Object for the SauceDemo login page (https://www.saucedemo.com).
"""

from playwright.sync_api import Page

from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class LoginPage(BasePage):
    """Encapsulates all interactions with the SauceDemo login page."""

    # ── Selectors ─────────────────────────────────────────────────────────────
    USERNAME_INPUT = "#user-name"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#login-button"
    ERROR_MESSAGE = "[data-test='error']"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # ── Actions ───────────────────────────────────────────────────────────────

    def open(self, base_url: str) -> "LoginPage":
        """Navigate to the login page."""
        self.navigate(base_url)
        return self

    def enter_username(self, username: str) -> "LoginPage":
        logger.debug("Entering username: %s", username)
        self.page.fill(self.USERNAME_INPUT, username)
        return self

    def enter_password(self, password: str) -> "LoginPage":
        logger.debug("Entering password")
        self.page.fill(self.PASSWORD_INPUT, password)
        return self

    def click_login(self) -> None:
        logger.info("Clicking login button")
        self.page.click(self.LOGIN_BUTTON)

    def login(self, username: str, password: str) -> None:
        """Convenience method: fill both fields and submit."""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    # ── Assertions / getters ──────────────────────────────────────────────────

    def get_error_message(self) -> str:
        """Return the visible error message text (empty string if absent)."""
        locator = self.page.locator(self.ERROR_MESSAGE)
        if locator.is_visible():
            return locator.inner_text()
        return ""

    def is_error_displayed(self) -> bool:
        """Return True if an error message is currently displayed."""
        return self.page.locator(self.ERROR_MESSAGE).is_visible()
