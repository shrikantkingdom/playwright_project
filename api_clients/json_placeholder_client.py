"""
api_clients/json_placeholder_client.py
High-level API client for JSONPlaceholder (https://jsonplaceholder.typicode.com).
Wraps all resource endpoints with typed, documented methods.
"""

from typing import Any

import httpx

from api_clients.base_client import BaseAPIClient
from utils.logger import get_logger

logger = get_logger(__name__)


class JSONPlaceholderClient(BaseAPIClient):
    """
    API client for JSONPlaceholder REST API.

    Endpoints covered:
    - /posts        GET (list / single), POST, PUT, PATCH, DELETE
    - /users        GET (list / single)
    - /todos        GET (list / single)
    - /comments     GET (list / filtered)
    """

    def __init__(self, base_url: str = "https://jsonplaceholder.typicode.com", token: str = "") -> None:
        super().__init__(base_url=base_url, token=token)

    # ── Posts ─────────────────────────────────────────────────────────────────

    def get_posts(self) -> httpx.Response:
        """GET /posts – retrieve all posts."""
        return self.get("/posts")

    def get_post(self, post_id: int) -> httpx.Response:
        """GET /posts/{id} – retrieve a single post."""
        return self.get(f"/posts/{post_id}")

    def create_post(self, payload: dict[str, Any]) -> httpx.Response:
        """POST /posts – create a new post."""
        return self.post("/posts", json=payload)

    def update_post(self, post_id: int, payload: dict[str, Any]) -> httpx.Response:
        """PUT /posts/{id} – fully replace a post."""
        return self.put(f"/posts/{post_id}", json=payload)

    def partial_update_post(self, post_id: int, payload: dict[str, Any]) -> httpx.Response:
        """PATCH /posts/{id} – partially update a post."""
        return self.patch(f"/posts/{post_id}", json=payload)

    def delete_post(self, post_id: int) -> httpx.Response:
        """DELETE /posts/{id} – delete a post."""
        return self.delete(f"/posts/{post_id}")

    def get_post_comments(self, post_id: int) -> httpx.Response:
        """GET /posts/{id}/comments – retrieve comments for a post."""
        return self.get(f"/posts/{post_id}/comments")

    # ── Users ─────────────────────────────────────────────────────────────────

    def get_users(self) -> httpx.Response:
        """GET /users – retrieve all users."""
        return self.get("/users")

    def get_user(self, user_id: int) -> httpx.Response:
        """GET /users/{id} – retrieve a single user."""
        return self.get(f"/users/{user_id}")

    # ── Todos ─────────────────────────────────────────────────────────────────

    def get_todos(self) -> httpx.Response:
        """GET /todos – retrieve all todos."""
        return self.get("/todos")

    def get_todo(self, todo_id: int) -> httpx.Response:
        """GET /todos/{id} – retrieve a single todo."""
        return self.get(f"/todos/{todo_id}")

    def get_todos_by_user(self, user_id: int) -> httpx.Response:
        """GET /todos?userId={id} – retrieve todos filtered by user."""
        return self.get("/todos", params={"userId": user_id})
