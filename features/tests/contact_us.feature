Feature: Contact Us Page

Scenario Outline: User can open the Contact Us page
  Given Open Reelly main page
  When Log in with "<email>" and "<password>"
  And Click on the Market Offers option
  And Click on the Menu option
  And Click on Contact Us option
  Then Verify the right page opens
  And Verify there are at least 4 social media icons
  And Verify the "Connect the company" button is available and clickable


#  Scenario Outline: User can open the Contact Us page
#    Given Open Reelly main page
#    When Log in with "<email>" and "<password>"
#    And Click on the settings option
#    And Click on Contact Us option
#    Then Verify the right page opens
#    And Verify there are at least 4 social media icons
#    And Verify the "Connect the company" button is available and clickable

  Examples:
    | email                 | password      |
    | user_email | user_password |