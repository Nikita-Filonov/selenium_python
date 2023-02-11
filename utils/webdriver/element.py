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

from utils.types.webdriver.client import AppWebDriverInterface
from utils.types.webdriver.waiting import Method


class ElementWait:
    def __init__(self, webelement, timeout: int, ignored_exceptions: list = None):
        self._webelement = webelement
        self._timeout = 10 if timeout == 0 else timeout

        if ignored_exceptions:
            self._ignored_exceptions = ignored_exceptions
        else:
            self._ignored_exceptions = NoSuchElementException

    def until(self, method: Method, message=""):
        screen = None
        stacktrace = None

        end_time = time.time() + self._timeout
        while True:
            try:
                value = method(self._webelement)
                if value:
                    return value
            except self._ignored_exceptions as exc:
                screen = getattr(exc, "screen", None)
                stacktrace = getattr(exc, "stacktrace", None)

            time.sleep(0.5)
            if time.time() > end_time:
                break

        raise TimeoutException(message, screen, stacktrace)


class ElementsShould:
    """ElementsShould API: Commands (aka Expectations) for the current list of Elements."""

    def __init__(
        self,
        app_web_driver: AppWebDriverInterface,
        elements: "Elements",
        timeout: int,
        ignored_exceptions: list = None
    ):
        self._app_web_driver = app_web_driver
        self._elements = elements
        self._wait = app_web_driver.wait(
            timeout=timeout,
            use_self=True,
            ignored_exceptions=ignored_exceptions
        )

    def have_length(self, length: int) -> bool:
        try:
            if self._elements.length() == length:
                return True

            locator = self._elements.locator
            value = self._wait.until(
                lambda drvr: len(drvr.find_elements(*locator)) == length
            )
        except TimeoutException:
            value = False

        if value:
            return True

        raise AssertionError(f"Length of elements was not equal to {length}")

    def not_be_empty(self) -> "Elements":
        try:
            if not self._elements.is_empty():
                return self._elements

            locator = self._elements.locator
            value = self._wait.until(lambda drvr: drvr.find_elements(*locator))
        except TimeoutException:
            value = False

        if value:
            return Elements(self._app_web_driver, value, self._elements.locator)

        raise AssertionError("List of elements was empty")


