from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from time import sleep
from pages.base_page import Page

class Header(Page):
    SETTINGS_OPTION = (By.XPATH, "//a[@href='https://soft.reelly.io/settings' and .//span[text()='Settings']]")
    CONTACT_US = (By.XPATH, "//a[.//div[text()='Contact us']]")
    MARKET_OFFERS_OPTION = (By.XPATH, "//a[.//span[contains(text(),'Market Offers')]]")
    MENU_BUTTON = (By.XPATH, "//div[text()='Menu']")


    def wait_for_header_to_load(self):
        self.wait_until_element_present(*self.SETTINGS_OPTION)
    sleep(2)

    def click_market_offers(self):
        sleep(2)
        # Wait for element to be present
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.MARKET_OFFERS_OPTION)
        )
        sleep(2)
        # Scroll into view (important for mobile)
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
        # Wait until clickable
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.MARKET_OFFERS_OPTION)
        )
        sleep(2)
        # Click
        element.click()
        sleep(4)

    def click_menu(self):
        sleep(4)
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.MENU_BUTTON)
        )
        sleep(2)
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.MENU_BUTTON)
        )
        sleep(2)
        element.click()
        sleep(4)

    def wait_for_settings_panel(self):
        self.driver.wait.until(
            EC.visibility_of_element_located(self.CONTACT_US),
            message="Settings panel not visible yet"
        )

    def click_settings(self):
        sleep(5)
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

    def click_contact_us(self, retries=5):
        attempt = 0
        while attempt < retries:
            try:
                # Wait until the element is visible and clickable using the original locator
                visible_el = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(self.CONTACT_US)
                )

                # Scroll into view
                self.scroll_into_view(visible_el)

                # Optional: dismiss any alert (location/notification popup)
                try:
                    WebDriverWait(self.driver, 2).until(EC.alert_is_present())
                    alert = self.driver.switch_to.alert
                    print(f"Alert detected: {alert.text}, dismissing")
                    alert.dismiss()
                except:
                    pass

                # Click with ActionChains
                ActionChains(self.driver).move_to_element(visible_el).click().perform()
                print("Contact Us clicked successfully")
                return

            except Exception as e:
                attempt += 1
                print(f"Attempt {attempt}: Element not ready, retrying...")
                sleep(1)
                if attempt == retries:
                    raise Exception("Unable to click Contact Us after multiple retries") from e