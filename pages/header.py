from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from pages.base_page import Page

class Header(Page):
    SETTINGS_OPTION = (By.XPATH, "//a[@href='https://soft.reelly.io/settings' and .//span[text()='Settings']]")
    CONTACT_US = (By.CSS_SELECTOR, "a[href='/contact-us']")


    def wait_for_header_to_load(self):
        self.wait_until_element_present(*self.SETTINGS_OPTION)

    def wait_for_settings_panel(self):
        self.driver.wait.until(
            EC.visibility_of_element_located(self.CONTACT_US),
            message="Settings panel not visible yet"
        )

    def click_settings(self):
        sleep(4)
        # Wait until element is present
        self.wait_until_element_present(*self.SETTINGS_OPTION)

        # Find element
        element = self.find_element(*self.SETTINGS_OPTION)

        # Scroll into view using base_page helper
        self.scroll_into_view(element)
        sleep(1)  # allow animation

        # Move to it and click
        actions = ActionChains(self.driver)
        actions.move_to_element(element).click().perform()

        print("Settings clicked")
        self.wait_for_settings_panel()
        sleep(1)

    # def click_settings(self):
    #     sleep(100)
    #     elements = self.driver.find_elements(*self.SETTINGS_OPTION)
    #     visible_el = next((el for el in elements if el.is_displayed()), None)
    #     if not visible_el:
    #         raise Exception("No visible Settings element found")
    #
    #     self.scroll_into_view(visible_el)
    #     sleep(1)
    #     ActionChains(self.driver).move_to_element(visible_el).click().perform()
    #     sleep(2)
    #     print("Settings clicked")

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
