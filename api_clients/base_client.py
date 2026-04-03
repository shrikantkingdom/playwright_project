"""
api_clients/base_client.py
Reusable HTTP client base class using httpx.
Handles authentication headers, response logging, and timing.
"""

import time
from typing import Any

import httpx

from utils.logger import get_logger

logger = get_logger(__name__)


class BaseAPIClient:
    """
    Thin wrapper around httpx.Client.

    All public API clients should inherit from this class and set
    `base_url` in their constructor.
    """

    def __init__(self, base_url: str, token: str = "", timeout: float = 10.0) -> None:
        self.base_url = base_url.rstrip("/")
        self._timeout = timeout
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        self._client = httpx.Client(base_url=self.base_url, headers=headers, timeout=timeout)

    # ── Low-level request helpers ─────────────────────────────────────────────

    def _request(self, method: str, path: str, **kwargs) -> httpx.Response:
        """
        Execute an HTTP request and log timing information.
        Returns the raw httpx.Response.
        """
        url = path if path.startswith("http") else f"{self.base_url}/{path.lstrip('/')}"
        logger.info("%s %s", method.upper(), url)
        start = time.perf_counter()
        response = self._client.request(method, path, **kwargs)
        elapsed_ms = (time.perf_counter() - start) * 1_000
        logger.info(
            "  → %d  (%.2f ms)",
            response.status_code,
            elapsed_ms,
        )
        response.elapsed_ms = elapsed_ms  # type: ignore[attr-defined]
        return response

    def get(self, path: str, **kwargs) -> httpx.Response:
        return self._request("GET", path, **kwargs)

    def post(self, path: str, json: Any = None, **kwargs) -> httpx.Response:
        return self._request("POST", path, json=json, **kwargs)

    def put(self, path: str, json: Any = None, **kwargs) -> httpx.Response:
        return self._request("PUT", path, json=json, **kwargs)

    def patch(self, path: str, json: Any = None, **kwargs) -> httpx.Response:
        return self._request("PATCH", path, json=json, **kwargs)

    def delete(self, path: str, **kwargs) -> httpx.Response:
        return self._request("DELETE", path, **kwargs)

    def close(self) -> None:
        """Close the underlying HTTP connection pool."""
        self._client.close()

    # Context-manager support
    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