class ElementShould:
    """ElementShould API: Commands (aka Expectations) for the current Element."""

    def __init__(self, app_web_driver, element: "Element", timeout: int, ignored_exceptions: list = None):
        self._app_web_driver = app_web_driver
        self._element = element
        self._wait = ElementWait(
            element.webelement, timeout, ignored_exceptions
        )

    def be_clickable(self) -> "Element":
        try:
            value = self._wait.until(
                lambda e: e.is_displayed() and e.is_enabled()
            )
        except TimeoutException:
            value = False
        if value:
            return self._element
        raise AssertionError("Element was not clickable")

    def be_disabled(self) -> "Element":
        try:
            value = self._wait.until(lambda e: not e.is_enabled())
        except TimeoutException:
            value = False
        if value:
            return self._element
        raise AssertionError("Element was not disabled")

    def be_enabled(self) -> "Element":
        try:
            value = self._wait.until(lambda e: e.is_enabled())
        except TimeoutException:
            value = False
        if value:
            return self._element
        raise AssertionError("Element was not enabled")

    def be_focused(self) -> "Element":
        try:
            value = self._wait.until(
                lambda e: e == self._app_web_driver.webdriver.switch_to.active_element)
        except TimeoutException:
            value = False

        if value:
            return self._element
        raise AssertionError("Element was not focused")

    def be_hidden(self) -> "Element":
        try:
            value = self._wait.until(lambda e: e and not e.is_displayed())
        except TimeoutException:
            value = False

        if value:
            return self._element
        raise AssertionError("Element was not hidden")

    def be_visible(self) -> "Element":
        try:
            value = self._wait.until(lambda e: e and e.is_displayed())
        except TimeoutException:
            value = False

        if value:
            return self._element
        raise AssertionError("Element was not visible")

    def have_text(self, text: str, case_sensitive=True) -> "Element":
        try:
            if case_sensitive:
                value = self._wait.until(lambda e: e.text == text)
            else:
                value = self._wait.until(
                    lambda e: e.text.strip().lower() == text.lower()
                )
        except TimeoutException:
            value = False

        if value:
            return self._element

        raise AssertionError(
            f"Expected text: `{text}` - Actual text: `{self._element.text()}`"
        )

    def contain_text(self, text, case_sensitive=True) -> "Element":
        try:
            if case_sensitive:
                value = self._wait.until(lambda e: text in e.text)
            else:
                value = self._wait.until(
                    lambda e: text.lower() in e.text.strip().lower())
        except TimeoutException:
            value = False

        if value:
            return self._element
        raise AssertionError(
            f"Expected `{text}` to be in `{self._element.text()}`")

    def have_value(self, value) -> "Element":
        try:
            val = self._wait.until(lambda e: e.get_attribute("value") == value)
        except TimeoutException:
            val = False

        if val:
            return self._element
        raise AssertionError(
            f'Expected value: `{value}` - Actual value: `{self._element.get_attribute("value")}`')

    def disappear(self):
        try:
            value = self._wait.until(
                ec.invisibility_of_element(self._element.webelement))
        except TimeoutException:
            value = False
        if value:
            return self._app_web_driver
        raise AssertionError("Element was still visible or still in the DOM")

    def not_have_value(self, value) -> "Element":
        try:
            val = self._wait.until(lambda e: e.get_attribute("value") != value)
        except TimeoutException:
            val = False

        if val:
            return self._element
        raise AssertionError(f"Element had value matching ``{value}``")

    def not_have_text(self, text, case_sensitive=True) -> "Element":
        try:
            if case_sensitive:
                value = self._wait.until(lambda e: e.text != text)
            else:
                value = self._wait.until(
                    lambda e: e.text.strip().lower() != text.lower())
        except TimeoutException:
            value = False

        if value:
            return self._element
        raise AssertionError(f"Element had the text matching ``{text}``")


class Elements(list["Element"]):
    """Elements API: Represents a list of DOM webelements and includes commands to work with them."""

    def __init__(
        self,
        app_web_driver: AppWebDriverInterface,
        web_elements: list[WebElement],
        locator: Optional[Tuple]
    ):
        self._list = [
            Element(app_web_driver, element, None)for element in web_elements
        ]
        self._app_web_driver = app_web_driver
        self.locator = locator
        super().__init__(self._list)

    def length(self) -> int:
        """The number of elements in the list."""
        return len(self._list)

    def is_empty(self) -> bool:
        """Checks if there are zero elements in the list."""
        return self.length() == 0

    def should(self, timeout: int = 0, ignored_exceptions: list = None) -> ElementsShould:
        """A collection of expectations for this list of elements.

        Examples:
        ```
            app_web_driver.find("option").should().not_be_empty()
        ```
        """
        if timeout:
            wait_time = timeout
        else:
            wait_time = self._app_web_driver.config.driver.wait_time
        return ElementsShould(self._app_web_driver, self, wait_time, ignored_exceptions)

    def first(self) -> "Element":
        """Gets the first element in the list.

        Raises:
            `IndexError` if the list is empty.
        """
        if self.length() > 0:
            return self._list[0]
        raise IndexError("Cannot get first() from an empty list")

    def last(self) -> "Element":
        """Gets the last element in the list.

        Raises:
            `IndexError` if the list is empty.
        """
        if self.length() > 0:
            return self._list[-1]
        raise IndexError("Cannot get last() from an empty list")


