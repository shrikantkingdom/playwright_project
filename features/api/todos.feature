Feature: Todos API
  As an API consumer
  I want to retrieve and filter todo items
  So that I can track task completion

  @api @smoke
  Scenario: Get all todos returns 200
    When I request all todos
    Then the response status should be 200

  @api @smoke
  Scenario: Get all todos returns a non-empty list
    When I request all todos
    Then the response should be a non-empty list

  @api @smoke
  Scenario: Get all todos returns 200 todos
    When I request all todos
    Then the response should contain exactly 200 items

  @api @smoke
  Scenario: Get single todo returns 200
    When I request todo with id 1
    Then the response status should be 200

  @api @smoke
  Scenario: Get single todo matches todo schema
    When I request todo with id 1
    Then the response should match the todo schema

  @api @smoke
  Scenario: Todo completed field is a boolean
    When I request todo with id 1
    Then the completed field should be a boolean

  @api @smoke
  Scenario: Get non-existent todo returns 404
    When I request todo with id 9999
    Then the response status should be 404

  @api @regression
  Scenario: Filter todos by user id
    When I request todos for user with id 1
    Then the response should be a non-empty list

  @api @regression
  Scenario: User 1 has exactly 20 todos
    When I request todos for user with id 1
    Then the response should contain exactly 20 items
