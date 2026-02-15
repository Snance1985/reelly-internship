from selenium.webdriver.common.by import By
from pages.base_page import Page

class ContactPage(Page):

    SOCIAL_MEDIA_ICONS = (By.CSS_SELECTOR, "a.social-link")
    CONNECT_BUTTON = (By.XPATH, "//button[contains(text(),'Connect the company')]")

    def is_correct_page_opened(self):
        return "contact" in self.driver.current_url.lower()

    def get_social_media_icons_count(self):
        icons = self.driver.find_elements(*self.SOCIAL_MEDIA_ICONS)
        return len(icons)

    def is_connect_button_clickable(self):
        element = self.wait_until_clickable(self.CONNECT_BUTTON)
        return element.is_enabled()