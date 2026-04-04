Feature: Posts API
  As an API consumer
  I want to perform CRUD operations on posts
  So that I can manage content

  @api @smoke
  Scenario: Get all posts returns 200
    When I request all posts
    Then the response status should be 200

  @api @smoke
  Scenario: Get all posts returns a non-empty list
    When I request all posts
    Then the response should be a non-empty list

  @api @smoke
  Scenario: Get all posts returns 100 posts
    When I request all posts
    Then the response should contain exactly 100 items

  @api @smoke
  Scenario: Get single post returns 200
    When I request post with id 1
    Then the response status should be 200

  @api @smoke
  Scenario: Get single post matches post schema
    When I request post with id 1
    Then the response should match the post schema

  @api @smoke
  Scenario: Get single post id matches the requested id
    When I request post with id 1
    Then the response id should be 1

  @api @smoke
  Scenario: Get non-existent post returns 404
    When I request post with id 9999
    Then the response status should be 404

  @api @smoke
  Scenario: Get post comments returns a list
    When I request comments for post with id 1
    Then the response should be a non-empty list

  @api @performance
  Scenario: Get all posts response time is acceptable
    When I request all posts
    Then the response time should be within the configured threshold

  @api @performance
  Scenario: Get single post response time is acceptable
    When I request post with id 1
    Then the response time should be within the configured threshold

  @api @regression
  Scenario: Create post returns 201
    When I create a new post
    Then the response status should be 201

  @api @regression
  Scenario: Created post has an auto-generated id
    When I create a new post
    Then the response should contain an id field

  @api @regression
  Scenario: Created post matches created post schema
    When I create a new post
    Then the response should match the created post schema

  @api @regression
  Scenario: Created post mirrors the submitted payload
    When I create a post with title "BDD Test Title" and body "BDD Test Body"
    Then the response title should be "BDD Test Title"
    And the response body should be "BDD Test Body"

  @api @regression
  Scenario: Full update of a post returns 200
    When I fully update post with id 1
    Then the response status should be 200

  @api @regression
  Scenario: Full update changes the post title
    When I fully update post with id 1 with title "BDD Updated Title"
    Then the response title should be "BDD Updated Title"

  @api @regression
  Scenario: Partial update of a post returns 200
    When I partially update post with id 1
    Then the response status should be 200

  @api @regression
  Scenario: Partial update only modifies supplied fields
    When I partially update post with id 1 with title "BDD Patched Title"
    Then the response title should be "BDD Patched Title"

  @api @regression
  Scenario: Delete a post returns 200
    When I delete post with id 1
    Then the response status should be 200

  @api @regression
  Scenario: Delete a post returns an empty body
    When I delete post with id 1
    Then the response body should be an empty JSON object
