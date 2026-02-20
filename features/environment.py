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

    if browser_name.lower() == "chrome":
        chrome_options = ChromeOptions()

        if headless:
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--window-size=1920,1080")

        prefs = {
            "profile.default_content_setting_values.geolocation": 2,
            "profile.default_content_setting_values.notifications": 2
        }
        chrome_options.add_experimental_option("prefs", prefs)

        driver_path = ChromeDriverManager().install()
        service = ChromeService(driver_path)
        context.driver = webdriver.Chrome(service=service, options=chrome_options)

    elif browser_name.lower() == "firefox":
        firefox_options = FirefoxOptions()

        if headless:
            firefox_options.add_argument("--headless")

        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference("permissions.default.desktop-notification", 2)
        firefox_profile.set_preference("geo.enabled", False)
        firefox_options.profile = firefox_profile

        driver_path = GeckoDriverManager().install()
        service = FirefoxService(driver_path)
        context.driver = webdriver.Firefox(service=service, options=firefox_options)

    else:
        raise Exception(f"Browser '{browser_name}' is not supported!")

    if not headless:
        context.driver.maximize_window()

    context.driver.implicitly_wait(4)
    context.driver.wait = WebDriverWait(context.driver, timeout=10)

    context.app = Application(context.driver)


def before_scenario(context, scenario):
    # Change these easily:
    browser_init(context, browser_name="firefox", headless=True)


def after_scenario(context, scenario):
    if hasattr(context, 'driver'):
        context.driver.quit()