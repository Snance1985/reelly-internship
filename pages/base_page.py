from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

class Page:
    def __init__(self, driver):
        self.driver = driver
        self.driver.wait = WebDriverWait(driver, timeout=10)
        self.base_url = 'https://soft.reelly.io'

    def open_url(self, end_url=''):
        self.driver.get(f'{self.base_url}{end_url}')

    def find_element(self, *locator):
        return self.driver.find_element(*locator)

    def find_elements(self, *locator):
        return self.driver.find_elements(*locator)

    def click(self, *locator):
        self.find_element(*locator).click()

    def input_text(self, text, *locator):
        self.find_element(*locator).send_keys(text)

    def scroll_into_view(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

    def wait_until_element_present(self, *locator):
        self.driver.wait.until(
            EC.presence_of_element_located(locator),
            message=f'Element not present by locator {locator}'
        )

    def wait_until_clickable_click(self, *locator):
        self.driver.wait.until(
            EC.element_to_be_clickable(locator),
            message=f'Element not clickable by locator {locator}'
        ).click()

    def wait_until_visible(self, *locator):
        self.driver.wait.until(
            EC.visibility_of_element_located(locator),
            message=f'Element not visible by locator {locator}'
        )