"""config/environments/staging.py – staging environment overrides."""
from config.base_config import BaseConfig

STAGING_CONFIG = BaseConfig(
    ui_base_url="https://www.saucedemo.com",
    api_base_url="https://jsonplaceholder.typicode.com",
    headless=True,
    api_max_response_ms=3_000,
)
