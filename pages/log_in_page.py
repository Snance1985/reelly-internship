from selenium.webdriver.common.by import By
from pages.base_page import Page

class LogInPage(Page):

    EMAIL = (By.CSS_SELECTOR, "input[type='email']")
    PASSWORD = (By.CSS_SELECTOR, "input[type='password']")
    CONTINUE = (By.XPATH, "//a[text()='Continue']")

    def login(self, email, password):
        print("Waiting for email input...")
        self.wait_until_element_present(*self.EMAIL)
        print("Entering email")
        self.find_element(*self.EMAIL).send_keys(email)
        print("Entering password")
        self.find_element(*self.PASSWORD).send_keys(password)
        print("Clicking continue")
        self.wait_until_clickable_click(*self.CONTINUE)
        print("Login attempted")