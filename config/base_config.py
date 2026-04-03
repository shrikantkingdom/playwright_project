"""
config/base_config.py
Central configuration loader.  Reads from a .env file (if present) and
environment variables, then returns the correct per-environment config.
"""

import os
from dataclasses import dataclass, field

from dotenv import load_dotenv

# Load .env at import time; real env vars always win (override=False)
load_dotenv(override=False)


@dataclass
class BaseConfig:
    """Holds all tuneable settings for the test run."""

    # ── Application URLs ────────────────────────────────────────────────────
    ui_base_url: str = "https://www.saucedemo.com"
    api_base_url: str = "https://jsonplaceholder.typicode.com"

    # ── Authentication ───────────────────────────────────────────────────────
    sauce_username: str = "standard_user"
    sauce_password: str = "secret_sauce"
    api_token: str = ""

    # ── Browser settings ─────────────────────────────────────────────────────
    browser: str = "chromium"          # chromium | firefox | webkit
    headless: bool = True
    slow_mo: int = 0                   # milliseconds between actions

    # ── Timeouts ─────────────────────────────────────────────────────────────
    default_timeout: int = 30_000      # milliseconds

    # ── Retry / parallelism ──────────────────────────────────────────────────
    reruns: int = 2
    reruns_delay: int = 1
    workers: int = 2

    # ── Performance thresholds ───────────────────────────────────────────────
    api_max_response_ms: int = 2_000   # API calls must complete within 2 s

    # ── Reporting / artefacts ────────────────────────────────────────────────
    screenshot_dir: str = "reports/screenshots"
    video_dir: str = "reports/videos"
    trace_dir: str = "reports/traces"


def get_config() -> BaseConfig:
    """
    Factory that builds a BaseConfig from environment variables.
    Environment variables always override defaults.
    """
    return BaseConfig(
        ui_base_url=os.getenv("UI_BASE_URL", "https://www.saucedemo.com"),
        api_base_url=os.getenv("API_BASE_URL", "https://jsonplaceholder.typicode.com"),
        sauce_username=os.getenv("SAUCE_USERNAME", "standard_user"),
        sauce_password=os.getenv("SAUCE_PASSWORD", "secret_sauce"),
        api_token=os.getenv("API_TOKEN", ""),
        browser=os.getenv("BROWSER", "chromium"),
        headless=os.getenv("HEADLESS", "true").lower() == "true",
        slow_mo=int(os.getenv("SLOW_MO", "0")),
        default_timeout=int(os.getenv("DEFAULT_TIMEOUT", "30000")),
        reruns=int(os.getenv("RERUNS", "2")),
        reruns_delay=int(os.getenv("RERUNS_DELAY", "1")),
        workers=int(os.getenv("WORKERS", "2")),
        api_max_response_ms=int(os.getenv("API_MAX_RESPONSE_MS", "2000")),
    )
