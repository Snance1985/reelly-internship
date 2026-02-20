from selenium.webdriver.common.by import By
from pages.base_page import Page

class ContactPage(Page):
    SOCIAL_MEDIA_ICONS = (By.CSS_SELECTOR, "a.contact-button.w-inline-block")
    CONNECT_BUTTON = (By.XPATH, "//div[contains(text(),'Connect the company')]")

    def is_correct_page_opened(self):
        return "contact" in self.driver.current_url.lower()

    def get_social_media_icons_count(self):
        return len([el for el in self.driver.find_elements(*self.SOCIAL_MEDIA_ICONS) if el.is_displayed()])

    def is_connect_button_clickable(self):
        element = self.find_elements(*self.CONNECT_BUTTON)
        visible_el = next((el for el in element if el.is_displayed()), None)
        return visible_el is not None and visible_el.is_enabled()