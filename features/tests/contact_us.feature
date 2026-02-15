Feature: Contact Us Page

  Scenario Outline: User can open the Contact us page
    Given Open Reelly main page
    When Log in with "<email>" and "<password>"
    And Click on the settings option
    And Click on Contact us option
    Then Verify the right page opens
    And Verify there are at least 4 social media icons
    And Verify the "Connect the company" button is available and clickable

  Examples:
    | email               | password      |
    | spnance1985@gmail.com     | W0rthy1sth3L4mb!|