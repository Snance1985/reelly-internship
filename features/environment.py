import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from app.application import Application


def browser_init(context, browser_name="browserstack", headless=False):

    browser_name = browser_name.lower()

    # ======================================================
    # BROWSERSTACK (MacOS + Firefox)
    # ======================================================
    if browser_name == "browserstack":

        USERNAME = os.getenv("BROWSERSTACK_USERNAME")
        ACCESS_KEY = os.getenv("BROWSERSTACK_ACCESS_KEY")

        if not USERNAME or not ACCESS_KEY:
            raise Exception("BrowserStack credentials not set in environment variables.")

        options = FirefoxOptions()
        options.set_capability("browserName", "Firefox")
        options.set_capability("browserVersion", "latest")
        options.set_capability("bstack:options", {
            "os": "OS X",
            "osVersion": "Monterey",
            "sessionName": "Behave Mac Firefox Test",
            "buildName": "Automation Framework Build",
            "local": "false"
        })

        context.driver = webdriver.Remote(
            command_executor=f"https://{USERNAME}:{ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub",
            options=options
        )

    # ======================================================
    # LOCAL CHROME
    # ======================================================
    elif browser_name == "chrome":

        chrome_options = ChromeOptions()

        if headless:
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--window-size=1920,1080")

        prefs = {
            "profile.default_content_setting_values.geolocation": 2,
            "profile.default_content_setting_values.notifications": 2
        }
        chrome_options.add_experimental_option("prefs", prefs)

        service = ChromeService(ChromeDriverManager().install())

        context.driver = webdriver.Chrome(
            service=service,
            options=chrome_options
        )

    # ======================================================
    # LOCAL FIREFOX
    # ======================================================
    elif browser_name == "firefox":

        firefox_options = FirefoxOptions()

        if headless:
            firefox_options.add_argument("--headless")

        firefox_options.set_preference("permissions.default.desktop-notification", 2)
        firefox_options.set_preference("geo.enabled", False)

        service = FirefoxService(GeckoDriverManager().install())

        context.driver = webdriver.Firefox(
            service=service,
            options=firefox_options
        )

    else:
        raise Exception(f"Browser '{browser_name}' is not supported.")

    # ======================================================
    # COMMON SETUP
    # ======================================================

    context.driver.implicitly_wait(4)
    context.driver.wait = WebDriverWait(context.driver, 10)

    # Don't maximize BrowserStack or headless sessions
    if browser_name != "browserstack" and not headless:
        context.driver.maximize_window()

    context.app = Application(context.driver)


def before_scenario(context, scenario):
    # Change execution mode here:
    browser_init(context, browser_name="browserstack", headless=False)


def after_scenario(context, scenario):
    if hasattr(context, "driver"):
        context.driver.quit()