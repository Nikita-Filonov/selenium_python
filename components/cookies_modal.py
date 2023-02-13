import allure

from page_factory.button import Button
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
        if self.accept_button.is_displayed() and self.customize_button.is_displayed():
            self.accept_button.click()
