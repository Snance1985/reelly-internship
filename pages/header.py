from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pages.base_page import Page
from time import sleep

class Header(Page):
    SETTINGS_OPTION = (By.XPATH, "//a[@href='https://soft.reelly.io/settings' and .//span[text()='Settings']]")
    CONTACT_US = (By.CSS_SELECTOR, "a[href='/contact-us']")

    def click_settings(self):
        elements = self.driver.find_elements(*self.SETTINGS_OPTION)
        visible_el = next((el for el in elements if el.is_displayed()), None)
        if not visible_el:
            raise Exception("No visible Settings element found")

        self.scroll_into_view(visible_el)
        sleep(1)
        ActionChains(self.driver).move_to_element(visible_el).click().perform()
        sleep(2)
        print("Settings clicked")

    def click_contact_us(self):
        elements = self.driver.find_elements(*self.CONTACT_US)
        visible_el = next((el for el in elements if el.is_displayed()), None)
        if not visible_el:
            raise Exception("No visible Contact Us element found")

        self.scroll_into_view(visible_el)
        sleep(1)
        ActionChains(self.driver).move_to_element(visible_el).click().perform()
        sleep(2)
        print("Contact Us clicked")
