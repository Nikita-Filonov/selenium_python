from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as ec

from utils.types.webdriver.page import PageInterface
from utils.types.webdriver.element import ElementInterface
from utils.webdriver.driver.element_wait import ElementWait
from selenium.common.exceptions import StaleElementReferenceException


class ElementShould:

    def __init__(
        self,
        driver: PageInterface,
        element: ElementInterface,
        timeout: int,
        ignored_exceptions: list = None
    ):
        self._driver = driver
        self._element = element
        self._wait = ElementWait(
            element.webelement, timeout, ignored_exceptions
        )

    def be_clickable(self) -> ElementInterface:
        try:
            value = self._wait.until(
                lambda e: e.is_displayed() and e.is_enabled()
            )
        except TimeoutException:
            value = False
        if value:
            return self._element

        raise AssertionError("Element was not clickable")

    def be_hidden(self) -> ElementInterface:
        try:
            value = self._wait.until(lambda e: e and not e.is_displayed())
        except TimeoutException:
            value = False

        if value:
            return self._element
        raise AssertionError("Element was not hidden")

    def be_visible(self) -> ElementInterface:
        try:
            value = self._wait.until(lambda e: e and e.is_displayed())
        except TimeoutException:
            value = False

        if value:
            return self._element
        raise AssertionError("Element was not visible")

    def have_text(self, text: str, case_sensitive=True) -> "ElementInterface":
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

    def have_value(self, value) -> ElementInterface:
        try:
            val = self._wait.until(lambda e: e.get_attribute("value") == value)
        except TimeoutException:
            val = False

        if val:
            return self._element
        raise AssertionError(
            f'Expected value: `{value}` - Actual value: `{self._element.get_attribute("value")}`'
        )

    def disappear(self):
        try:
            value = self._wait.until(
                ec.invisibility_of_element(self._element.webelement)
            )
        except TimeoutException:
            value = False
        if value:
            return self._app_web_driver
        raise AssertionError("Element was still visible or still in the DOM")

    def not_have_value(self, value) -> ElementInterface:
        try:
            val = self._wait.until(lambda e: e.get_attribute("value") != value)
        except TimeoutException:
            val = False

        if val:
            return self._element
        raise AssertionError(f"Element had value matching ``{value}``")

    def not_have_text(self, text: str, case_sensitive=True) -> ElementInterface:
        try:
            if case_sensitive:
                value = self._wait.until(lambda e: e.text != text)
            else:
                value = self._wait.until(
                    lambda e: e.text.strip().lower() != text.lower()
                )
        except TimeoutException:
            value = False

        if value:
            return self._element
        raise AssertionError(f"Element had the text matching ``{text}``")
