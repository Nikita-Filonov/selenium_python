import time
from typing import Optional, Tuple

from selenium.common.exceptions import (NoSuchElementException,
                                        TimeoutException, WebDriverException)
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select
from utils.types.webdriver.elements import ElementsInterface

from utils.types.webdriver.page import PageInterface
from utils.webdriver.driver.element_should import ElementShould


class Element:

    def __init__(
        self,
        driver: PageInterface,
        web_element: WebElement,
        locator: Optional[Tuple]
    ):
        self._driver = driver
        self._webelement = (web_element,)
        self.locator = locator

    @property
    def webelement(self) -> WebElement:
        if isinstance(self._webelement, Tuple):
            return self._webelement[0]
        return self._webelement

    def should(self, timeout: int = 0, ignored_exceptions: list = None) -> ElementShould:
        if timeout:
            wait_time = timeout
        else:
            wait_time = self._driver.config.driver.wait_time

        return ElementShould(self._driver, self, wait_time, ignored_exceptions)

    def is_displayed(self) -> bool:
        return self.webelement.is_displayed()

    def is_enabled(self) -> bool:
        return self.webelement.is_enabled()

    def click(self, force=False):
        if force:
            self._driver.webdriver.execute_script(
                "arguments[0].click()",
                self.webelement
            )
        else:
            self.webelement.click()

        return self._driver

    def double_click(self):
        ActionChains(self._driver.webdriver) \
            .double_click(self.webelement)\
            .perform()

        return self._driver

    def hover(self):
        ActionChains(self._driver.webdriver) \
            .move_to_element(self.webelement) \
            .perform()

        return self._driver

    def type(self, *args) -> "Element":
        ActionChains(self._driver.webdriver) \
            .move_to_element(self.webelement) \
            .send_keys(*args)\
            .perform()

        return self._driver

    def fill(self, *args) -> "Element":
        self.webelement.send_keys(args)
        return self

    def clear(self) -> "Element":
        self.webelement.clear()
        return self

    def text(self) -> str:
        return self.webelement.text
        by = By.CSS_SELECTOR

        try:
            if timeout == 0:
                elements = self.webelement.find_elements(by, css)
            else:
                elements = self._driver.wait(timeout).until(
                    lambda _: self.webelement.find_elements(by, css),
                    f"Could not find any elements with CSS: `{css}`"
                )
        except TimeoutException:
            elements = []

        return Elements(self._driver, elements, locator=(by, css))

    def get_xpath(self, xpath: str, timeout: int = None) -> "Element":
        by = By.XPATH

        if timeout == 0:
            elements = self.webelement.find_element(by, xpath)
        else:
            elements = self._driver.wait(timeout).until(
                lambda _: self.webelement.find_element(by, xpath),
                f"Could not find any elements with the xpath: `{xpath}`",
            )

        return Element(self._driver, elements, locator=(by, xpath))

    def find_xpath(self, xpath: str, timeout: int = None) -> "ElementsInterface":
        from utils.webdriver.driver.elements import Elements

        by = By.XPATH

        try:
            if timeout == 0:
                elements = self.webelement.find_elements(by, xpath)
            else:
                elements = self._driver.wait(timeout).until(
                    lambda _: self.webelement.find_elements(by, xpath),
                    f"Could not find any elements with the xpath: `{xpath}`",
                )
        except TimeoutException:
            elements = []
        return Elements(self._driver, elements, locator=(by, xpath))

    def screenshot(self, filename) -> "Element":
        self.webelement.screenshot(filename)
        return self

    def scroll_into_view(self) -> "Element":
        self._driver.webdriver.execute_script(
            "arguments[0].scrollIntoView(true);",
            self.webelement
        )
        return self
