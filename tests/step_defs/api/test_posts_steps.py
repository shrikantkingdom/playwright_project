"""
tests/step_defs/api/test_posts_steps.py
Step definitions for features/api/posts.feature.
"""

from pathlib import Path

from pytest_bdd import parsers, scenarios, then, when

from data.test_data import PostData
from utils.schema_validator import CREATED_POST_SCHEMA, POST_SCHEMA, validate_schema

FEATURES_DIR = Path(__file__).parent.parent.parent.parent / "features"
scenarios(str(FEATURES_DIR / "api" / "posts.feature"))


# ── When ──────────────────────────────────────────────────────────────────────


@when("I request all posts")
def when_request_all_posts(api_client, context):
    context["response"] = api_client.get_posts()


@when(parsers.parse("I request post with id {post_id:d}"))
def when_request_post(api_client, context, post_id):
    context["response"] = api_client.get_post(post_id)


@when(parsers.parse("I request comments for post with id {post_id:d}"))
def when_request_post_comments(api_client, context, post_id):
    context["response"] = api_client.get_post_comments(post_id)


@when("I create a new post")
def when_create_post(api_client, context):
    payload = PostData.valid_post()
    context["payload"] = payload
    context["response"] = api_client.create_post(payload)


@when(parsers.parse('I create a post with title "{title}" and body "{body}"'))
def when_create_post_with_data(api_client, context, title, body):
    payload = {"userId": 1, "title": title, "body": body}
    context["response"] = api_client.create_post(payload)


@when(parsers.parse("I fully update post with id {post_id:d}"))
def when_full_update_post(api_client, context, post_id):
    payload = PostData.valid_post()
    context["response"] = api_client.update_post(post_id, payload)


@when(parsers.parse('I fully update post with id {post_id:d} with title "{title}"'))
def when_full_update_post_with_title(api_client, context, post_id, title):
    payload = PostData.valid_post()
    payload["title"] = title
    context["response"] = api_client.update_post(post_id, payload)


@when(parsers.parse("I partially update post with id {post_id:d}"))
def when_partial_update_post(api_client, context, post_id):
    context["response"] = api_client.partial_update_post(post_id, {"title": "Updated"})


@when(parsers.parse('I partially update post with id {post_id:d} with title "{title}"'))
def when_partial_update_post_with_title(api_client, context, post_id, title):
    context["response"] = api_client.partial_update_post(post_id, {"title": title})


@when(parsers.parse("I delete post with id {post_id:d}"))
def when_delete_post(api_client, context, post_id):
    context["response"] = api_client.delete_post(post_id)


# ── Then ──────────────────────────────────────────────────────────────────────


@then("the response should match the post schema")
def then_post_schema(context):
    validate_schema(context["response"].json(), POST_SCHEMA)


@then(parsers.parse("the response id should be {expected_id:d}"))
def then_response_id(context, expected_id):
    actual = context["response"].json()["id"]
    assert actual == expected_id, f"Expected id {expected_id}, got {actual}"


@then("the response should match the created post schema")
def then_created_post_schema(context):
    validate_schema(context["response"].json(), CREATED_POST_SCHEMA)
