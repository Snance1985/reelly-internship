import os
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

# Chrome
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager

# Firefox
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager

from app.application import Application


def browser_init(context):
    """
    Initializes browser based on BROWSER environment variable.
    Default: chrome
    """

    browser = os.getenv("BROWSER", "chrome")

    # -------------------------
    # CHROME
    # -------------------------
    if browser == "chrome":
        chrome_options = ChromeOptions()

        # Headless mode
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--window-size=1920,1080")

        # Disable notifications & geolocation popup
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_experimental_option(
            "prefs",
            {
                "profile.default_content_setting_values.geolocation": 1
            },
        )

        service = ChromeService(ChromeDriverManager().install())
        context.driver = webdriver.Chrome(service=service, options=chrome_options)

    # -------------------------
    # FIREFOX
    # -------------------------
    elif browser == "firefox":
        firefox_options = FirefoxOptions()

        # Headless mode
        firefox_options.add_argument("-headless")

        # Disable geolocation popup
        firefox_options.set_preference("permissions.default.geo", 2)
        firefox_options.set_preference("geo.enabled", False)

        service = FirefoxService(GeckoDriverManager().install())
        context.driver = webdriver.Firefox(service=service, options=firefox_options)

    else:
        raise Exception(f"Browser '{browser}' is not supported.")

    # Common settings
    context.driver.maximize_window()
    context.driver.implicitly_wait(4)
    context.driver.wait = WebDriverWait(context.driver, timeout=10)
    context.app = Application(context.driver)


def before_scenario(context, scenario):
    print('\nStarted scenario:', scenario.name)
    browser_init(context)


def before_step(context, step):
    print('\nStarted step:', step)


def after_step(context, step):
    if step.status == 'failed':
        print('\nStep failed:', step)


def after_scenario(context, scenario):
    context.driver.quit()