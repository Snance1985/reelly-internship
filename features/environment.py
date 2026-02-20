from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from app.application import Application

def browser_init(context):
    chrome_options = Options()

    # Block location & notifications
    prefs = {
        "profile.default_content_setting_values.geolocation": 2,
        "profile.default_content_setting_values.notifications": 2
    }
    chrome_options.add_experimental_option("prefs", prefs)

    driver_path = ChromeDriverManager().install()
    service = Service(driver_path)
    context.driver = webdriver.Chrome(service=service, options=chrome_options)

    context.driver.maximize_window()
    context.driver.implicitly_wait(4)
    context.driver.wait = WebDriverWait(context.driver, 10)

    context.app = Application(context.driver)

def before_scenario(context, scenario):
    browser_init(context)

def after_scenario(context, scenario):
    if hasattr(context, 'driver'):
        context.driver.quit()
