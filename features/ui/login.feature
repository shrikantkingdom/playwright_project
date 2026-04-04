Feature: User Authentication
  As a SauceDemo user
  I want to authenticate into the application
  So that I can access the product inventory

  @ui @smoke
  Scenario: Successful login with standard user
    Given I am on the login page
    When I login with username "standard_user" and password "secret_sauce"
    Then I should be redirected to the inventory page

  @ui @smoke
  Scenario: Login page has correct title
    Given I am on the login page
    Then the page title should be "Swag Labs"

  @ui @smoke
  Scenario: Locked out user sees error message
    Given I am on the login page
    When I login with username "locked_out_user" and password "secret_sauce"
    Then I should see the error message containing "locked out"

  @ui @smoke
  Scenario: Invalid credentials do not grant access
    Given I am on the login page
    When I login with username "invalid_user" and password "wrong_password"
    Then I should not be redirected to the inventory page

  @ui @smoke
  Scenario: Empty username shows validation error
    Given I am on the login page
    When I click login without entering credentials
    Then I should see an error about missing username

  @ui @smoke
  Scenario: Empty password shows validation error
    Given I am on the login page
    When I enter username "standard_user" and click login without a password
    Then I should see an error about missing password

  @ui @regression
  Scenario: Logout redirects to login page
    Given I am logged in as "standard_user" with password "secret_sauce"
    When I logout from the application
    Then I should be on the login page
