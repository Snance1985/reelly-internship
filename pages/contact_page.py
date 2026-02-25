from selenium.webdriver.common.by import By
from pages.base_page import Page
from time import sleep

class ContactPage(Page):
    SOCIAL_MEDIA_ICONS = (By.CSS_SELECTOR, "a.contact-button.w-inline-block")
    CONNECT_BUTTON = (By.XPATH, "//div[contains(text(),'Connect the company')]")

    def is_correct_page_opened(self):
        return "contact" in self.driver.current_url.lower()

    def scroll_to_social_media_icons(self):
        """
        Scrolls to each social media icon individually so that
        all are visible on mobile view.
        """
        # Wait until at least one icon is present
        self.wait_until_element_present(*self.SOCIAL_MEDIA_ICONS)
        elements = [el for el in self.driver.find_elements(*self.SOCIAL_MEDIA_ICONS) if el.is_displayed()]

        for el in elements:
            self.scroll_into_view(el)
            sleep(0.3)  # short pause to allow smooth scrolling

    def get_social_media_icons_count(self):
        # Scroll to make sure all icons are visible
        self.scroll_to_social_media_icons()
        return len([el for el in self.driver.find_elements(*self.SOCIAL_MEDIA_ICONS) if el.is_displayed()])

    def is_connect_button_clickable(self):
        element = self.find_elements(*self.CONNECT_BUTTON)
        visible_el = next((el for el in element if el.is_displayed()), None)
        return visible_el is not None and visible_el.is_enabled()