class Element:
    """Element API: Represents a single DOM webelement and includes the commands to work with it."""

    def __init__(
        self,
        app_web_driver: AppWebDriverInterface,
        web_element: WebElement,
        locator: Optional[Tuple]
    ):
        self._app_web_driver = app_web_driver
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
            wait_time = self._app_web_driver.config.driver.wait_time

        return ElementShould(self._app_web_driver, self, wait_time, ignored_exceptions)

    def is_displayed(self) -> bool:
        return self.webelement.is_displayed()

    def is_enabled(self) -> bool:
        return self.webelement.is_enabled()

    def click(self, force=False):
        if force:
            self._app_web_driver.webdriver.execute_script(
                "arguments[0].click()",
                self.webelement
            )
        else:
            self.webelement.click()

        return self._app_web_driver

    def double_click(self):
        ActionChains(self._app_web_driver.webdriver) \
            .double_click(self.webelement)\
            .perform()

        return self._app_web_driver

    def hover(self):
        ActionChains(self._app_web_driver.webdriver) \
            .move_to_element(self.webelement) \
            .perform()

        return self._app_web_driver

    def type(self, *args) -> "Element":
        ActionChains(self._app_web_driver.webdriver) \
            .move_to_element(self.webelement) \
            .send_keys(*args)\
            .perform()

        return self._app_web_driver

    def fill(self, *args) -> "Element":
        self.webelement.send_keys(args)
        return self

    def clear(self) -> "Element":
        self.webelement.clear()
        return self

    def text(self) -> str:
        return self.webelement.text

    def contains(self, text: str, timeout: int = None) -> "Element":
        locator = (By.XPATH, f'.//*[contains(text(), "{text}")]')

        if timeout == 0:
            element = self.webelement.find_element(*locator)
        else:
            element = self._app_web_driver.wait(timeout).until(
                lambda _: self.webelement.find_element(
                    *locator), f"Could not find element with the text: `{text}`"
            )
        return Element(self._app_web_driver, element, locator)

    def get(self, css: str, timeout: int = None) -> "Element":
        by = By.CSS_SELECTOR

        if timeout == 0:
            element = self.webelement.find_element(by, css)
        else:
            element = self._app_web_driver.wait(timeout).until(
                lambda _: self.webelement.find_element(by, css),
                f"Could not find element with the CSS: `{css}`"
            )
        return Element(self._app_web_driver, element, locator=(by, css))

    def find(self, css: str, timeout: int = None) -> Elements:
        by = By.CSS_SELECTOR

        try:
            if timeout == 0:
                elements = self.webelement.find_elements(by, css)
            else:
                elements = self._app_web_driver.wait(timeout).until(
                    lambda _: self.webelement.find_elements(by, css),
                    f"Could not find any elements with CSS: `{css}`"
                )
        except TimeoutException:
            elements = []

        return Elements(self._app_web_driver, elements, locator=(by, css))

    def getx(self, xpath: str, timeout: int = None) -> "Element":
        by = By.XPATH

        if timeout == 0:
            elements = self.webelement.find_element(by, xpath)
        else:
            elements = self._app_web_driver.wait(timeout).until(
                lambda _: self.webelement.find_element(by, xpath),
                f"Could not find any elements with the xpath: `{xpath}`",
            )

        return Element(self._app_web_driver, elements, locator=(by, xpath))

    def findx(self, xpath: str, timeout: int = None) -> "Elements":
        by = By.XPATH

        try:
            if timeout == 0:
                elements = self.webelement.find_elements(by, xpath)
            else:
                elements = self._app_web_driver.wait(timeout).until(
                    lambda _: self.webelement.find_elements(by, xpath),
                    f"Could not find any elements with the xpath: `{xpath}`",
                )
        except TimeoutException:
            elements = []
        return Elements(self._app_web_driver, elements, locator=(by, xpath))

    def screenshot(self, filename) -> "Element":
        self.webelement.screenshot(filename)
        return self

    def scroll_into_view(self) -> "Element":
        self._app_web_driver.webdriver.execute_script(
            "arguments[0].scrollIntoView(true);",
            self.webelement
        )
        return self
