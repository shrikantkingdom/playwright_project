"""
tests/step_defs/conftest.py
Shared BDD fixtures available to all step definition modules.
"""
import pytest


@pytest.fixture
def context():
    """Mutable dictionary for passing state between BDD steps within a scenario."""
    return {}
