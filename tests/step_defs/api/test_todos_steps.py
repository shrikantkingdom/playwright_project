"""
tests/step_defs/api/test_todos_steps.py
Step definitions for features/api/todos.feature.
"""

from pathlib import Path

from pytest_bdd import parsers, scenarios, then, when

from utils.schema_validator import TODO_SCHEMA, validate_schema

FEATURES_DIR = Path(__file__).parent.parent.parent.parent / "features"
scenarios(str(FEATURES_DIR / "api" / "todos.feature"))


# ── When ──────────────────────────────────────────────────────────────────────


@when("I request all todos")
def when_request_all_todos(api_client, context):
    context["response"] = api_client.get_todos()


@when(parsers.parse("I request todo with id {todo_id:d}"))
def when_request_todo(api_client, context, todo_id):
    context["response"] = api_client.get_todo(todo_id)


@when(parsers.parse("I request todos for user with id {user_id:d}"))
def when_request_todos_by_user(api_client, context, user_id):
    context["response"] = api_client.get_todos_by_user(user_id)


# ── Then ──────────────────────────────────────────────────────────────────────


@then("the response should match the todo schema")
def then_todo_schema(context):
    validate_schema(context["response"].json(), TODO_SCHEMA)


@then("the completed field should be a boolean")
def then_completed_boolean(context):
    completed = context["response"].json()["completed"]
    assert isinstance(completed, bool), f"Expected boolean 'completed', got {type(completed).__name__}"
