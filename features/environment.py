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
    # LOCAL CHROME (Mobile Emulation Enabled)
    # ======================================================
    if browser_name == "chrome":

        chrome_options = ChromeOptions()

        mobile_emulation = {
        # Portrait
            "deviceMetrics": {
                "width": 390,
                "height": 844,
                "pixelRatio": 3.0
            },
            "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) "
                         "AppleWebKit/605.1.15 (KHTML, like Gecko) "
                         "Version/16.0 Mobile/15E148 Safari/604.1"
        }

        # Horizontal
        """
        mobile_emulation = {
            "deviceMetrics": {
                "width": 844,
                "height": 390,
                "pixelRatio": 3.0
            },
            "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) "
                         "AppleWebKit/605.1.15 (KHTML, like Gecko) "
                         "Version/16.0 Mobile/15E148 Safari/604.1"
        }
        """

        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

        if headless:
            chrome_options.add_argument("--headless=new")

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

    # Only maximize if NOT headless and NOT mobile emulation
    if browser_name == "firefox" and not headless:
        context.driver.maximize_window()

    context.app = Application(context.driver)


def before_scenario(context, scenario):
    # 👇 Change execution mode here if needed
    browser_init(context, browser_name="chrome", headless=False)


def after_scenario(context, scenario):
    if hasattr(context, "driver"):
        context.driver.quit()