"""config/environments/qa.py – QA environment overrides."""
from config.base_config import BaseConfig

QA_CONFIG = BaseConfig(
    ui_base_url="https://www.saucedemo.com",
    api_base_url="https://jsonplaceholder.typicode.com",
    headless=True,
)
