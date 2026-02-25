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


def browser_init(context, browser_name="chrome", headless=False):

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

        #  Mobile emulation in landscape mode (width > height)
        mobile_emulation = {
            "deviceMetrics": {"width": 844, "height": 390, "pixelRatio": 3},  # Landscape iPhone 14 Pro
            "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) "
                         "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
        }

        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

        # Optional: force window size (helps with some mobile layouts)
        chrome_options.add_argument("--window-size=844,390")  # Landscape

        # Disable notifications & geolocation prompts
        prefs = {
            "profile.default_content_setting_values.geolocation": 2,
            "profile.default_content_setting_values.notifications": 2
        }
        chrome_options.add_experimental_option("prefs", prefs)

        driver_path = ChromeDriverManager().install()
        service = ChromeService(driver_path)
        context.driver = webdriver.Chrome(service=service, options=chrome_options)

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
    browser_init(context, browser_name="chrome", headless=False)


def after_scenario(context, scenario):
    if hasattr(context, "driver"):
        context.driver.quit()