"""
tests/api/test_posts.py
API tests for the JSONPlaceholder /posts endpoint.

Covers: GET (list + single), POST, PUT, PATCH, DELETE
Markers: api, smoke, regression, performance
"""

import pytest

from utils.schema_validator import (
    CREATED_POST_SCHEMA,
    POST_SCHEMA,
    validate_schema,
)


@pytest.mark.api
@pytest.mark.smoke
class TestGetPosts:
    """Tests for GET /posts and GET /posts/{id}."""

    def test_get_all_posts_returns_200(self, api_client, config):
        """GET /posts should return HTTP 200."""
        response = api_client.get_posts()
        assert response.status_code == 200

    def test_get_all_posts_returns_list(self, api_client):
        """GET /posts should return a JSON array."""
        response = api_client.get_posts()
        data = response.json()
        assert isinstance(data, list), "Response body should be a list"
        assert len(data) > 0, "List should not be empty"

    def test_get_all_posts_count(self, api_client):
        """JSONPlaceholder serves exactly 100 posts."""
        response = api_client.get_posts()
        assert len(response.json()) == 100

    def test_get_single_post_returns_200(self, api_client):
        """GET /posts/1 should return HTTP 200."""
        response = api_client.get_post(1)
        assert response.status_code == 200

    def test_get_single_post_schema(self, api_client):
        """GET /posts/1 response body should match the post schema."""
        response = api_client.get_post(1)
        validate_schema(response.json(), POST_SCHEMA)

    def test_get_single_post_id_matches(self, api_client):
        """The returned post id should match the requested id."""
        post_id = 5
        response = api_client.get_post(post_id)
        assert response.json()["id"] == post_id

    def test_get_non_existent_post_returns_404(self, api_client):
        """GET /posts/9999 should return HTTP 404."""
        response = api_client.get_post(9999)
        assert response.status_code == 404

    def test_get_post_comments(self, api_client):
        """GET /posts/1/comments should return a non-empty list."""
        response = api_client.get_post_comments(1)
        assert response.status_code == 200
        comments = response.json()
        assert isinstance(comments, list) and len(comments) > 0


@pytest.mark.api
@pytest.mark.performance
class TestGetPostsPerformance:
    """Basic response-time assertions for the posts endpoint."""

    def test_get_posts_response_time(self, api_client, config):
        """GET /posts should respond within the configured threshold."""
        response = api_client.get_posts()
        assert response.elapsed_ms <= config.api_max_response_ms, (
            f"GET /posts took {response.elapsed_ms:.0f} ms "
            f"(limit: {config.api_max_response_ms} ms)"
        )

    def test_get_single_post_response_time(self, api_client, config):
        """GET /posts/1 should respond within the configured threshold."""
        response = api_client.get_post(1)
        assert response.elapsed_ms <= config.api_max_response_ms


@pytest.mark.api
@pytest.mark.regression
class TestCreatePost:
    """Tests for POST /posts."""

    def test_create_post_returns_201(self, api_client):
        """POST /posts should return HTTP 201 Created."""
        payload = {"userId": 1, "title": "New Test Post", "body": "Body content here."}
        response = api_client.create_post(payload)
        assert response.status_code == 201

    def test_created_post_has_generated_id(self, api_client):
        """The created post should include an auto-generated id."""
        payload = {"userId": 1, "title": "Test", "body": "Test body"}
        response = api_client.create_post(payload)
        data = response.json()
        assert "id" in data
        assert isinstance(data["id"], int)

    def test_created_post_schema(self, api_client):
        """POST /posts response should match the created-post schema."""
        from data.test_data import PostData

        payload = PostData.valid_post(user_id=3)
        response = api_client.create_post(payload)
        validate_schema(response.json(), CREATED_POST_SCHEMA)

    def test_created_post_mirrors_payload(self, api_client):
        """The response should echo back the submitted title and body."""
        payload = {"userId": 7, "title": "Mirror Test", "body": "Mirror body"}
        response = api_client.create_post(payload)
        data = response.json()
        assert data["title"] == payload["title"]
        assert data["body"] == payload["body"]
        assert data["userId"] == payload["userId"]


@pytest.mark.api
@pytest.mark.regression
class TestUpdatePost:
    """Tests for PUT and PATCH /posts/{id}."""

    def test_put_post_returns_200(self, api_client):
        """PUT /posts/1 should return HTTP 200."""
        payload = {"id": 1, "userId": 1, "title": "Updated Title", "body": "Updated body"}
        response = api_client.update_post(1, payload)
        assert response.status_code == 200

    def test_put_post_updates_title(self, api_client):
        """PUT /posts/1 should reflect the new title in the response."""
        new_title = "Fully Replaced Title"
        payload = {"id": 1, "userId": 1, "title": new_title, "body": "Updated body"}
        response = api_client.update_post(1, payload)
        assert response.json()["title"] == new_title

    def test_patch_post_returns_200(self, api_client):
        """PATCH /posts/1 should return HTTP 200."""
        response = api_client.partial_update_post(1, {"title": "Patched Title"})
        assert response.status_code == 200

    def test_patch_post_updates_only_title(self, api_client):
        """PATCH should update only the supplied field."""
        new_title = "Only Title Changed"
        response = api_client.partial_update_post(1, {"title": new_title})
        assert response.json()["title"] == new_title


@pytest.mark.api
@pytest.mark.regression
class TestDeletePost:
    """Tests for DELETE /posts/{id}."""

    def test_delete_post_returns_200(self, api_client):
        """DELETE /posts/1 should return HTTP 200."""
        response = api_client.delete_post(1)
        assert response.status_code == 200

    def test_delete_post_returns_empty_body(self, api_client):
        """DELETE /posts/1 response body should be an empty JSON object."""
        response = api_client.delete_post(1)
        assert response.json() == {}
