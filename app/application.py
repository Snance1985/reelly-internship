from pages.base_page import Page
from pages.main_page import MainPage
from pages.header import Header
from pages.contact_page import ContactPage
from pages.log_in_page import LogInPage

class Application:

    def __init__(self, driver):
        self.base_page = Page(driver)
        self.main_page = MainPage(driver)
        self.header = Header(driver)
        self.contact_page = ContactPage(driver)
        self.log_in_page = LogInPage(driver)