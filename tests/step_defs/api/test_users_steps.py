"""
tests/step_defs/api/test_users_steps.py
Step definitions for features/api/users.feature.
"""

from pathlib import Path

from pytest_bdd import parsers, scenarios, then, when

from utils.schema_validator import USER_SCHEMA, validate_schema

FEATURES_DIR = Path(__file__).parent.parent.parent.parent / "features"
scenarios(str(FEATURES_DIR / "api" / "users.feature"))


# ── When ──────────────────────────────────────────────────────────────────────


@when("I request all users")
def when_request_all_users(api_client, context):
    context["response"] = api_client.get_users()


@when(parsers.parse("I request user with id {user_id:d}"))
def when_request_user(api_client, context, user_id):
    context["response"] = api_client.get_user(user_id)


# ── Then ──────────────────────────────────────────────────────────────────────


@then("the response should match the user schema")
def then_user_schema(context):
    validate_schema(context["response"].json(), USER_SCHEMA)


@then('the response email should contain "@"')
def then_email_valid(context):
    email = context["response"].json()["email"]
    assert "@" in email, f"Expected '@' in email, got: '{email}'"


@then("all users should have id, name, username, and email fields")
def then_all_users_have_required_fields(context):
    users = context["response"].json()
    required = {"id", "name", "username", "email"}
    for user in users:
        missing = required - user.keys()
        assert not missing, f"User {user.get('id')} is missing fields: {missing}"


@then("all user ids should be unique")
def then_user_ids_unique(context):
    users = context["response"].json()
    ids = [u["id"] for u in users]
    assert len(ids) == len(set(ids)), "User ids should be unique"
