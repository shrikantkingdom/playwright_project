Feature: Inventory Page Navigation
  As a logged-in user
  I want to browse and sort products on the inventory page
  So that I can find items to purchase

  Background:
    Given I am logged in as "standard_user" with password "secret_sauce"

  @ui @smoke
  Scenario: Inventory page loads with products
    Then the inventory container should be visible
    And the product list should not be empty

  @ui @smoke
  Scenario: Inventory page shows exactly 6 products
    Then I should see exactly 6 products

  @ui @smoke
  Scenario: All product names are non-empty
    Then all product names should be non-empty

  @ui @smoke
  Scenario: All product prices are displayed
    Then all product prices should start with "$"

  @ui @regression
  Scenario: Sort products by name Z to A
    When I sort products by "za"
    Then the products should be sorted in descending alphabetical order

  @ui @regression
  Scenario: Sort products by name A to Z
    When I sort products by "az"
    Then the products should be sorted in ascending alphabetical order

  @ui @regression
  Scenario: Sort products by price low to high
    When I sort products by "lohi"
    Then the products should be sorted by price ascending

  @ui @regression
  Scenario: Sort products by price high to low
    When I sort products by "hilo"
    Then the products should be sorted by price descending
