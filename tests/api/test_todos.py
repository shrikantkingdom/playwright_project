"""
tests/api/test_todos.py
API tests for the JSONPlaceholder /todos endpoint.

Markers: api, regression
"""

import pytest

from utils.schema_validator import TODO_SCHEMA, validate_schema


@pytest.mark.api
@pytest.mark.smoke
class TestGetTodos:
    """Tests for GET /todos and GET /todos/{id}."""

    def test_get_all_todos_returns_200(self, api_client):
        """GET /todos should return HTTP 200."""
        response = api_client.get_todos()
        assert response.status_code == 200

    def test_get_all_todos_returns_list(self, api_client):
        """GET /todos should return a JSON list."""
        response = api_client.get_todos()
        assert isinstance(response.json(), list)

    def test_get_all_todos_count(self, api_client):
        """JSONPlaceholder provides exactly 200 todos."""
        response = api_client.get_todos()
        assert len(response.json()) == 200

    def test_get_single_todo_returns_200(self, api_client):
        """GET /todos/1 should return HTTP 200."""
        response = api_client.get_todo(1)
        assert response.status_code == 200

    def test_get_single_todo_schema(self, api_client):
        """GET /todos/1 response should match the todo schema."""
        response = api_client.get_todo(1)
        validate_schema(response.json(), TODO_SCHEMA)

    def test_todo_completed_field_is_boolean(self, api_client):
        """Each todo should have a boolean 'completed' field."""
        response = api_client.get_todo(1)
        data = response.json()
        assert isinstance(data["completed"], bool)

    def test_get_non_existent_todo_returns_404(self, api_client):
        """GET /todos/9999 should return HTTP 404."""
        response = api_client.get_todo(9999)
        assert response.status_code == 404


@pytest.mark.api
@pytest.mark.regression
class TestTodoFiltering:
    """Tests for filtering todos by user."""

    def test_filter_todos_by_user(self, api_client):
        """GET /todos?userId=1 should only return todos for user 1."""
        response = api_client.get_todos_by_user(1)
        assert response.status_code == 200
        todos = response.json()
        assert len(todos) > 0, "User 1 should have todos"
        assert all(t["userId"] == 1 for t in todos), "All todos should belong to user 1"

    def test_filter_todos_returns_correct_count(self, api_client):
        """User 1 has exactly 20 todos in JSONPlaceholder."""
        response = api_client.get_todos_by_user(1)
        assert len(response.json()) == 20
