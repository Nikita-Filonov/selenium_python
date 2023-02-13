import allure
from selenium.common.exceptions import StaleElementReferenceException

from utils.webdriver.driver.element import Element
from utils.webdriver.driver.elements import Elements
from utils.webdriver.driver.page import Page


class Component:
    def __init__(self, page: Page, locator: str, name: str) -> None:
        self._page = page
        self._locator = locator
        self._name = name

    @property
    def type_of(self) -> str:
        return 'component'

    @property
    def name(self) -> str:
        return self._name

    def get_element(self, **kwargs) -> Element:
        locator = self._locator.format(**kwargs)

        with allure.step(f'Getting {self.type_of} with name "{self.name}" and locator "{locator}"'):
            return self._page.get_xpath(locator)

    def get_elements(self, **kwargs) -> Elements:
        locator = self._locator.format(**kwargs)

        with allure.step(f'Getting {self.type_of}s with name "{self.name}" and locator "{locator}"'):
            return self._page.find_xpath(locator)

    def click(self, **kwargs) -> None:
        with allure.step(f'Clicking {self.type_of} with name "{self.name}"'):
            element = self.get_element(**kwargs)
            element.click()

    def should_be_visible(self, **kwargs) -> None:
        with allure.step(f'Checking that {self.type_of} "{self.name}" is visible'):
            try:
                element = self.get_element(**kwargs)
                element.should().be_visible()
            except StaleElementReferenceException:
                self.should_be_visible(**kwargs)

    def should_have_text(self, text: str, **kwargs) -> None:
        with allure.step(f'Checking that {self.type_of} "{self.name}" has text "{text}"'):
            try:
                element = self.get_element(**kwargs)
                element.should().have_text(text)
            except StaleElementReferenceException:
                self.should_have_text(text, **kwargs)

    def is_displayed(self, **kwargs) -> bool:
        with allure.step(f'Checking if {self.type_of} "{self.name}" is visible'):
            element = self.get_element(**kwargs)
            return element.is_displayed()
