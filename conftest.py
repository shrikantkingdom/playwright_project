"""
conftest.py  (root)
Top-level pytest fixtures shared across ALL tests.

Fixtures defined here:
- config          – active BaseConfig instance
- api_client      – JSONPlaceholderClient (session-scoped)
- browser_context – Playwright BrowserContext with video/trace/screenshot support
- page             – Playwright Page derived from browser_context
- authenticated_page – Page already logged into SauceDemo
"""

import os
from pathlib import Path

import pytest
from playwright.sync_api import BrowserContext, Page, sync_playwright

from api_clients.json_placeholder_client import JSONPlaceholderClient
from config.base_config import get_config, BaseConfig
from pages.login_page import LoginPage
from utils.helpers import ensure_dir
from utils.logger import get_logger

logger = get_logger(__name__)


# ── Configuration ─────────────────────────────────────────────────────────────


@pytest.fixture(scope="session")
def config() -> BaseConfig:
    """Return the active configuration object (read once per session)."""
    cfg = get_config()
    logger.info(
        "Test session config: env=%s  browser=%s  headless=%s",
        os.getenv("ENV", "qa"),
        cfg.browser,
        cfg.headless,
    )
    return cfg


# ── API client ────────────────────────────────────────────────────────────────


@pytest.fixture(scope="session")
def api_client(config: BaseConfig) -> JSONPlaceholderClient:
    """
    Session-scoped API client.  A single httpx connection pool is reused
    for the whole test session, then closed on teardown.
    """
    client = JSONPlaceholderClient(base_url=config.api_base_url, token=config.api_token)
    yield client
    client.close()


# ── Playwright browser / context / page ──────────────────────────────────────


@pytest.fixture(scope="session")
def playwright_instance():
    """Start a single Playwright instance for the session."""
    with sync_playwright() as pw:
        yield pw


@pytest.fixture(scope="session")
def browser(playwright_instance, config: BaseConfig):
    """Launch the configured browser (session-scoped)."""
    launch_options = {"headless": config.headless, "slow_mo": config.slow_mo}

    browser_map = {
        "chromium": playwright_instance.chromium,
        "firefox": playwright_instance.firefox,
        "webkit": playwright_instance.webkit,
    }
    browser_launcher = browser_map.get(config.browser.lower(), playwright_instance.chromium)
    browser = browser_launcher.launch(**launch_options)
    logger.info("Browser launched: %s", config.browser)
    yield browser
    browser.close()


@pytest.fixture
def browser_context(browser, config: BaseConfig, request) -> BrowserContext:
    """
    Function-scoped BrowserContext with:
    - Video recording  → reports/videos/
    - Trace collection → reports/traces/
    Cleans up and saves artefacts after each test.
    """
    video_dir = ensure_dir("reports/videos")
    trace_dir = ensure_dir("reports/traces")

    context = browser.new_context(
        viewport={"width": 1280, "height": 720},
        record_video_dir=str(video_dir),
    )
    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield context

    # ── Teardown ──────────────────────────────────────────────────────────────
    test_name = request.node.name.replace("/", "_").replace(" ", "_")
    trace_path = trace_dir / f"{test_name}.zip"
    context.tracing.stop(path=str(trace_path))
    logger.info("Trace saved: %s", trace_path)
    context.close()


@pytest.fixture
def page(browser_context: BrowserContext, config: BaseConfig) -> Page:
    """Function-scoped Page with default timeout set from config."""
    p = browser_context.new_page()
    p.set_default_timeout(config.default_timeout)
    yield p
    p.close()


@pytest.fixture
def authenticated_page(page: Page, config: BaseConfig) -> Page:
    """
    Function-scoped Page that is already logged in to SauceDemo.
    Tests that need an authenticated session should use this fixture.
    """
    login = LoginPage(page)
    login.open(config.ui_base_url)
    login.login(config.sauce_username, config.sauce_password)
    # Wait until the inventory page is loaded
    page.wait_for_url("**/inventory.html")
    logger.info("Authenticated page ready for test")
    yield page


# ── Screenshot on failure ─────────────────────────────────────────────────────


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture a screenshot when any UI test fails."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        # Only for tests that have the `page` fixture
        page_fixture: Page = item.funcargs.get("page") or item.funcargs.get("authenticated_page")
        if page_fixture is not None:
            screenshot_dir = ensure_dir("reports/screenshots")
            safe_name = item.name.replace("/", "_").replace(" ", "_")
            screenshot_path = screenshot_dir / f"FAILED_{safe_name}.png"
            try:
                page_fixture.screenshot(path=str(screenshot_path), full_page=True)
                logger.warning("Screenshot on failure: %s", screenshot_path)
            except Exception as exc:  # noqa: BLE001
                logger.warning("Could not capture failure screenshot: %s", exc)
