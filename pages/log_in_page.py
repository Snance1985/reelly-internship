from selenium.webdriver.common.by import By
from pages.base_page import Page
from time import sleep

class LogInPage(Page):
    EMAIL = (By.CSS_SELECTOR, "input[wized='emailInput']")
    PASSWORD = (By.CSS_SELECTOR, "input[type='password']")
    CONTINUE = (By.XPATH, "//a[normalize-space()='Continue']")

    def login(self, email, password):
        sleep(2)  # wait for iframe and slow page load

        # Check for iframe
        iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
        for iframe in iframes:
            self.driver.switch_to.frame(iframe)
            if self.driver.find_elements(*self.EMAIL):
                break
            self.driver.switch_to.default_content()

        # Fill email
        self.wait_until_visible(*self.EMAIL)
        email_field = self.find_element(*self.EMAIL)
        email_field.click()
        email_field.clear()
        email_field.send_keys(email)

        # Fill password
        password_field = self.find_element(*self.PASSWORD)
        password_field.click()
        password_field.clear()
        password_field.send_keys(password)

        # Click Continue
        self.wait_until_clickable_click(*self.CONTINUE)
        sleep(2)

        # Switch back to main content
        self.driver.switch_to.default_content()
