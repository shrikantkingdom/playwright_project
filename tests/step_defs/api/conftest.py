"""
tests/step_defs/api/conftest.py
Shared API response assertion steps available to all API step modules.

These steps operate on context['response'] set by each resource's When steps.
"""

from pytest_bdd import parsers, then


@then(parsers.parse("the response status should be {status:d}"))
def check_response_status(context, status):
    assert context["response"].status_code == status, (
        f"Expected status {status}, got {context['response'].status_code}"
    )


@then("the response should be a non-empty list")
def check_non_empty_list(context):
    data = context["response"].json()
    assert isinstance(data, list), f"Expected list, got {type(data).__name__}"
    assert len(data) > 0, "Response list should not be empty"


@then(parsers.parse("the response should contain exactly {count:d} items"))
def check_item_count(context, count):
    data = context["response"].json()
    assert len(data) == count, f"Expected {count} items, got {len(data)}"


@then("the response time should be within the configured threshold")
def check_response_time(context, config):
    elapsed = context["response"].elapsed_ms
    threshold = config.api_max_response_ms
    assert elapsed <= threshold, (
        f"Response time {elapsed:.0f} ms exceeded threshold {threshold} ms"
    )


@then("the response should contain an id field")
def check_has_id(context):
    data = context["response"].json()
    assert "id" in data, "Response does not contain an 'id' field"


@then(parsers.parse('the response title should be "{title}"'))
def check_response_title(context, title):
    assert context["response"].json()["title"] == title


@then(parsers.parse('the response body should be "{body}"'))
def check_response_body_field(context, body):
    assert context["response"].json()["body"] == body


@then("the response body should be an empty JSON object")
def check_empty_body(context):
    data = context["response"].json()
    assert data == {}, f"Expected empty JSON object, got {data}"
