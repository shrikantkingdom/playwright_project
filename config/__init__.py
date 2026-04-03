"""
config/__init__.py
Exposes the active configuration object based on the ENV variable.
"""

from config.base_config import BaseConfig, get_config

__all__ = ["BaseConfig", "get_config"]
