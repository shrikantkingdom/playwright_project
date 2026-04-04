Feature: Shopping Cart Operations
  As a logged-in user
  I want to manage my shopping cart
  So that I can complete purchases

  Background:
    Given I am logged in as "standard_user" with password "secret_sauce"

  @ui @regression
  Scenario: Adding an item to the cart increments the badge
    When I add the item at index 0 to the cart
    Then the cart badge should show 1

  @ui @regression
  Scenario: Adding multiple items updates the badge count
    When I add the item at index 0 to the cart
    And I add the item at index 1 to the cart
    Then the cart badge should show 2

  @ui @regression
  Scenario: Cart page contains the added item
    When I add the item at index 0 to the cart
    And I navigate to the cart
    Then the cart should contain 1 item

  @ui @regression
  Scenario: Removing an item decreases the item count
    When I add the item at index 0 to the cart
    And I add the item at index 1 to the cart
    And I navigate to the cart
    And I remove the first item from the cart
    Then the cart should contain 1 item

  @ui @regression
  Scenario: Complete checkout flow
    When I add the item at index 0 to the cart
    And I navigate to the cart
    And I click checkout
    And I fill in checkout information
    And I finish the checkout
    Then I should see the order confirmation
