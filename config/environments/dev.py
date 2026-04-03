"""config/environments/dev.py – development overrides."""
from config.base_config import BaseConfig

DEV_CONFIG = BaseConfig(
    ui_base_url="https://www.saucedemo.com",
    api_base_url="https://jsonplaceholder.typicode.com",
    headless=False,
    slow_mo=100,
)
