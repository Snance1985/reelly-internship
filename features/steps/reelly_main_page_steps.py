from behave import given, when, then
from pages.header import Header
from pages.contact_page import ContactPage
from time import sleep


@given('Open Reelly main page')
def open_main(context):
    print("Opening Reelly main page...")
    context.app.main_page.open_main_page()
    context.app.header.wait_for_header_to_load()

@when('Log in with "{email}" and "{password}"')
def step_login(context, email, password):
    context.app.log_in_page.login(email, password)

@when('Click on the settings option')
def step_click_settings(context):
    context.header = Header(context.driver)
    context.header.click_settings()


@when('Click on Contact us option')
def click_contact(context):
    context.app.settings_page.click_contact_us()


@then('Verify the right page opens')
def step_verify_page(context):
    context.contact_page = ContactPage(context.driver)
    assert context.contact_page.is_correct_page_opened(), \
        "Contact page did not open correctly"


@then('Verify there are at least 4 social media icons')
def step_verify_icons(context):
    count = context.contact_page.get_social_media_icons_count()
    assert count >= 4, f"Expected at least 4 icons, but found {count}"


@then('Verify the "Connect the company" button is available and clickable')
def step_verify_button(context):
    assert context.contact_page.is_connect_button_clickable(), \
        "Connect the company button is not clickable"