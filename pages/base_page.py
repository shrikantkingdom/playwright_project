"""
pages/base_page.py
Base class for all Page Objects.  Provides common interactions and
screenshot capture utilities.
"""

from pathlib import Path

from playwright.sync_api import Page

from utils.helpers import ensure_dir, timestamp
from utils.logger import get_logger

logger = get_logger(__name__)


class BasePage:
    """
    All page-object classes inherit from BasePage.

    Provides:
    - Common navigation helpers
    - Element wait helpers
    - Screenshot capture on demand / failure
    """

    def __init__(self, page: Page) -> None:
        self.page = page

    # ── Navigation ───────────────────────────────────────────────────────────

    def navigate(self, url: str) -> None:
        """Navigate to the given URL and wait until the network is idle."""
        logger.info("Navigating to: %s", url)
        self.page.goto(url, wait_until="networkidle")

    def get_current_url(self) -> str:
        """Return the current page URL."""
        return self.page.url

    def get_title(self) -> str:
        """Return the current page title."""
        return self.page.title()

    # ── Wait helpers ─────────────────────────────────────────────────────────

    def wait_for_selector(self, selector: str, timeout: int = 10_000) -> None:
        """Block until *selector* is visible."""
        self.page.wait_for_selector(selector, state="visible", timeout=timeout)

    def wait_for_url(self, url_pattern: str, timeout: int = 10_000) -> None:
        """Block until the URL matches *url_pattern*."""
        self.page.wait_for_url(url_pattern, timeout=timeout)

    # ── Screenshots ──────────────────────────────────────────────────────────

    def take_screenshot(self, name: str = "", directory: str = "reports/screenshots") -> Path:
        """
        Capture a PNG screenshot.  Returns the path written to disk.
        """
        ensure_dir(directory)
        file_name = f"{name}_{timestamp()}.png" if name else f"screenshot_{timestamp()}.png"
        path = Path(directory) / file_name
        self.page.screenshot(path=str(path), full_page=True)
        logger.info("Screenshot saved: %s", path)
        return path
