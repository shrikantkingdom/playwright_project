"""
tests/api/test_users.py
API tests for the JSONPlaceholder /users endpoint.

Markers: api, smoke, regression
"""

import pytest

from utils.schema_validator import USER_SCHEMA, validate_schema


@pytest.mark.api
@pytest.mark.smoke
class TestGetUsers:
    """Tests for GET /users and GET /users/{id}."""

    def test_get_all_users_returns_200(self, api_client):
        """GET /users should return HTTP 200."""
        response = api_client.get_users()
        assert response.status_code == 200

    def test_get_all_users_returns_list(self, api_client):
        """GET /users should return a JSON list."""
        response = api_client.get_users()
        data = response.json()
        assert isinstance(data, list)

    def test_get_all_users_count(self, api_client):
        """JSONPlaceholder provides exactly 10 users."""
        response = api_client.get_users()
        assert len(response.json()) == 10

    def test_get_single_user_returns_200(self, api_client):
        """GET /users/1 should return HTTP 200."""
        response = api_client.get_user(1)
        assert response.status_code == 200

    def test_get_single_user_schema(self, api_client):
        """GET /users/1 response should match the user schema."""
        response = api_client.get_user(1)
        validate_schema(response.json(), USER_SCHEMA)

    def test_get_single_user_has_email(self, api_client):
        """Each user should have a non-empty email address."""
        response = api_client.get_user(1)
        data = response.json()
        assert "email" in data
        assert "@" in data["email"], "Email should contain @"

    def test_get_non_existent_user_returns_404(self, api_client):
        """GET /users/9999 should return HTTP 404."""
        response = api_client.get_user(9999)
        assert response.status_code == 404

    def test_all_users_have_required_fields(self, api_client):
        """Every user in the list should have id, name, username, email."""
        response = api_client.get_users()
        users = response.json()
        required_keys = {"id", "name", "username", "email"}
        for user in users:
            missing = required_keys - user.keys()
            assert not missing, f"User {user.get('id')} is missing fields: {missing}"

    def test_user_ids_are_unique(self, api_client):
        """All user ids in the list should be unique."""
        response = api_client.get_users()
        ids = [u["id"] for u in response.json()]
        assert len(ids) == len(set(ids)), "User ids should be unique"


@pytest.mark.api
@pytest.mark.performance
class TestUsersPerformance:
    """Basic response-time checks for the users endpoint."""

    def test_get_users_response_time(self, api_client, config):
        """GET /users should respond within the configured threshold."""
        response = api_client.get_users()
        assert response.elapsed_ms <= config.api_max_response_ms, (
            f"GET /users took {response.elapsed_ms:.0f} ms "
            f"(limit: {config.api_max_response_ms} ms)"
        )
