from selenium.common.exceptions import TimeoutException

from utils.types.webdriver.driver.element import ElementInterface
from utils.types.webdriver.driver.element_should import ElementShouldInterface
from utils.types.webdriver.driver.page import PageInterface
from utils.webdriver.driver.element_wait import ElementWait


class ElementShould(ElementShouldInterface):
    """ElementShould API: Commands (aka Expectations) for the current Element"""

    def __init__(
            self,
            page: PageInterface,
            element: ElementInterface,
            timeout: int,
            ignored_exceptions: list = None
    ):
        self._page = page
        self._element = element
        self._wait = ElementWait(
            element.web_element, timeout, ignored_exceptions
        )

    def be_clickable(self) -> ElementInterface:
        """An expectation that the element is displayed and enabled so you can click it"""
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
        """An expectation that the element is not displayed but still in the DOM (aka hidden)"""
        try:
            value = self._wait.until(lambda e: e and not e.is_displayed())
        except TimeoutException:
            value = False

        if value:
            return self._element
        raise AssertionError("Element was not hidden")

    def be_visible(self) -> ElementInterface:
        """An expectation that the element is displayed"""
        try:
            value = self._wait.until(lambda e: e and e.is_displayed())
        except TimeoutException:
            value = False

        if value:
            return self._element

        raise AssertionError("Element was not visible")

    def have_text(self, text: str, case_sensitive=True) -> "ElementInterface":
        """An expectation that the element has the given text"""
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
