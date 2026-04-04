Feature: Users API
  As an API consumer
  I want to retrieve user data
  So that I can access user information

  @api @smoke
  Scenario: Get all users returns 200
    When I request all users
    Then the response status should be 200

  @api @smoke
  Scenario: Get all users returns a non-empty list
    When I request all users
    Then the response should be a non-empty list

  @api @smoke
  Scenario: Get all users returns 10 users
    When I request all users
    Then the response should contain exactly 10 items

  @api @smoke
  Scenario: Get single user returns 200
    When I request user with id 1
    Then the response status should be 200

  @api @smoke
  Scenario: Get single user matches user schema
    When I request user with id 1
    Then the response should match the user schema

  @api @smoke
  Scenario: Get single user has a valid email
    When I request user with id 1
    Then the response email should contain "@"

  @api @smoke
  Scenario: Get non-existent user returns 404
    When I request user with id 9999
    Then the response status should be 404

  @api @smoke
  Scenario: All users have required fields
    When I request all users
    Then all users should have id, name, username, and email fields

  @api @smoke
  Scenario: All user ids are unique
    When I request all users
    Then all user ids should be unique

  @api @performance
  Scenario: Get all users response time is acceptable
    When I request all users
    Then the response time should be within the configured threshold
