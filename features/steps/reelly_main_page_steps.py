from behave import given, when, then
from pages.header import Header
from pages.contact_page import ContactPage
from time import sleep

@given('Open Reelly main page')
def open_main(context):
    print("Opening Reelly main page...")
    context.app.main_page.open_main_page()
    sleep(2)  # allow page to settle

@when('Log in with "{email}" and "{password}"')
def step_login(context, email, password):
    context.app.log_in_page.login(email, password)
    sleep(2)  # give time for redirect after login

@when('Click on the settings option')
def step_click_settings(context):
    context.header = context.app.header
    context.header.click_settings()
    sleep(2)  # wait for settings panel

@when('Click on Contact Us option')
def step_click_contact(context):
    context.app.header.click_contact_us()
    sleep(2)  # wait for page transition

@then('Verify the right page opens')
def step_verify_page(context):
    context.contact_page = context.app.contact_page
    assert context.contact_page.is_correct_page_opened(), "Contact page did not open correctly"

@then('Verify there are at least 4 social media icons')
def step_verify_icons(context):
    count = context.contact_page.get_social_media_icons_count()
    assert count >= 4, f"Expected at least 4 icons, but found {count}"

@then('Verify the "Connect the company" button is available and clickable')
def step_verify_button(context):
    assert context.contact_page.is_connect_button_clickable(), "Connect the company button is not clickable"
