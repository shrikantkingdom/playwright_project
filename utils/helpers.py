"""
utils/helpers.py
General-purpose helper utilities shared across the test framework.
"""

import time
from datetime import datetime
from pathlib import Path
from typing import Any

from utils.logger import get_logger

logger = get_logger(__name__)


def timestamp() -> str:
    """Return a filesystem-safe ISO-like timestamp string."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def ensure_dir(path: str | Path) -> Path:
    """Create *path* (and any parents) if it does not exist, then return it."""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def measure_elapsed_ms(func):
    """
    Decorator that logs and returns execution time in milliseconds.

    Usage::

        @measure_elapsed_ms
        def my_function():
            ...
    """

    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed_ms = (time.perf_counter() - start) * 1_000
        logger.debug("%s executed in %.2f ms", func.__name__, elapsed_ms)
        return result

    return wrapper


def flatten_dict(d: dict[str, Any], parent_key: str = "", sep: str = ".") -> dict:
    """Recursively flatten a nested dictionary."""
    items: list = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)
