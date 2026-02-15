from selenium.webdriver.common.by import By
from pages.base_page import Page
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

class Header(Page):

    SETTINGS_OPTION = (By.XPATH, "//div[text()='Settings']")
    CONTACT_US = (By.CSS_SELECTOR, "a[href='/contact-us']")

    def wait_for_header_to_load(self):
        self.wait_until_element_present(*self.SETTINGS_OPTION)

    def wait_for_settings_panel(self):
        self.driver.wait.until(
            EC.visibility_of_element_located(self.CONTACT_US),
            message="Settings panel not visible yet"
        )

    def click_settings(self):
        self.wait_until_clickable_click(*self.SETTINGS_OPTION)
        print("Settings clicked")
        self.wait_for_settings_panel()
        sleep(5)

    def click_contact_us(self):
        print("Waiting for Contact Us link to be visible and clickable...")
        self.wait_until_visible(*self.CONTACT_US)
        self.wait_until_clickable(*self.CONTACT_US)

        element = self.driver.find_element(*self.CONTACT_US)
        sleep(4)
        actions = ActionChains(self.driver)
        sleep(4)
        actions.move_to_element(element)
        actions.click().perform()
        sleep(4)
        print("Contact Us clicked")