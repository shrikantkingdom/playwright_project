"""
utils/schema_validator.py
Thin wrapper around jsonschema for reusable response schema validation.
"""

from typing import Any

import jsonschema
from jsonschema import ValidationError

from utils.logger import get_logger

logger = get_logger(__name__)

# ── Common reusable schemas ──────────────────────────────────────────────────

POST_SCHEMA = {
    "type": "object",
    "required": ["id", "userId", "title", "body"],
    "properties": {
        "id": {"type": "integer"},
        "userId": {"type": "integer"},
        "title": {"type": "string"},
        "body": {"type": "string"},
    },
    "additionalProperties": False,
}

USER_SCHEMA = {
    "type": "object",
    "required": ["id", "name", "username", "email"],
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "username": {"type": "string"},
        "email": {"type": "string", "format": "email"},
        "address": {"type": "object"},
        "phone": {"type": "string"},
        "website": {"type": "string"},
        "company": {"type": "object"},
    },
}

TODO_SCHEMA = {
    "type": "object",
    "required": ["id", "userId", "title", "completed"],
    "properties": {
        "id": {"type": "integer"},
        "userId": {"type": "integer"},
        "title": {"type": "string"},
        "completed": {"type": "boolean"},
    },
    "additionalProperties": False,
}

CREATED_POST_SCHEMA = {
    "type": "object",
    "required": ["id", "userId", "title", "body"],
    "properties": {
        "id": {"type": "integer"},
        "userId": {"type": "integer"},
        "title": {"type": "string"},
        "body": {"type": "string"},
    },
}


def validate_schema(data: Any, schema: dict) -> None:
    """
    Validate *data* against *schema*.
    Raises AssertionError with a descriptive message on failure.
    """
    try:
        jsonschema.validate(instance=data, schema=schema)
        logger.debug("Schema validation passed.")
    except ValidationError as exc:
        logger.error("Schema validation failed: %s", exc.message)
        raise AssertionError(f"Schema validation failed: {exc.message}") from exc
