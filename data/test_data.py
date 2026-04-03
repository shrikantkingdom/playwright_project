"""
data/test_data.py
Centralised test data factory using Faker.
Keeps test files clean by separating data generation from test logic.
"""

from faker import Faker

fake = Faker()


class SauceDemoUsers:
    """Static credentials for SauceDemo test accounts."""

    STANDARD = {"username": "standard_user", "password": "secret_sauce"}
    LOCKED_OUT = {"username": "locked_out_user", "password": "secret_sauce"}
    PROBLEM = {"username": "problem_user", "password": "secret_sauce"}
    PERFORMANCE_GLITCH = {"username": "performance_glitch_user", "password": "secret_sauce"}
    INVALID = {"username": "invalid_user", "password": "wrong_password"}


class PostData:
    """Factory methods for generating post payloads."""

    @staticmethod
    def valid_post(user_id: int = 1) -> dict:
        """Return a valid post creation payload."""
        return {
            "userId": user_id,
            "title": fake.sentence(nb_words=6),
            "body": fake.paragraph(nb_sentences=3),
        }

    @staticmethod
    def minimal_post() -> dict:
        """Return the bare-minimum post payload."""
        return {"userId": 1, "title": "Test Post", "body": "Test body content."}


class CheckoutData:
    """Factory for checkout form test data."""

    @staticmethod
    def valid_info() -> dict:
        """Return a dict with first_name, last_name, postal_code."""
        return {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "postal_code": fake.postcode(),
        }
