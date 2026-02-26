import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.wait import WebDriverWait
from app.application import Application

def browser_init(context, browser_name="chrome", headless=False):
    browser_name = browser_name.lower()

    # ======================================================
    # BROWSERSTACK MOBILE
    # ======================================================
    if browser_name == "browserstack":
        USERNAME = os.getenv("BROWSERSTACK_USERNAME")
        ACCESS_KEY = os.getenv("BROWSERSTACK_ACCESS_KEY")
        if not USERNAME or not ACCESS_KEY:
            raise Exception("BrowserStack credentials not set in environment variables.")

        # Chrome mobile emulation options for BrowserStack
        chrome_options = ChromeOptions()

        # Mobile device capabilities
        chrome_options.set_capability("browserName", "Firefox")
        chrome_options.set_capability("browserVersion", "latest")
        chrome_options.set_capability("bstack:options", {
            "deviceName": "iPhone 12",
            "realMobile": False,
            "osVersion": "17",
            "sessionName": "Behave Test Emulator",
            "buildName": "Reelly Automation Build",
            "local": "false",
            # Optional: turn on video recording and logs
            "debug": True,
            "networkLogs": True,
            "consoleLogs": "verbose"
        })

        # Block popups: locations & notifications
        prefs = {
            "profile.default_content_setting_values.geolocation": 2,
            "profile.default_content_setting_values.notifications": 2
        }
        chrome_options.add_experimental_option("prefs", prefs)

        context.driver = webdriver.Remote(
            command_executor=f"https://{USERNAME}:{ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub",
            options=chrome_options
        )

    # ======================================================
    # LOCAL CHROME (PORTRAIT MOBILE)
    # ======================================================
    elif browser_name == "chrome":
        chrome_options = ChromeOptions()

        # Mobile emulation (portrait)
        mobile_emulation = {"deviceName": "iPhone 14"}
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

        # Block popups
        prefs = {
            "profile.default_content_setting_values.geolocation": 2,
            "profile.default_content_setting_values.notifications": 2
        }
        chrome_options.add_experimental_option("prefs", prefs)

        context.driver = webdriver.Chrome(options=chrome_options)

    else:
        raise Exception(f"Browser '{browser_name}' is not supported.")

    # ======================================================
    # COMMON SETUP
    # ======================================================
    context.driver.implicitly_wait(4)
    context.driver.wait = WebDriverWait(context.driver, 10)
    context.app = Application(context.driver)

def before_scenario(context, scenario):
    max_attempts = 2
    for attempt in range(max_attempts):
        try:
            browser_init(context, browser_name="browserstack", headless=False)
            break
        except Exception as e:
            if attempt == max_attempts - 1:
                raise e
            print(f"Retrying BrowserStack init due to error: {e}")

def after_scenario(context, scenario):
    if hasattr(context, "driver"):
        context.driver.quit()