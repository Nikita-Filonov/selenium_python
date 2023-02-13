import allure
from selenium.common.exceptions import TimeoutException

from page_factory.button import Button
from utils.logger import logger
from utils.webdriver.driver.page import Page


class CookiesModal:
    def __init__(self, page: Page) -> None:
        self.accept_button = Button(
            page,
            locator='//div[@id="accept-choices"]',
            name='Accept all & visit the site'
        )
        self.customize_button = Button(
            page,
            locator='//div[@id="sn-b-custom"]',
            name='Customise choices'
        )

    @allure.step('Accepting all cookies')
    def accept_cookies(self):
        try:
            if self.accept_button.is_displayed() and self.customize_button.is_displayed():
                self.accept_button.click()
        except TimeoutException:
            logger.error('Cookies modal did not appear')
